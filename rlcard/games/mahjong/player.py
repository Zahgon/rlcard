
class MahjongPlayer:

    def __init__(self, player_id, np_random):
        ''' Initilize a player.

        Args:
            player_id (int): The id of the player
        '''
        self.np_random = np_random
        self.player_id = player_id
        self.hand = []
        self.pile = []

    def get_player_id(self):
        ''' Return the id of the player
        '''

        return self.player_id

    def print_hand(self):
        pass

    def print_pile(self):
        pass

    def play_card(self, dealer, card):
        ''' Play one card
        Args:
            dealer (object): Dealer
            Card (object): The card to be play.
        '''
        card = self.hand.pop(self.hand.index(card))
        dealer.table.append(card)

    def chow(self, dealer, cards):
        ''' Perform Chow
        Args:
            dealer (object): Dealer
            Cards (object): The cards to be Chow.
        '''
        last_card = dealer.table.pop(-1)
        for card in cards:
            if card in self.hand and card != last_card:
                self.hand.pop(self.hand.index(card))
        self.pile.append(cards)

    def gong(self, dealer, cards):
        ''' Perform Gong
        Args:
            dealer (object): Dealer
            Cards (object): The cards to be Gong.
        '''
        for card in cards:
            if card in self.hand:
                self.hand.pop(self.hand.index(card))
        self.pile.append(cards)

    def pong(self, dealer, cards):
        ''' Perform Pong
        Args:
            dealer (object): Dealer
            Cards (object): The cards to be Pong.
        '''
        for card in cards:
            if card in self.hand:
                self.hand.pop(self.hand.index(card))
        self.pile.append(cards)
