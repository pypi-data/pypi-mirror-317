from PyQt6.QtGui import QPalette, QIcon
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QSpinBox,
    QPushButton,
    QComboBox,
)
from .metrognome_logic import MetrognomeLogic
from .audio_manager import AudioManager, Sound


class MetrognomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MetroGnome")

        self.highlight_color = self.palette().color(QPalette.ColorRole.Highlight).name()
        self.highlighted_text_color = (
            self.palette().color(QPalette.ColorRole.HighlightedText).name()
        )

        self.logic = MetrognomeLogic()
        self.audio_manager = AudioManager()
        self.logic.beatSound.connect(self.audio_manager.play_sound_by_name)
        self.logic.beatIndex.connect(self.highlight_current_beat)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout()
        central_widget.setLayout(self.main_layout)

        self.bpm_spin = QSpinBox()
        self.bpm_spin.setRange(40, 300)
        self.bpm_spin.setValue(120)

        self.numerator_spin = QSpinBox()
        self.numerator_spin.setRange(1, 16)
        self.numerator_spin.setValue(4)

        self.denominator_spin = QSpinBox()
        self.denominator_spin.setRange(1, 16)
        self.denominator_spin.setValue(4)

        form_layout = QFormLayout()
        form_layout.addRow("BPM:", self.bpm_spin)
        form_layout.addRow("Numerator:", self.numerator_spin)
        form_layout.addRow("Denominator:", self.denominator_spin)
        self.main_layout.addLayout(form_layout)

        # Single toggle button
        self.toggle_btn = QPushButton("Start")
        self.main_layout.addWidget(self.toggle_btn)

        # Layout for beat comboboxes
        self.beats_layout = QHBoxLayout()
        self.main_layout.addLayout(self.beats_layout)

        self.bpm_spin.valueChanged.connect(self.update_bpm)
        self.numerator_spin.valueChanged.connect(self.time_signature_changed)
        self.denominator_spin.valueChanged.connect(self.time_signature_changed)
        self.toggle_btn.clicked.connect(self.toggle_metronome)

        self.update_bpm()
        self.time_signature_changed()

    def highlight_current_beat(self, current_idx: int):
        """
        Called each time a beat fires.
        We'll highlight the corresponding combo box and reset others.
        """

        for i, combo in enumerate(self.beat_combos):
            if i == current_idx:
                combo.setStyleSheet(
                    f"background-color: {self.highlight_color}; color: {self.highlighted_text_color};"
                )
            else:
                combo.setStyleSheet("")

    def update_bpm(self):
        self.logic.set_bpm(self.bpm_spin.value())

    def time_signature_changed(self):
        n = self.numerator_spin.value()
        d = self.denominator_spin.value()
        self.logic.set_time_signature(n, d)

        # Rebuild comboboxes
        while self.beats_layout.count():
            item = self.beats_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.beat_combos = []
        for i in range(n):
            combo = QComboBox()
            [combo.addItem(s.name.capitalize()) for s in Sound]
            combo.currentTextChanged.connect(
                lambda sound_name, idx=i: self.logic.set_beat_sound(
                    idx, Sound[sound_name.upper()]
                )
            )
            self.beats_layout.addWidget(combo)
            self.beat_combos.append(combo)

    def toggle_metronome(self):
        if self.logic.is_running():
            self.logic.stop()
            self.toggle_btn.setText("Start")
        else:
            self.logic.start()
            self.toggle_btn.setText("Stop")
