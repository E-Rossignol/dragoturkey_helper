from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout


class SplashScreen(QWidget):
    """Simple splash screen with animated dots."""

    def __init__(self, parent=None, duration_ms=1800):
        super().__init__(parent, flags=Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.duration_ms = duration_ms

        self.label_title = QLabel("Dofus Emotes Script Generator")
        self.label_sub = QLabel("Chargement")
        self.label_title.setObjectName("splashTitle")
        self.label_sub.setObjectName("splashSub")

        v = QVBoxLayout()
        v.addStretch()
        v.addWidget(self.label_title, 0, Qt.AlignCenter)
        v.addWidget(self.label_sub, 0, Qt.AlignCenter)
        v.addStretch()
        self.setLayout(v)

        # animation: update dots every 350ms
        self._dots = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)

    def start(self):
        self._timer.start(350)
        QTimer.singleShot(self.duration_ms, self.finish)

    def _tick(self):
        self._dots = (self._dots + 1) % 4
        self.label_sub.setText("Chargement" + "." * self._dots)

    def finish(self):
        self._timer.stop()
        self.close()
