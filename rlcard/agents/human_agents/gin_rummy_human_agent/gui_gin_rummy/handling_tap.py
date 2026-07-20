
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game_canvas import GameCanvas

from . import configurations
from . import starting_new_game

from .canvas_item import CanvasItem
from .handling_tap_stock_pile import handle_tap_stock_pile
from .handling_tap_discard_pile import handle_tap_discard_pile
from .handling_tap_held_pile import handle_tap_held_pile
from .handling_tap_player_pane import handle_tap_player_pane

from rlcard.games.gin_rummy.utils.gin_rummy_error import GinRummyProgramError


def on_game_canvas_tap(event):
    pass


def _handle_tap(hit_item: CanvasItem, event, game_canvas: 'GameCanvas'):
    pass
