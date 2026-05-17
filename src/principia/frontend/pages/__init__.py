"""NiceGUI page registration."""

from principia.frontend.pages.home import register_home_page


def register_pages() -> None:
    """Register all frontend pages."""
    register_home_page()
