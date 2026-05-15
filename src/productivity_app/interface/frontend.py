"""Frontend UI using tkinter"""

import tkinter as tk
from tkinter import messagebox
from .inputs import InputDialog
from .image_manager import TkinterImageManager
from .panels import StatusPanel, GoalsPanel, InactiveGoalsPanel, ButtonBar
from pathlib import Path


class FrontEnd:
    """Main frontend controller - coordinates UI panels and event handling"""

    def __init__(self, event_bus):
        self.image_manager = TkinterImageManager(
            image_dir=Path(__file__).resolve().parent / "assets"
        )
        self.event_bus = event_bus
        self.window = tk.Tk()
        self.window.title("Productivity App")
        self.window.geometry("800x600")

        # Create UI panels
        self.status_panel = StatusPanel(self.window)
        self.button_bar = ButtonBar(self.window)
        self.goals_panel = GoalsPanel(self.window, self.image_manager)
        self.inactive_goals_panel = InactiveGoalsPanel(self.window)

        # Pack UI elements in order
        self.status_panel.pack()
        self._setup_buttons()
        self.goals_panel.pack()
        self.inactive_goals_panel.pack()

        # Setup interactions
        self.goals_panel.bind_header_click(lambda e: self.goals_panel.toggle_visibility())

        # Subscribe to backend events on the event bus.
        self.event_bus.subscribe("day_completed", self._on_day_completed)
        self.event_bus.subscribe("week_completed", self._on_week_completed)
        self.event_bus.subscribe("goal_saved", self._on_successful_save_goal)
        self.event_bus.subscribe("goals_reset", self._on_successful_reset_goals)
        self.event_bus.subscribe("inactive_goal_saved", self._on_successful_save_inactive_goal)
        self.event_bus.subscribe("inactive_goals_reset", self._on_successful_reset_inactive_goals)

        print("[Frontend] UI initialized")

    def _setup_buttons(self):
        """Configure all buttons and their event handlers"""
        self.button_bar.add_button(
            "add_goal",
            "Add goal",
            self._on_add_goal
        )
        self.button_bar.add_button(
            "reset_goals",
            "Reset goals",
            self._on_reset_goals
        )
        self.button_bar.add_button(
            "add_inactive_goal",
            "Add inactive goal",
            self._on_add_inactive_goal
        )
        self.button_bar.add_button(
            "reset_inactive_goals",
            "Reset inactive goals",
            self._on_reset_inactive_goals
        )

    # Goal Event Handlers

    def _on_add_goal(self):
        """Called when user clicks add goal button"""
        goal = self.get_input(message="Add 1 goal.")
        if goal is not None:
            self.event_bus.emit("user_add_goal", {"goal": goal})

    def _on_reset_goals(self):
        """Called when user clicks reset goals button"""
        self.event_bus.emit("reset_goals", {"message": "Goals have been reset."})

    def _on_successful_save_goal(self, data):
        """Called when backend emits 'goal_saved'."""
        print(f"[Frontend] Received goal_saved: {data}")
        self.status_panel.set_text(f"✓ {data['message']}")
        goals = data.get("goals", [])
        self.goals_panel.update_goals(goals)

    def _on_successful_reset_goals(self, data):
        """Called when backend emits 'goals_reset'."""
        print(f"[Frontend] Received goals_reset: {data}")
        self.goals_panel.reset()
        self.status_panel.set_text("Goals have been reset.")

    # Inactive Goal Event Handlers

    def _on_add_inactive_goal(self):
        """Called when user clicks add inactive goal button"""
        goal = self.get_input(message="Add 1 inactive goal.")
        if goal is not None:
            self.event_bus.emit("user_add_inactive_goal", {"goal": goal})

    def _on_reset_inactive_goals(self):
        """Called when user clicks reset inactive goals button"""
        self.event_bus.emit("reset_inactive_goals", {"message": "Inactive goals reset."})

    def _on_successful_save_inactive_goal(self, data):
        """Called when backend emits 'inactive_goal_saved'."""
        print(f"[Frontend] Received inactive_goal_saved: {data}")
        goals = data.get("inactive_goals", [])
        self.inactive_goals_panel.update_goals(goals)

    def _on_successful_reset_inactive_goals(self, data):
        """Called when backend emits 'inactive_goals_reset'."""
        print(f"[Frontend] Received inactive_goals_reset: {data}")
        self.inactive_goals_panel.reset()
        self.status_panel.set_text("Inactive goals have been reset.")

    # Cycle Event Handlers

    def _on_day_completed(self, data):
        """Handle day_completed event from backend"""
        # TODO: implement day-specific logic if needed
        pass

    def _on_week_completed(self, data):
        """Handle week_completed event from backend"""
        print(f"[Frontend] Received week_completed: {data}")
        self.status_panel.set_text(f"★ {data['message']}")
        messagebox.showinfo("Week Completed", "Week complete. Set new goals using 'Add goal' button.")

    # UI Utilities

    def step(self):
        """Start the UI loop"""
        print("[Frontend] Starting UI loop")
        self.window.mainloop()

    def get_input(self, message) -> str | None:
        """Creates a text input dialog.
        
        Args:
            message: Prompt text for the dialog
            
        Returns:
            User input string or None if cancelled
        """
        input_dialog = InputDialog(self.window, message)
        self.window.wait_window(input_dialog)
        return input_dialog.result
