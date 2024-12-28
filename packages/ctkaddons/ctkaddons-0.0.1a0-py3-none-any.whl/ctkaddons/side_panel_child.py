from typing import Any
import customtkinter as ctk
import tkscenes


class SidePane(ctk.CTkBaseClass):
    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs)

        self.pane = ctk.CTkFrame(master)
        self.center = ctk.CTkFrame(self.pane, fg_color="transparent")
        self.center.pack(expand=True, anchor="center")

        self.items: dict[str, ctk.CTkButton] = {}

    def add(self, key: str, name=None, image=None, command=None):
        if name is None:
            name = key

        self.items[key] = ctk.CTkButton(self.center, text=name, image=image, command=command)

        self.items[key].pack(padx=5, pady=5)

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

        self.pane.pack(
            padx=settings["padx"],
            pady=settings["pady"],
            ipadx=settings["ipadx"],
            ipady=settings["ipady"],
            side=settings["side"],
            anchor=settings["anchor"],
            fill=settings["fill"],
            expand=settings["expand"]
        )

    def pack_forget(self):
        self.pane.pack_forget()


class MainPane(ctk.CTkBaseClass):
    def __init__(self, master: Any, fg_color=None, bg_color="transparent", **kwargs):
        super().__init__(master, **kwargs)

        self.pane = ctk.CTkFrame(master, fg_color=fg_color, bg_color=bg_color)

        self.scenes: dict[str, tkscenes.Scene] = {}
        self._current_scene = None
        self._has_drawn = False

    def __getitem__(self, item: str) -> tkscenes.Scene:
        return self.scenes[item]

    def add_scene(self, key: str):
        if len(self.scenes) == 0:
            self._current_scene = key

        self.scenes[key] = tkscenes.Scene()

    def change_scene(self, key: str):
        self._current_scene = key

        if self._has_drawn:
            for scene in self.scenes.keys():
                if scene == key:
                    continue

                self.scenes[scene].unload()

            self.scenes[key].load()

    def pack(self, _key=None, **kwargs):
        self._has_drawn = True

        if _key is None:
            _key = list(self.scenes.keys())[0]

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

        self.pane.pack(
            padx=settings["padx"],
            pady=settings["pady"],
            ipadx=settings["ipadx"],
            ipady=settings["ipady"],
            side=settings["side"],
            anchor=settings["anchor"],
            fill=settings["fill"],
            expand=settings["expand"]
        )

        self.scenes[_key].load()

    def pack_forget(self):
        self.pane.pack_forget()
