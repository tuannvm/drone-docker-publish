#!/usr/bin/env python
# coding=utf-8

# TODO: predefine env
import os
import docker
import time
import commands

# USERNAME = os.getenv("DOCKER_USERNAME") or "tuannvm+quaybot"
USERNAME = os.getenv("DOCKER_USERNAME")
# PASSWORD = os.getenv("DOCKER_PASSWORD") or "V9WSBL9LWNGTTQBHE4J7C37PWC07JJAM65W2EMK1VWLK3I5FBEGQ7EWWHV2UPXD7"
PASSWORD = os.getenv("DOCKER_PASSWORD")
REPOSITORY = os.getenv("DOCKER_REGISTRY")
ORGANIZATION = os.getenv("PLUGIN_ORGANIZATION")
base_path = os.getenv("DRONE_REPO_LINK").split("//")[1] + "/"
# last_commit_id = os.getenv("DRONE_PREV_COMMIT_SHA") or "3b2b483ec8e81ecd88db428111cc89474b9cc37c"
last_commit_id = "3b2b483ec8e81ecd88db428111cc89474b9cc37c"
# last_commit_id = os.getenv("DRONE_PREV_COMMIT_SHA")
cmd = "git diff --name-status " + last_commit_id + " HEAD | awk '{print $2}'"

os.system("dockerd &")
time.sleep(3)  # delays for 5 seconds

client = docker.DockerClient(version="auto")
# cmd = "cd /Users/tuannvm/Projects/honestbee/base-images && git diff --name-status " + last_commit_id + " HEAD | awk '{print $2}'"

status, output = commands.getstatusoutput(cmd)
changed_objects = output.split("\n")

print USERNAME
print REPOSITORY
print ORGANIZATION
print base_path
print last_commit_id
print cmd
print changed_objects
for ob in changed_objects:
    if ob != ".drone.yml" and ob != ".drone.yml.sig":
        folder_path = os.path.dirname(ob)
        client.login(username=USERNAME, password=PASSWORD, registry=REPOSITORY)
        if os.path.isfile(folder_path + "/Dockerfile"):
            client.images.build(path=folder_path,
                                tag=REPOSITORY + "/" + ORGANIZATION + "/" + folder_path + ":latest",
                                rm=True,
                                cache_from=["alpine"],
                                timeout=120)

            client.images.push(repository=REPOSITORY + "/" + ORGANIZATION + "/" + folder_path, tag="latest")
        else:
            print "No changes. Skipping build..."
