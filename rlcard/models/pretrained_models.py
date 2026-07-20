import os

import rlcard
from rlcard.agents import CFRAgent
from rlcard.models.model import Model

ROOT_PATH = os.path.join(rlcard.__path__[0], 'models/pretrained')

class LeducHoldemCFRModel(Model):
    def __init__(self):
        ''' Load pretrained model
        '''
        env = rlcard.make('leduc-holdem')
        self.agent = CFRAgent(env, model_path=os.path.join(ROOT_PATH, 'leduc_holdem_cfr'))
        self.agent.load()
    @property
    def agents(self):
        pass

