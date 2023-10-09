# Ejecutar git pull
output=$(git pull)

# Verificar si la salida contiene "Enumerating objects"
if [[ $output == *"Enumerating objects"* ]]; then
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
else
    echo "NO HAY ACTUALIZACIONES"
fi

echo "FIN DEL BASH"

