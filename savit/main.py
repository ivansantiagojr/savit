import tomllib

import typer

from savit.config import CONFIG_FILE, set_env

app = typer.Typer(help="Helping you to write docs by saving your commands")


@app.command()
def config():
    """
    Saves your configurations to ~/.config/savit/config.toml 
    """
    if CONFIG_FILE.exists():
        print("Config file already exists")
        raise typer.Exit()
    set_env()


@app.command()
def start():
    """
    Start saving your commands
    """

    if not CONFIG_FILE.exists():
        set_env()

    saving = typer.style("saving", fg=typer.colors.GREEN)
    savit_stop = typer.style("savit stop", fg=typer.colors.BLUE)
    typer.echo(
        f"""
               Started {saving}!
               Use your commands and when you are done use {savit_stop} 
               Don't erase your shell history file!
               """
    )


@app.command()
def stop(
    txt: bool = typer.Option(False, help="Saves your commands to a .txt file"),
    md: bool = typer.Option(False, help="Saves your commands to a .txt file"),
):
    """
    Stop saving your commands and writes them to a file
    """
    with CONFIG_FILE.open("rb") as f:
        config_toml = tomllib.load(f)
        hist_path = config_toml["savit"]["history_path"]

    with open(hist_path, "r") as hist:
        hist_list = hist.readlines()
        start_index = len(hist_list) - 1 - hist_list[::-1].index("savit start\n")
        saved_commands = hist_list[start_index + 1 : -1]

    if txt:
        output_format = "txt"
    elif md:
        output_format = "md"
    else:
        output_format = config_toml["savit"]["output_format"]

    with open(f"./commands.{output_format}", "w") as commands:
        for command in saved_commands:
            commands.write(f"```sh\n{command}```\n\n")
        print("Commands saved")


@app.callback(invoke_without_command=True)
def main():
    """
    Save your commands
    """
    ...
