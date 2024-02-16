import subprocess
# Comment to test
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print(f'Command: {command} executed successfully')
    else:
        print('Command failed with the following output:')
        print(result.stderr)
        exit(-1)

    print(result.stdout)
    
try:
    run_command(['sudo', 'mkdir', '/opt/raspberry-machine'])
except Excetion as e:
    print(f"ERROR: FALLO EN: {e}")
    
# REPLACE PROJECT FOLDER
#run_command(['sudo', 'mkdir', '/opt/raspberry-machine'])
run_command(['sudo', 'rm', '-r', '/opt/raspberry-machine'])
run_command(['sudo', 'cp', '-r', 'raspberry-machine', '/opt/'])
run_command(['sudo', 'chown', '-R', 'www-data:www-data', '/opt/raspberry-machine'])
run_command(['sudo', 'mkdir', '/opt/raspberry-machine/config/login_data'])
run_command(['sudo', 'touch', '/opt/raspberry-machine/config/login_data/venvias.json'])
run_command(['sudo', 'touch', '/opt/raspberry-machine/config/login_data/transactions.json'])
run_command(['sudo', 'chown', '-R', 'www-data:www-data', '/opt/raspberry-machine/config/login_data/'])

run_command(['sudo', 'cp', 'tag-pub-v2', '/etc/tolls/'])
run_command(['sudo', 'chown', '-R', 'www-data:www-data', '/etc/tolls/tag-pub-v2'])

# Comando para crear o editar el crontab
#crontab_cmd = 'crontab -'

# Contenido del cron job que se agregará al crontab
#cron_job = '* * * * * tail -n 10000 /var/log/apache2/raspberry/api-error.log > /var/log/apache2/raspberry/api-error.tmp && mv /var/log/apache2/raspberry/api-error.tmp /var/log/apache2/raspberry/api-error.log\n'

# Crear o editar el crontab
#subprocess.run(crontab_cmd, input=cron_job.encode(), shell=True, check=True)
#
command = ['sudo', 'chmod', 'u+rw', '/var/log/apache2/raspberry/api-error.log']
run_command(command)
# UPDATE DEPENDENCIES
run_command(['sudo', '/opt/raspberry-var/venv/bin/pip', 'install', '-r', '/opt/raspberry-machine/requirements-release.txt'])

command = ['sudo', 'cp', 'manage.sh', '/opt/raspberry-commands/']
run_command(command)
command = ['sudo', "usermod", "-a", "-G", "dialout", "www-data"]
run_command(command)
command = ['sudo', 'chmod', '+x', '/opt/raspberry-commands/manage.sh']
run_command(command)


run_command(['sudo', '/opt/raspberry-commands/manage.sh', 'migrate'])
run_command(['sudo', '/opt/raspberry-commands/manage.sh', 'makemigrations'])
run_command(['sudo', '/opt/raspberry-commands/manage.sh', 'migrate'])

  
