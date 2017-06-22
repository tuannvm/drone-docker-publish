#!/usr/bin/env python
# coding=utf-8

# TODO: predefine env
import os
import docker
import time

 os.system("dockerd &")

 time.sleep(3)  # delays for 5 seconds

client = docker.DockerClient(version="auto")
last_commit = os.getenv("DRONE_PREV_COMMIT_SHA") or "276b8fffee67ddadb1c616caae3fb6a967a7b462"
cmd = "git diff --name-status " + last_commit + " HEAD | grep Dockerfile"
print os.system(cmd)

client.images.build(path="helmbuildbase/", tag="tuannvm/latest", cache_from=["alpine"], dockerfile="Dockerfile", timeout=10)
