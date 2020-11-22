#!/bin/bash

sleep 5

path="/home/$(ls /home)"



echo $path


if [ -d $SNAP_COMMON/Payloads ]; then
	cd $SNAP_COMMON
	python3 $SNAP/bin/pythoncode/app.py
	exit 0
else
	mkdir $SNAP_COMMON/Payloads
	cp -r $SNAP/bin/pythoncode/Payloads/*.json $SNAP_COMMON/Payloads/
	cd $SNAP_COMMON
	python3 $SNAP/bin/pythoncode/app.py
	exit 0
fi


exit 1


