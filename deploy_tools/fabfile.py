from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, sudo
import random

REPO_URL = "https://github.com/anosike212/to_do.git"
USER = "ubuntu"
HOST = "3.17.147.108"
env.key_filename = ["~/documents/pythoncodes/networks/obey the testing goat.pem"]

def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ("database", "static", "virtualenv", "source"):
        sudo(f"mkdir -p {site_folder}/{subfolder}")

def _get_latest_source(source_folder):
    if exists(source_folder + "/.git"):
        sudo(f"cd {source_folder} && git fetch")
    else:
        sudo(f"git clone {REPO_URL} {source_folder}")
    current_commit = local("git log -n 1 --format=%H", capture=True)
    sudo(f"cd {source_folder} && git reset --hard {current_commit}")

def _update_settings(source_folder, site_name):
    settings_path = source_folder + "/to_do/settings.py"
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path, 
        'ALLOWED_HOSTS =.+$',
        f'ALLOWED_HOSTS = ["{site_name}"]'
    )
    secret_key_file = source_folder + "/to_do/secret_key.py"
    if not exists(secret_key_file):
        chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        key = "".join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + "/../virtualenv"
    if not exists(virtualenv_folder + "/bin/pip"):
        sudo(f"python3.6 -m venv {virtualenv_folder}")
    sudo(f"{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt")

def _update_static_files(source_folder):
    sudo(
        f"cd {source_folder}"
        " && ../virtualenv/bin/python manage.py collectstatic --noinput"
    )

def _update_database(source_folder):
    sudo(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py migrate --noinput'
    )

def deploy():
    site_folder = f"/home/{env.user}/sites/{env.host}"
    source_folder = site_folder + "/source"
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)