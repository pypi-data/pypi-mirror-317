from typing import Any
import customtkinter as ctk
import datetime
import math
import tkscenes as scn


def is_leep_year(year: int) -> bool:
    return False


class Calender(ctk.CTkBaseClass):
    def __init__(self, master: Any, date=datetime.date.today(), **kwargs):
        super().__init__(master, **kwargs)

        self._today = datetime.date.today()

        self.frame = ctk.CTkFrame(master)
        self.frame.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.labels = [
            ctk.CTkLabel(self.frame, text="Sun"),
            ctk.CTkLabel(self.frame, text="Mon"),
            ctk.CTkLabel(self.frame, text="Tue"),
            ctk.CTkLabel(self.frame, text="Wed"),
            ctk.CTkLabel(self.frame, text="Thu"),
            ctk.CTkLabel(self.frame, text="Fri"),
            ctk.CTkLabel(self.frame, text="Sat")
        ]
        self.dates = scn.Scene()

        self._config_grid(date)
        self._add_dates()

        self._has_drawn = False

    def _add_dates(self):
        for i in range(self._num_of_days):
            if datetime.date(self._year, self._month, i + 1) == self._today:
                color = "#f00a09"
                hover_color = "#a10807"
            else:
                color = None
                hover_color = None
            self.dates[str(i + 1)] = ctk.CTkButton(self.frame, text=str(i + 1), fg_color=color, hover_color=hover_color)
            self.dates[str(i + 1)].set_mode(
                "grid",
                row=(i + self._weekday) // 7 + 1,
                column=(i + self._weekday) % 7,
                padx=5, pady=5,
                sticky="nsew"
            )

    def _config_grid(self, date):
        # self.frame.rowconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=0)

        self._month = date.month
        self._year = date.year
        self._weekday = datetime.date(self._year, self._month, 1).weekday() + 1

        if self._weekday > 6:
            self._weekday = 0

        if self._month == 2:
            if is_leep_year(self._year):
                self._num_of_days = 29
            else:
                self._num_of_days = 28
        else:
            self._num_of_days = [None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][self._month]

        self.frame.rowconfigure([int(i) + 1 for i in range(math.ceil((self._weekday + self._num_of_days) / 7))], weight=1)

    def __getitem__(self, item: str | int) -> ctk.CTkButton:
        return self.dates[str(item)].widget

    def pack(self, **kwargs):
        self._has_drawn = True

        # pack main frame
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

        # pack date bar
        for index, item in enumerate(self.labels):
            item.grid(row=0, column=index)

        self.dates.load()

    def pack_forget(self):
        self.frame.pack_forget()

        for item in self.labels:
            item.pack_forget()

        self.dates.unload()

    def change_time(self, date: datetime.date) -> None:
        self.dates.destroy()
        self._config_grid(date)
        self._add_dates()

        if self._has_drawn:
            self.dates.load()

    @property
    def year(self) -> int:
        return self._year

    @property
    def month(self) -> int:
        return self._month
