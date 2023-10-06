##!/bin/sh

# Security
# export "ALLOWED_HOSTS=192.168.1.100 api.raspberry.com"
# export "CSRF_TRUSTED_ORIGINS=http://www.tolls-local.com:8090 http://localhost:8000  http://127.0.0.1:8000 http://192.168.1.163:8000"
# export "CORS_ORIGIN_WHITELIST=http://localhost:8000 http://www.tolls-local.com:8090 http://localhost:9000"

# # Config files
# export "DEVICES_FILE=devices.json"
# export "MODULES_FILE=modules.json"
# export "FARES_CONFIG_FILE=fares.json"


# # Var (Logs and sessions)
# export "LOGGING_LEVEL=INFO"
# export "LOG_DIRECTORY=/opt/raspberry-var/log"
# export "SESSIONS_PATH=/opt/raspberry-var/sessions"

# # Regional API
# export "REGIONAL_API_URL=https://tollsfontur.com:9088/api/"
# export "REGIONAL_API_USER=deferred_gate_taguanes"
# export "REGIONAL_API_PASSW=23-88pi54=.+(ajZ)"
# export "POST_REFERER=https://www.tollsfontur.com/"
# # RDS
# export "RDS_SQLITE3=/opt/raspberry-var/tolls-raspberry.db"

# # Node Info
# export "NODE_TYPE=gate"
# export "NODE_CODE=COJARMTG01"
# export "COMPANY_CODE=1010101010101"
# export "TOLL_SITE=COJ001"
# export "TOLLS_LANE=COJARMTG01"
# export "DIRECTION=entering"

# #Atenna
# export "ANTENNA_IP=192.168.1.99"
# export "CAMERA_USER=admin"

# #camera
# export "CAMERA_URL=127.0.0.1"
# export "CAMERA_USER=admin"
# export "CAMERA_PASSWORD=rseadmin123"

# #Fare
# export "FARE_CATEGORIES=625336d30fa751ed230b4a94,625336d30fa751ed230b4a95,625336d30fa751ed230b4a96,625336d30fa751ed230b4a97,625336d30fa751ed230b4a98,625336d30fa751ed230b4a99,625336d30fa751ed230b4a9a,625336d30fa751ed230b4a9b,62911b2ced9a2c01961f185d,62926868eee21a976ed2d7b3"
# export "TRAVEL_TIMES=3,4,6,6,7,8,12,12,12,30"

# # App
# export "DJANGO_SETTINGS_MODULE=tolls_raspberry_proj.settings"
# export "SIMULATE_PORTS=0"

# #Deferred calls
# export "DEFERRED_API_USER=deferred_gate_taguanes"
# export "DEFERRED_API_PASSW=23-88pi54=.+(ajZ)"

# # Restart Command
# export "RESTART_COMMAND=sudo usr/bin/systemctl reload apache2"
# export "STARTUP_COMMAND=sudo usr/bin/systemctl start pigpiod"
# export "REMOTE_API_URL=https://tollsfontur.com:9088/api/"
# export "PATH=$PATH:/opt/raspberry-machine/"

# # Pins
# export "GATE_UP_PIN=23"
# export "GATE_DOWN_PIN=24"
# export "GATE_STATUS_PIN=22"
# export "GATE_LOOP_PIN=27"
# export "BOOTH_LOOP_PIN=17"

# # Active Devices
# export "ANTENNA_ACTIVE=1"
# export "CAMERA_ACTIVE=0"
# export "GATE_ACTIVE=1"
# export "GATE_LOOP_ACTIVE=1"
# export "BOOTH_LOOP_ACTIVE=1"
# export "API_CALLER_ACTIVE=1"
# export "SYSTEM_STATE_STATISTICS_ACTIVE_SCREEN=1"
# export "SEND_DEFERRED_MESSAGES_TO_REGIONAL=1"

export "USE_ENV_FILE=/etc/tolls/api.env"

cd /opt/raspberry-machine
/opt/raspberry-var/venv/bin/python3 tolls_raspberry_proj/manage.pyc $1 $2 $3 $4 $5
