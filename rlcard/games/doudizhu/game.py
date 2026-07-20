# -*- coding: utf-8 -*-
import functools
from heapq import merge
import numpy as np

from rlcard.games.doudizhu.utils import cards2str, doudizhu_sort_card, CARD_RANK_STR
from rlcard.games.doudizhu import Player
from rlcard.games.doudizhu import Round
from rlcard.games.doudizhu import Judger


class DoudizhuGame:
    def __init__(self, allow_step_back=False):
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()
        self.num_players = 3

    def init_game(self):
        ''' Initialize players and state.

        Returns:
            dict: first state in one game
            int: current player's id
        '''
        self.winner_id = None
        self.history = []

        self.players = [Player(num, self.np_random)
                        for num in range(self.num_players)]

        self.played_cards = [np.zeros((len(CARD_RANK_STR), ), dtype=np.int)
                                for _ in range(self.num_players)]
        self.round = Round(self.np_random, self.played_cards)
        self.round.initiate(self.players)

        self.judger = Judger(self.players, self.np_random)

        player_id = self.round.current_player
        self.state = self.get_state(player_id)

        return self.state, player_id

    def step(self, action):
        ''' Perform one draw of the game

        Args:
            action (str): specific action of doudizhu. Eg: '33344'

        Returns:
            dict: next player's state
            int: next player's id
        '''
        if self.allow_step_back:
            pass

        player = self.players[self.round.current_player]
        self.round.proceed_round(player, action)
        if (action != 'pass'):
            self.judger.calc_playable_cards(player)
        if self.judger.judge_game(self.players, self.round.current_player):
            self.winner_id = self.round.current_player
        next_id = (player.player_id+1) % len(self.players)
        self.round.current_player = next_id

        state = self.get_state(next_id)
        self.state = state

        return state, next_id

    def step_back(self):
        pass

    def get_state(self, player_id):
        ''' Return player's state

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        '''
        player = self.players[player_id]
        others_hands = self._get_others_current_hand(player)
        num_cards_left = [len(self.players[i].current_hand) for i in range(self.num_players)]
        if self.is_over():
            actions = []
        else:
            actions = list(player.available_actions(self.round.greater_player, self.judger))
        state = player.get_state(self.round.public, others_hands, num_cards_left, actions)

        return state

    @staticmethod
    def get_num_actions():
        pass

    def get_player_id(self):
        ''' Return current player's id

        Returns:
            int: current player's id
        '''
        return self.round.current_player

    def get_num_players(self):
        ''' Return the number of players in doudizhu

        Returns:
            int: the number of players in doudizhu
        '''
        return self.num_players

    def is_over(self):
        ''' Judge whether a game is over

        Returns:
            Bool: True(over) / False(not over)
        '''
        if self.winner_id is None:
            return False
        return True

    def _get_others_current_hand(self, player):
        player_up = self.players[(player.player_id+1) % len(self.players)]
        player_down = self.players[(player.player_id-1) % len(self.players)]
        others_hand = merge(player_up.current_hand, player_down.current_hand, key=functools.cmp_to_key(doudizhu_sort_card))
        return cards2str(others_hand)
