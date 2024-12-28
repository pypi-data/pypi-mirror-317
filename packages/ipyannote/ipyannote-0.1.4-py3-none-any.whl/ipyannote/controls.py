
import anywidget

from traitlets import Bool, Float


import importlib.metadata
import pathlib

from ipywidgets import jslink

try:
    __version__ = importlib.metadata.version("ipyannote")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


class Controls(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "controls.js"
    _css = pathlib.Path(__file__).parent / "static" / "controls.css"

    current_time = Float(0.0).tag(sync=True)
    playing = Bool(False).tag(sync=True)

    def sync(self, waveform: "Waveform"): # type: ignore
        keys = ["playing", "current_time"]
        unlinks = {key: jslink((self, key), (waveform, key)).unlink for key in keys}

        def unlink():
            for unlink in unlinks.values():
                unlink()

        return unlink

