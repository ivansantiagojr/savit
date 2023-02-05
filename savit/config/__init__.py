import os
import tomllib
from pathlib import Path

import typer
from click import Choice

HISTORY_PATH = ""
DOT_CONFIG_FILE = Path(typer.get_app_dir("savit"))
CONFIG_FILE: Path = Path(DOT_CONFIG_FILE) / "config.toml"


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

    if confirmation_prompt := typer.confirm(
        "is this your history file?", default=True
    ):
        print("Config file saved")

    else:
        HISTORY_PATH = Path(input("Enter the path of your history file: "))
        config_toml_string = f"""[savit]
history_path = {HISTORY_PATH}"""
        with CONFIG_FILE.open("w") as f:
            f.write(config_toml_string)

        print(f"{HISTORY_PATH} saved")

    output_format = typer.prompt(
        "Choose an output format", type=Choice(["txt", "md"]), show_choices=True
    )
    output_folder = input(
        "Type the path to the folder where commands should be store (leave blank to save on current usage directory): "
    )

    with CONFIG_FILE.open("a") as f:
        f.write(f'output_format = "{output_format}"\n')
        if output_folder:
            f.write(f'output_folder = "{output_folder}"\n')
        else:
            f.write('output_folder = "./"')
