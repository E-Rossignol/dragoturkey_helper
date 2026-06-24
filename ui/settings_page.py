"""Settings page for shortcut capture and script generation."""

from pathlib import Path

from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QHBoxLayout,
    QMessageBox,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPixmap

from config import load_config, save_config, set_first_run


class KeySequenceEdit(QLineEdit):
    """Capture a key combination and render it as a readable shortcut."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._sequence = ""
        self.setReadOnly(True)
        self.setAlignment(Qt.AlignCenter)
        self._recording = False
        self._prev_display = ""

    def focusInEvent(self, ev):
        self._prev_display = self.text()
        self._recording = True
        self.setText("")
        self.setStyleSheet("background-color: #2b2f33; color: #ffffff; border: 1px solid #4a90e2;")

    def focusOutEvent(self, ev):
        if self._recording:
            self._recording = False
            self.setText(self._prev_display)
            self.setStyleSheet("")
        super().focusOutEvent(ev)

    def keyPressEvent(self, event):
        mods = []
        m = event.modifiers()
        if m & Qt.ControlModifier:
            mods.append("Ctrl")
        if m & Qt.AltModifier:
            mods.append("Alt")
        if m & Qt.ShiftModifier:
            mods.append("Shift")
        if m & Qt.MetaModifier:
            mods.append("Meta")

        key = event.key()
        if key in (Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt, Qt.Key_Meta):
            return

        if key == Qt.Key_Escape:
            if self._recording:
                self._recording = False
                self.setText(self._prev_display)
                self.setStyleSheet("")
            try:
                self.clearFocus()
            except Exception:
                pass
            return

        raw_text = event.text()
        name = None
        if raw_text and ord(raw_text[0]) >= 32:
            name = raw_text.upper()
        else:
            if Qt.Key_A <= key <= Qt.Key_Z:
                name = chr(key)
            elif Qt.Key_0 <= key <= Qt.Key_9:
                name = chr(key)
            else:
                key_map = {
                    Qt.Key_Escape: "Esc",
                    Qt.Key_Tab: "Tab",
                    Qt.Key_Backspace: "Backspace",
                    Qt.Key_Return: "Enter",
                    Qt.Key_Enter: "Enter",
                    Qt.Key_Space: "Space",
                    Qt.Key_F1: "F1",
                    Qt.Key_F2: "F2",
                    Qt.Key_F3: "F3",
                    Qt.Key_F4: "F4",
                    Qt.Key_F5: "F5",
                    Qt.Key_F6: "F6",
                    Qt.Key_F7: "F7",
                    Qt.Key_F8: "F8",
                    Qt.Key_F9: "F9",
                    Qt.Key_F10: "F10",
                    Qt.Key_F11: "F11",
                    Qt.Key_F12: "F12",
                }
                name = key_map.get(key, "Key")

        if isinstance(name, str):
            name = name.upper()
        else:
            name = str(name)

        seq = "+".join(mods + [name])
        self._sequence = seq
        self.setText(seq)
        self._recording = False
        self.setStyleSheet("")

    def sequence(self) -> str:
        return self._sequence


class SettingsPage(QWidget):
    """Configure attract, repel, and toggle shortcuts plus the output path."""

    def __init__(self, navigate_to):
        super().__init__()
        self.navigate_to = navigate_to
        self.cfg = load_config()

        layout = QVBoxLayout()

        kiss_path = Path(__file__).resolve().parent.parent / "ressources" / "kiss.png"
        kiss_pix = QPixmap(str(kiss_path))
        kiss_lbl = QLabel()
        if not kiss_pix.isNull():
            kiss_lbl.setPixmap(kiss_pix.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label_att = QLabel("Attirer la monture:")
        label_att.setStyleSheet("font-weight: 600; color: #d6d6d6;")
        lab_att_h = QHBoxLayout()
        lab_att_h.setContentsMargins(0, 0, 0, 0)
        lab_att_h.addWidget(kiss_lbl)
        lab_att_h.addWidget(label_att)
        lab_att_w = QWidget()
        lab_att_w.setLayout(lab_att_h)

        self.attract_input = KeySequenceEdit()
        if self.cfg.get("attract_shortcut"):
            self.attract_input.setText(self.cfg.get("attract_shortcut"))
            self.attract_input._sequence = self.cfg.get("attract_shortcut")
        self.attract_input.setFixedWidth(300)
        att_row = QWidget()
        att_row_h = QHBoxLayout()
        att_row_h.setContentsMargins(0, 0, 0, 0)
        att_row_h.addWidget(lab_att_w)
        att_row_h.addStretch()
        att_row_h.addSpacing(20)
        att_row_h.addWidget(self.attract_input)
        att_row.setLayout(att_row_h)

        fart_path = Path(__file__).resolve().parent.parent / "ressources" / "fart.png"
        fart_pix = QPixmap(str(fart_path))
        fart_lbl = QLabel()
        if not fart_pix.isNull():
            fart_lbl.setPixmap(fart_pix.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label_rep = QLabel("Eloigner la monture:")
        label_rep.setStyleSheet("font-weight: 600; color: #d6d6d6;")
        lab_rep_h = QHBoxLayout()
        lab_rep_h.setContentsMargins(0, 0, 0, 0)
        lab_rep_h.addWidget(fart_lbl)
        lab_rep_h.addWidget(label_rep)
        lab_rep_w = QWidget()
        lab_rep_w.setLayout(lab_rep_h)

        self.repel_input = KeySequenceEdit()
        if self.cfg.get("repel_shortcut"):
            self.repel_input.setText(self.cfg.get("repel_shortcut"))
            self.repel_input._sequence = self.cfg.get("repel_shortcut")
        self.repel_input.setFixedWidth(300)
        rep_row = QWidget()
        rep_row_h = QHBoxLayout()
        rep_row_h.setContentsMargins(0, 0, 0, 0)
        rep_row_h.addWidget(lab_rep_w)
        rep_row_h.addStretch()
        rep_row_h.addSpacing(20)
        rep_row_h.addWidget(self.repel_input)
        rep_row.setLayout(rep_row_h)

        label_tog = QLabel("Start/Stop le script:")
        label_tog.setStyleSheet("font-weight: 600; color: #d6d6d6;")
        lab_tog_h = QHBoxLayout()
        lab_tog_h.setContentsMargins(0, 0, 0, 0)
        lab_tog_h.addWidget(label_tog)
        lab_tog_w = QWidget()
        lab_tog_w.setLayout(lab_tog_h)

        self.toggle_input = KeySequenceEdit()
        if self.cfg.get("toggle_shortcut"):
            self.toggle_input.setText(self.cfg.get("toggle_shortcut"))
            self.toggle_input._sequence = self.cfg.get("toggle_shortcut")
        self.toggle_input.setFixedWidth(300)
        tog_row = QWidget()
        tog_row_h = QHBoxLayout()
        tog_row_h.setContentsMargins(0, 0, 0, 0)
        tog_row_h.addWidget(lab_tog_w)
        tog_row_h.addStretch()
        tog_row_h.addSpacing(20)
        tog_row_h.addWidget(self.toggle_input)
        tog_row.setLayout(tog_row_h)

        layout.addStretch()
        layout.addWidget(att_row)
        layout.addStretch()
        layout.addWidget(rep_row)
        layout.addStretch()
        layout.addWidget(tog_row)
        layout.addStretch()

        self.validation_label = QLabel("")
        self.validation_label.setStyleSheet("color: #ff8080;")
        self.validation_label.setVisible(False)

        label_path = QLabel("Chemin du script:")
        label_path.setStyleSheet("font-weight: 600; color: #d6d6d6;")
        storage_row = QWidget()
        storage_h = QHBoxLayout()
        storage_h.setContentsMargins(0, 0, 0, 0)
        storage_h.addWidget(label_path)
        storage_h.addSpacing(20)
        self.storage_input = QLineEdit(self.cfg.get("storage_path", ""))
        self.storage_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.browse = QPushButton("Parcourir")
        self.browse.setFixedWidth(150)
        self.browse.clicked.connect(self._browse)
        storage_h.addWidget(self.storage_input, 1)
        storage_h.addWidget(self.browse)
        storage_row.setLayout(storage_h)
        layout.addWidget(storage_row)

        self.save_btn = QPushButton("Valider et enregistrer")
        layout.addStretch()
        layout.addWidget(self.validation_label)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        self.save_btn.clicked.connect(self._save)
        self.attract_input.textChanged.connect(lambda _: self._validate_shortcuts())
        self.repel_input.textChanged.connect(lambda _: self._validate_shortcuts())
        self.toggle_input.textChanged.connect(lambda _: self._validate_shortcuts())
        self._validate_shortcuts()

    def showEvent(self, event):
        super().showEvent(event)

        def _clear_focus():
            fw = QApplication.focusWidget()
            if fw is not None and self.isAncestorOf(fw):
                try:
                    fw.clearFocus()
                except Exception:
                    pass

        QTimer.singleShot(0, _clear_focus)

    def _browse(self):
        d = QFileDialog.getExistingDirectory(self, "Choisir dossier de stockage")
        if d:
            self.storage_input.setText(d)

    def _show_toast(self, text: str, timeout_ms: int = 1200):
        toast = QLabel(text)
        toast.setWindowFlags(Qt.ToolTip | Qt.WindowStaysOnTopHint)
        toast.setStyleSheet(
            "background: rgba(50,50,50,0.95); color: white; padding: 8px 12px; border-radius: 6px; font-weight: 600;"
        )
        toast.adjustSize()
        center = self.mapToGlobal(self.rect().center())
        x = center.x() - toast.width() // 2
        bottom = self.mapToGlobal(self.rect().bottomLeft()).y()
        y = bottom - toast.height() - 24
        toast.move(QPoint(x, y))
        toast.show()
        QTimer.singleShot(timeout_ms, toast.close)

    def _save(self):
        a = self.attract_input.sequence() or self.attract_input.text().strip()
        r = self.repel_input.sequence() or self.repel_input.text().strip()
        t = self.toggle_input.sequence() or self.toggle_input.text().strip()
        if not a or not r or not t:
            QMessageBox.warning(self, "Validation", "Tous les raccourcis doivent être définis.")
            return
        if a == r or a == t or r == t:
            QMessageBox.warning(self, "Validation", "Tous les raccourcis doivent être différents.")
            return
        self.cfg["attract_shortcut"] = a
        self.cfg["repel_shortcut"] = r
        self.cfg["toggle_shortcut"] = t
        self.cfg["storage_path"] = self.storage_input.text().strip()
        self.cfg["first_run"] = False
        save_config(self.cfg)
        set_first_run(False)
        self.navigate_to("main")

    def navigate_to(self, page_name):
        if page_name == "main":
            try:
                self.mainpage.refresh()
            except Exception:
                pass
        self.stacked_widget.setCurrentIndex(self.page_map[page_name])

    def _generate(self):
        a = self.attract_input.sequence() or self.attract_input.text().strip()
        r = self.repel_input.sequence() or self.repel_input.text().strip()
        if not a or not r:
            QMessageBox.warning(self, "Validation", "Les deux raccourcis doivent être définis.")
            return
        if a == r:
            QMessageBox.warning(self, "Validation", "Les deux raccourcis doivent être différents.")
            return

        storage = self.storage_input.text().strip()

        if not storage:
            dlg = QFileDialog()
            fp, _ = dlg.getSaveFileName(self, "Enregistrer le script", "script.txt", "Text Files (*.txt)")
            if not fp:
                return
            out = fp
        else:
            p = Path(storage)
            try:
                p.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Impossible de créer le dossier: {e}")
                return
            out = str(p / "generated_script.txt")

        try:
            with open(out, "w", encoding="utf-8") as f:
                f.write(f"Attract: {a}\n")
                f.write(f"Repel: {r}\n")
                f.write(f"Storage path: {storage or out}\n")
            QMessageBox.information(self, "Génération terminée", f"Fichier créé: {out}")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Échec de l'écriture du fichier: {e}")

    def _validate_shortcuts(self):
        a = self.attract_input.sequence() or self.attract_input.text().strip()
        r = self.repel_input.sequence() or self.repel_input.text().strip()
        t = self.toggle_input.sequence() or self.toggle_input.text().strip()
        if not a or not r or not t:
            self.validation_label.setText("Tous les raccourcis doivent être renseignés.")
            self.validation_label.setVisible(True)
            self.save_btn.setEnabled(False)
            return
        if a == r or a == t or r == t:
            self.validation_label.setText("Les raccourcis ne peuvent pas être identiques.")
            self.validation_label.setVisible(True)
            self.save_btn.setEnabled(False)
            return
        self.validation_label.setVisible(False)
        self.save_btn.setEnabled(True)


class RegeneratePage(QWidget):
    """Regenerate the script from the stored configuration."""

    def __init__(self, navigate_to):
        super().__init__()
        self.navigate_to = navigate_to
        self.cfg = load_config()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Regénérer le script à partir des paramètres enregistrés."))
        self.gen_btn = QPushButton("Générer maintenant")
        self.back = QPushButton("Retour menu")
        layout.addWidget(self.gen_btn)
        layout.addWidget(self.back)
        self.setLayout(layout)

        self.gen_btn.clicked.connect(self._generate)
        self.back.clicked.connect(lambda: self.navigate_to("menu"))

    def _generate(self):
        path = self.cfg.get("storage_path") or ""
        if not path:
            dlg = QFileDialog()
            fp, _ = dlg.getSaveFileName(self, "Enregistrer le script", "script.txt", "Text Files (*.txt)")
            if not fp:
                return
            out = fp
        else:
            p = Path(path)
            p.mkdir(parents=True, exist_ok=True)
            out = str(p / "generated_script.txt")

        with open(out, "w", encoding="utf-8") as f:
            f.write(f"Attract: {self.cfg.get('attract_shortcut')}\n")
            f.write(f"Repel: {self.cfg.get('repel_shortcut')}\n")
        self.navigate_to("menu")
