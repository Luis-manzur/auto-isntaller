import subprocess
import os


def print_result(result):
    if result.returncode == 0:
        print('Command executed successfully')
    else:
        print('Command failed with the following output:')
        print(result.stderr)
        exit(-1)

    print(result.stdout)


def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    print_result(result)


def update_system():
    print('sudo apt update, running....')
    run_command(['sudo', 'apt', 'update'])


def install_apache():
    print('sudo apt install -y apache2, running....')
    run_command(['sudo', 'apt', 'install', '-y', 'apache2'])


def modify_hosts_file():
    print('modifying hosts ...')
    with open('/etc/hosts', 'a') as f:
        f.write('127.0.0.1 api.raspberry.com\n')
    print('host modified')


def configure_apache_ports():
    print('Configuring apache ports...')
    with open('/etc/apache2/ports.conf', 'r') as f:
        content = f.read()
    content = content.replace('Listen 443', '#Listen 443')
    content = content.replace('<IfModule ssl_module>', '#<IfModule ssl_module>')
    content = content.replace('<IfModule mod_gnutls.c>', '#<IfModule mod_gnutls.c>')
    content = content.replace('</IfModule>', '#</IfModule>')
    content += '\n# Regional API\nListen 8280\n'
    with open('/etc/apache2/ports.conf', 'w') as f:
        f.write(content)
    print('Apache ports configured')


def configure_apache_server():
    print('Configuring apache server...')
    with open('/etc/apache2/apache2.conf', 'r') as f:
        content = f.read()
    content += '\nServerName api.raspberry.com\n'
    with open('/etc/apache2/apache2.conf', 'w') as f:
        f.write(content)
    print('Apache server configured')


def create_directories():
    print('creating log and sessions directories...')
    subprocess.run(['sudo', 'mkdir', '-p', '/var/log/apache2/raspberry'], check=True)
    subprocess.run(['sudo', 'chown', '-R', 'www-data:www-data', '/var/log/apache2/raspberry'], check=True)
    subprocess.run(['sudo', 'mkdir', '-p', '/opt/raspberry-var/sessions'], check=True)
    subprocess.run(['sudo', 'chown', '-R', 'www-data:www-data', '/opt/raspberry-var/sessions'], check=True)
    print('log and sessions directories created')


def enable_apache_modules():
    print('Enabling Apache modules ...')
    run_command(['sudo', 'apt-get', 'install', '-y', 'python3-pip', 'apache2', 'libapache2-mod-wsgi-py3'])
    run_command(['sudo', 'a2enmod', 'wsgi'])
    print('Apache modules enabled')


def grant_apache_permissions():
    print('Granting apache permissions')
    with open('/etc/sudoers', 'r') as f:
        content = f.readlines()

    sudo_index = content.index('%sudo\tALL=(ALL:ALL) ALL\n') + 1
    content.insert(sudo_index, '\nCmnd_Alias WWW_ACTIONS=/usr/bin/systemctl reload apache2, /usr/bin/chown -R www-data\:www-data /opt/raspberry-machine\n')

    with open('/etc/sudoers', 'w') as f:
        f.writelines(content)

    subprocess.run(['sudo', 'gpasswd', '--add', 'www-data', 'dialout'], check=True)
    print('All apache permissions granted')


def run_all():
    update_system()
    install_apache()
    modify_hosts_file()
    configure_apache_ports()
    configure_apache_server()
    create_directories()
    enable_apache_modules()
    grant_apache_permissions()


def run_func(func):
    if func == 'update_system':
        update_system()
    elif func == 'install_apache':
        install_apache()
    elif func == 'modify_hosts_file':
        modify_hosts_file()
    elif func == 'configure_apache_ports':
        configure_apache_ports()
    elif func == 'configure_apache_server':
        configure_apache_server()
    elif func == 'create_directories':
        create_directories()
    elif func == 'enable_apache_modules':
        enable_apache_modules()
    elif func == 'grant_apache_permissions':
        grant_apache_permissions()


def main_menu():
    while True:
        choice = input('Choose an option:\n1. Run all functions\n2. Run a specific function\n3. Exit\n')

        if choice == '1':
            run_all()
        elif choice == '2':
            func_choice = input('Choose a function to run:\n1. update_system()\n2. install_apache()\n3. modify_hosts_file()\n4. configure_apache_ports()\n5. configure_apache_server()\n6. create_directories()\n7. enable_apache_modules()\n8. grant_apache_permissions()\n')
            if func_choice == '1':
                run_func('update_system')
            elif func_choice == '2':
                run_func('install_apache')
            elif func_choice == '3':
                run_func('modify_hosts_file')
            elif func_choice == '4':
                run_func('configure_apache_ports')
            elif func_choice == '5':
                run_func('configure_apache_server')
            elif func_choice == '6':
                run_func('create_directories')
            elif func_choice == '7':
                run_func('enable_apache_modules')
            elif func_choice == '8':
                run_func('grant_apache_permissions')
            else:
                print('Invalid choice. Please choose again.')
        elif choice == '3':
            break
        else:
            print('Invalid choice. Please choose again.')


if __name__ == '__main__':
    main_menu()