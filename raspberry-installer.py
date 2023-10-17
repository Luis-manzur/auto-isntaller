import subprocess
import sys


def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed with the following output: {result.stderr}")
        exit(-1)
    print(result.stdout)


def  install_packages(packages):
    for package in packages:
        command = ["sudo", "apt-get", "install", "-y", package]
        run_command(command)


def create_project_folder():
    command = ['sudo', 'cp', '-r', 'raspberry-machine', '/opt/']
    run_command(command)

    command = ['sudo', 'chown', 'www-data:www-data', '/opt/raspberry-machine']
    run_command(command)
    run_command(['sudo', 'mkdir', '/opt/raspberry-machine/config/login_data'])
    run_command(['sudo', 'touch', '/opt/raspberry-machine/config/login_data/venvias.json'])
    run_command(['sudo', 'touch', '/opt/raspberry-machine/config/login_data/transactions.json'])
    run_command(['sudo', 'chown', '-R', 'www-data:www-data', '/opt/raspberry-machine/config/login_data/'])

    subprocess.run(['sudo', 'chown', 'www-data:www-data', '/opt/raspberry-machine/config/login_data/'], capture_output=True, text=True)
    


def create_env():
    print('creating .env ...\n\n')

    command = ['sudo', 'mkdir', '/etc/tolls']
    run_command(command)

    command = ['sudo', 'cp', '.env', '/etc/tolls/api.env']
    run_command(command)

    run_command(['sudo', 'cp', 'tag-pub-v2', '/etc/tolls/'])
    run_command(['sudo', 'chown', '-R', 'www-data:www-data', '/etc/tolls/tag-pub-v2'])

    print('\n\n.env created\n\n')


def prepare_app_directories():
    print('preparing app directories ....\n\n')

    command = ['sudo', 'mkdir', '-p', '/opt/raspberry-var/log']
    run_command(command)

    command = ['sudo', 'mkdir', '-p', '/opt/raspberry-var/sessions']
    run_command(command)

    command = ['sudo', 'mkdir', '-p', '/opt/raspberry-var/updates']
    run_command(command)

    command = ['sudo', 'chown', '-R', 'www-data:www-data', '/opt/raspberry-var']
    run_command(command)

    command = ['sudo', 'chown', '-R', 'www-data:www-data', '/opt/raspberry-var/sessions/']
    run_command(command)

    command = ['sudo', 'chown', '-R', 'www-data:www-data', '/opt/raspberry-var/log/']
    run_command(command)

    command = ['sudo', 'chown', '-R', 'www-data:www-data', '/opt/raspberry-var/updates/']
    run_command(command)

    print('\n\nDirectories created\n\n')


def create_venv():
    print('Creating and installing dependencies ...\n\n')

    command = ['sudo', 'python3', '-m', 'venv', '/opt/raspberry-var/venv']
    run_command(command)

    command = ['sudo', 'usermod', '-a', '-G', 'gpio', 'www-data']
    run_command(command)

    command = ['sudo', '/opt/raspberry-var/venv/bin/pip', 'install', '-r', '/opt/raspberry-machine/requirements-release.txt']
    run_command(command)

    command = ['sudo', 'apt-get', 'install', '-y', 'libopenblas-dev']
    run_command(command)
    
    command = ['sudo', 'apt-get', 'install', '-y', 'libhdf5-dev']
    run_command(command)
    
    command = ['sudo', 'apt-get', 'install', '-y', 'libhdf5-serial-dev']
    run_command(command)
    
    command = ['sudo', 'apt-get', 'install', '-y', 'libatlas-base-dev']
    run_command(command)
    
    command = ['sudo', 'apt-get', 'install', '-y', 'libjasper-dev']
    run_command(command)
    
    
    run_command(command) 

    print('\n\nVenv created\n\n')


def create_admin_commands():
    print('Creating admin commands ... \n\n')

    command = ['sudo', 'mkdir', '-p', '/opt/raspberry-commands']
    run_command(command)

    command = ['sudo', 'cp', 'manage.sh', '/opt/raspberry-commands/']
    run_command(command)

    command = ['sudo', 'chmod', '+x', '/opt/raspberry-commands/manage.sh']
    run_command(command)

    command = ['sudo', '/opt/raspberry-commands/manage.sh', 'makemigrations']
    run_command(command)

    command = ['sudo', '/opt/raspberry-commands/manage.sh', 'migrate']
    run_command(command)

    command = ['sudo', 'chown', '-R', 'www-data:www-data', '/opt/']

    run_command(command)
    command = ['sudo', "usermod", "-a", "-G", "dialout", "www-data"]
    run_command(command)

    # Comando para crear o editar el crontab
    crontab_cmd = 'crontab -'

    # Contenido del cron job que se agregará al crontab
    cron_job = '* * * * * tail -n 10000 /var/log/apache2/raspberry/api-error.log > /var/log/apache2/raspberry/api-error.tmp && mv /var/log/apache2/raspberry/api-error.tmp /var/log/apache2/raspberry/api-error.log\n'

    # Crear o editar el crontab
    subprocess.run(crontab_cmd, input=cron_job.encode(), shell=True, check=True)

    command = ['sudo', 'chmod', 'u+rw', '/var/log/apache2/raspberry/api-error.log']
    
    
    print('\n\nCommands created and executed\n\n')


def activate_apache():
    print('Activating apache ...\n\n')

    command = ['sudo', 'cp', 'raspberry-api.conf', '/etc/apache2/sites-available/raspberry-api.conf']
    run_command(command)

    command = ['sudo', 'a2ensite', 'raspberry-api.conf']
    run_command(command)

    command = ['sudo', 'a2dissite', '000-default.conf']
    run_command(command)

    command = ['sudo', 'a2enmod', 'headers']
    run_command(command)

    command = ['sudo', 'systemctl', 'restart', 'apache2']
    run_command(command)

    print('\n\napache activated')


def print_instructions():
    print("""=== Check the status of the Apache2 service and that everything went correctly:
To see the running status (should have a green circle in front of it):
> sudo systemctl status apache2.service

To see the messages it gave when it started (only necessary if it gave an error and does not have a green circle):
> journalctl -xe

To check the application logs in case of error:
> tail -f /var/log/apache2/raspberry/api-error.log

Note 1: The -f option is to make it listen and show new logs as they appear in real time. You can call this command in a separate console and leave it there for a long time

Note 2: You canadd the "cut" command at the end to cut the date and time of the log ("-c 70-" is to show characters 70 onwards):
> tail -f /var/log/apache2/raspberry/api-error.log | cut -c 70-
> clear; tail -n 0 -f /var/log/apache2/raspberry/api-error.log | cut -c 79-

Note 3: The second command clears the screen and does not display any previously existing lines (-n 0). It will show the new ones that appear.

With this, the service should be running normally and listening for connections through port 8280""")


def main():
    packages = ["libqt5gui5", "libqt5webkit5", "libqt5test5"]
    install_packages(packages)

    create_project_folder()

    create_env()

    prepare_app_directories()

    create_venv()

    create_admin_commands()

    activate_apache()

    print_instructions()


def print_menu():
    print("1. Install packages")
    print("2. Create project folder")
    print("3. Create environment file")
    print("4. Prepare app directories")
    print("5. Create virtual environment")
    print("6. Create admin commands")
    print("7. Activate Apache")
    print("8. Run all")
    print("9. Quit")


def run_menu():
    while True:
        print_menu()
        choice = input("Enter your choice (1-9): ")

        if choice == "1":
            install_packages(["libqt5gui5", "libqt5webkit5", "libqt5test5"])
        elif choice == "2":
            create_project_folder()
        elif choice == "3":
            create_env()
        elif choice == "4":
            prepare_app_directories()
        elif choice == "5":
            create_venv()
        elif choice == "6":
            create_admin_commands()
        elif choice == "7":
            activate_apache()
        elif choice == "8":
            main()
        elif choice == "9":
            sys.exit()
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    run_menu()
