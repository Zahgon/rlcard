
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game_canvas import GameCanvas

from typing import List, Tuple

from rlcard.games.base import Card

import rlcard.games.gin_rummy.judge as judge
import rlcard.games.gin_rummy.utils.utils as gin_rummy_utils

from rlcard.games.gin_rummy.utils.melding import get_best_meld_clusters

from . import configurations
from . import status_messaging
from . import utils

from .configurations import DRAW_CARD_ACTION_ID, PICK_UP_DISCARD_ACTION_ID
from .configurations import DISCARD_ACTION_ID, KNOCK_ACTION_ID, GIN_ACTION_ID


class GameCanvasPostDoingAction(object):

    def __init__(self, game_canvas: 'GameCanvas'):
        self.game_canvas = game_canvas

    def post_do_get_card_action(self,
                                player_id: int,
                                drawn_card_item_id: int,
                                hit_item_id: int,
                                drawn_card_item_tag: int):
        pass

    def post_do_discard_action(self, player_id: int, selected_held_pile_item_id: int):
        pass

    def post_do_discard_card_drawn_from_stock_pile_action(self, top_stock_pile_item_id: int):
        pass

    def post_do_knock_action(self, selected_held_pile_item_id: int):
        pass

    def post_do_gin_action(self):
        pass

    def post_do_declare_dead_hand_action(self, player_id: int):
        pass


    def _show_meld_piles(self):
        pass

    def _get_best_meld_cluster(self, player_id: int) -> List[List[Card]]:
        pass

    def put_down_meld_cluster(self, meld_cluster, player_id: int):
        pass

    def put_down_meld_pile(self, meld_pile: List[Card], anchor: Tuple[int, int], player_id: int):
        pass


    def _move_loop(self, item_id, to_location, index=0, dx=0, dy=0, completion=None):
        pass
