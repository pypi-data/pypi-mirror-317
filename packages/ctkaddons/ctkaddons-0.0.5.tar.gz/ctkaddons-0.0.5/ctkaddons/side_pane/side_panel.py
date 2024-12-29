from typing import Any
import customtkinter as ctk
import tkscenes

from .side_panel_child import SidePane as SidePane
from .side_panel_child import MainPane as MainPane


class CTkSidePanel(ctk.CTkBaseClass):
    """
    Create a side panel
    """
    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs)

        self.frame = ctk.CTkFrame(master, fg_color="transparent")

        self.side_pane = SidePane(self.frame)
        self.main_pane = MainPane(self.frame, fg_color="transparent")

    def __getitem__(self, item: str) -> tkscenes.Scene:
        """
        Get the scene
        :param item: Identifier
        :return:
        """
        return self.main_pane[item]

    def add_scene(self, key: str, name=None, image=None, anchor="center"):
        """
        Add a scene
        :param key: Identifier
        :param name: Name of the entry
        :param image:
        :param anchor:
        :return:
        """
        if name is None:
            name = key

        self.side_pane.add(key, name, image, lambda: self.change_scene(key), anchor)
        self.main_pane.add_scene(key)

    def change_scene(self, key: str):
        """
        Change the current scene
        :param key: Identifier
        :return:
        """
        self.main_pane.change_scene(key)

    def _render_panes(self):
        self.side_pane.pack(fill="y", side="left", padx=5, pady=5)
        self.main_pane.pack(fill="both", side="left", expand=True, padx=5, pady=5)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
        self._render_panes()

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)
        self._render_panes()

    def place(self, **kwargs):
        self.frame.place(**kwargs)
        self._render_panes()

    def pack_forget(self):
        self.frame.pack_forget()

    def grid_forget(self):
        self.frame.grid_forget()

    def place_forget(self):
        self.frame.place_forget()

    @property
    def main_panel(self) -> ctk.CTkFrame:
        """
        :return: The main panel
        """
        return self.main_pane.pane
