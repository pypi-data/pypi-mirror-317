from typing import Callable, Optional

import anywidget

# import traitlets
from traitlets import Unicode, Float, Dict, List, Int, Bool

import numpy as np
import io
import base64
import scipy.io.wavfile
from pyannote.core import Annotation, Segment

import importlib.metadata
import pathlib

from ipywidgets import jslink
from .labels import Labels

try:
    __version__ = importlib.metadata.version("ipyannote")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


class Waveform(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "waveform.js"
    _css = pathlib.Path(__file__).parent / "static" / "waveform.css"

    # used to pass audio to the frontend
    audio_as_base64 = Unicode().tag(sync=True)

    # used to synchronize pool of labels
    labels = Dict(key_trait=Unicode(), value_trait=Unicode()).tag(sync=True)
    color_cycle = Int(0).tag(sync=True)
    active_label = Unicode(None, allow_none=True).tag(sync=True)

    # used to synchronize players
    current_time = Float(0.0).tag(sync=True)
    scroll_time = Float(0.0).tag(sync=True)
    zoom = Float().tag(sync=True)

    playing = Bool(False).tag(sync=True)

    # list of segments
    segments = List(
        Dict(
            per_key_traits={
                "start": Float(),
                "end": Float(),
                "label": Unicode(),
                "id": Unicode(),
                "active": Bool(),
            }
        )
    ).tag(sync=True)
    active_segment = Unicode(None, allow_none=True).tag(sync=True)

    def __init__(
        self,
        audio: Optional[str] = None,
        annotation: Optional[Annotation] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if audio is not None:
            self.audio = audio
        if annotation is not None:
            self.annotation = annotation

    @staticmethod
    def to_base64(waveform: np.ndarray, sample_rate: int) -> str:
        with io.BytesIO() as content:
            scipy.io.wavfile.write(content, sample_rate, waveform)
            content.seek(0)
            b64 = base64.b64encode(content.read()).decode()
            b64 = f"data:audio/x-wav;base64,{b64}"
        return b64

    @property
    def audio(self) -> str:
        raise NotImplementedError("This is a read-only property")

    @audio.setter
    def audio(self, audio: str):
        # reset annotation when audio changes
        del self.annotation

        sample_rate, waveform = scipy.io.wavfile.read(audio)
        waveform = waveform.astype(np.float32)
        waveform /= np.max(np.abs(waveform)) + 1e-8
        self.audio_as_base64 = self.to_base64(waveform, sample_rate)

    @audio.deleter
    def audio(self):
        # reset annotation when audio changes
        del self.annotation

        sample_rate = 16000
        waveform = np.zeros((sample_rate,), dtype=np.float32)
        self.audio_as_base64 = self.to_base64(waveform, sample_rate)

    @property
    def annotation(self) -> Annotation:
        annotation = Annotation()
        for region in self.segments:
            segment = Segment(region["start"], region["end"])
            annotation[segment, region["id"]] = region["label"]
        return annotation

    @annotation.setter
    def annotation(self, annotation: Annotation):
        # check that track IDs are unique strings
        segments, track_ids, labels = zip(*annotation.itertracks(yield_label=True))
        assert len(set(track_ids)) == len(track_ids), "Track IDs must be unique."
        assert all(
            isinstance(track_id, str) for track_id in track_ids
        ), "Track IDs must be strings."

        regions = []
        for segment, track_id, label in zip(segments, track_ids, labels):
            regions.append(
                {
                    "start": segment.start,
                    "end": segment.end,
                    "id": track_id,
                    "label": label,
                    "active": False,
                }
            )

        self.segments = regions

    @annotation.deleter
    def annotation(self):
        self.segments = []

    def _jslink(
        self,
        other: "Labels | Waveform",
        keys: list[str] = [],
    ) -> Callable:
        """Link attributes with other waveform

        Parameters
        ----------
        other : Waveform
            The other Waveform widget
        keys : list[str]
            List of attributes to link

        Returns
        -------
        unlink : Callable
            Function to unlink the attributes
        """
        unlinks = {key: jslink((self, key), (other, key)).unlink for key in keys}

        def unlink():
            for unlink in unlinks.values():
                unlink()

        return unlink

    def js_sync_player(self, other: "Waveform") -> Callable:
        return self._jslink(other, ["current_time", "zoom", "scroll_time"])

    def js_sync_labels(self, other: "Labels | Waveform") -> Callable:
        return self._jslink(other, ["labels", "color_cycle", "active_label"])
