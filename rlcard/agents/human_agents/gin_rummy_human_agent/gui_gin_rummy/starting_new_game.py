
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game_canvas import GameCanvas

import tkinter as tk

from ..gin_rummy_human_agent import HumanAgent

from . import configurations
from . import info_messaging
from . import utils

from .env_thread import EnvThread

import rlcard.games.gin_rummy.utils.utils as gin_rummy_utils
from rlcard.games.gin_rummy.utils.gin_rummy_error import GinRummyProgramError


def start_new_game(game_canvas: 'GameCanvas'):
    pass


def _reset_game_canvas(game_canvas: 'GameCanvas'):
    pass


def show_new_game(game_canvas: 'GameCanvas'):
    pass
