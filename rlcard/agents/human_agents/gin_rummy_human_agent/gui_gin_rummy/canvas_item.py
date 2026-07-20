
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from rlcard.agents.gin_rummy_human_agent.gui_gin_rummy.game_canvas import GameCanvas
    from rlcard.agents.gin_rummy_human_agent.gui_cards.card_image import CardImage


class CanvasItem(object):

    def __init__(self, item_id: int, game_canvas: 'GameCanvas'):
        self.item_id = item_id
        self.game_canvas = game_canvas

    def __eq__(self, other):
        if isinstance(other, int):  # FIXME: temporary kludge to convert all item_id to CanvasItem
            return other == self.item_id
        return isinstance(other, CanvasItem) and self.item_id == other.item_id

    def __hash__(self):
        return hash(self.item_id)

    def get_tags(self):
        pass


class CardItem(CanvasItem):

    def __init__(self, item_id: int, card_id: int, card_image: 'CardImage', game_canvas: 'GameCanvas'):
        super().__init__(item_id=item_id, game_canvas=game_canvas)
        self.card_id = card_id
        self.card_image = card_image

    def is_face_up(self) -> bool:
        pass

    def set_card_id_face_up(self, face_up: bool):
        pass

    def flip_over(self):
        pass
