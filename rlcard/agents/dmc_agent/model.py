
import numpy as np

import torch
from torch import nn

class DMCNet(nn.Module):
    def __init__(
        self,
        state_shape,
        action_shape,
        mlp_layers=[512,512,512,512,512]
    ):
        super().__init__()
        input_dim = np.prod(state_shape) + np.prod(action_shape)
        layer_dims = [input_dim] + mlp_layers
        fc = []
        for i in range(len(layer_dims)-1):
            fc.append(nn.Linear(layer_dims[i], layer_dims[i+1]))
            fc.append(nn.ReLU())
        fc.append(nn.Linear(layer_dims[-1], 1))
        self.fc_layers = nn.Sequential(*fc)

    def forward(self, obs, actions):
        obs = torch.flatten(obs, 1)
        actions = torch.flatten(actions, 1)
        x = torch.cat((obs, actions), dim=1)
        values = self.fc_layers(x).flatten()
        return values

class DMCAgent:
    def __init__(
        self,
        state_shape,
        action_shape,
        mlp_layers=[512,512,512,512,512],
        exp_epsilon=0.01,
        device="0",
    ):
        self.use_raw = False
        self.device = 'cuda:'+device if device != "cpu" else "cpu"
        self.net = DMCNet(state_shape, action_shape, mlp_layers).to(self.device)
        self.exp_epsilon = exp_epsilon
        self.action_shape = action_shape

    def step(self, state):
        action_keys, values = self.predict(state)

        if self.exp_epsilon > 0 and np.random.rand() < self.exp_epsilon:
            action = np.random.choice(action_keys)
        else:
            action_idx = np.argmax(values)
            action = action_keys[action_idx]

        return action

    def eval_step(self, state):
        action_keys, values = self.predict(state)

        action_idx = np.argmax(values)
        action = action_keys[action_idx]

        info = {}
        info['values'] = {state['raw_legal_actions'][i]: float(values[i]) for i in range(len(action_keys))}

        return action, info

    def share_memory(self):
        pass

    def eval(self):
        pass

    def parameters(self):
        pass

    def predict(self, state):
        obs = state['obs'].astype(np.float32)
        legal_actions = state['legal_actions']
        action_keys = np.array(list(legal_actions.keys()))
        action_values = list(legal_actions.values())
        # One-hot encoding if there is no action features
        for i in range(len(action_values)):
            if action_values[i] is None:
                action_values[i] = np.zeros(self.action_shape[0])
                action_values[i][action_keys[i]] = 1
        action_values = np.array(action_values, dtype=np.float32)

        obs = np.repeat(obs[np.newaxis, :], len(action_keys), axis=0)

        values = self.net.forward(torch.from_numpy(obs).to(self.device),
                                  torch.from_numpy(action_values).to(self.device))

        return action_keys, values.cpu().detach().numpy()

    def forward(self, obs, actions):
        return self.net.forward(obs, actions)

    def load_state_dict(self, state_dict):
        pass

    def state_dict(self):
        pass

    def set_device(self, device):
        pass

class DMCModel:
    def __init__(
        self,
        state_shape,
        action_shape,
        mlp_layers=[512,512,512,512,512],
        exp_epsilon=0.01,
        device=0
    ):
        self.agents = []
        for player_id in range(len(state_shape)):
            agent = DMCAgent(
                state_shape[player_id],
                action_shape[player_id],
                mlp_layers,
                exp_epsilon,
                device,
            )
            self.agents.append(agent)

    def share_memory(self):
        pass

    def eval(self):
        pass

    def parameters(self, index):
        pass

    def get_agent(self, index):
        pass

    def get_agents(self):
        pass
