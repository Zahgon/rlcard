from copy import deepcopy, copy
import numpy as np

from rlcard.games.limitholdem import Dealer
from rlcard.games.limitholdem import Player, PlayerStatus
from rlcard.games.limitholdem import Judger
from rlcard.games.limitholdem import Round


class LimitHoldemGame:
    def __init__(self, allow_step_back=False, num_players=2):
        """Initialize the class limit holdem game"""
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()


        self.small_blind = 1
        self.big_blind = 2 * self.small_blind

        self.raise_amount = self.big_blind
        self.allowed_raise_num = 4

        self.num_players = num_players

        self.history_raise_nums = [0 for _ in range(4)]

        self.dealer = None
        self.players = None
        self.judger = None
        self.public_cards = None
        self.game_pointer = None
        self.round = None
        self.round_counter = None
        self.history = None
        self.history_raises_nums = None

    def configure(self, game_config):
        """Specify some game specific parameters, such as number of players"""
        self.num_players = game_config['game_num_players']

    def init_game(self):
        """
        Initialize the game of limit texas holdem

        This version supports two-player limit texas holdem

        Returns:
            (tuple): Tuple containing:

                (dict): The first state of the game
                (int): Current player's id
        """
        self.dealer = Dealer(self.np_random)

        self.players = [Player(i, self.np_random) for i in range(self.num_players)]

        self.judger = Judger(self.np_random)

        for i in range(2 * self.num_players):
            self.players[i % self.num_players].hand.append(self.dealer.deal_card())

        self.public_cards = []

        s = self.np_random.randint(0, self.num_players)
        b = (s + 1) % self.num_players
        self.players[b].in_chips = self.big_blind
        self.players[s].in_chips = self.small_blind

        self.game_pointer = (b + 1) % self.num_players

        self.round = Round(raise_amount=self.raise_amount,
                           allowed_raise_num=self.allowed_raise_num,
                           num_players=self.num_players,
                           np_random=self.np_random)

        self.round.start_new_round(game_pointer=self.game_pointer, raised=[p.in_chips for p in self.players])

        self.round_counter = 0

        self.history = []

        state = self.get_state(self.game_pointer)

        self.history_raise_nums = [0 for _ in range(4)]

        return state, self.game_pointer

    def step(self, action):
        """
        Get the next state

        Args:
            action (str): a specific action. (call, raise, fold, or check)

        Returns:
            (tuple): Tuple containing:

                (dict): next player's state
                (int): next player id
        """
        if self.allow_step_back:
            r = deepcopy(self.round)
            b = self.game_pointer
            r_c = self.round_counter
            d = deepcopy(self.dealer)
            p = deepcopy(self.public_cards)
            ps = deepcopy(self.players)
            rn = copy(self.history_raise_nums)
            self.history.append((r, b, r_c, d, p, ps, rn))

        self.game_pointer = self.round.proceed_round(self.players, action)

        self.history_raise_nums[self.round_counter] = self.round.have_raised

        if self.round.is_over():
            if self.round_counter == 0:
                self.public_cards.append(self.dealer.deal_card())
                self.public_cards.append(self.dealer.deal_card())
                self.public_cards.append(self.dealer.deal_card())

            elif self.round_counter <= 2:
                self.public_cards.append(self.dealer.deal_card())

            if self.round_counter == 1:
                self.round.raise_amount = 2 * self.raise_amount

            self.round_counter += 1
            self.round.start_new_round(self.game_pointer)

        state = self.get_state(self.game_pointer)

        return state, self.game_pointer

    def step_back(self):
        pass

    def get_num_players(self):
        """
        Return the number of players in limit texas holdem

        Returns:
            (int): The number of players in the game
        """
        return self.num_players

    @staticmethod
    def get_num_actions():
        pass

    def get_player_id(self):
        """
        Return the current player's id

        Returns:
            (int): current player's id
        """
        return self.game_pointer

    def get_state(self, player):
        """
        Return player's state

        Args:
            player (int): player id

        Returns:
            (dict): The state of the player
        """
        chips = [self.players[i].in_chips for i in range(self.num_players)]
        legal_actions = self.get_legal_actions()
        state = self.players[player].get_state(self.public_cards, chips, legal_actions)
        state['raise_nums'] = self.history_raise_nums

        return state

    def is_over(self):
        """
        Check if the game is over

        Returns:
            (boolean): True if the game is over
        """
        alive_players = [1 if p.status in (PlayerStatus.ALIVE, PlayerStatus.ALLIN) else 0 for p in self.players]
        if sum(alive_players) == 1:
            return True

        if self.round_counter >= 4:
            return True
        return False

    def get_payoffs(self):
        """
        Return the payoffs of the game

        Returns:
            (list): Each entry corresponds to the payoff of one player
        """
        hands = [p.hand + self.public_cards if p.status == PlayerStatus.ALIVE else None for p in self.players]
        chips_payoffs = self.judger.judge_game(self.players, hands)
        payoffs = np.array(chips_payoffs) / self.big_blind
        return payoffs

    def get_legal_actions(self):
        """
        Return the legal actions for current player

        Returns:
            (list): A list of legal actions
        """
        return self.round.get_legal_actions()
