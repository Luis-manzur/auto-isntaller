#!/bin/bash


# Check if there are new changes
if [[ $(git pull -uno | grep "Enumerating objects") ]]; then
	# Fetched new data, unzip the file
	unzip tolls-raspberry-api_py3.9.2_release.zip
	# Rename the unzipped folder
	mv release-tolls-raspberry-api raspberry-machine
	# Run a Python file
	python raspberry-updater.py
	# Delete the folder
	rm -rf raspberry-machine
	# Restart Apache server
	sudo sysemctl restart apache2
fi
