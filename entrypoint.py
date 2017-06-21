#!/usr/bin/env python
# coding=utf-8

# TODO: predefine env
import os
import docker
import time

os.system("dockerd &")

time.sleep(3)  # delays for 5 seconds

client = docker.DockerClient(version="auto")

client.images.build(path="hembuildbase/", tag="tuannvm/latest", cache_from=["alpine"], dockerfile="Dockerfile", timeout=10)
