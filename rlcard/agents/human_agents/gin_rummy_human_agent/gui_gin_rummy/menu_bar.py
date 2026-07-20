
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game_frame import GameFrame

import tkinter as tk
from tkinter import messagebox

from .preferences_window import PreferencesWindow


class MenuBar(tk.Menu):

    def __init__(self, root: tk.Tk, game_frame: 'GameFrame'):
        super().__init__(root)
        self.game_frame = game_frame

        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(label="New Game", command=self.on_new_game_menu_clicked)
        self.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(self, tearoff=False)
        edit_menu.add_command(label="Preferences", command=self.on_preference_menu_clicked)
        self.add_cascade(label="Edit", menu=edit_menu)

        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(label="About", command=self.on_about_menu_clicked)
        self.add_cascade(label="Help", menu=help_menu)

        root.configure(menu=self)

    def on_new_game_menu_clicked(self):
        pass

    def on_preference_menu_clicked(self):
        pass

    @staticmethod
    def on_about_menu_clicked():
        pass
