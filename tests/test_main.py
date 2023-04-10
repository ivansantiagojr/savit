from pathlib import Path

import pytest
from typer.testing import CliRunner

from savit.config import CONFIG_FILE
from savit.main import app

runner = CliRunner()


@pytest.fixture
def temp_config_file():
    config_file = CONFIG_FILE
    if config_file.exists():
        config_file.unlink()
    yield config_file


def test_main_help():
    result = runner.invoke(app, ['--help'])
    assert result.exit_code == 0
    assert 'Helping you to write docs by saving your commands' in result.output


def test_start_help():
    result = runner.invoke(app, ['start', '--help'])
    assert result.exit_code == 0
    assert 'Start saving your commands' in result.output


def test_start_no_config(temp_config_file):
    if temp_config_file.exists():
        temp_config_file.unlink()

    result = runner.invoke(app, ['start'], input='y\nmd\n\n')

    assert result.exit_code == 0
    assert temp_config_file.exists()


def test_start_with_config():
    result = runner.invoke(app, ['start'])
    assert result.exit_code == 0
    assert 'Started saving' in result.output


def test_config_help():
    result = runner.invoke(app, ['config', '--help'])
    assert result.exit_code == 0
    assert (
        'Saves your configurations to ~/.config/savit/config.toml'
        in result.output
    )


def test_config_file_exists():
    result = runner.invoke(app, ['config'])
    assert result.exit_code == 0
    assert 'Config file already exists' in result.output


def test_config_file_does_not_exist(temp_config_file: Path):
    if temp_config_file.exists():
        temp_config_file.unlink()

    result = runner.invoke(app, ['config'], input='y\nmd\n\n')

    assert result.exit_code == 0
    assert temp_config_file.exists()


def test_config_open_file():
    result = runner.invoke(app, ['config', '--open-file'])
    assert result.exit_code == 0


def test_stop_help():
    result = runner.invoke(app, ['stop', '--help'])
    assert result.exit_code == 0
    assert (
        'Stop saving your commands and writes them to a file' in result.output
    )


def test_stop():
    result = runner.invoke(app, ['stop'])
    assert result.exit_code == 0
    assert 'Commands saved' in result.output


def test_stop_txt():
    result = runner.invoke(app, ['stop', '--txt'])
    assert result.exit_code == 0
    assert 'Commands saved' in result.output


def test_stop_md():
    result = runner.invoke(app, ['stop', '--md'])
    assert result.exit_code == 0
    assert 'Commands saved' in result.output


def test_stop_with_file():
    result = runner.invoke(app, ['stop', '--file', 'test.txt'])
    assert result.exit_code == 0
    assert 'Commands saved' in result.output


def test_stop_with_file_and_txt_or_md():
    result = runner.invoke(app, ['stop', '--file', 'test.txt', '--md'])

    assert result.exit_code == 0
    assert (
        "You can't use --txt or --md with --file. Use only one of them"
        in result.stdout
    )


def test_stop_with_absotule_path_file():
    result = runner.invoke(app, ['stop', '--file', '/tmp/test.txt'])
    assert result.exit_code == 0
    assert 'Commands saved' in result.output


def test_stop_config_does_not_exist(temp_config_file):
    if temp_config_file.exists():
        temp_config_file.unlink()

    result = runner.invoke(app, ['stop'])
    assert result.exit_code == 0
    assert 'File not found' in result.output
