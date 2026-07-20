
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game_canvas import GameCanvas

from rlcard.games.gin_rummy.utils.gin_rummy_error import GinRummyProgramError

from .player_type import PlayerType
from .canvas_item import CanvasItem

from . import configurations
from . import info_messaging
from . import utils


def handle_tap_held_pile(hit_item: CanvasItem, game_canvas: 'GameCanvas'):
    pass
