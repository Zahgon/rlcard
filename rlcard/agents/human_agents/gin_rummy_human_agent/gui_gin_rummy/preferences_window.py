
from tkinter import *
import tkinter.colorchooser as colorchooser
from configparser import ConfigParser

from . import configurations
from .configurations import config_path
from .configurations import settings_section
from .configurations import show_status_messages_option, warning_as_option, game_background_color_option
from .configurations import window_size_factor_option
from .configurations import is_show_tips_option
from .configurations import is_debug_option


class PreferencesWindow(object):



    def __init__(self, view):
        self.parent = view.master
        self.view = view

        self.pref_window = Toplevel(self.parent)
        self.pref_window.title("Gin Rummy Preferences")

        self.game_background_color = configurations.GAME_BACKGROUND_COLOR
        self.original_game_background_color = self.game_background_color  # used if color dialog cancelled

        row = 0

        row += 1
        self.show_status_messages_listbox = self.create_choice_line(row=row, choice_name=show_status_messages_option)

        row += 1
        self.warnings_as_listbox = self.create_choice_line(row=row, choice_name=warning_as_option)

        row += 1
        Label(self.pref_window, text="Game background color").grid(row=row, sticky=W, padx=5, pady=5)
        self.game_background_color_button = Button(self.pref_window, text='Select color')
        self.game_background_color_button.configure(command=self.set_game_background_color)
        self.game_background_color_button.grid(row=row, column=1, columnspan=2, sticky=W, padx=5, pady=5)

        row += 1
        Label(self.pref_window, text="Window size (percent)").grid(row=row, sticky=W, padx=5, pady=5)
        self.window_size_scale = Scale(self.pref_window, from_=50, to=100, orient=HORIZONTAL)
        self.window_size_scale.set(configurations.WINDOW_SIZE_FACTOR)
        self.window_size_scale.grid(row=row, column=1, columnspan=2, sticky=W, padx=5, pady=5)

        row += 1
        self.is_show_tips = BooleanVar()
        self.is_show_tips.set(configurations.IS_SHOW_TIPS)
        self.is_show_tips_checkbutton = self.create_checkbutton(text="show tips", variable=self.is_show_tips)
        self.is_show_tips_checkbutton.grid(row=row, column=0, columnspan=3, sticky=W, padx=5, pady=5)

        row += 1
        self.is_debug = BooleanVar()
        self.is_debug.set(configurations.IS_DEBUG)
        self.is_debug_checkbutton = self.create_checkbutton(text="is debug", variable=self.is_debug)
        self.is_debug_checkbutton.grid(row=row, column=0, columnspan=3, sticky=W, padx=5, pady=5)

        row += 1
        cancel_button = Button(self.pref_window, text="Cancel", command=self.on_cancel_button_clicked)
        cancel_button.grid(row=row, column=1, sticky=E, padx=5, pady=5)
        save_button = Button(self.pref_window, text="Save", command=self.on_save_button_clicked)
        save_button.grid(row=row, column=2, sticky=E, padx=5, pady=5)

        self.pref_window.transient(self.parent)

    def set_game_background_color(self):  # store because color cannot be obtained from its widget
        pass

    def on_save_button_clicked(self):
        pass

    def set_new_values(self):
        pass

    def on_cancel_button_clicked(self):
        pass

    def create_checkbutton(self, text: str, variable: BooleanVar):
        pass

    def create_listbox(self, row, column, columnspan, items):
        pass

    def create_choice_line(self, row: int, choice_name: str):
        pass
