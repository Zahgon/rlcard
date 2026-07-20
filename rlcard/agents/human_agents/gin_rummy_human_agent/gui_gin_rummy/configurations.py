
import os

from configparser import ConfigParser


GOING_OUT_DEADWOOD_COUNT = 10


MAX_DRAWN_CARD_COUNT = 52

DISCARD_PILE_TAG = "discard_pile"
STOCK_PILE_TAG = "stock_pile"
NORTH_HELD_PILE_TAG = "north_held_pile"
SOUTH_HELD_PILE_TAG = "south_held_pile"
PLAYER_HELD_PILE_TAGS = [NORTH_HELD_PILE_TAG, SOUTH_HELD_PILE_TAG]

DRAWN_TAG = "drawn"
JOGGED_TAG = "jogged"
SELECTED_TAG = "selected"

SCORE_PLAYER_0_ACTION_ID = 0
SCORE_PLAYER_1_ACTION_ID = 1
DRAW_CARD_ACTION_ID = 2
PICK_UP_DISCARD_ACTION_ID = 3
DECLARE_DEAD_HAND_ACTION_ID = 4
GIN_ACTION_ID = 5
DISCARD_ACTION_ID = 6
KNOCK_ACTION_ID = DISCARD_ACTION_ID + 52


IS_KEEP_TURN_WHEN_DISCARDING_CARD_PICKED_UP = False  # TODO: make True the default value


config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'game_options.ini')  # Note this

config = ConfigParser()
found = config.read(config_path)

settings_section = "settings"
show_status_messages_option = "show_status_messages"
warning_as_option = 'warning_as'
game_background_color_option = 'game_background_color'
window_size_factor_option = 'window_size_factor'
is_show_tips_option = "is_show_tips"
is_debug_option = "is_debug"

SHOW_STATUS_MESSAGES = config.get(section=settings_section, option=show_status_messages_option, fallback="verbose")
WARNINGS_AS = config.get(section=settings_section, option=warning_as_option, fallback="alert_messages")
GAME_BACKGROUND_COLOR = config.get(section=settings_section, option=game_background_color_option, fallback="#007F00")
WINDOW_SIZE_FACTOR = config.getint(section=settings_section, option=window_size_factor_option, fallback=75)
IS_SHOW_TIPS = config.getboolean(section=settings_section, option=is_show_tips_option, fallback=True)
IS_DEBUG = False
