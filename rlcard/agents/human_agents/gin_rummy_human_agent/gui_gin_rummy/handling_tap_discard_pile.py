
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game_canvas import GameCanvas

from .canvas_item import CanvasItem

from . import configurations
from . import info_messaging
from . import starting_new_game
from . import utils

from rlcard.games.gin_rummy.utils.gin_rummy_error import GinRummyProgramError


def handle_tap_discard_pile(hit_item: CanvasItem, game_canvas: 'GameCanvas'):
    pass



def _handle_can_draw_from_discard_pile(hit_item: CanvasItem, game_canvas: 'GameCanvas'):  # hit_item is source
    pass


def _handle_can_discard_card(hit_item: CanvasItem, game_canvas: 'GameCanvas'):  # hit_item is target
    pass
