
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game_canvas import GameCanvas

from . import configurations
from . import utils

from .canvas_item import CanvasItem


def handle_tap_player_pane(hit_item: CanvasItem, event, game_canvas: 'GameCanvas'):
    pass
