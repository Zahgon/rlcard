
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game_app import GameApp

import tkinter as tk

from typing import List, Dict

from ..gin_rummy_human_agent import HumanAgent
from ..gui_cards.card_image import CardImage, CardBackImage

from . import handling_tap_to_arrange_held_pile
from . import configurations
from . import handling_tap
from . import info_messaging

from .canvas_item import CardItem, CanvasItem
from .configurations import DECLARE_DEAD_HAND_ACTION_ID
from .game_canvas_debug import GameCanvasDebug
from .game_canvas_getter import GameCanvasGetter
from .game_canvas_post_doing_action import GameCanvasPostDoingAction
from .game_canvas_query import GameCanvasQuery
from .game_canvas_updater import GameCanvasUpdater
from .player_type import PlayerType

import rlcard.games.gin_rummy.utils.utils as gin_rummy_utils

from rlcard.games.gin_rummy.utils.action_event import KnockAction, GinAction
from rlcard.games.gin_rummy.utils.gin_rummy_error import GinRummyProgramError


class GameCanvas(tk.Canvas):

    def __init__(self, parent: tk.Frame, window_width, window_height, scale_factor, game_app: 'GameApp'):
        bottom_info_label_height = int(32 * scale_factor)
        canvas_width = window_width
        canvas_height = window_height - bottom_info_label_height
        super().__init__(master=parent, width=window_width,
                         height=window_height,
                         background=configurations.GAME_BACKGROUND_COLOR,
                         highlightthickness=0,
                         name="game_canvas")

        canvas_items = []  # type: [CanvasItem]

        card_back_image = CardBackImage(scale_factor=scale_factor)
        card_images = {}  # type: Dict[(str, str)]  # card_images by rank by suit
        for card_id in range(52):
            card = gin_rummy_utils.card_from_card_id(card_id)
            card_image = CardImage(rank=card.rank, suit=card.suit, scale_factor=scale_factor)
            card_images[card.rank, card.suit] = card_image

        card_item_ids = []  # type: List[int]
        for card_id in range(52):
            card = gin_rummy_utils.card_from_card_id(card_id)
            card_image = card_images[card.rank, card.suit]
            card_item_id = self.create_image((0, -9999), image=card_image, anchor="nw")
            self.itemconfigure(card_item_id, state=tk.HIDDEN)
            card_item_ids.append(card_item_id)

        card_items = []  # type: List[CardItem]
        for card_id in range(52):
            card = gin_rummy_utils.card_from_card_id(card_id)
            card_item_id = card_item_ids[card_id]
            card_image = card_images[card.rank, card.suit]
            card_item = CardItem(item_id=card_item_id, card_id=card_id, card_image=card_image, game_canvas=self)
            card_items.append(card_item)
            canvas_items.append(card_item)

        card_width = card_images["A", "S"].width()
        card_height = card_images["A", "S"].height()

        stock_pile_indent = card_width * 2
        stock_pile_tab = max(int(1 * scale_factor), 1)  # Note making int
        stock_pile_anchor = (stock_pile_indent, canvas_height / 2 - card_height / 2)
        discard_pile_anchor = (stock_pile_indent + card_width * 1.8, canvas_height / 2 - card_height / 2)

        held_pile_tab = max(int(card_width * 0.47), 1)  # Note making int
        max_held_pile_width = 10 * held_pile_tab + card_width
        north_held_pile_anchor = (canvas_width / 2 - max_held_pile_width / 2,
                                  stock_pile_anchor[1] - card_height * 1.5)
        south_held_pile_anchor = (canvas_width / 2 - max_held_pile_width / 2,
                                  stock_pile_anchor[1] + card_height * 1.5)

        discard_pile_box_left = discard_pile_anchor[0]
        discard_pile_box_top = discard_pile_anchor[1]
        discard_pile_box_right = discard_pile_box_left + card_width
        discard_pile_box_bottom = discard_pile_box_top + card_height
        discard_pile_box_item_id = self.create_rectangle(discard_pile_box_left,
                                                         discard_pile_box_top,
                                                         discard_pile_box_right,
                                                         discard_pile_box_bottom,
                                                         fill="gray")
        discard_pile_box_item = CanvasItem(item_id=discard_pile_box_item_id, game_canvas=self)
        canvas_items.append(discard_pile_box_item)

        player_panes = []
        for player_id in range(2):
            left = 0
            right = canvas_width
            top = 0 if player_id == 0 else stock_pile_anchor[1] + card_height
            bottom = stock_pile_anchor[1] if player_id == 0 else canvas_height
            player_pane_id = self.create_rectangle(left, top, right, bottom, width=0)
            player_pane = CanvasItem(item_id=player_pane_id, game_canvas=self)
            canvas_items.append(player_pane)
            player_panes.append(player_pane)

        held_pile_ghost_card_items = []
        player_held_pile_anchors = [north_held_pile_anchor, south_held_pile_anchor]
        held_pile_tags = [configurations.NORTH_HELD_PILE_TAG, configurations.SOUTH_HELD_PILE_TAG]
        for player_id in range(2):
            x, y = player_held_pile_anchors[player_id]
            x -= held_pile_tab
            ghost_card_item_id = self.create_rectangle(x, y, x + card_width, y + card_height, width=0, fill='')
            self.itemconfig(ghost_card_item_id, tag=held_pile_tags[player_id])
            ghost_card_item = CanvasItem(item_id=ghost_card_item_id, game_canvas=self)
            canvas_items.append(ghost_card_item)
            held_pile_ghost_card_items.append(ghost_card_item)

        info_label = tk.Label(self, text="", padx=10 * scale_factor, anchor="w")
        info_label.config(font=(None, int(bottom_info_label_height * 0.6)))
        info_label.place(x=0, y=canvas_height, width=window_width, height=bottom_info_label_height)

        going_out_button = tk.Button(self, text="Knock", command=self.on_going_out)
        going_out_button.configure(font=(None, int(card_height * 0.15)))
        going_out_button_x = stock_pile_anchor[0] - card_width * 1.5
        going_out_button_y = stock_pile_anchor[1] + card_height / 2 - going_out_button.winfo_reqheight() / 2
        going_out_button.place(x=going_out_button_x, y=going_out_button_y)
        going_out_button_place = going_out_button.place_info()  # remember place
        going_out_button.place_forget()  # hide button

        going_out_button_height = going_out_button.winfo_reqheight()
        dead_hand_button = tk.Button(self, text="Dead hand", command=self.on_dead_hand)
        dead_hand_button.configure(font=(None, int(card_height * 0.15)))
        dead_hand_button.place(x=going_out_button_x, y=going_out_button_y + going_out_button_height * 1.5)
        dead_hand_button_place = dead_hand_button.place_info()  # remember place
        dead_hand_button.place_forget()  # hide button

        cell_width = int(120 * scale_factor)
        cell_height = int(50 * scale_factor)
        cell_border_thickness = int(3 * scale_factor)
        cell_dy = int(5 * scale_factor)
        score_pad_widget = tk.Canvas(self, bg='white', highlightthickness=0)
        score_pad_widget.configure(width=2 * cell_width, height=2 * cell_height)
        score_pad_cells = []
        for row in range(2):
            for col in range(2):
                text = ""
                if row == 0:
                    text = ["Me", "You"][col]
                score_pad_cell = tk.Label(score_pad_widget, text=text, padx=0, pady=0, height=0, bg=None)
                score_pad_cell.config(width=7)  # Note: need to be fixed width to blank out
                score_pad_cell.config(font=("Times", int(cell_height * 0.6)))
                indent = 4 * scale_factor
                score_pad_cell.place(x=indent + col * cell_width, y=0 if row == 0 else cell_height)
                if row == 1:
                    score_pad_cells.append(score_pad_cell)
        indent_x = 10 * scale_factor
        indent_y = 5 * scale_factor
        score_pad_widget.create_line(indent_x, cell_height - indent_y, 2 * cell_width - indent_x,
                                     cell_height - indent_y, fill='black', width=cell_border_thickness)
        score_pad_widget.create_line(cell_width, cell_dy, cell_width, 2 * cell_height - cell_dy,
                                     fill='black', width=cell_border_thickness)
        score_pad_widget.pack()
        score_pad_widget.place(x=discard_pile_anchor[0] + 3 * card_width,
                               y=stock_pile_anchor[1] + card_height / 2 - cell_height)

        info_message_label = tk.Label(self, anchor='nw', justify='left')
        info_message_label.configure(wraplength=185 * scale_factor)  # in pixels
        info_message_label.configure(width=0, height=0)  # dimensions in text units; wraplength determines width
        info_message_label.place(x=10 * scale_factor, y=stock_pile_anchor[1])

        self.bind("<Button-1>", handling_tap.on_game_canvas_tap)
        self.bind("<Shift-Button-1>", handling_tap_to_arrange_held_pile.on_tap_to_arrange_held_pile)
        self.bind("<Button-2>", handling_tap_to_arrange_held_pile.on_tap_to_arrange_held_pile)

        canvas_item_by_item_id = {}
        for canvas_item in canvas_items:
            canvas_item_by_item_id[canvas_item.item_id] = canvas_item

        self.scale_factor = scale_factor
        self.held_pile_tags = held_pile_tags
        self.dealer_id = 0  # type: int  # Note: has no effect; will be set later to correct value
        self.canvas_items = canvas_items
        self.card_back_image = card_back_image
        self.card_images = card_images
        self.card_item_ids = card_item_ids
        self.card_items = card_items
        self.card_width = card_width
        self.card_height = card_height
        self.stock_pile_anchor = stock_pile_anchor
        self.stock_pile_tab = stock_pile_tab
        self.discard_pile_anchor = discard_pile_anchor
        self.discard_pile_tab = stock_pile_tab
        self.discard_pile_box_item = discard_pile_box_item
        self.player_panes = player_panes
        self.player_held_pile_anchors = player_held_pile_anchors
        self.held_pile_tab = held_pile_tab
        self.held_pile_ghost_card_items = held_pile_ghost_card_items
        self.info_label = info_label
        self.going_out_button_place = going_out_button_place
        self.going_out_button = going_out_button
        self.dead_hand_button_place = dead_hand_button_place
        self.dead_hand_button = dead_hand_button
        self.score_pad_cells = score_pad_cells
        self.info_message_label = info_message_label
        self.game_app = game_app
        self.canvas_item_by_item_id = canvas_item_by_item_id
        self.debug = GameCanvasDebug(game_canvas=self)
        self.getter = GameCanvasGetter(game_canvas=self)
        self.post_doing_action = GameCanvasPostDoingAction(game_canvas=self)
        self.query = GameCanvasQuery(game_canvas=self)

        self.pack()

        info_message_background = configurations.GAME_BACKGROUND_COLOR
        self._configure_info_message_label_colors(background_color=info_message_background)
        self.game_canvas_updater = GameCanvasUpdater(game_canvas=self)

    @property
    def current_player_id(self) -> int or None:  # convenience property to briefly get current_player_id
        pass

    @property
    def player_types(self) -> List[PlayerType]:
        pass

    def is_treating_as_human(self, player_id) -> bool:
        pass

    def update_configurations(self):
        pass

    def update_configuration_game_background_color(self, background_color):
        pass


    def on_dead_hand(self):
        pass

    def on_going_out(self):
        pass


    def _configure_info_message_label_colors(self, background_color):
        pass
