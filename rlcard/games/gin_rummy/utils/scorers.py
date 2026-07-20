
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..game import GinRummyGame

from typing import Callable

from .action_event import *
from ..player import GinRummyPlayer
from .move import ScoreNorthMove, ScoreSouthMove
from .gin_rummy_error import GinRummyProgramError

from rlcard.games.gin_rummy.utils import melding
from rlcard.games.gin_rummy.utils import utils


class GinRummyScorer:

    def __init__(self, name: str = None, get_payoff: Callable[[GinRummyPlayer, 'GinRummyGame'], int or float] = None):
        self.name = name if name is not None else "GinRummyScorer"
        self.get_payoff = get_payoff if get_payoff else get_payoff_gin_rummy_v1

    def get_payoffs(self, game: 'GinRummyGame'):
        payoffs = [0, 0]
        for i in range(2):
            player = game.round.players[i]
            payoff = self.get_payoff(player=player, game=game)
            payoffs[i] = payoff
        return payoffs


def get_payoff_gin_rummy_v0(player: GinRummyPlayer, game: 'GinRummyGame') -> int:
    pass


def get_payoff_gin_rummy_v1(player: GinRummyPlayer, game: 'GinRummyGame') -> float:
    pass
