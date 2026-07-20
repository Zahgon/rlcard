
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game_canvas import GameCanvas
    from rlcard.envs.gin_rummy import GinRummyEnv
from ..gin_rummy_human_agent import HumanAgent

from typing import List

from rlcard.games.gin_rummy.utils.action_event import ActionEvent
from rlcard.games.gin_rummy.utils.move import GinRummyMove
from rlcard.games.gin_rummy.utils.move import PlayerMove
from rlcard.games.gin_rummy.utils.move import DealHandMove
from rlcard.games.gin_rummy.utils.move import DrawCardMove, PickupDiscardMove, DeclareDeadHandMove
from rlcard.games.gin_rummy.utils.move import DiscardMove, KnockMove, GinMove
from rlcard.games.gin_rummy.utils.move import ScoreNorthMove, ScoreSouthMove
from rlcard.games.gin_rummy.utils.gin_rummy_error import GinRummyProgramError

from . import configurations
from . import handling_tap_discard_pile
from . import handling_tap_held_pile
from . import starting_new_game
from . import status_messaging
from . import utils

from .player_type import PlayerType

import rlcard.games.gin_rummy.utils.utils as gin_rummy_utils


class GameCanvasUpdater(object):

    def __init__(self, game_canvas: 'GameCanvas'):
        self.game_canvas = game_canvas
        self.env_thread = None
        self.pending_human_action_ids = []  # type: List[int]
        self.busy_body_id = None  # type: int or None
        self.is_stopped = False

    @property
    def mark(self) -> int:  # convenience property to briefly get mark
        pass

    @property
    def moves(self) -> List[GinRummyMove]:  # convenience property to briefly get moves
        pass

    @property
    def env(self) -> 'GinRummyEnv':
        pass

    @property
    def human_agent(self) -> 'HumanAgent' or None:
        pass

    def apply_canvas_updates(self):
        if not self.env_thread.is_stopped:
            self._advance_mark()
            delay_ms = 1
            self.game_canvas.after(delay_ms, func=self.apply_canvas_updates)
        else:
            self.is_stopped = True

    def did_perform_actions(self, actions: List[int]):
        pass


    def _advance_mark(self):
        if self.env.game.round is None:
            return
        if self.game_canvas.query.is_game_over() and self.mark >= len(self.moves):
            return
        if self.busy_body_id is not None:
            return
        if self.human_agent and not self.human_agent.is_choosing_action_id:
            return
        if self.human_agent and self.human_agent.chosen_action_id is not None:
            return
        if self.env_thread.is_action_id_available():
            move = self.moves[self.mark]
            thinking_time_in_ms = 0  # type: int
            if isinstance(move, DealHandMove):
                if not self.mark == 0:
                    raise GinRummyProgramError("mark={} must be 0.".format(self.mark))
                self.busy_body_id = move.player_dealing.player_id
            elif isinstance(move, ScoreNorthMove) or isinstance(move, ScoreSouthMove):
                self.busy_body_id = move.player.player_id
            elif isinstance(move, PlayerMove):
                self.busy_body_id = move.player.player_id
                thinking_time_in_ms = 1000  # type: int  # simulate the computer thinking
            else:
                raise GinRummyProgramError("GameCanvasUpdater advance_mark: unknown move={move}")
            if self.mark > 0:
                if self.game_canvas.player_types[self.busy_body_id] == PlayerType.human_player:
                    raise GinRummyProgramError("busy_body_id={} must not be human player.".format(self.busy_body_id))
            if not self.busy_body_id == self.game_canvas.getter.get_current_player_id():
                raise GinRummyProgramError("busy_body_id={} must equal current_player_id={}".format(self.busy_body_id, self.game_canvas.getter.get_current_player_id()))
            self._show_prolog_messages_on_computer_turn()
            self.game_canvas.after(thinking_time_in_ms, self._advance_mark_for_computer_player)
            return
        if self.pending_human_action_ids:
            action_id = self.pending_human_action_ids.pop(0)  # pending_human_action_ids is queue
            if utils.is_debug():
                action_event = ActionEvent.decode_action(action_id=action_id)
                print("S {}".format(action_event))  # FIXME: South may not always be actor
            self.human_agent.chosen_action_id = action_id
            return
        if not self.mark >= len(self.moves):  # FIXME: should be no pending computer moves
            raise GinRummyProgramError("Should be no pending computer moves.")
        waiting_player_id = self.env_thread.get_waiting_player_id()
        if waiting_player_id is None:
            return
        if self.human_agent.chosen_action_id is not None:
            raise GinRummyProgramError("self.human_agent.chosen_action_id must not be None.")
        if self.busy_body_id is not None:
            raise GinRummyProgramError("busy_body_id={} must be None.".format(self.busy_body_id))
        if not waiting_player_id == self.game_canvas.getter.get_current_player_id():
            raise GinRummyProgramError("waiting_player_id={} must be current_player_id.".format(waiting_player_id))
        self.busy_body_id = waiting_player_id
        if not self.game_canvas.player_types[self.busy_body_id] == PlayerType.human_player:
            raise GinRummyProgramError("busy_body_id={} must be human player.".format(self.busy_body_id))
        raw_legal_actions = self.human_agent.state['raw_legal_actions']
        if self.game_canvas.query.is_scoring(legal_actions=raw_legal_actions):
            if not len(raw_legal_actions) == 1:
                raise GinRummyProgramError("len(legal_actions)={} must be 1.".format(len(raw_legal_actions)))
            action_id = raw_legal_actions[0]
            self._perform_score_action_id(action_id=action_id)
            return
        self._show_prolog_messages_on_human_turn()


    def _perform_deal_hand_move(self, move: DealHandMove):
        pass

    def _perform_score_action_id(self, action_id: int):
        if utils.is_debug():
            if self.busy_body_id == 0:
                if not action_id == configurations.SCORE_PLAYER_0_ACTION_ID:
                    raise GinRummyProgramError("action_id={} must be SCORE_PLAYER_0_ACTION_ID".format(action_id))
            else:
                if not action_id == configurations.SCORE_PLAYER_1_ACTION_ID:
                    raise GinRummyProgramError("action_id={} must be SCORE_PLAYER_1_ACTION_ID".format(action_id))
        self.game_canvas.after_idle(self.did_perform_actions, [action_id])


    def _show_prolog_messages_on_human_turn(self):
        legal_actions = self.human_agent.state['legal_actions']
        status_messaging.show_prolog_message(player_id=self.busy_body_id,
                                             legal_actions=legal_actions,
                                             game_canvas=self.game_canvas)


    def _show_prolog_messages_on_computer_turn(self):
        legal_actions = self.game_canvas.getter.get_legal_actions(player_id=self.busy_body_id)
        status_messaging.show_prolog_message(player_id=self.busy_body_id,
                                             legal_actions=legal_actions,
                                             game_canvas=self.game_canvas)

    def _advance_mark_for_computer_player(self):
        pass

    def _perform_draw_card_move(self, move: DrawCardMove):
        pass

    def _perform_pick_up_discard_move(self, move: PickupDiscardMove):
        pass

    def _do_perform_declare_dead_hand_move(self, move: DeclareDeadHandMove):
        pass

    def _perform_discard_move(self, move: DiscardMove):
        pass

    def _perform_knock_move(self, move: KnockMove):
        pass

    def _perform_gin_move(self, move: GinMove):
        pass
