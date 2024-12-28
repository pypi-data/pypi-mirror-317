"""NextGenWindow module."""

from t_nextgen.ng_app_manager import NGAppManager


class NextGenWindow:
    """NextGenWindow class."""

    def __init__(self, app_path: str) -> None:
        """Initialize NextGenWindow."""
        self.desktop_app = NGAppManager(app_path)
