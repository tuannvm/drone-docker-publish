#!/usr/bin/env python
# coding=utf-8

# TODO: predefine env
import os
import docker
import time
import commands

REPOSITORY = os.getenv("PLUGIN_REGISTRY") or "quay.io"
ORGANIZATION = os.getenv("PLUGIN_ORGANIZATION") or "honestbee"
base_path = os.getenv("DRONE_REPO_LINK").split("//")[1] + "/"
last_commit_id = os.getenv("DRONE_PREV_COMMIT_SHA") or "3b2b483ec8e81ecd88db428111cc89474b9cc37c"
cmd = "cd " + base_path + " && git diff --name-status " + last_commit_id + " HEAD | awk '{print $2}'"

os.system("dockerd &")
time.sleep(3)  # delays for 5 seconds

client = docker.DockerClient(version="auto")
# cmd = "cd /Users/tuannvm/Projects/honestbee/base-images && git diff --name-status " + last_commit_id + \ " HEAD | awk '{print $2}'"

status, output = commands.getstatusoutput(cmd)
changed_objects = output.split("\n")

for ob in changed_objects:
    if ob != ".drone.yml" and ob != ".drone.yml.sig":
        folder_path = os.path.dirname(ob)
        if os.path.isfile(folder_path + "/Dockerfile"):
            client.images.build(path=folder_path,
                                tag=REPOSITORY + "/" + ORGANIZATION + "/" + folder_path + ":latest",
                                rm=True,
                                cache_from=["alpine"],
                                timeout=120)
        else:
            print "No changes. Skipping build..."
