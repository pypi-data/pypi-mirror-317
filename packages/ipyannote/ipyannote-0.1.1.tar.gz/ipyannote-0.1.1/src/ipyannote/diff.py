from ipyannote import Waveform, Labels
from ipywidgets import VBox
from pyannote.core import Annotation

from pyannote.metrics.errors.identification import IdentificationErrorAnalysis
from pyannote.metrics.diarization import DiarizationErrorRate


class Diff(VBox):
    def __init__(self, audio: str, reference: Annotation, hypothesis: Annotation):
        _reference = Waveform(audio=audio)
        _hypothesis = Waveform(audio=audio)
        _common_labels = Labels()
        self._errors = Waveform(audio=audio)
        self._error_labels = Labels(
            {
            "false alarm": "#00ff00",
            "missed detection": "#ffa500",
            "confusion": "#ff0000",
            }
        )

        super().__init__(
            [_common_labels, _reference, _hypothesis, self._errors, self._error_labels]
        )

        _common_labels.sync(_reference)
        _reference.annotation = reference
        _common_labels.sync(_hypothesis)
        _hypothesis.sync_player(_reference)

        mapped_hypothesis = self.map_labels(reference, hypothesis)
        errors = self.diff(reference, mapped_hypothesis)

        _hypothesis.annotation = mapped_hypothesis
        self._error_labels.sync(self._errors)
        self._errors.annotation = errors.rename_tracks("string")
        self._errors.sync_player(_reference)

    def map_labels(self, reference, hypothesis):
        optimal_mapping = DiarizationErrorRate().optimal_mapping
        mapping = optimal_mapping(reference, hypothesis)
        print(mapping)
        mapped_hypothesis = hypothesis.rename_labels(mapping)
        return mapped_hypothesis

    def diff(self, reference, mapped_hypothesis) -> Annotation:
        errors: Annotation = IdentificationErrorAnalysis().difference(
            reference, mapped_hypothesis
        )
        mapping = {error: error[0] for error in errors.labels()}
        print(mapping)
        errors = errors.rename_labels(mapping).subset(["correct"], invert=True)
        return errors