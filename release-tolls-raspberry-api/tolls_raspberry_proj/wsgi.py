"""
WSGI config for ticketing machine api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

is_runserver = 'runserver' in sys.argv[1:]
is_runsslserver = 'runsslserver' in sys.argv[1:]
is_running_development = is_runserver or is_runsslserver

# Import environment
use_env_file = os.environ.get('USE_ENV_FILE')
if use_env_file or (not is_running_development):
    from tolls_raspberry_proj.environment_vars import import_env, update_path

    import_env()
    update_path()

# Execute start-up commands
from startup_command import startup_command

startup_command()

# Load application

# noinspection PyUnresolvedReferences
import modules

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

import multiprocessing
import threading
import time
from logger import get_logger

logger = get_logger()

_server_stopped_signal = None


def stop_detector_proc(signal):
    try:
        while True:
            time.sleep(0.8)
    except KeyboardInterrupt:
        pass

    signal.set()


def wait_and_process():
    global _server_stopped_signal
    from api.login.utils import cleanup_db, reset_transits
    cleanup_db(remove_sessions=True, clear_runtime_cache=True)

    import settings
    from api.login_handlers import LoginHandlers
    time.sleep(0.5 if settings.IS_RUNNING_DEVELOPMENT else 2)

    if not settings.SIMULATE_PORTS:
        # noinspection PyUnresolvedReferences
        import RPi.GPIO as GPIO
        GPIO.cleanup()

    if reset_transits():
        logger.info('Transit and transaction data has been reset')
    else:
        logger.info('Error while trying to reset Transit and transaction data')

    # Load modules and drivers
    modules_template_context = {}

    # Inject environment variables to the modules template context
    env_prefix_transaction = 'FONTUR_'
    env_prefix_venvias = 'VENVIAS_'
    env_prefix_devices = 'DEVICES_'
    env_prefix_cobremex = 'COBREMEX_'
    env_prefix_transit_viewer = 'TRANSIT_VIEWER_'
    for k, v in os.environ.items():
        if k.startswith(env_prefix_transaction) or k.startswith(env_prefix_devices) or k.startswith(
                env_prefix_venvias) or k.startswith(env_prefix_cobremex) or k.startswith(env_prefix_transit_viewer):
            modules_template_context[k] = v

    # Remove regional.pickle file
    try:
        file = os.path.join(settings.SESSIONS_PATH, 'venvias.pickle')
        os.remove(file)
    except Exception as e:
        logger.info("Session file .pickle is already deleted")

    required_template_vars = (env_prefix_venvias, env_prefix_devices)
    all_loaded = modules.current_manager().load_modules(
        'modules', settings.MODULES_CONFIG_FILEPATH, modules_template_context,
        required_template_vars=required_template_vars)

    all_loaded = all_loaded and modules.current_manager().load_modules(
        'drivers', settings.DEVICES_CONFIG_FILEPATH, modules_template_context,
        required_template_vars=required_template_vars)

    if all_loaded:

        _server_stopped_signal = multiprocessing.Event()
        proc = multiprocessing.Process(
            target=stop_detector_proc, name='stop_detector', args=(_server_stopped_signal,))
        proc.start()

        login_handlers = LoginHandlers()
        login_handlers.register_handlers()

        while not _server_stopped_signal.wait(2):
            pass

        proc.join()

    # Stop drivers and modules
    modules.current_manager().stop()


if not os.environ.get('already_run'):
    if not is_running_development:
        # To allow the UI detect the server has started
        time.sleep(1.5)

    os.environ['already_run'] = 'true'
    thread = threading.Thread(target=wait_and_process, name='wait_and_process', daemon=False)
    thread.start()
