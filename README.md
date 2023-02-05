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

* `config`: Saves your configurations to...
* `start`: Start saving your commands
* `stop`: Stop saving your commands and writes them to...

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

