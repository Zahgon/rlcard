
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game_canvas import GameCanvas

from .canvas_item import CanvasItem
from .player_type import PlayerType

from . import handling_tap
from . import utils

from rlcard.games.gin_rummy.utils.gin_rummy_error import GinRummyProgramError


def on_tap_to_arrange_held_pile(event):
    pass


def handle_tap_to_arrange_held_pile(hit_item: CanvasItem, game_canvas: 'GameCanvas'):
    pass
