
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game_canvas import GameCanvas

from .canvas_item import CanvasItem

from . import configurations
from . import info_messaging
from . import utils


def handle_tap_stock_pile(hit_item: CanvasItem, game_canvas: 'GameCanvas'):  # hit_item is source
    pass
