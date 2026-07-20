
import os
import threading
import time
import timeit
import pprint
from collections import deque

import torch
from torch import multiprocessing as mp
from torch import nn

from .file_writer import FileWriter
from .model import DMCModel
from .pettingzoo_model import DMCModelPettingZoo
from .utils import (
    get_batch,
    create_buffers,
    create_optimizers,
    act,
    log,
)
from .pettingzoo_utils import (
    create_buffers_pettingzoo,
    act_pettingzoo,
)

def compute_loss(logits, targets):
    pass

def learn(
    position,
    actor_models,
    agent,
    batch,
    optimizer,
    training_device,
    max_grad_norm,
    mean_episode_return_buf,
    lock
):
    pass


class DMCTrainer:    
    def __init__(
        self,
        env,
        cuda="",
        is_pettingzoo_env=False,
        load_model=False,
        xpid='dmc',
        save_interval=30,
        num_actor_devices=1,
        num_actors=5,
        training_device="0",
        savedir='experiments/dmc_result',
        total_frames=100000000000,
        exp_epsilon=0.01,
        batch_size=32,
        unroll_length=100,
        num_buffers=50,
        num_threads=4,
        max_grad_norm=40,
        learning_rate=0.0001,
        alpha=0.99,
        momentum=0,
        epsilon=0.00001
    ):
        self.env = env

        self.plogger = FileWriter(
            xpid=xpid,
            rootdir=savedir,
        )

        self.checkpointpath = os.path.expandvars(
            os.path.expanduser('%s/%s/%s' % (savedir, xpid, 'model.tar')))

        self.T = unroll_length
        self.B = batch_size

        self.xpid = xpid
        self.load_model = load_model
        self.savedir = savedir
        self.save_interval = save_interval
        self.num_actor_devices = num_actor_devices
        self.num_actors = num_actors
        self.training_device = training_device
        self.total_frames = total_frames
        self.exp_epsilon = exp_epsilon
        self.num_buffers = num_buffers
        self.num_threads = num_threads
        self.max_grad_norm = max_grad_norm
        self.learning_rate =learning_rate
        self.alpha = alpha
        self.momentum = momentum
        self.epsilon = epsilon

        self.is_pettingzoo_env = is_pettingzoo_env
        if not self.is_pettingzoo_env:
            self.num_players = self.env.num_players
            self.action_shape = self.env.action_shape
            if self.action_shape[0] == None:  # One-hot encoding
                self.action_shape = [[self.env.num_actions] for _ in range(self.num_players)]

            def model_func(device):
                pass
        else:
            self.num_players = self.env.num_agents

            def model_func(device):
                pass
        self.model_func = model_func

        self.mean_episode_return_buf = [deque(maxlen=100) for _ in range(self.num_players)]

        if cuda == "": # Use CPU
            self.device_iterator = ['cpu']
            self.training_device = "cpu"
        else:
            self.device_iterator = range(num_actor_devices)

    def start(self):
        pass
