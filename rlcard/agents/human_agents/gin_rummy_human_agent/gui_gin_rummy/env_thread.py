
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game_canvas import GameCanvas

from typing import List

import threading
import time

from rlcard.envs.gin_rummy import GinRummyEnv

from rlcard.games.gin_rummy.utils.move import GinRummyMove, ScoreSouthMove

from ..gin_rummy_human_agent import HumanAgent

from . import utils
from . import status_messaging


class EnvThread(threading.Thread):

    def __init__(self, gin_rummy_env: GinRummyEnv, game_canvas: 'GameCanvas'):
        super().__init__()
        self.gin_rummy_env = gin_rummy_env
        self.game_canvas = game_canvas
        self.setDaemon(daemonic=True)
        self.name = "WorkerGinRummyEnvironment"
        self.mark = 0
        self.is_stopped = False

    @property
    def moves(self) -> List[GinRummyMove]:
        pass


    def is_action_id_available(self) -> bool:
        move_sheet = self.gin_rummy_env.game.round.move_sheet
        move_count = len(move_sheet)
        return self.mark < move_count


    def get_waiting_player_id(self) -> int or None:  # FIXME: rework this
        waiting_player_id = None  # type: int or None
        is_action_id_available = self.is_action_id_available()
        if not is_action_id_available:
            for player_id, agent in enumerate(self.gin_rummy_env.agents):
                if isinstance(agent, HumanAgent) and agent.is_choosing_action_id:
                    waiting_player_id = player_id
        return waiting_player_id


    def stop(self):
        pass

    def run(self) -> None:
        self.game_canvas.game_canvas_updater.apply_canvas_updates()
        _, payoffs = self.gin_rummy_env.run(is_training=False)

        is_game_complete = False
        move_sheet = self.gin_rummy_env.game.round.move_sheet
        if move_sheet and isinstance(move_sheet[-1], ScoreSouthMove):
            is_game_complete = True

        if is_game_complete:
            while not self.is_stopped and self.gin_rummy_env.game.round.is_over and self.mark < len(self.moves):
                time.sleep(0.1)  # FIXME: provide a timeout ???

        if not self.is_stopped and self.gin_rummy_env.game.round.is_over and is_game_complete:
            status_messaging.show_game_over_message(game=self.gin_rummy_env.game, game_canvas=self.game_canvas)
            for player_id in range(2):  # update score_pad for both players
                payoff = payoffs[player_id]
                if isinstance(payoffs, float):
                    text = "{:.2f}".format(payoff)
                else:
                    text = "{}".format(payoff)
                self.game_canvas.score_pad_cells[player_id].configure(text=text)

        if utils.is_debug():
            print("EnvThread finished")
