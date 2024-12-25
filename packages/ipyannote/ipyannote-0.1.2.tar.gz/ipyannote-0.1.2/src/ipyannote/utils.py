from pyannote.core import Annotation, Segment

def load_rttm(file_rttm, keep_type="SPEAKER"):
    """Load RTTM file

    Parameter
    ---------
    file_rttm : `str`
        Path to RTTM file.
    keep_type : str, optional
        Only keep lines with this type (field #1 in RTTM specs).
        Defaults to "SPEAKER".

    Returns
    -------
    annotations : `dict`
        Speaker diarization as a {uri: pyannote.core.Annotation} dictionary.
    """

    annotations = dict()

    with open(file_rttm, 'r') as rttm:
        lines = rttm.readlines()
        for l, line in enumerate(lines):
            _, uri, _, start, duration, _, _, label, *_ = line.strip().split(' ')
            start = float(start)
            duration = float(duration)
            segment = Segment(float(start), float(start) + float(duration))
            annotations.setdefault(uri, Annotation(uri=uri))[segment, str(l)] = label
    
    return annotations
