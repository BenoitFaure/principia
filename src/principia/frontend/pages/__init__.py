"""NiceGUI page registration."""

from principia.frontend.pages.supervised_learning_main import (
    register_supervised_learning_main_page,
)


def register_pages() -> None:
    """Register all frontend pages."""
    register_supervised_learning_main_page()
