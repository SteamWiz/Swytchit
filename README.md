# Swytchit

Switch environment context easily in the shell

## Usage

```bash
sw your/project/directory
```

- `sw` (no argument) — argparse prints a usage error and exits with code 2
- Performs a `cd` operation to the project
- Starts a subshell
- Within the subshell, runs `source` on `.swytchitrc.sh` files in the project directory and any ancestor directories

Use the `exit` command when done with the project to exit the subshell and clear the environment.

Note that `.swytchitrc.sh` can support any source operation, including:

- Set environment variables
- Define aliases
- Define functions

## Why?

- Easily switch virtual environments for scripting languages (Python, Ruby, etc)
- Easily populate project-specific environment variables and aliases
- Use with the `op` CLI from 1Password to keep project-specific secrets in memory

## Installation (MacOS)

```bash
brew install pipx
pipx install swytchit
```

Also do a profile/rc song and dance something like this:

```bash
echo 'if [[ -n $SWYTCHITRC ]]; then source $SWYTCHITRC; fi' >> $ZDOTDIR/.zshrc
source $ZDOTDIR/.zshrc
```

(use e.g. `.profile` or `.bashrc` if not on `zsh`)


## Rules

- Only works in TTY shell (no piping)
- Only works for a descendent of user's home directory
- Resolves symlinks first
