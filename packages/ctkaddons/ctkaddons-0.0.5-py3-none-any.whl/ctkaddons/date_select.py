from typing import Any
import customtkinter as ctk
import datetime

from customtkinter import CTkFrame

from .calender import CTkCalender, month_names


class CTkDateSelect(ctk.CTkBaseClass):
    """
    Creates a dropdown for selecting dates
    """
    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs)

        self._date = datetime.date.today()
        self._dropdown = ctk.CTkButton(master, text=str(self._date), command=self._open_popup)

        self._window = None

    def select_date(self, date: datetime.date):
        self._dropdown.configure(
            True,
            text=str(date)
        )
        self._window.destroy()

    def _open_popup(self):
        # stupid
        def insanity():
            self._calender[1].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 1)
                )
            )
            self._calender[2].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 2)
                )
            )
            self._calender[3].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 3)
                )
            )
            self._calender[4].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 4)
                )
            )
            self._calender[5].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 5)
                )
            )
            self._calender[6].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 6)
                )
            )
            self._calender[7].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 7)
                )
            )
            self._calender[8].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 8)
                )
            )
            self._calender[9].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 9)
                )
            )
            self._calender[10].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 10)
                )
            )
            self._calender[11].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 11)
                )
            )
            self._calender[12].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 12)
                )
            )
            self._calender[13].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 13)
                )
            )
            self._calender[14].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 14)
                )
            )
            self._calender[15].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 15)
                )
            )
            self._calender[16].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 16)
                )
            )
            self._calender[17].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 17)
                )
            )
            self._calender[18].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 18)
                )
            )
            self._calender[19].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 19)
                )
            )
            self._calender[20].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 20)
                )
            )
            self._calender[21].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 21)
                )
            )
            self._calender[22].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 22)
                )
            )
            self._calender[23].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 23)
                )
            )
            self._calender[24].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 24)
                )
            )
            self._calender[25].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 25)
                )
            )
            self._calender[26].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 26)
                )
            )
            self._calender[27].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 27)
                )
            )
            self._calender[28].configure(
                True,
                command=lambda: self.select_date(
                    datetime.date(self._calender.year, self._calender.month, 28)
                )
            )
            if self._calender.len_of_month >= 29:
                self._calender[29].configure(
                    True,
                    command=lambda: self.select_date(
                        datetime.date(self._calender.year, self._calender.month, 29)
                    )
                )
            if self._calender.len_of_month >= 30:
                self._calender[30].configure(
                    True,
                    command=lambda: self.select_date(
                        datetime.date(self._calender.year, self._calender.month, 30)
                    )
                )
            if self._calender.len_of_month >= 31:
                self._calender[31].configure(
                    True,
                    command=lambda: self.select_date(
                        datetime.date(self._calender.year, self._calender.month, 31)
                    )
                )

        # command
        def change_time(n: int):
            year = self._calender.year
            month = self._calender.month

            month += n

            if month > 12:
                month = 1
                year += 1
            if month < 1:
                month = 12
                year -= 1

            self._calender.change_time(
                datetime.date(year, month, 1)
            )

            insanity()

            self._text.configure(True, text=f"{month_names[month][:3]} {year}")

        # code
        self._window = ctk.CTkToplevel()
        self._window.title("Select a date")
        self._window.geometry("400x300")

        self._top_bar = CTkFrame(self._window)
        self._top_bar.pack(fill="x", padx=5, pady=5)

        self._top_bar.columnconfigure([0, 1, 2], weight=1)
        self._top_bar.rowconfigure(0, weight=1)

        self._calender = CTkCalender(self._window)
        self._calender.pack(fill="both", padx=5, pady=5, expand=True)

        insanity()

        self._text = ctk.CTkLabel(
            self._top_bar,
            text=f"{month_names[self._calender.month][:3]} {self._calender.year}"
        )
        self._next = ctk.CTkButton(
            self._top_bar, text="Next",
            command=lambda: change_time(1)
        )
        self._back = ctk.CTkButton(
            self._top_bar, text="Back",
            command=lambda: change_time(-1)
        )

        self._back.grid(row=0, column=0, padx=5, pady=5, sticky="news")
        self._text.grid(row=0, column=1, padx=5, pady=5)
        self._next.grid(row=0, column=2, padx=5, pady=5, sticky="news")

    def pack(self, **kwargs):
        self._dropdown.pack(**kwargs)

    def grid(self, **kwargs):
        self._dropdown.grid(**kwargs)

    def place(self, **kwargs):
        self._dropdown.place(**kwargs)
