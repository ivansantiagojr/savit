# `savit`

Helping you to write docs by saving your commands

**Usage**:

```console
$ savit [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `config`: Saves your configurations to ~/.config/savit/config.toml
* `start`: Start saving your commands
* `stop`: Stop saving your commands and writes them to a file

## `savit config`

Saves your configurations to ~/.config/savit/config.toml

**Usage**:

```console
$ savit config [OPTIONS]
```

**Options**:

* `--open-file`: Opens the config file  [default: False]
* `--help`: Show this message and exit.

## `savit start`

Start saving your commands

**Usage**:

```console
$ savit start [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `savit stop`

Stop saving your commands and writes them to a file

**Usage**:

```console
$ savit stop [OPTIONS]
```

**Options**:

* `--txt`: Saves your commands to a .txt file  [default: False]
* `--md`: Saves your commands to a .md file  [default: False]
* `--file PATH`: File (may include path) to save your commands
* `--help`: Show this message and exit.


**Points of attention**
* Don't use aliases to savit commands, since savit works by reading your shell history, the app will work in an unexpected way if aliases are used;
* Make sure to have your config file at `~/.config/savit/config.toml` correctly set up;


**Config file structure**
```toml
[savit]
history_path = "" # path to your shell history file
output_format = "" # output format to use by deafault (txt or md)
output_folder = "" # folder to save your commands by default (use ./ to save commands from the location where savit runs)
```