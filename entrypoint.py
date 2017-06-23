#!/usr/bin/env python
# coding=utf-8

# TODO: predefine env
import os
import docker
import time
import commands

os.system("dockerd --host unix:///var/run/docker.sock --storage-driver vfs &")
time.sleep(3)  # delays for 3 seconds

# variable to check and skipp build if duplicate
duplicate_folder_path = ""

# Get environment variables
USERNAME = os.getenv("DOCKER_USERNAME")
PASSWORD = os.getenv("DOCKER_PASSWORD")
REPOSITORY = os.getenv("DOCKER_REGISTRY")
ORGANIZATION = os.getenv("PLUGIN_ORGANIZATION")
last_commit_id = os.getenv("DRONE_PREV_COMMIT_SHA") or os.getenv("DRONE_COMMIT_SHA")

# Run git diff to check for modified or added files & folders
cmd = "git diff --name-status " + \
      last_commit_id + \
      " HEAD | awk '{print $2}'"
status, output = commands.getstatusoutput(cmd)
# beautify output, get folder/file
try:
    changed_objects = output.split("\n")
except ValueError:
    print "No changes. Skipping build..."
    exit(0)

# Connect to local docker daemon
client = docker.DockerClient(version="auto")

for ob in changed_objects:  # loop through folder lists
    if ob != ".drone.yml" and ob != ".drone.yml.sig":  # skip build if only drone config files are changed
        folder_path = os.path.dirname(ob)  # get folder name
        if folder_path == duplicate_folder_path:  # check for duplication, skip if true
            break
        client.login(username=USERNAME,
                     password=PASSWORD,
                     registry=REPOSITORY)  # authenticate with repository
        if os.path.isfile(folder_path + "/Dockerfile"):  # check if modified folders have Dockerfile or not
            print "building " + folder_path + " image..."
            client.images.build(path=folder_path,
                                tag=REPOSITORY + "/" + ORGANIZATION + "/" + folder_path + ":latest",
                                rm=True,
                                cache_from=["alpine"],
                                timeout=120)  # build image

            print "pushing " + folder_path + " to " + REPOSITORY + "..."
            client.images.push(repository=REPOSITORY + "/" + ORGANIZATION + "/" + folder_path,
                               tag="latest")  # push image to repository
            duplicate_folder_path = folder_path
