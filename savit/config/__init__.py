import os
import tomllib
from pathlib import Path

import typer
from click import Choice

HISTORY_PATH = ""
DOT_CONFIG_FILE = Path.home() / ".config" / "savit"
CONFIG_FILE = DOT_CONFIG_FILE / "config.toml"


def set_env():
    DOT_CONFIG_FILE.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.touch(exist_ok=True)

    shell = os.getenv("SHELL")
    home = Path.home()
    if shell.find("zsh") != -1:
        config_toml_string = f"""[savit]
history_path = "{home}/.zhistory"
"""
        with CONFIG_FILE.open("w") as f:
            f.write(config_toml_string)

        with CONFIG_FILE.open("rb") as f:
            config_toml = tomllib.load(f)
        HISTORY_PATH = config_toml["savit"]["history_path"]

    elif shell.find("bash") != -1:
        config_toml_string = f"""[savit]
history_path = "{home}/.bash_history"
"""
        with CONFIG_FILE.open("w") as f:
            f.write(config_toml_string)

        with CONFIG_FILE.open("rb") as f:
            config_toml = tomllib.load(f)

        HISTORY_PATH = config_toml["savit"]["history_path"]

    elif shell.find("fish") != -1:
        config_toml_string = f"""[savit]
history_path = "{home}/.local/share/fish/fish_history"
"""
        with CONFIG_FILE.open("w") as f:
            f.write(config_toml_string)

        with CONFIG_FILE.open("rb") as f:
            config_toml = tomllib.load(f)

        HISTORY_PATH = config_toml["savit"]["history_path"]

    print(HISTORY_PATH)

    confirmation_prompt = typer.confirm("is this your history file?", default=True)
    if confirmation_prompt:
        print("Config file saved")

    else:
        print("Please change the HISTORY_PATH variable in the config file")

        HISTORY_PATH = Path(input("Enter the path of your history file: "))
        config_toml_string = f"""[savit]
history_path = {HISTORY_PATH}"""
        with CONFIG_FILE.open("w") as f:
            f.write(config_toml_string)

        print(f"{HISTORY_PATH} saved")

    output_format = typer.prompt(
        "Choose an output format", type=Choice(["txt", "md"]), show_choices=True
    )

    with CONFIG_FILE.open("a") as f:
        f.write(f'output_format = "{output_format}"')