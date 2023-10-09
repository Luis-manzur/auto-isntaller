#!/bin/bash

$(git pull > a.txt)
# Ejecutar git pull y filtrar la salida con grep
if tail -n 100 a.txt | grep -q "file changed"; then
        # Ejecutar comandos adicionales
        echo "Actualizando..."
        # Agrega aquí los comandos que deseas ejecutar cuando hay actualizaciones
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
        rm a.txt
fi
