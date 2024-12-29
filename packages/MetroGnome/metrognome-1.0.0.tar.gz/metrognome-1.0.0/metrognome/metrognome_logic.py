from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from .audio_manager import Sound


class MetrognomeLogic(QObject):
    beatSound = pyqtSignal(Sound)
    beatIndex = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._bpm = 120
        self._numerator = 4
        self._denominator = 4
        self._timer = QTimer()
        self._timer.timeout.connect(self._on_tick)
        self._beat_sounds = [Sound.BEEP] * 4
        self._current_beat_index = 0

    def set_bpm(self, bpm: int):
        self._bpm = bpm
        if self._timer.isActive():
            self._restart_timer()

    def set_time_signature(self, numerator: int, denominator: int):
        self._numerator = numerator
        self._denominator = denominator
        self._current_beat_index = 0
        self._ensure_beat_sounds_length()
        if self._timer.isActive():
            self._restart_timer()

    def set_beat_sound(self, beat_index: int, sound: Sound):
        if 0 <= beat_index < len(self._beat_sounds):
            self._beat_sounds[beat_index] = sound

    def start(self):
        if not self._timer.isActive():
            self._restart_timer()

    def stop(self):
        if self._timer.isActive():
            self._timer.stop()
        self._current_beat_index = 0

    def is_running(self):
        return self._timer.isActive()

    def _on_tick(self):
        sound_to_play = self._beat_sounds[self._current_beat_index]
        self.beatSound.emit(sound_to_play)
        self.beatIndex.emit(self._current_beat_index)
        self._current_beat_index += 1
        if self._current_beat_index >= self._numerator:
            self._current_beat_index = 0

    def _restart_timer(self):
        beat_duration_s = (60.0 / self._bpm) * (4.0 / self._denominator)
        interval_ms = int(beat_duration_s * 1000)
        self._timer.setInterval(interval_ms)
        self._timer.start()

    def _ensure_beat_sounds_length(self):
        if len(self._beat_sounds) < self._numerator:
            self._beat_sounds += [Sound.BEEP] * (
                self._numerator - len(self._beat_sounds)
            )
        else:
            self._beat_sounds = self._beat_sounds[: self._numerator]
