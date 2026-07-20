
from typing import Dict, Any

from enum import Enum


class DealerForRound(Enum):
    North = 0
    South = 1
    Random = 2


class Setting(Enum):
    dealer_for_round = "dealer_for_round"
    stockpile_dead_card_count = "stockpile_dead_card_count"
    going_out_deadwood_count = "going_out_deadwood_count"
    max_drawn_card_count = "max_drawn_card_count"
    max_move_count = "max_move_count"
    is_allowed_knock = "is_allowed_knock"
    is_allowed_gin = "is_allowed_gin"
    is_allowed_pick_up_discard = "is_allowed_pick_up_discard"
    is_allowed_to_discard_picked_up_card = "is_allowed_to_discard_picked_up_card"
    is_always_knock = "is_always_knock"
    is_south_never_knocks = "is_south_never_knocks"

    @staticmethod
    def default_setting() -> Dict['Setting', Any]:
        pass

    @staticmethod
    def simple_gin_rummy_setting():  # speeding up training 200213
        pass


dealer_for_round = Setting.dealer_for_round
stockpile_dead_card_count = Setting.stockpile_dead_card_count
going_out_deadwood_count = Setting.going_out_deadwood_count
max_drawn_card_count = Setting.max_drawn_card_count
max_move_count = Setting.max_move_count
is_allowed_knock = Setting.is_allowed_knock
is_allowed_gin = Setting.is_allowed_gin
is_allowed_pick_up_discard = Setting.is_allowed_pick_up_discard
is_allowed_to_discard_picked_up_card = Setting.is_allowed_to_discard_picked_up_card
is_always_knock = Setting.is_always_knock
is_south_never_knocks = Setting.is_south_never_knocks


class Settings(object):

    def __init__(self):
        self.scorer_name = "GinRummyScorer"
        default_setting = Setting.default_setting()
        self.dealer_for_round = default_setting[Setting.dealer_for_round]
        self.stockpile_dead_card_count = default_setting[Setting.stockpile_dead_card_count]
        self.going_out_deadwood_count = default_setting[Setting.going_out_deadwood_count]
        self.max_drawn_card_count = default_setting[Setting.max_drawn_card_count]
        self.max_move_count = default_setting[Setting.max_move_count]
        self.is_allowed_knock = default_setting[Setting.is_allowed_knock]
        self.is_allowed_gin = default_setting[Setting.is_allowed_gin]
        self.is_allowed_pick_up_discard = default_setting[Setting.is_allowed_pick_up_discard]
        self.is_allowed_to_discard_picked_up_card = default_setting[Setting.is_allowed_to_discard_picked_up_card]
        self.is_always_knock = default_setting[Setting.is_always_knock]
        self.is_south_never_knocks = default_setting[Setting.is_south_never_knocks]

    def change_settings(self, config: Dict[Setting, Any]):
        pass

    def print_settings(self):
        pass

    @staticmethod
    def get_config_with_invalid_settings_set_to_default_value(config: Dict[Setting, Any]) -> Dict[Setting, Any]:
        pass

