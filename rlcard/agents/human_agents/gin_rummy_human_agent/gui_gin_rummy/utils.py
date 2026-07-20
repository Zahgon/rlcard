
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game_canvas import GameCanvas

from typing import List

import tkinter as tk

import rlcard.games.gin_rummy.utils.utils as gin_rummy_utils

from rlcard.games.gin_rummy.utils.gin_rummy_error import GinRummyProgramError

from .canvas_item import CardItem, CanvasItem
from .player_type import PlayerType

from .configurations import SCORE_PLAYER_0_ACTION_ID, SCORE_PLAYER_1_ACTION_ID
from .configurations import DRAW_CARD_ACTION_ID, PICK_UP_DISCARD_ACTION_ID
from .configurations import DECLARE_DEAD_HAND_ACTION_ID
from .configurations import DISCARD_ACTION_ID, KNOCK_ACTION_ID

from . import configurations


def is_debug() -> bool:
    result = __debug__ and configurations.IS_DEBUG
    return result


def gin_rummy_sort_order_id(card_id: int) -> int:
    pass


def move_to(item_id: int, x: int, y: int, parent: tk.Canvas):
    pass


def translated_by(dx: float, dy: float, location):
    pass


def player_name(player_id: int) -> str:
    return "North" if player_id == 0 else "South" if player_id == 1 else "X"


def player_short_name(player_id: int) -> str:
    pass


def get_action_type(action: int) -> int:
    pass


def get_action_card_id(action: int) -> int or None:
    pass



def set_card_id_face_up(card_id: int, face_up: bool, game_canvas: 'GameCanvas'):
    pass


def flip_card_id(card_id: int, game_canvas: 'GameCanvas'):
    pass


def jog_card_id(card_id: int, dx: float, dy: float, game_canvas: 'GameCanvas'):
    pass


def drop_item_ids(item_ids: List[int], on_item_id: int, player_id: int, game_canvas: 'GameCanvas'):
    pass


def fan_held_pile(player_id: int, game_canvas: 'GameCanvas'):
    pass


def held_pile_insert(card_item_id: int, above_hit_item_id: int or None, player_id: int, game_canvas: 'GameCanvas'):
    pass


def set_card_item_id_face_up(card_item_id: int, face_up: bool, game_canvas: 'GameCanvas'):
    pass


def toggle_discard_pile_item_selected(game_canvas: 'GameCanvas'):
    pass


def toggle_held_pile_item_selected(item: CanvasItem, game_canvas: 'GameCanvas'):
    pass


def toggle_stock_pile_item_selected(game_canvas: 'GameCanvas'):
    pass
