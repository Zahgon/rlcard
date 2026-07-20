

class Tray(object):

    def __init__(self, board_id: int):
        if board_id <= 0:
            raise Exception(f'Tray: invalid board_id={board_id}')
        self.board_id = board_id

    @property
    def dealer_id(self):
        pass

    @property
    def vul(self):
        pass

    def __str__(self):
        return f'{self.board_id}: dealer_id={self.dealer_id} vul={self.vul}'
