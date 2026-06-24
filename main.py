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
        self.menu = MainMenu(self.navigate_to)
        self.reverse = ReverseTextPage(self.navigate_to)
        self.swapcase = SwapCasePage(self.navigate_to)
        self.settings = SettingsPage(self.navigate_to)
        self.regen = RegeneratePage(self.navigate_to)
        self.mainpage = MainPage(self.navigate_to)
        self.addWidget(self.menu)
        self.addWidget(self.reverse)
        self.addWidget(self.swapcase)
        self.addWidget(self.settings)
        self.addWidget(self.regen)
        self.addWidget(self.mainpage)

        self.setWindowTitle("Dragodinde Helper")
        self.setFixedSize(900, 900)

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
        if page_name == "main":
            try:
                self.mainpage.refresh()
            except Exception:
                pass
        self.setCurrentIndex(idx)


def main():
    app = QApplication(sys.argv)

    qss_file = Path(__file__).resolve().parent / "dark_theme.qss"
    if qss_file.exists():
        with open(qss_file, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

    window = App()

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
    try:
        screen_geom = QApplication.desktop().availableGeometry(window)
        x = screen_geom.x() + (screen_geom.width() - window.width()) // 2
        y = screen_geom.y()
        window.move(x, y)
    except Exception:
        try:
            screen_center = QApplication.desktop().screen().rect().center()
            window.move(screen_center - window.rect().center())
        except Exception:
            pass
    window.navigate_to(start_page)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
