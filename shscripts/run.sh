#!/bin/bash

sleep 10

path="/home/$(ls /home)"



echo $path


if [ -d $SNAP_DATA/Payloads ]; then
	cd $SNAP_DATA
	python3 $SNAP/bin/pythoncode/app.py
	exit 0
else
	mkdir $SNAP_DATA/Payloads
	cp -r $SNAP/bin/pythoncode/Payloads/*.json $SNAP_DATA/Payloads/
	cd $SNAP_DATA
	python3 $SNAP/bin/pythoncode/app.py
	exit 0
fi


exit 1


