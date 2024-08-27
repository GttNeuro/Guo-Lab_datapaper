from __future__ import annotations

import logging
from typing import Optional

from heudiconv.utils import SeqInfo

lgr = logging.getLogger("heudiconv")


def create_key(
    template: Optional[str],
    outtype: tuple[str, ...] = ("nii.gz",),
    annotation_classes: None = None,
) -> tuple[str, tuple[str, ...], None]:
    if template is None or not template:
        raise ValueError("Template must be a valid format string")
    return (template, outtype, annotation_classes)


def infotodict(
    seqinfo: list[SeqInfo],
) -> dict[tuple[str, tuple[str, ...], None], list[str]]:
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    t1w = create_key('sub-{subject}/anat/sub-{subject}_T1w') 
    LanguageControl = create_key('sub-{subject}/func/sub-{subject}_task-LanguageControl_run-{item:02d}_bold') 
    CognitiveControl = create_key('sub-{subject}/func/sub-{subject}_task-CognitiveControl_run-{item:02d}_bold') 
    info = {t1w: [], LanguageControl: [], CognitiveControl: []}
    last_run = len(seqinfo)

    for s in seqinfo:
        """
        The namedtuple `s` contains the following fields:

        * total_files_till_now
        * example_dcm_file
        * series_id
        * dcm_dir_name
        * unspecified2
        * unspecified3
        * dim1
        * dim2
        * dim3
        * dim4
        * TR
        * TE
        * protocol_name
        * is_motion_corrected
        * is_derived
        * patient_id
        * study_description
        * referring_physician_name
        * series_description
        * image_type
        """

        if (s.dim3 == 144) and ('T1' in s.dcm_dir_name):
            info[t1w].append(s.series_id)
        if (s.dim3 == 33) and ('LanguageControl' in s.dcm_dir_name):
            info[LanguageControl].append(s.series_id)
        if (s.dim3 == 33) and ('CognitiveControl' in s.dcm_dir_name):
            info[CognitiveControl].append(s.series_id)
    return info
