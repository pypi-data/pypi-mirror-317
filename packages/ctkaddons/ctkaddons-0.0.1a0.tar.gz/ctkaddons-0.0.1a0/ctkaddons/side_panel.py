from typing import Any
import customtkinter as ctk
import tkscenes

from ctkaddons.side_panel_child import SidePane as SidePane
from ctkaddons.side_panel_child import MainPane as MainPane


class SidePanel(ctk.CTkBaseClass):
    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs)

        self.frame = ctk.CTkFrame(master, fg_color="transparent")

        self.side_pane = SidePane(self.frame)
        self.main_pane = MainPane(self.frame, fg_color="transparent")

    def __getitem__(self, item: str) -> tkscenes.Scene:
        return self.main_pane[item]

    def add_scene(self, key: str, name=None, image=None):
        if name is None:
            name = key

        self.side_pane.add(key, name, image, lambda: self.change_scene(key))
        self.main_pane.add_scene(key)

    def change_scene(self, key: str):
        self.main_pane.change_scene(key)

    def pack(self, **kwargs):
        settings = {
            "padx": 0,
            "pady": 0,
            "ipadx": 0,
            "ipady": 0,
            "side": "top",
            "anchor": "center",
            "fill": None,
            "expand": False
        }

        for key in settings.keys():
            if key in kwargs.keys():
                settings[key] = kwargs[key]

        self.frame.pack(
            padx=settings["padx"],
            pady=settings["pady"],
            ipadx=settings["ipadx"],
            ipady=settings["ipady"],
            side=settings["side"],
            anchor=settings["anchor"],
            fill=settings["fill"],
            expand=settings["expand"]
        )

        self.side_pane.pack(fill="y", side="left", padx=5, pady=5)
        self.main_pane.pack(fill="both", side="left", expand=True, padx=5, pady=5)

    def pack_forget(self):
        self.frame.pack_forget()
        self.side_pane.pack_forget()
        self.main_pane.pack_forget()
