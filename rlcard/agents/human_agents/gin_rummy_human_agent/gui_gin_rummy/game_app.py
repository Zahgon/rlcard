
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from rlcard.envs.gin_rummy import GinRummyEnv

from typing import Callable

import tkinter as tk

import rlcard

from rlcard.agents.random_agent import RandomAgent

from ..gin_rummy_human_agent import HumanAgent

from .game_frame import GameFrame
from .menu_bar import MenuBar


class GameApp(object):

    def __init__(self, make_gin_rummy_env: Callable[[], 'GinRummyEnv'] = None):
        self.make_gin_rummy_env = make_gin_rummy_env if make_gin_rummy_env else GameApp._make_gin_rummy_env
        root = tk.Tk()
        root.resizable(False, False)
        self.game_frame = GameFrame(root=root, game_app=self)
        self.menu_bar = MenuBar(root, game_frame=self.game_frame)
        root.mainloop()

    @staticmethod
    def _make_gin_rummy_env() -> 'GinRummyEnv':
        pass
