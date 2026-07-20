from collections import defaultdict
import numpy as np


def wrap_state(state):
    if "obs" in state and "legal_actions" in state and "raw_legal_actions" in state:
        return state

    wrapped_state = {}
    wrapped_state["obs"] = state["observation"]
    legal_actions = np.flatnonzero(state["action_mask"])
    wrapped_state["legal_actions"] = {l: None for l in legal_actions}
    wrapped_state["raw_legal_actions"] = list(wrapped_state["legal_actions"].keys())
    return wrapped_state


def run_game_pettingzoo(env, agents, is_training=False):
    env.reset()
    trajectories = defaultdict(list)
    for agent_name in env.agent_iter():
        obs, reward, done, _ = env.last()
        trajectories[agent_name].append((obs, reward, done))

        if done:
            action = None
        else:
            if is_training:
                action = agents[agent_name].step(obs)
            else:
                action, _ = agents[agent_name].eval_step(obs)
        trajectories[agent_name].append(action)

        env.step(action)
    return trajectories


def reorganize_pettingzoo(trajectories):
    pass


def tournament_pettingzoo(env, agents, num_episodes):
    pass
