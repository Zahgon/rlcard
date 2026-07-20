
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game_canvas import GameCanvas

from . import configurations

from rlcard.games.gin_rummy.player import GinRummyPlayer

import rlcard.games.gin_rummy.utils.utils as gin_rummy_utils


class GameCanvasDebug(object):

    def __init__(self, game_canvas: 'GameCanvas'):
        self.game_canvas = game_canvas

    def get_card_name(self, card_item_id: int) -> str:
        pass

    def description(self):
        pass
