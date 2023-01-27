import os

import typer

app = typer.Typer()


HISTORY_PATH: str


@app.command()
def config():
    """
    Saves the path of your shell history file
    """
    shell = os.getenv("SHELL")
    home = os.getenv("HOME")
    if shell.find("zsh") != -1:
        HISTORY_PATH = f"{home}/.zhistory"

    elif shell.find("bash") != -1:
        HISTORY_PATH = f"{home}/.bash_history"

    elif shell.find("fish") != -1:
        HISTORY_PATH = f"{home}/.local/share/fish/fish_history"

    print(HISTORY_PATH)
    confirmation_prompt = input("is this your history file? [y/n]: ")
    if confirmation_prompt == "y":
        print("Config file saved")
    else:
        print("Please change the HISTORY_PATH variable in the config file")
        HISTORY_PATH = input("Enter the path of your history file: ")

    print(HISTORY_PATH)


@app.command()
def start():
    """
    Start saving your commands
    """
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
def stop():
    """
    Stop saving your commands and writes them to a file
    """
    with open(HISTORY_PATH, "r") as hist:
        hist_list = hist.readlines()
        start_index = (
            len(hist_list) - 1 - hist_list[::-1].index("python savit/main.py start\n")
        )
        saved_commands = hist_list[start_index + 1 : -1]
        with open("cmds/commands.md", "w") as commands:
            for command in saved_commands:
                commands.write(f"```sh\n{command}```\n\n")
            print("Commands saved")


if __name__ == "__main__":
    app()
