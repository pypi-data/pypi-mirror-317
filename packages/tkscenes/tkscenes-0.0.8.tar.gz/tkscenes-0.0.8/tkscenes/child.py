class Child:
    def __init__(self, widget) -> None:
        """
        Create a child object
        :param widget: A TKinter or customtkinter widget
        """
        self.widget = widget
        self.mode = "pack"
        self.mode_settings = {}

    def set_mode(self, mode: str, **kwargs):
        """
        Define if the widget should use pack, grid, or place. Also define the settings.
        :param mode: Should be "pack", "grid", or "place"
        :param kwargs: Settings
        :return:
        """
        self.mode = mode
        self.mode_settings = kwargs

    def render(self):
        """
        Pack, grid or place the widget on the window.
        :return:
        """
        if self.mode == "pack":
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

            for i in settings.keys():
                if i in self.mode_settings.keys():
                    settings[i] = self.mode_settings[i]

            self.widget.pack(
                padx=settings["padx"],
                pady=settings["pady"],
                ipadx=settings["ipadx"],
                ipady=settings["ipady"],
                side=settings["side"],
                anchor=settings["anchor"],
                fill=settings["fill"],
                expand=settings["expand"]
            )
            return
        if self.mode == "grid":
            settings = {
                "column": 0,
                "row": 0,
                "columnspan": 1,
                "rowspan": 1,
                "padx": 0,
                "pady": 0,
                "ipadx": 0,
                "ipady": 0,
                "sticky": "center"
            }

            for i in settings.keys():
                if i in self.mode_settings.keys():
                    settings[i] = self.mode_settings[i]

            self.widget.grid(
                padx=settings["padx"],
                pady=settings["pady"],
                ipadx=settings["ipadx"],
                ipady=settings["ipady"],
                column=settings["column"],
                row=settings["row"],
                columnspan=settings["columnspan"],
                rowspan=settings["rowspan"],
                sticky=settings["sticky"]
            )
            return
        if self.mode == "place":
            settings = {
                "pady": 0, "padx": 0,
                "ipadx": 0, "ipady": 0,
                "x": 0, "y": 0,
                "width": 100, "height": 50,
                "relx": 0, "rely": 0,
                "relwidth": 0.3, "relheight": 0.2,
                "anchor": "nw"
            }

            for i in settings.keys():
                if i in self.mode_settings.keys():
                    settings[i] = self.mode_settings[i]

            self.widget.place(
                x=settings["x"],
                y=settings["y"],
                width=settings["width"],
                height=settings["height"],
                relx=settings["relx"],
                rely=settings["rely"],
                relwidth=settings["relwidth"],
                relheight=settings["relheight"],
                anchor=settings["anchor"]
            )
            return

    def unrender(self):
        """
        Remove the widget from window
        :return:
        """
        if self.mode == "pack":
            self.widget.pack_forget()
            return
        if self.mode == "grid":
            self.widget.grid_forget()
            return
        if self.mode == "place":
            self.widget.place_forget()
            return

    def destroy(self):
        """
        Remove the widget from the window and erases it from existance
        :return:
        """
        self.widget.destroy()
