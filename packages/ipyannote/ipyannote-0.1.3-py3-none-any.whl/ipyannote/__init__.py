from ipywidgets import VBox
from pyannote.core import Annotation

from .waveform import Waveform
from .labels import Labels
from .errors import Errors

class IPyannote(VBox):

    def __init__(self, audio: str, annotation: Annotation):
        self._waveform = Waveform(audio=audio, annotation=annotation)
        self._labels = Labels()
        self._labels.sync(self._waveform)
        super().__init__([self._waveform, self._labels])

    @property
    def annotation(self) -> Annotation:
        return self._waveform.annotation

    @annotation.setter
    def annotation(self, annotation: Annotation):
        self._waveform.annotation = annotation

    @annotation.deleter
    def annotation(self):
        del self._waveform.annotation


__all__ = ["Labels", "Waveform", "IPyannote", "Errors"]
