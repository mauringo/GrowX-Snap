#!/bin/bash

sleep 5

path="/home/$(ls /home)"


python3 $SNAP/bin/pythoncode/camera.py
