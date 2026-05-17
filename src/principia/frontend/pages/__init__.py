"""NiceGUI page registration."""

from nicegui import ui

from principia.frontend.language import LearningStage, get_user_learning_stage
from principia.frontend.pages.reinforcement_learning_main import (
    reinforcement_learning_main,
)
from principia.frontend.pages.supervised_learning_main import supervised_learning_main


def register_pages() -> None:
    """Register all frontend pages."""

    @ui.page("/")
    def main_page() -> None:
        if get_user_learning_stage() == LearningStage.REINFORCEMENT:
            reinforcement_learning_main()
            return

        supervised_learning_main()
