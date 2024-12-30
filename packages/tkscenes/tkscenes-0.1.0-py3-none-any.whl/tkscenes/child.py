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
            self.widget.pack(**self.mode_settings)
            return
        if self.mode == "grid":
            self.widget.grid(**self.mode_settings)
            return
        if self.mode == "place":
            self.widget.place(**self.mode_settings)
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
