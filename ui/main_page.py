from pathlib import Path
import os

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFormLayout,
    QHBoxLayout,
    QApplication,
    QFrame,
    QFileDialog,
    QSizePolicy,
    QSpacerItem,
    QMessageBox,
    QDialog,
    QTextBrowser,
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt

from config import load_config


class MainPage(QWidget):
    def __init__(self, navigate_to):
        super().__init__()
        self.navigate_to = navigate_to
        self.cfg = load_config()

        icon_path = (
            Path(__file__).resolve().parent.parent / "ressources" / "dd_icon.ico"
        )
        if icon_path.exists():
            QApplication.setWindowIcon(QIcon(str(icon_path)))
            self.setWindowIcon(QIcon(str(icon_path)))

        root_layout = QVBoxLayout()

        hdr = QLabel("Paramètres enregistrés")
        hdr_font = QFont()
        hdr_font.setPointSize(16)
        hdr_font.setBold(True)
        hdr.setFont(hdr_font)
        hdr.setAlignment(Qt.AlignCenter)

        center_frame = QFrame()
        center_frame.setFrameShape(QFrame.StyledPanel)
        center_frame.setMaximumWidth(700)
        center_frame.setStyleSheet(
            "background: #1f2326; border-radius: 8px; padding: 18px;"
        )
        center_layout = QVBoxLayout()
        center_layout.setSpacing(12)
        center_frame.setLayout(center_layout)

        center_layout.addWidget(hdr, alignment=Qt.AlignHCenter)
        center_layout.addStretch()

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignLeft)
        form.setFormAlignment(Qt.AlignCenter)

        badge_style = (
            "background: #2d6cdf; color: white; padding: 6px 10px; border-radius: 6px;"
            "font-weight: 600;"
        )
        kiss_path = Path(__file__).resolve().parent.parent / "ressources" / "kiss.png"
        kiss_pix = QPixmap(str(kiss_path))
        kiss_lbl = QLabel()
        if not kiss_pix.isNull():
            kiss_lbl.setPixmap(
                kiss_pix.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        label_att = QLabel("Attirer:")
        label_att.setStyleSheet("color: #d6d6d6; font-weight: 600;")
        lab_att_h = QHBoxLayout()
        lab_att_h.setContentsMargins(0, 0, 0, 0)
        lab_att_h.addWidget(kiss_lbl)
        lab_att_h.addWidget(label_att)
        lab_att_w = QWidget()
        lab_att_w.setLayout(lab_att_h)

        self.attract = QLabel(self.cfg.get("attract_shortcut", ""))
        self.attract.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.attract.setStyleSheet(badge_style)
        form.addRow(lab_att_w, self.attract)

        fart_path = Path(__file__).resolve().parent.parent / "ressources" / "fart.png"
        fart_pix = QPixmap(str(fart_path))
        fart_lbl = QLabel()
        if not fart_pix.isNull():
            fart_lbl.setPixmap(
                fart_pix.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        label_rep = QLabel("Éloigner:")
        label_rep.setStyleSheet("color: #d6d6d6; font-weight: 600;")
        lab_rep_h = QHBoxLayout()
        lab_rep_h.setContentsMargins(0, 0, 0, 0)
        lab_rep_h.addWidget(fart_lbl)
        lab_rep_h.addWidget(label_rep)
        lab_rep_w = QWidget()
        lab_rep_w.setLayout(lab_rep_h)

        self.repel = QLabel(self.cfg.get("repel_shortcut", ""))
        self.repel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.repel.setStyleSheet(badge_style)
        form.addRow(lab_rep_w, self.repel)

        label_tog = QLabel("Start/Stop script:")
        label_tog.setStyleSheet("color: #d6d6d6; font-weight: 600;")
        lab_tog_h = QHBoxLayout()
        lab_tog_h.setContentsMargins(0, 0, 0, 0)
        lab_tog_h.addWidget(label_tog)
        lab_tog_w = QWidget()
        lab_tog_w.setLayout(lab_tog_h)

        self.toggle = QLabel(self.cfg.get("toggle_shortcut", "nik"))
        self.toggle.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.toggle.setStyleSheet(badge_style)
        form.addRow(lab_tog_w, self.toggle)

        raw_path = (self.cfg.get("storage_path") or "").strip()
        if raw_path:
            try:
                abs_path = str(Path(raw_path).expanduser().resolve())
            except Exception:
                abs_path = raw_path
        else:
            abs_path = "(non défini)"

        label_path = QLabel("Chemin: ")
        label_path.setStyleSheet("color: #d6d6d6; font-weight: 600;")
        lab_path_h = QHBoxLayout()
        lab_path_h.setContentsMargins(0, 0, 0, 0)
        lab_path_h.addWidget(label_path)
        lab_path_w = QWidget()
        lab_path_w.setLayout(lab_path_h)

        self.path_lbl = QLabel(abs_path)
        self.path_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.path_lbl.setStyleSheet(
            badge_style + " font-family: 'Consolas', 'Courier New', monospace;"
        )
        self.path_lbl.setMinimumHeight(70)
        self.path_lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        form.addRow(lab_path_w, self.path_lbl)

        self._abs_path = abs_path

        center_layout.addLayout(form)

        center_layout.addStretch()

        actions_h = QHBoxLayout()
        actions_h.setSpacing(6)

        self.info_btn = QPushButton("?")
        self.info_btn.setFixedSize(60, 60)
        self.info_btn.setStyleSheet(
            "background: #2b2d31; color: #d6d6d6; border-radius: 20px; font-size: 24px;"
        )
        info_container = QWidget()
        info_layout = QHBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.addWidget(self.info_btn)
        info_container.setLayout(info_layout)
        actions_h.addWidget(info_container, alignment=Qt.AlignVCenter)

        self.generate_btn = QPushButton("Générer le script")
        self.generate_btn.setFixedWidth(220)
        actions_h.addWidget(self.generate_btn)

        actions_container = QWidget()
        actions_container.setLayout(actions_h)
        center_layout.addWidget(actions_container, alignment=Qt.AlignHCenter)

        center_layout.addStretch()

        self.back = QPushButton("Modifier les paramètres")
        self.back.setFixedWidth(300)
        center_layout.addWidget(self.back, alignment=Qt.AlignHCenter)

        root_layout.addItem(QSpacerItem(20, 40))
        root_layout.addWidget(center_frame, alignment=Qt.AlignHCenter)
        root_layout.addItem(QSpacerItem(20, 40))

        self.setLayout(root_layout)

        self.back.clicked.connect(lambda: self.navigate_to("settings"))

        self.generate_btn.clicked.connect(self._generate)
        self.info_btn.clicked.connect(lambda: InfoDialog(self).exec_())

    def refresh(self):
        self.cfg = load_config()
        self.attract.setText(self.cfg.get("attract_shortcut", ""))
        self.repel.setText(self.cfg.get("repel_shortcut", ""))
        self.toggle.setText(self.cfg.get("toggle_shortcut", ""))
        raw_path = (self.cfg.get("storage_path") or "").strip()
        if raw_path:
            try:
                abs_path = str(Path(raw_path).expanduser().resolve())
            except Exception:
                abs_path = raw_path
        else:
            abs_path = "(non défini)"
        self.path_lbl.setText(abs_path)
        self._abs_path = abs_path

    def _generate(self):
        cfg = load_config()
        a = cfg.get("attract_shortcut") or ""
        r = cfg.get("repel_shortcut") or ""
        t = cfg.get("toggle_shortcut") or ""
        if not a or not r or not t:
            QMessageBox.warning(
                self,
                "Validation",
                "Les trois raccourcis doivent être définis dans les paramètres.",
            )
            return
        path = cfg.get("storage_path") or ""
        if not path:
            dlg = QFileDialog()
            fp, _ = dlg.getSaveFileName(
                self, "Enregistrer le script", "script.txt", "Text Files (*.txt)"
            )
            if not fp:
                return
            out = fp
        else:
            p = Path(path)
            try:
                p.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                QMessageBox.warning(
                    self, "Erreur", f"Impossible de créer le dossier: {e}"
                )
                return
            out = str(p / "dragoturkey_script.akh")

        try:
            with open(out, "w", encoding="utf-8") as f:
                f.write("Toast(Message, Duration := 2000) {\n")
                f.write('    myGui := Gui("+AlwaysOnTop +ToolWindow -Caption")\n')
                f.write('    myGui.BackColor := "000000"\n')
                f.write('    myGui.SetFont("s16 cWhite", "Arial")\n')
                f.write('    myGui.Add("Text", , Message)\n')
                f.write("    x := A_ScreenWidth - 300\n")
                f.write('    myGui.Show("x" x " y20 w280 h50 NoActivate")\n')
                f.write("    SetTimer () => myGui.Destroy(), -Duration\n")
                f.write("}\n")
                f.write("\n")
                f.write('Toast("Script lancé", 2000)\n')
                f.write("\n")
                f.write("toggle := false\n")
                f.write("\n")
                f.write(f"{t}::\n")
                f.write("{\n")
                f.write("    global toggle\n")
                f.write("    toggle := !toggle\n")
                f.write("    if (toggle) {\n")
                f.write('        Toast("Macro activée", 2000)\n')
                f.write("        SetTimer MyLoop, 100\n")
                f.write("    } else {\n")
                f.write('        Toast("Macro désactivée", 2000)\n')
                f.write("        SetTimer MyLoop, 0\n")
                f.write("    }\n")
                f.write("}\n")
                f.write("\n")
                f.write("^F11::\n")
                f.write("{\n")
                f.write('    Toast("Script arrêté", 2000)\n')
                f.write("    Sleep 2000\n")
                f.write("    ExitApp\n")
                f.write("}\n")
                f.write("\n")
                f.write("MyLoop() {\n")
                f.write(f'    Send "{r}"\n')
                f.write("    Sleep 3500\n")
                f.write(f'    Send "{a}"\n')
                f.write("    Sleep 3500\n")
                f.write("}\n")

            dlg = QMessageBox(self)
            dlg.setWindowTitle("Génération terminée")
            dlg.setText(f"Fichier créé: {out}")
            dlg.setIcon(QMessageBox.Information)
            open_btn = dlg.addButton("Ouvrir le dossier", QMessageBox.ActionRole)
            dlg.addButton(QMessageBox.Ok)
            dlg.exec_()
            clicked = dlg.clickedButton()
            if clicked == open_btn:
                folder = os.path.dirname(out)
                try:
                    os.startfile(folder)
                except Exception:
                    try:
                        import subprocess

                        if os.name == "posix":
                            subprocess.run(["xdg-open", folder])
                        else:
                            subprocess.run(["open", folder])
                    except Exception:
                        QMessageBox.warning(
                            self, "Erreur", "Impossible d'ouvrir le dossier."
                        )
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Échec de l'écriture du fichier: {e}")


class InfoDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Information")
        self.setModal(True)
        self.resize(520, 320)

        layout = QVBoxLayout()

        txt = QTextBrowser()
        txt.setReadOnly(True)
        txt.setOpenExternalLinks(True)
        txt.setHtml(
            '<p>1) Download and install AutoHotkey from <a href="https://www.autohotkey.com">https://www.autohotkey.com.</a></p>'
            "<p>2) Launch the generated script by double-clicking it. An AutoHotkey icon should appear in your system tray.</p>"
            "<p>3) Use the shortcut you configured to start/stop the script.</p>"
            '<p>4) To totally shut down the script, use the shortcut "Ctrl + F11".</p>'
            "<p>5) Enjoy !</p>"
        )
        layout.addWidget(txt)

        btn = QPushButton("Close")
        btn.clicked.connect(self.accept)
        btn.setFixedWidth(120)
        btn_h = QHBoxLayout()
        btn_h.addStretch()
        btn_h.addWidget(btn)
        layout.addLayout(btn_h)

        self.setLayout(layout)
