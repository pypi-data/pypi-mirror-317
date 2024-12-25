import sys
import os
import yaml
import subprocess

from .app import IgniteApp
from .route import get_registered_routes
from .config import load_settings_from_file, settings

DEFAULT_CONFIG_FILE = "ignite.yaml"

def load_ignite_yaml():
    if not os.path.exists(DEFAULT_CONFIG_FILE):
        return {}
    with open(DEFAULT_CONFIG_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def save_ignite_yaml(data: dict):
    with open(DEFAULT_CONFIG_FILE, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False)

def main(argv):
    config_path = None
    other_args = []
    for arg in argv[1:]:
        if arg.startswith("--config="):
            config_path = arg.split("=", 1)[1]
        else:
            other_args.append(arg)

    if config_path:
        loaded = load_settings_from_file(config_path)
        settings.DEBUG = loaded.DEBUG
        settings.DATABASE_URL = loaded.DATABASE_URL
        settings.SECRET_KEY = loaded.SECRET_KEY
        settings.JWT_SECRET = loaded.JWT_SECRET
        settings.PLUGINS_FOLDER = loaded.PLUGINS_FOLDER

    if not other_args:
        print("Usage: ignite <command> [options]")
        sys.exit(1)

    command = other_args[0]
    args = other_args[1:]

    if command == "init":
        init_project_config()
    elif command == "config":
        config_cmd(args)
    elif command == "run":
        run_script_cmd(args)
    elif command == "runserver":
        run_server_cmd(args)
    elif command == "db":
        db_cmd(args)
    else:
        print(f"Unknown command: {command}")

def init_project_config():
    if os.path.exists(DEFAULT_CONFIG_FILE):
        print(f"{DEFAULT_CONFIG_FILE} already exists.")
        return

    data = {
        "name": "my-ignite-project",
        "version": "0.1.0",
        "description": "A new Ignite project.",
        "scripts": {
            "start": "python manage.py runserver --config=configs/development.yaml",
            "syncdb": "python manage.py db sync --config=configs/development.yaml"
        },
        "plugins_folder": "plugins",
        "dependencies": {}
    }
    save_ignite_yaml(data)
    print(f"Created {DEFAULT_CONFIG_FILE} with default settings.")

def config_cmd(args):
    if not args:
        print("Usage: ignite config <set|get|show> [options]")
        return

    subcmd = args[0]
    data = load_ignite_yaml()

    if subcmd == "set":
        if len(args) < 3:
            print("Usage: ignite config set <key> <value>")
            return
        key = args[1]
        value = " ".join(args[2:])
        data[key] = value
        save_ignite_yaml(data)
        print(f"Set '{key}' = '{value}' in {DEFAULT_CONFIG_FILE}")

    elif subcmd == "get":
        if len(args) < 2:
            print("Usage: ignite config get <key>")
            return
        key = args[1]
        val = data.get(key)
        if val is None:
            print(f"'{key}' not found in {DEFAULT_CONFIG_FILE}")
        else:
            print(val)

    elif subcmd == "show":
        import pprint
        pprint.pprint(data)

    else:
        print(f"Unknown config subcommand: {subcmd}")

def run_script_cmd(args):
    if not args:
        print("Usage: ignite run <scriptName>")
        return
    script_name = args[0]

    data = load_ignite_yaml()
    scripts = data.get("scripts", {})
    if script_name not in scripts:
        print(f"Script '{script_name}' not found in {DEFAULT_CONFIG_FILE}")
        return

    command_line = scripts[script_name]
    print(f"Running script '{script_name}': {command_line}")
    subprocess.run(command_line, shell=True)

def run_server_cmd(args):
    app = IgniteApp()
    from .route import get_registered_routes
    for path, func, methods in get_registered_routes():
        app.add_route(path, func, methods)
    app.run()

def db_cmd(args):
    if not args:
        print("Usage: ignite db <subcommand>")
        return
    subcmd = args[0]
    if subcmd == "sync":
        from .db import create_database
        db = create_database(settings.DATABASE_URL)
        db.connect()
        print("[DB] Synced successfully.")
    else:
        print(f"Unknown db subcommand: {subcmd}")
