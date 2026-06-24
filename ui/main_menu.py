from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from config import is_first_run


class MainMenu(QWidget):
    def __init__(self, navigate_to):
        super().__init__()
        self.navigate_to = navigate_to
        layout = QVBoxLayout()

        if is_first_run():
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
