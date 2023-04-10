import tomllib
from pathlib import Path
from typing import Optional

import typer

from savit.config import CONFIG_FILE, set_env

app = typer.Typer(help='Helping you to write docs by saving your commands')


@app.command()
def config(
    open_file: bool = typer.Option(
        False, '--open-file', help='Opens the config file'
    )
) -> None:
    """
    Saves your configurations to ~/.config/savit/config.toml
    """
    if open_file:
        typer.launch(str(CONFIG_FILE), locate=True)
        raise typer.Exit()
    if CONFIG_FILE.exists():
        print('Config file already exists')
        raise typer.Exit()

    set_env()


@app.command()
def start() -> None:
    """
    Start saving your commands
    """

    if not CONFIG_FILE.exists():
        set_env()

    saving = typer.style('saving', fg=typer.colors.GREEN)
    savit_stop = typer.style('savit stop', fg=typer.colors.BLUE)
    typer.echo(
        f"""
               Started {saving}!
               Use your commands and when you are done use {savit_stop} 
               Don't erase your shell history file!
               """
    )


@app.command()
def stop(
    txt: bool = typer.Option(
        False, '--txt', help='Saves your commands to a .txt file'
    ),
    md: bool = typer.Option(
        False, '--md', help='Saves your commands to a .md file'
    ),
    file: Optional[Path] = typer.Option(
        None, help='File (may include path) to save your commands'
    ),
) -> None:
    """
    Stop saving your commands and writes them to a file
    """
    try:
        with CONFIG_FILE.open('rb') as f:
            config_toml = tomllib.load(f)
            hist_path = config_toml['savit']['history_path']

        with open(hist_path, 'rb') as hist:
            hist_list = [
                command.decode('utf-8') for command in hist.readlines()
            ]

            start_index = (
                len(hist_list) - 1 - hist_list[::-1].index('savit start\n')
            )
            saved_commands = hist_list[start_index + 1 : -1]

        output_format = config_toml['savit']['output_format']
        if file is None:
            if txt:
                output_format = 'txt'
            elif md:
                output_format = 'md'
            else:
                output_format = config_toml['savit']['output_format']

            output_folder = config_toml['savit']['output_folder']
            output_file = str(
                Path(output_folder) / f'commands.{output_format}'
            )
        elif txt or md:
            typer.secho(
                "You can't use --txt or --md with --file. Use only one of them",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit()

        elif not file.is_absolute():
            output_folder = config_toml['savit']['output_folder']
            output_file = str(Path(output_folder) / file)

        elif file.is_absolute():
            output_file = str(file)

        with open(output_file, 'w') as commands:
            for command in saved_commands:
                if output_format == 'txt' or output_file.endswith('.txt'):
                    commands.write(f'{command}')
                elif output_format == 'md' or output_file.endswith('.md'):
                    commands.write(f'```console\n{command}```\n\n')
            print('Commands saved')
    except FileNotFoundError as e:
        typer.echo(f'File not found: {e}', err=True)
    except Exception as e:
        typer.echo(f'Error: {e}', err=True)


@app.callback()
def main() -> None:
    """
    Save your commands
    """
    ...
