# Modular Framework for the Rock-Paper-Scissors Game.

![Rock Paper Scissors image](https://raw.githubusercontent.com/JamzTyson/Rock_Scissors_Paper/main/assets/rsp.png)


*A solo game of "Rock, Paper, Scissors" against the computer, implemented in
modern Python.*

## Purpose
This project provides a modular and extensible framework for creating and
experimenting with the Rock-Paper-Scissors game and its variants.

While the default game implements the classic three-choice version
(Rock, Paper, Scissors) with a simple Terminal interface, the architecture
supports:

- Adding more choices with cyclic rules
(e.g., Rock-Paper-Scissors-Lizard-Batman).
- Adding a more complex or graphical interface.
- Customising input handling and game logic.
- Adding more players.
- Adding more advanced strategies for the computer player.
- Defining new rules and behaviors.

## Overview

A dynamic implementation of "Rock, Paper, Scissors" against the computer,
with support for additional choices. The game uses cyclic rules to determine
the winner, ensuring every option beats some choices and is beaten by an equal
number of other choices, thus there must be an odd number of choices.

## Features

- Play the classic version of "Rock, Paper, Scissors."
- Extend the game with custom rules, more choices, or alternative
user interface.
- Unit tests (pytest) are provided to validate game logic.

## How It Works

Rather than hard coded "Scissor beats Paper" rules, the game generates rules
dynamically from a list of choices, following the rules:

1. Each item beats `(n-1)//2` predecessors and is beaten by `(n-1)//2`
successors, where `n` is the total number of choices.
2. The total number of choices (`DEFAULT_CHOICE_NAMES`) must always be odd.
3. Choices cannot start with the letter 'Q' (reserved for "Quit").
4. All choices must start with a unique letter.

### Example Custom Configuration

An example configuration with five options:

```python
DEFAULT_CHOICE_NAMES = ('Rock', 'Batman', 'Paper', 'Lizard', 'Scissors')
```

The corresponding rules would be:

- **Rock blunts Scissors:** Rock wins.
- **Rock crushes Lizard:** Rock wins.
- **Batman vaporizes Rock:** Batman wins.
- **Batman smashes Scissors:** Batman wins.
- **Paper disproves Batman:** Paper wins.
- **Paper wraps Rock:** Paper wins.
- **Lizard eats Paper:** Lizard wins.
- **Lizard poisons Batman:** Lizard wins.
- **Scissors decapitate Lizard:** Scissors win.
- **Scissors cut Paper:** Scissors win.
- **Draw:** Both choose the same option.


If you make changes to DEFAULT_CHOICE_NAMES, ensure that you run
[test_default_choices.py](rock_scissors_paper_framework/tests/test_default_choices.py).

## Getting Started

### Prerequisites

- Python 3.10.11 or later.
- Pytest (for running unit tests)

See the [pyproject.toml](pyproject.toml) file for full details.

## Running the game

It is not necessary to install this game to run it, though instructions for
installing are provided in the [Installation](#installing-the-game) section.

The quickest way to run the latest version of the game is to simply
download the raw `.py` file from the
[GitHub Repository](https://github.com/JamzTyson/Rock_Scissors_Paper/blob/main/rock_scissors_paper_framework/rsp.py)
and run it from a terminal window:

```bash
python3 /path/to/rsp.py
```

## Cloning this repository:

```bash
git clone https://github.com/JamzTyson/Rock_Scissors_Paper.git
```

**Running the game from the cloned repository:**

Navigate to the project directory:

```bash
cd rock_scissors_paper_framework
```

And then launch the game with:

```bash
python3 rsp.py
```


## Installing the Game

### Installing from PyPi

The recommended way to install the game is to install for the
current user with [pipx](https://pipx.pypa.io/latest/installation/).

```bash
pipx install rock-scissors-paper-framework
```

**Note:** The PyPI package name is rock-scissors-paper-framework, but
the package is imported as rock_scissors_paper_framework in your Python code.
After installation, the main entry point for the game is the
`rsp` command or `rsp.py`.

If you prefer local development or customisation, install the package
within a virtual environment:

```bash
# Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install the package using pip (or pipx):
pip install rock-scissors-paper-framework

 # Run the application:
rsp

 # Deactivate the virtual environment when finished:
deactivate
```

## How to Play

1. Start the game by running rsp.py
2. When prompted, choose an option by typing its initial letter
(e.g., R for Rock, S for Scissors). The input is case-insensitive.
3. The computer selects its option randomly.
4. The winner is determined based on the [predefined rules](#default-rules).
5. Type `Q` to quit the game.

**Note:** If the game has been [installed](#installing-the-game), the `rsp.py`
file can be run using the command:

```bash
$ rsp
```


**Example Session:**

```bash
Player: 0 | Computer: 0

[R]ock, [P]aper, [S]cissors, or [Q] to quit:
```

Player enters R, S, or P (case-insensitive):

```bash
r
```

```bash
You = Rock : Computer = Scissors : YOU WIN
Player: 1 | Computer: 0
```

### Default Rules:

- **Rock blunts Scissors:** Rock wins.
- **Scissors cut Paper:** Scissors win.
- **Paper wraps Rock:** Paper wins.
- **Draw:** Both choose the same option.

## Contributing

Contributions are welcome!

If you encounter any bugs, please open an issue on the GitHub repository.

If you have ideas for new features, extended rules, or bug fixes, feel free
to submit a pull request. Please ensure your changes are well-documented and
are accompanied by pytests (if applicable).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE)
file for details.

**Author:** JamzTyson

For inquiries, reach out through GitHub issues or discussions.
