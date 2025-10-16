import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QStackedWidget

from ui.main_menu import MainMenu
from ui.reverse_text_page import ReverseTextPage
from ui.swap_case_page import SwapCasePage
from ui.settings_page import SettingsPage, RegeneratePage
from ui.main_page import MainPage
from config import is_first_run


class App(QStackedWidget):
    def __init__(self):
        super().__init__()
        # create pages
        self.menu = MainMenu(self.navigate_to)
        self.reverse = ReverseTextPage(self.navigate_to)
        self.swapcase = SwapCasePage(self.navigate_to)
        self.settings = SettingsPage(self.navigate_to)
        self.regen = RegeneratePage(self.navigate_to)
        self.mainpage = MainPage(self.navigate_to)
        # add pages (index order)
        self.addWidget(self.menu)      # index 0
        self.addWidget(self.reverse)   # index 1
        self.addWidget(self.swapcase)  # index 2
        self.addWidget(self.settings)  # index 3
        self.addWidget(self.regen)     # index 4
        self.addWidget(self.mainpage)  # index 5

        self.setWindowTitle("Dragodinde Helper")
        self.setFixedSize(900, 900)
        # pages created

    def navigate_to(self, page_name: str):
        mapping = {
            "menu": 0,
            "reverse": 1,
            "swapcase": 2,
            "settings": 3,
            "regen": 4,
            "main": 5,
        }
        idx = mapping.get(page_name, 0)
        # if navigating to main page, refresh its displayed values first
        if page_name == "main":
            try:
                self.mainpage.refresh()
            except Exception:
                pass
        self.setCurrentIndex(idx)


def main():
    app = QApplication(sys.argv)

    # apply QSS theme if available
    qss_path = Path(__file__).with_name("..") / "dark_theme.qss"
    # resolve relative path correctly
    qss_file = Path(__file__).resolve().parent / "dark_theme.qss"
    if qss_file.exists():
        with open(qss_file, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

    window = App()

    # Directly create and show main window (no splash)
    # if it's the first run, start on settings; otherwise show the main summary page
    start_page = "settings" if is_first_run() else "main"
    window.show()
    try:
        window.raise_()
        window.activateWindow()
    except Exception:
        pass
    try:
        window.resize(800, 600)
        window.move(100, 100)
    except Exception:
        pass
    # position: top of the screen (available geometry) and horizontally centered
    try:
        screen_geom = QApplication.desktop().availableGeometry(window)
        x = screen_geom.x() + (screen_geom.width() - window.width()) // 2
        y = screen_geom.y()  # top of available area (avoids taskbar)
        window.move(x, y)
    except Exception:
        # fallback to previous behavior if anything fails
        try:
            screen_center = QApplication.desktop().screen().rect().center()
            window.move(screen_center - window.rect().center())
        except Exception:
            pass
    window.navigate_to(start_page)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
