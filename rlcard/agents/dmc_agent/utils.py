
import logging
import traceback

import numpy as np
import torch

shandle = logging.StreamHandler()
shandle.setFormatter(
    logging.Formatter(
        '[%(levelname)s:%(process)d %(module)s:%(lineno)d %(asctime)s] '
        '%(message)s'))
log = logging.getLogger('doudzero')
log.propagate = False
log.addHandler(shandle)
log.setLevel(logging.INFO)

def get_batch(
    free_queue,
    full_queue,
    buffers,
    batch_size,
    lock
):
    pass

def create_buffers(
    T,
    num_buffers,
    state_shape,
    action_shape,
    device_iterator,
):
    pass

def create_optimizers(
    num_players,
    learning_rate,
    momentum,
    epsilon,
    alpha,
    learner_model
):
    pass

def act(
    i,
    device,
    T,
    free_queue,
    full_queue,
    model,
    buffers,
    env
):
    pass
