"""Sway window system."""

from json import loads
from subprocess import PIPE, Popen

from hints.window_systems.window_system import WindowSystem, WindowSystemType


class Sway(WindowSystem):
    """Sway Window system class."""

    def __init__(self):
        self.focused_window = self._get_focused_window_from_sway_tree()
        self.focused_workspace = self._get_focused_workspace_from_sway_tree()
        self.focused_output = self._get_focused_output_from_sway_tree()

    def _get_focused_window_from_sway_tree(self):
        swaytree = Popen(["swaymsg", "-t", "get_tree"], stdout=PIPE)
        focused = Popen(
            ["jq", ".. | select(.type?) | select(.focused==true)"],
            stdin=swaytree.stdout,
            stdout=PIPE,
        )

        return loads(focused.communicate()[0].decode("utf-8"))

    def _get_focused_workspace_from_sway_tree(self):
        swaytree = Popen(["swaymsg", "-t", "get_workspaces"], stdout=PIPE)
        focused = Popen(
            ["jq", ".[] | select(.focused==true)"],
            stdin=swaytree.stdout,
            stdout=PIPE,
        )

        return loads(focused.communicate()[0].decode("utf-8"))

    def _get_focused_output_from_sway_tree(self):
        swaytree = Popen(["swaymsg", "-t", "get_outputs"], stdout=PIPE)
        focused = Popen(
            ["jq", ".[] | select(.focused==true)"],
            stdin=swaytree.stdout,
            stdout=PIPE,
        )

        return loads(focused.communicate()[0].decode("utf-8"))

    @property
    def window_system_type(self) -> WindowSystemType:
        """Get window_sysetm_type.

        :return: The window system type.
        """
        return WindowSystemType.WAYLAND

    @property
    def focused_window_extents(self) -> tuple[int, int, int, int]:
        """Get active window extents.

        :return: Active window extents (x, y, width, height).
        """
        # The focused widnow does not included offsets for the top bar (swaybar).
        # So we need to calcuare the height of the bar for the current monitor.
        # Unknow if this will be an issue with other bars on sway.
        bar_height = (
            self.focused_output["rect"]["height"]
            - self.focused_workspace["rect"]["height"]
        )

        return (
            self.focused_window["rect"]["x"],
            self.focused_window["rect"]["y"] - bar_height,
            self.focused_window["rect"]["width"],
            self.focused_window["rect"]["height"],
        )

    @property
    def focused_window_pid(self) -> int:
        """Get Process ID corresponding to the focused widnow.

        :return: Process ID of focused window.
        """
        return self.focused_window["pid"]

    @property
    def focused_applicaiton_name(self) -> str:
        """Get focused application name.

        This name is the name used to identify applications for per-
        application rules.

        :return: Focused application name.
        """
        return self.focused_window["app_id"]
