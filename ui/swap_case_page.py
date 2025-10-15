from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton
from text_utils import swap_case


class SwapCasePage(QWidget):
    """Page that swaps case of entered text."""

    def __init__(self, navigate_to):
        super().__init__()
        self.navigate_to = navigate_to
        layout = QVBoxLayout()

        self.input = QLineEdit()
        self.submit = QPushButton("Submit")
        self.result = QLabel("")
        self.back = QPushButton("Retour menu")

        layout.addWidget(self.input)
        layout.addWidget(self.submit)
        layout.addWidget(self.result)
        layout.addWidget(self.back)
        layout.addStretch()

        self.setLayout(layout)

        self.submit.clicked.connect(self.on_submit)
        self.back.clicked.connect(lambda: self.navigate_to("menu"))

    def on_submit(self):
        text = self.input.text() or ""
        self.result.setText(swap_case(text))
