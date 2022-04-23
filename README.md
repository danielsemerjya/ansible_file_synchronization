# Introduction

This is a test problem, that will test your knowledge of Python, Ansible and Docker.

# Story

We have multiple machines in a cluster. 
Each of them stores small metadata file (several kilobytes) in some fixed location.
It is possible that machine will crash and this file will be lost. 

Objective of the task is to make sure that metadata file is present and has the same contents on all machines.
For simplicity, we can assume that at any time there is at least one server that has metadata file.

# To do

You are given a skeleton of the code with associated tests.
Business logic is implemented in Ansible.
Test is implemented in Python with a help of Docker.

Your task is to complete both business logc and tests following hints marked with `#TODO` marks.

## Implement logic of the file synchronization.
`synchronize_file.yml` requires `fileToSync` variable to be defined, which contains path with metadata file.

Its semantics is as follows:

- *You can assume that it is impossible for two machines to have different metadata file.*
- If metadata file is absent on all machines, playbook should fail immediately with human-readable error message.
- Otherwise playbook should take the metadata file from one machine that does have it and copy file to all machines that don't.

## Write tests for the playbook.
Implementation of tests has been started in the `run_tests.py`. 
Use created helper functions to run tests in Docker containers. 
Refer to the example test that shows how to use the framework.

## Optimize runtime of tests
Currently tests use CentOS image to run. 
Change it so test builds its own lightweight image.
Also, there is a lag in stopping/removing test containers that you are asked to get rid of. Tearing down containers should take less than a second.

# How to use given project
You need to have docker-ce, python3 and python3-virtualenv installed.

To run tests use `run_tests.sh` script.

Good luck!
