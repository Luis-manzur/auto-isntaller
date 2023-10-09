#!/bin/bash


# Check if there are new changes
if [[ $(git pull | grep -q "Enumerating objects") ]]; then
	echo "SI HAY NUEVA ACTUALIZACION"
    	# Fetched new data, unzip the file
	unzip tolls-raspberry-api_py3.9.2_release.zip
	# Rename the unzipped folder
	mv release-tolls-raspberry-api raspberry-machine
	# Run a Python file
	python raspberry-updater.py
	# Delete the folder
	rm -rf raspberry-machine
	# Restart Apache server
	sudo systemctl restart apache2
else
	echo "NO HAY CAMBIOS"
fi
