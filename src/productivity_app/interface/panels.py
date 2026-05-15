"""UI panels for organizing frontend components"""

import tkinter as tk


class StatusPanel:
    """Manages status messages display"""

    FONT = ("Arial", 12)
    PADY = 10

    def __init__(self, parent):
        self.label = tk.Label(
            parent,
            text="Status: Waiting...",
            font=self.FONT,
            wraplength=500
        )

    def pack(self, **kwargs):
        """Pack the status label"""
        self.label.pack(pady=self.PADY, **kwargs)

    def set_text(self, text):
        """Update status text"""
        self.label.config(text=text)


class GoalsPanel:
    """Manages current goals display and visibility toggle"""

    FONT = ("Arial", 12)
    PADY = 10
    NO_GOALS_TEXT = "Your goals will appear here. Recommended: 3-5 goals per week."

    def __init__(self, parent, image_manager):
        self.image_manager = image_manager
        self.frame = tk.Frame(parent)

        self.eye_img = image_manager.get_image("eye")
        self.eye_slash_img = image_manager.get_image("eye-slash")

        self.header = tk.Label(
            self.frame,
            text=" Current goals",
            image=self.eye_img,
            compound="left",
            font=(self.FONT[0], self.FONT[1], "bold"),
            anchor="w"
        )

        self.label = tk.Label(
            self.frame,
            text=self.NO_GOALS_TEXT,
            font=self.FONT,
            wraplength=500,
            justify="left"
        )

        self.header.pack(anchor="w")
        self.label.pack(anchor="w", pady=(self.PADY, 0))

    def pack(self, **kwargs):
        """Pack the goals frame"""
        self.frame.pack(pady=self.PADY, fill="x", **kwargs)

    def bind_header_click(self, callback):
        """Bind click event to the header"""
        self.header.bind("<Button-1>", callback)

    def update_goals(self, goals):
        """Update the goals display"""
        if goals:
            self.label.config(text=f"Current goals:\n{chr(10).join(goals)}")
        else:
            self.label.config(text=self.NO_GOALS_TEXT)

    def reset(self):
        """Reset to default state"""
        self.label.config(text=self.NO_GOALS_TEXT)
        if self.eye_img:
            self.header.config(image=self.eye_img)
        if self.label.winfo_ismapped():
            pass  # Already visible
        else:
            self.label.pack(anchor="w", pady=(self.PADY, 0))

    def toggle_visibility(self):
        """Toggle the visibility of the goals label"""
        if self.label.winfo_ismapped():
            self.label.pack_forget()
            if self.eye_slash_img:
                self.header.config(image=self.eye_slash_img)
        else:
            self.label.pack(anchor="w", pady=(self.PADY, 0))
            if self.eye_img:
                self.header.config(image=self.eye_img)


class InactiveGoalsPanel:
    """Manages inactive goals display"""

    FONT = ("Arial", 12)
    PADY = 10

    def __init__(self, parent):
        self.label = tk.Label(
            parent,
            text="Inactive goals: None",
            font=self.FONT,
            wraplength=500,
            justify="left"
        )

    def pack(self, **kwargs):
        """Pack the inactive goals label"""
        self.label.pack(pady=self.PADY, **kwargs)

    def update_goals(self, goals):
        """Update inactive goals display"""
        if goals:
            self.label.config(text=f"Inactive goals:\n{chr(10).join(goals)}")
        else:
            self.label.config(text="Inactive goals: None")

    def reset(self):
        """Reset to default state"""
        self.label.config(text="Inactive goals: None")


class ButtonBar:
    """Manages button creation and event handling"""

    FONT = ("Arial", 12)
    PADX = 20
    PADY = 10

    def __init__(self, parent):
        self.parent = parent
        self.buttons = {}

    def add_button(self, name, text, command):
        """Add a button to the button bar"""
        button = tk.Button(
            self.parent,
            text=text,
            command=command,
            font=self.FONT,
            padx=self.PADX,
            pady=self.PADY
        )
        button.pack(pady=self.PADY)
        self.buttons[name] = button
        return button

    def get_button(self, name):
        """Get a button by name"""
        return self.buttons.get(name)
