"""Modular Framework for Rock-Paper-Scissors Game.

A flexible framework for building and customizing Rock-Paper-Scissors
and its variants. It is designed to be easily extended to include additional
choices and rules while maintaining the cyclic win-loss relationships.

The game is playable as an in-terminal solo game of 'Rock Paper Scissors'
against the computer.

Rules:
The choices are cyclically arranged such that:
    - Rock beats Scissors
    - Scissors beats Paper
    - Paper beats Rock

Features:
    - Validates custom game configurations.
    - Supports arbitrary numbers of choices, provided they meet specific
    criteria (e.g., odd number of choices, unique starting letters).
    - Modular components for game logic, user interface, and scoring.

The game may be extended with more choices that follow the rules:
    1. Each item beats (n-1)//2 predecessors and is beaten by the other
       (n-1)//2 items (where 'n' is the number of items).
    2. There must be an odd number of choices.
    3. No choice may begin with the `QUIT_KEY` character.
    4. All choices must begin with a unique letter.

Examples:
To add more choice _options, use a tuple like this::

    ('Rock', 'Batman', 'Paper', 'Lizard', 'Scissors')

The rules for extended choices would be:

    - Rock beats: Scissors and Lizard
    - Batman beats: Rock and Scissors
    - Paper beats: Batman and Rock
    - Lizard beats: Paper and Batman
    - Scissors beats: Lizard and Paper

Notes:
    Case-Insensitive Input Handling:
    Although lowercase normalization is more common, user input is normalized
    to uppercase to match the displayed menu _options. For example: 'R', 'P', 'S'.
"""

import logging
from dataclasses import dataclass, field
import os
import random
import sys
from enum import auto, Enum
from typing import Optional

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])


DEFAULT_CHOICE_NAMES: tuple[str, ...] = ('Rock', 'Paper', 'Scissors')
QUIT_KEY: str = 'Q'  # Reserved for quitting the program.

HandNames = tuple[str, ...]


class HandResult(Enum):
    """Possible results for each hand."""

    WIN = auto()
    LOSE = auto()
    DRAW = auto()


@dataclass
class Scores:
    """Tally of score for games played."""

    player: int = 0
    robo: int = 0


class GameOptions:
    """Game configuration for defining choices and rules.

    This class allows for custom configurations of game choices. It ensures
    that the rules of the game remain consistent by validating the provided
    choices.

    Designed for extensibility:
        - Add new choices with unique starting letters.
        - Ensure cyclic relationships between choices.

    Example:
        config = GameOptions(('Rock', 'Paper', 'Scissors', 'Lizard', 'Batman'))
    """

    def __init__(self, choice_names: HandNames) -> None:
        """Initialize game configuration object.

        choice names will be stripped of leading / trailing whitespace
        during validation.

        Args:
            choice_names (HandNames): A tuple of names for each Hand option.
        """
        self._hand_names: HandNames = self._validate_choices(choice_names)
        self._choice_keys: list[str] = self._generate_choice_keys()

    @property
    def names(self) -> HandNames:
        """Tuple of game choices.

        By default, this returns the strings 'Rock', 'Paper', 'Scissors' from
        DEFAULT_CHOICE_NAMES. If you wish to modify the available choices, ensure
        that you validate them.

        Returns:
            HandNames: The game choice names.
        """
        return self._hand_names

    @property
    def choice_keys(self) -> list[str]:
        """Return list of menu options."""
        return self._choice_keys

    @staticmethod
    def _validate_choices(choices: HandNames) -> HandNames:
        """Validate the provided game choices.

        Ensures the game configuration adheres to the rules:
            - Odd number of at least 3 choices.
            Required so that each choice beats the same number of choices
            as it is beaten by.
            - Each choice starts with a unique letter (case-insensitive).
            Required as choices are made by selecting the first letter.
            - Choices must be unique.

        Args:
            choices (HandNames): The hand names to choose from.

        Raises:
            TypeError: The choices are not tuple[str, ...].
            ValueError: The choices are invalid.

        Returns:
            HandNames: The validated tuple of choice names.
        """
        if not isinstance(choices, tuple):
            raise TypeError("Tuple required. "
                            f"Received {type(choices)}")

        if len(choices) < 3:
            raise ValueError("3 or more choices required. "
                             f"Received {len(choices)}")

        if len(choices) % 2 == 0:
            raise ValueError("Number of choices must be odd.")

        # Strip leading / trailing whitespace
        try:
            choices = tuple(choice.strip() for choice in choices)
        except AttributeError as exc:
            raise TypeError(f"Invalid choice name: {exc}") from exc

        # Check choice (str) items:
        found_choices: set[str] = set()
        found_keys: set[str] = set()
        for choice in choices:
            # choice is a string.
            if not isinstance(choice, str):
                raise TypeError("Each choice must be a string. "
                                f"Received {type(choice)}")
            # string not empty
            if choice == '':
                raise ValueError("Choice name cannot be an empty string.")
            # No duplicates
            if choice in found_choices:
                raise ValueError(f"Duplicate choice: {choice}")
            found_choices.add(choice)
            # Begins with a unique letter (case-insensitive).
            # Required as this version uses the first letter as the menu option.
            if choice[0].upper() in found_keys:
                raise ValueError("Each choice must begin with a unique letter. "
                                 f"Duplicate found: '{choice[0]}'.")
            found_keys.add(choice[0].upper())

        return choices

    def _generate_choice_keys(self) -> list[str]:
        """Generate a unique menu option for each Hand name.

        Currently, we use the uppercase first letter of the name, which
        must be unique.
        """
        return [choice[0].upper() for choice in self.names]


class UI:
    """Manages user interface ui.

    A simple text interface in a Terminal window.
    """

    def __init__(self, config: GameOptions) -> None:
        """Initialise user interface.

        Args:
            config (GameOptions): Contains Hand names and menu key properties.
        """
        self.names = config.names
        self._menu_options: list[str] = config.choice_keys

    def get_user_input(self) -> str:
        """Prompt user for input."""
        prompt = (f"{self._format_choices()}, "
                  f"or [{QUIT_KEY}] to quit: ")
        return input(prompt).strip().upper()

    def _format_choices(self) -> str:
        """Return formatted string of choices.

        Formatted string in the form:
            '[R]ock, [S]cissors, [P]aper'
        """
        return ', '.join([f"[{name[0].upper()}]{name[1:]}"
                          for name in self.names])

    def invalid_choice_message(self):
        """Display invalid choice message."""
        choice_str = ', '.join([f"'{option}'" for option in self._menu_options])
        print(f"Invalid choice. Must be one of: {choice_str}.")

    def display_result(self, game_score: Scores,
                       player: str = '',
                       robo: str = '',
                       result: Optional[HandResult] = None) -> None:
        """Display game result.

        Args:
            game_score (Scores): The current scores.
            player (str): The human player's hand name. Default = ''
            robo (str): The computer player's hand name. Default = ''
            result (HandResult): The Enum value 'WIN', 'LOSE' or 'DRAW'.
                Default = None
        """
        self.clear_screen()

        if result is not None:
            print(f"You = {player} : "
                  f"Computer = {robo} : YOU {result.name}")
        print(f"Player: {game_score.player} | Computer: {game_score.robo}\n")

    @staticmethod
    def exit_message() -> None:
        """Display exit message."""
        print("Bye")

    @staticmethod
    def clear_screen() -> None:
        """Clear Terminal ui."""
        if 'TERM' in os.environ:
            # Should work cross-platform for most terminals.
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            print('\n')  # In Thonny we settle for a new line.
            # Escape codes may work for other Terminal emulators.
            print("\n\033[H\033[J", end="")


@dataclass
class Hand:
    """Hand objects represent the hand gestures made by players of this game.

    Attributes:
        name (str): Example "Rock"
        choice_key (str): Example "R"
        beats_hands (list): A list of other Hand instances that this Hand beats.
    """

    name: str
    choice_key: str
    beats_hands: list['Hand'] = field(default_factory=list)


class HandManager:
    """Creates and manages Hand objects."""

    def __init__(self, options: GameOptions):
        """Initialize with game _options."""
        self._options = options

        # Create list of available Hand instances.
        self._hands = self._generate_hands()
        self._hands_by_key = self._map_key_to_hand()

        self._set_beats_properties()

    @property
    def hands(self) -> list[Hand]:
        """Return configured list of Hand objects.

        Used by robo_choice().
        """
        return self._hands

    def get_hand_by_key(self, key: str) -> Hand:
        """Return the Hand that has supplied key.

        Used by: player_choice().

        Raises:
            KeyError: If name is not a valid Hand name.

        Returns:
            Hand: The requested Hand.
        """
        return self._hands_by_key[key]

    def _generate_hands(self) -> list[Hand]:
        """Generate a list of Hands.

        One Hand for each GameOptions.name.
        Each Hand is initialised with a name and choice-key.
        """
        names = self._options.names
        keys = self._options.choice_keys
        return [Hand(name=name, choice_key=key) for name, key in zip(names, keys)]

    def _map_key_to_hand(self) -> dict[str, Hand]:
        """Return dict mapping choice keys to Hands."""
        return {hand.choice_key: hand for hand in self._hands}

    def _set_beats_properties(self) -> None:
        """Populate the 'beats_hands' properties of each Hand."""
        hand_beats_map = self._map_cyclic_hierarchy()
        for hand in self._hands:
            hand.beats_hands = hand_beats_map[hand.name]

    def _map_cyclic_hierarchy(self) -> dict[str, list[Hand]]:
        """Return dict mapping each hand name to a list of hands that it beats."""
        number_of_beaten = (len(self._options.names) - 1) // 2
        hierarchy_map = {}
        for idx, choice in enumerate(self._options.names):
            beaten = [self._hands[idx - j - 1] for
                      j in range(number_of_beaten)]
            hierarchy_map[choice] = beaten

        return hierarchy_map


def player_choice(hm: HandManager, ui: UI) -> Hand:
    """Prompt and return human's hand gesture object.

    Args:
        hm (HandManager): The HandManager object.
        ui (UI): The user interface object.

    Returns:
        Hand: The selected Hand() object.
    """
    while True:
        choice = ui.get_user_input()

        if choice == QUIT_KEY:
            quit_game(ui)

        try:
            return hm.get_hand_by_key(choice)
        except KeyError:
            ui.invalid_choice_message()


def robo_choice(hm: HandManager) -> Hand:
    """Return a randomly selected hand gesture object.

    Args:
        hm (HandManager): The HandManager object.

    Returns:
        Hand: The randomly selected hand object.
    """
    return random.choice(hm.hands)


def quit_game(ui: UI):
    """Exit the game and terminate the program."""
    ui.exit_message()
    sys.exit(0)


def main() -> None:
    """Game loop."""
    # Instantiate instances of Scores, GameOptions and UI.
    scores = Scores()
    config = GameOptions(DEFAULT_CHOICE_NAMES)
    ui = UI(config)

    ui.display_result(scores)

    # Generate hands available in this game.
    hand_manager = HandManager(config)

    while True:
        player_hand: Hand = player_choice(hand_manager, ui)
        robo_hand: Hand = robo_choice(hand_manager)

        if player_hand == robo_hand:
            ui.display_result(scores, player_hand.name,
                              robo_hand.name, HandResult.DRAW)
        elif robo_hand in player_hand.beats_hands:
            scores.player += 1
            ui.display_result(scores, player_hand.name,
                              robo_hand.name, HandResult.WIN)
        else:
            scores.robo += 1
            ui.display_result(scores, player_hand.name,
                              robo_hand.name, HandResult.LOSE)


if __name__ == '__main__':
    main()
