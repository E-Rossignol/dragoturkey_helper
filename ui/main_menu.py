from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from config import is_first_run


class MainMenu(QWidget):
    """Main menu with navigation buttons to the two pages."""

    def __init__(self, navigate_to):
        """navigate_to: callable(page_name: str) -> None"""
        super().__init__()
        self.navigate_to = navigate_to
        layout = QVBoxLayout()

        # default menu: different if first run or not
        if is_first_run():
            # on first run, provide direct access to settings
            self.btn_edit = QPushButton("Modifier paramètres")
            layout.addWidget(self.btn_edit)
            self.btn_edit.clicked.connect(lambda: self.navigate_to("settings"))
        else:
            self.btn_regen = QPushButton("Regénérer script")
            self.btn_edit = QPushButton("Modifier paramètres")
            layout.addWidget(self.btn_regen)
            layout.addWidget(self.btn_edit)
            self.btn_regen.clicked.connect(lambda: self.navigate_to("regen"))
            self.btn_edit.clicked.connect(lambda: self.navigate_to("settings"))
        layout.addStretch()
        self.setLayout(layout)
        
