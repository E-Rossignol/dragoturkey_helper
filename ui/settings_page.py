from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QHBoxLayout,
    QFormLayout,
    QSlider,
    QDoubleSpinBox,
    QMessageBox,
)
from PyQt5.QtCore import Qt, QTimer
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
    """Page to set attract/repel shortcuts, delay and storage path."""

    def __init__(self, navigate_to):
        super().__init__()
        self.navigate_to = navigate_to
        self.cfg = load_config()

        layout = QVBoxLayout()

        # Shortcuts form: icon before the left label, inputs on the right
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignLeft)

        # Attract label with icon on the left
        kiss_path = Path(__file__).resolve().parent.parent / "ressources" / "kiss.png"
        kiss_pix = QPixmap(str(kiss_path))
        kiss_lbl = QLabel()
        if not kiss_pix.isNull():
            kiss_lbl.setPixmap(kiss_pix.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label_att = QLabel("Attirer la monture")
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

        form.addRow(lab_att_w, self.attract_input)

        # Repel label with icon on the left
        fart_path = Path(__file__).resolve().parent.parent / "ressources" / "fart.png"
        fart_pix = QPixmap(str(fart_path))
        fart_lbl = QLabel()
        if not fart_pix.isNull():
            fart_lbl.setPixmap(fart_pix.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label_rep = QLabel("Eloigner la monture")
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

        form.addRow(lab_rep_w, self.repel_input)

        # Toggle label
        label_tog = QLabel("Start/Stop le script")
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

        form.addRow(lab_tog_w, self.toggle_input)

        layout.addLayout(form)

        # Inline validation label (hidden unless error)
        self.validation_label = QLabel("")
        self.validation_label.setStyleSheet("color: #ff8080;")
        self.validation_label.setVisible(False)
        layout.addWidget(self.validation_label)

        # Delay selection (2.0 - 10.0 seconds) with 0.5s steps
        layout.addWidget(QLabel("Délai (secondes):"))
        h = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        # slider operates in half-second steps by scaling values * 2
        self.slider.setMinimum(int(2 * 2))  # corresponds to 2.0s
        self.slider.setMaximum(int(10 * 2))  # corresponds to 10.0s
        # use 4.0s as the default if no saved config exists (user request)
        initial_delay = float(self.cfg.get("delay_seconds", 4.0))
        self.slider.setValue(int(initial_delay * 2))
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.delay_label = QLabel(f"{initial_delay:.1f}")

        # double spinbox for 0.5s precision
        self.spin = QDoubleSpinBox()
        self.spin.setRange(2.0, 10.0)
        self.spin.setSingleStep(0.5)
        self.spin.setDecimals(1)
        self.spin.setValue(initial_delay)

        # sync slider and spinbox (slider value is int representing half-seconds)
        def _slider_changed(v):
            val = v / 2.0
            self.delay_label.setText(f"{val:.1f}")
            if abs(self.spin.value() - val) > 1e-6:
                self.spin.setValue(val)

        def _spin_changed(v):
            intv = int(round(v * 2))
            if self.slider.value() != intv:
                self.slider.setValue(intv)
            self.delay_label.setText(f"{v:.1f}")

        self.slider.valueChanged.connect(_slider_changed)
        self.spin.valueChanged.connect(_spin_changed)
        h.addWidget(self.slider)
        h.addWidget(self.spin)
        layout.addLayout(h)

        # Storage path
        layout.addWidget(QLabel("Chemin pour stocker le script:"))
        sp_h = QHBoxLayout()
        self.storage_input = QLineEdit(self.cfg.get("storage_path", ""))
        self.browse = QPushButton("Parcourir")
        self.browse.clicked.connect(self._browse)
        sp_h.addWidget(self.storage_input)
        sp_h.addWidget(self.browse)
        layout.addLayout(sp_h)

        # Action buttons
        self.save_btn = QPushButton("Valider et enregistrer")
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        self.save_btn.clicked.connect(self._save)

        # connect live validation for shortcuts
        self.attract_input.textChanged.connect(lambda _: self._validate_shortcuts())
        self.repel_input.textChanged.connect(lambda _: self._validate_shortcuts())
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
        # store delay as float (seconds)
        self.cfg["delay_seconds"] = float(self.spin.value())
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

        delay = float(self.spin.value())
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
                f.write(f"Delay: {delay}\n")
                f.write(f"Storage path: {storage or out}\n")
            QMessageBox.information(self, "Génération terminée", f"Fichier créé: {out}")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Échec de l'écriture du fichier: {e}")

    def _validate_shortcuts(self):
        a = self.attract_input.sequence() or self.attract_input.text().strip()
        r = self.repel_input.sequence() or self.repel_input.text().strip()
        if not a or not r:
            self.validation_label.setText("Les deux raccourcis doivent être renseignés.")
            self.validation_label.setVisible(True)
            self.save_btn.setEnabled(False)
            return
        if a == r:
            self.validation_label.setText("Les deux raccourcis ne peuvent pas être identiques.")
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
            f.write(f"Delay: {self.cfg.get('delay_seconds')}\n")
        # go back to menu
        self.navigate_to("menu")
