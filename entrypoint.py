#!/usr/bin/env python
# coding=utf-8
import os
import docker
import time

os.system("dockerd &")

time.sleep(3)  # delays for 5 seconds

client = docker.DockerClient(version="auto")

# client.images.build(path="./", tag="tuannvm/latest", cache_from=["alpine"], dockerfile="Dockerfile-test", timeout=10)
