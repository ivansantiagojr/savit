import os
from pathlib import Path
from typing import Final

import typer
from click import Choice

HISTORY_PATH = ""
DOT_CONFIG_FILE: Final[Path] = Path(typer.get_app_dir("savit"))
CONFIG_FILE: Final[Path] = Path(DOT_CONFIG_FILE) / "config.toml"


def _get_shell_history(home: Path, config_file_name: str) -> str:
    return str(home) + config_file_name


def set_env() -> None:
    DOT_CONFIG_FILE.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.touch(exist_ok=True)

    shell = str(os.getenv("SHELL"))
    home = Path.home()
    if "zsh" in shell:
        HISTORY_PATH = _get_shell_history(home, "/.zhistory")
    elif "bash" in shell:
        HISTORY_PATH = _get_shell_history(home, "/.bash_history")
    elif "fish" in shell:
        HISTORY_PATH = _get_shell_history(home, "/.local/share/fish/fish_history")

    print(HISTORY_PATH)

    if confirmation_prompt := typer.confirm("is this your history file?", default=True):
        config_toml_string = f"""[savit]
history_path = "{HISTORY_PATH}"
"""
        with CONFIG_FILE.open("w") as f:
            f.write(config_toml_string)

        print("Config file saved")

    else:
        HISTORY_PATH = input("Enter the path of your history file: ")
        config_toml_string = f"""[savit]
history_path = "{HISTORY_PATH}"
"""
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

    print(f"Options saved on {CONFIG_FILE}")
    print("You can edit the config file later if you want to change the options")
