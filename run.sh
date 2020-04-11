#!/bin/bash



path="/home/$(ls /home)"



echo $path


if [ -d $SNAP_DATA/pythoncode ]; then
	cd $SNAP_DATA/pythoncode
	python3 $SNAP/bin/pythoncode/app.py
	exit 0
else
	mkdir $SNAP_DATA/pythoncode
	cp -r $SNAP/bin/pythoncode/*.json $SNAP_DATA/pythoncode/
	cd $SNAP_DATA/pythoncode
	python3 $SNAP/bin/pythoncode/app.py
	exit 0
fi


exit 1


