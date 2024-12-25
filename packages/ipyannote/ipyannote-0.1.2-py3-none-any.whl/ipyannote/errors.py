from ipyannote import Waveform, Labels
from ipywidgets import VBox
from pyannote.core import Annotation

from pyannote.metrics.errors.identification import IdentificationErrorAnalysis
from pyannote.metrics.diarization import DiarizationErrorRate


class Errors(VBox):
    def __init__(self, audio: str, reference: Annotation, hypothesis: Annotation):

        # create reference and hypothesis waveforms
        self.reference = Waveform(audio=audio)
        self.hypothesis = Waveform(audio=audio)
        # and their common speaker pool
        self.speaker_labels = Labels()

        # create error waveform
        self.errors = Waveform(audio=audio)
        # and the three types of errors
        self.error_labels = Labels(
            {
                "false alarm": "#00ff00",
                "missed detection": "#ffa500",
                "confusion": "#ff0000",
            }
        )

        super().__init__(
            [
                self.speaker_labels,
                self.reference,
                self.hypothesis,
                self.errors,
                self.error_labels,
            ]
        )

        # synchronize players
        self.hypothesis.js_sync_player(self.reference)
        self.errors.js_sync_player(self.reference)

        # synchronize speaker pools
        self.speaker_labels.sync(self.reference)
        self.speaker_labels.sync(self.hypothesis)

        # map hypothesis labels to reference labels
        self.reference.annotation = reference
        _hypothesis = self._match_speakers(reference, hypothesis)
        self.hypothesis.annotation = _hypothesis

        # compute errors
        errors = self._compute_errors(reference, _hypothesis)
        self.error_labels.sync(self.errors)
        self.errors.annotation = errors.rename_tracks("string")

    def _match_speakers(self, reference, hypothesis):
        mapping = {label: f"@{label}" for label in hypothesis.labels()}
        hypothesis = hypothesis.rename_labels(mapping)

        optimal_mapping = DiarizationErrorRate().optimal_mapping
        mapping = optimal_mapping(reference, hypothesis)
        mapped_hypothesis = hypothesis.rename_labels(mapping)
        return mapped_hypothesis

    def _compute_errors(self, reference, mapped_hypothesis) -> Annotation:
        errors: Annotation = IdentificationErrorAnalysis().difference(reference, mapped_hypothesis)
        # only keep error types
        mapping = {error: error[0] for error in errors.labels()}
        errors = errors.rename_labels(mapping).subset(["correct"], invert=True)
        return errors
