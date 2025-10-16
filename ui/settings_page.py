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
from pathlib import Path


class KeySequenceEdit(QLineEdit):
    """A simple widget to capture a key sequence from the keyboard.

    User focuses the field and presses the desired combination. The widget
    displays a human readable representation like 'Ctrl+Shift+A'.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._sequence = ""
        self.setReadOnly(True)
        # center displayed sequence text
        self.setAlignment(Qt.AlignCenter)
        self._recording = False
        self._prev_display = ""

    def focusInEvent(self, ev):
        # show visual recording state when the widget gains focus
        self._prev_display = self.text()
        self._recording = True
        self.setText("")
        # subtle highlight
        self.setStyleSheet("background-color: #2b2f33; color: #ffffff; border: 1px solid #4a90e2;")
        # do not call base to keep readOnly behavior for key presses

    def focusOutEvent(self, ev):
        # restore previous display if no sequence was recorded
        if self._recording:
            # user left without pressing a combo
            self._recording = False
            # restore previous text
            self.setText(self._prev_display)
            self.setStyleSheet("")
        # call base handler
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
        # ignore pure modifier presses
        if key in (Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt, Qt.Key_Meta):
            return

        # If the user presses Escape while the widget is recording, cancel
        # the recording and remove focus so the field stops showing the
        # recording UI. If not recording, still clear focus to follow the
        # requested UX.
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

        # Prefer the printable text Qt provides, but when modifiers are
        # present event.text() can be empty. In that case map common
        # letter/digit keys from the key code so combos like Ctrl+P
        # show as "Ctrl+P" instead of "Ctrl+Key".
        raw_text = event.text()
        name = None
        if raw_text and ord(raw_text[0]) >= 32:
            name = raw_text.upper()
        else:
            # letters
            if Qt.Key_A <= key <= Qt.Key_Z:
                name = chr(key)
            # digits
            elif Qt.Key_0 <= key <= Qt.Key_9:
                name = chr(key)
            else:
                # for special keys, map some common ones
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
        # normalize to a string
        if isinstance(name, str):
            name = name.upper()
        else:
            name = str(name)

        parts = mods + [name]
        seq = "+".join(parts)
        self._sequence = seq
        # show the recorded sequence and clear recording visual
        self.setText(seq)
        self._recording = False
        self.setStyleSheet("")

    def sequence(self) -> str:
        return self._sequence


class SettingsPage(QWidget):
    """Page to set attract/repel shortcuts and storage path."""

    def __init__(self, navigate_to):
        super().__init__()
        self.navigate_to = navigate_to
        self.cfg = load_config()

        layout = QVBoxLayout()

        # We'll lay out each setting row separately so we can insert stretches
        # and distribute the four elements evenly.

        # Attract label with icon on the left
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
        # fixed width 100px, centered text; align to the right of the row with spacing
        self.attract_input.setFixedWidth(300)
        # create a row container: left label (with icon) + stretch + spacing(20) + fixed field
        att_row = QWidget()
        att_row_h = QHBoxLayout()
        att_row_h.setContentsMargins(0, 0, 0, 0)
        att_row_h.addWidget(lab_att_w)
        att_row_h.addStretch()
        att_row_h.addSpacing(20)
        att_row_h.addWidget(self.attract_input)
        att_row.setLayout(att_row_h)

        # Repel label with icon on the left
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
        # fixed width 100px and right-aligned in the row
        self.repel_input.setFixedWidth(300)
        # repel row
        rep_row = QWidget()
        rep_row_h = QHBoxLayout()
        rep_row_h.setContentsMargins(0, 0, 0, 0)
        rep_row_h.addWidget(lab_rep_w)
        rep_row_h.addStretch()
        rep_row_h.addSpacing(20)
        rep_row_h.addWidget(self.repel_input)
        rep_row.setLayout(rep_row_h)

        # Toggle label
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
        # fixed width 100px and right-aligned in the row
        self.toggle_input.setFixedWidth(300)
        # toggle row
        tog_row = QWidget()
        tog_row_h = QHBoxLayout()
        tog_row_h.setContentsMargins(0, 0, 0, 0)
        tog_row_h.addWidget(lab_tog_w)
        tog_row_h.addStretch()
        tog_row_h.addSpacing(20)
        tog_row_h.addWidget(self.toggle_input)
        tog_row.setLayout(tog_row_h)

        # Now add the four rows to the main vertical layout with stretches between
        layout.addStretch()
        layout.addWidget(att_row)
        layout.addStretch()
        layout.addWidget(rep_row)
        layout.addStretch()
        layout.addWidget(tog_row)
        layout.addStretch()

        # Inline validation label (hidden unless error)
        self.validation_label = QLabel("")
        self.validation_label.setStyleSheet("color: #ff8080;")
        self.validation_label.setVisible(False)
        # validation_label will be placed above the save button (bottom)

        # storage row (fourth element)
        label_path = QLabel("Chemin du script:")
        label_path.setStyleSheet("font-weight: 600; color: #d6d6d6;")
        storage_row = QWidget()
        storage_h = QHBoxLayout()
        storage_h.setContentsMargins(0, 0, 0, 0)
        storage_h.addWidget(label_path)
        storage_h.addSpacing(20)
        # storage field expands but leave room for the fixed "Parcourir" button
        self.storage_input = QLineEdit(self.cfg.get("storage_path", ""))
        self.storage_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.browse = QPushButton("Parcourir")
        self.browse.setFixedWidth(150)
        self.browse.clicked.connect(self._browse)
        storage_h.addWidget(self.storage_input, 1)
        storage_h.addWidget(self.browse)
        storage_row.setLayout(storage_h)
        layout.addWidget(storage_row)

        # Action buttons
        self.save_btn = QPushButton("Valider et enregistrer")
        # push validation label and save button to bottom
        layout.addStretch()
        layout.addWidget(self.validation_label)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        self.save_btn.clicked.connect(self._save)

        # connect live validation for all three shortcut fields
        self.attract_input.textChanged.connect(lambda _: self._validate_shortcuts())
        self.repel_input.textChanged.connect(lambda _: self._validate_shortcuts())
        self.toggle_input.textChanged.connect(lambda _: self._validate_shortcuts())
        # initial validation state
        self._validate_shortcuts()

    def showEvent(self, event):
        """Clear focus from any child widget when the page becomes visible.

        This prevents a shortcut input from being pre-focused when the
        user navigates to the Settings page.
        """
        super().showEvent(event)
        # Clear focus after the event loop returns. Sometimes Qt will
        # move focus to a child after showEvent, so doing this with a
        # singleShot(0) ensures we clear focus last.
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

    # simple transient toast shown near bottom-center of the settings page
    def _show_toast(self, text: str, timeout_ms: int = 1200):
        toast = QLabel(text)
        toast.setWindowFlags(Qt.ToolTip | Qt.WindowStaysOnTopHint)
        toast.setStyleSheet(
            "background: rgba(50,50,50,0.95); color: white; padding: 8px 12px; border-radius: 6px; font-weight: 600;"
        )
        toast.adjustSize()
        # position at bottom-center of the widget, slightly above the bottom edge
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
        # after saving go to main page
        self.navigate_to("main")

    def navigate_to(self, page_name):
        """Navigate to a different page in the application."""
        if page_name == "main":
            # call refresh so MainPage displays the latest saved values
            try:
                self.mainpage.refresh()
            except Exception:
                pass
        # then switch page
        self.stacked_widget.setCurrentIndex(self.page_map[page_name])

    def _generate(self):
        """Generate a text file containing the current inputs at the user-specified path."""
        a = self.attract_input.sequence() or self.attract_input.text().strip()
        r = self.repel_input.sequence() or self.repel_input.text().strip()
        if not a or not r:
            QMessageBox.warning(self, "Validation", "Les deux raccourcis doivent être définis.")
            return
        if a == r:
            QMessageBox.warning(self, "Validation", "Les deux raccourcis doivent être différents.")
            return

        storage = self.storage_input.text().strip()

        # determine output path
        if not storage:
            # ask user for a file path
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
        # OK
        self.validation_label.setVisible(False)
        self.save_btn.setEnabled(True)


class RegeneratePage(QWidget):
    """Simple page that will create the script file using config values."""

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
        # create a simple text file in storage_path
        path = self.cfg.get("storage_path") or ""
        if not path:
            # ask user
            dlg = QFileDialog()
            fp, _ = dlg.getSaveFileName(self, "Enregistrer le script", "script.txt", "Text Files (*.txt)")
            if not fp:
                return
            out = fp
        else:
            from pathlib import Path

            p = Path(path)
            p.mkdir(parents=True, exist_ok=True)
            out = str(p / "generated_script.txt")

        with open(out, "w", encoding="utf-8") as f:
            f.write(f"Attract: {self.cfg.get('attract_shortcut')}\n")
            f.write(f"Repel: {self.cfg.get('repel_shortcut')}\n")
        # go back to menu
        self.navigate_to("menu")
