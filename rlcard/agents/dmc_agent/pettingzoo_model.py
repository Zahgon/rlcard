from collections import OrderedDict

from .model import DMCAgent
from rlcard.utils.pettingzoo_utils import wrap_state


class DMCAgentPettingZoo(DMCAgent):
    def step(self, state):
        return super().step(wrap_state(state))

    def eval_step(self, state):
        return super().eval_step(wrap_state(state))

    def feed(self, ts):
        pass


class DMCModelPettingZoo:
    def __init__(
        self,
        env,
        mlp_layers=[512,512,512,512,512],
        exp_epsilon=0.01,
        device="0"
    ):
        self.agents = OrderedDict()
        for agent_name in env.agents:
            agent = DMCAgentPettingZoo(
                env.observation_space(agent_name)["observation"].shape,
                (env.action_space(agent_name).n,),
                mlp_layers,
                exp_epsilon,
                device,
            )
            self.agents[agent_name] = agent

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
