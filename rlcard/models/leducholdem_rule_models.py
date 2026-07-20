import rlcard
from rlcard.models.model import Model

class LeducHoldemRuleAgentV1(object):
    def __init__(self):
        self.use_raw = True

    @staticmethod
    def step(state):
        ''' Predict the action when given raw state. A simple rule-based AI.
        Args:
            state (dict): Raw state from the game

        Returns:
            action (str): Predicted action
        '''
        legal_actions = state['raw_legal_actions']
        if 'raise' in legal_actions:
            return 'raise'
        if 'call' in legal_actions:
            return 'call'
        if 'check' in legal_actions:
            return 'check'
        else:
            return 'fold'

    def eval_step(self, state):
        ''' Step for evaluation. The same to step
        '''
        return self.step(state), []

class LeducHoldemRuleAgentV2(object):
    def __init__(self):
        self.use_raw = True

    @staticmethod
    def step(state):
        ''' Predict the action when given raw state. A simple rule-based AI.
        Args:
            state (dict): Raw state from the game

        Returns:
            action (str): Predicted action
        '''
        legal_actions = state['raw_legal_actions']
        state = state['raw_obs']
        hand = state['hand']
        public_card = state['public_card']
        action = 'fold'
        if public_card:
            if public_card[1] == hand[1]:
                action = 'raise'
            else:
                action = 'fold'
        else:
            if hand[0] == 'K':
                action = 'raise'
            elif hand[0] == 'Q':
                action = 'check'
            else:
                action = 'fold'

        if action in legal_actions:
            return action
        else:
            if action == 'raise':
                return 'call'
            if action == 'check':
                return 'fold'
            if action == 'call':
                return 'raise'
            else:
                return action

class LeducHoldemRuleModelV1(Model):

    def __init__(self):
        ''' Load pretrained model
        '''
        env = rlcard.make('leduc-holdem')
        rule_agent = LeducHoldemRuleAgentV1()
        self.rule_agents = [rule_agent for _ in range(env.num_players)]

    @property
    def agents(self):
        pass

class LeducHoldemRuleModelV2(Model):

    def __init__(self):
        ''' Load pretrained model
        '''
        env = rlcard.make('leduc-holdem')
        rule_agent = LeducHoldemRuleAgentV2()
        self.rule_agents = [rule_agent for _ in range(env.num_players)]

    @property
    def agents(self):
        pass
