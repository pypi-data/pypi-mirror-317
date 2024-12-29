from importlib.resources import files
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QSoundEffect
from enum import Enum


class Sound(Enum):
    BEEP = "beep.wav"
    CLICK = "click.wav"
    SNARE = "snare.wav"
    KICK = "kick.wav"


class AudioManager:
    """Loads and plays sound files for the Metrognome."""

    def __init__(self):
        self._player = QSoundEffect()
        self._player.setVolume(1.0)

    def play_sound_by_name(self, sound: Sound):
        path = str(files("metrognome.resources") / sound.value)
        self._player.stop()
        self._player.setSource(QUrl.fromLocalFile(path))
        self._player.play()
