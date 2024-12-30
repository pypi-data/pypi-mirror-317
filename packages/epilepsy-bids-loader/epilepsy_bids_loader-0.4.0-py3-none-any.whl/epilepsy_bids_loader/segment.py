import numpy as np
from typing import Any, List

from epilepsy_bids_loader import Run, Segment, BIDSLoader


def get_segment_stats(
    args: dict,
    carry: List[float],
    **kwargs
):
    run_data: Run = args["run_data"]
    seg_sizes = [
        seg.size
        for seg in run_data.segments_test
    ]
    return carry + seg_sizes


def fixed_segmentation(
    args: dict,
    carry: Any,
    loader: BIDSLoader,
    win_size: int,
    stride: int,
    train: bool = True,
    dev: bool = True,
    test: bool = True,
    **kwargs
):
    sub = args["sub"]
    ses = args["ses"]
    run = args["run"]
    run_data: Run = args["run_data"]
    N, C, L = run_data.x.shape
    segments = [
        Segment(
            smin=i,
            smax=i + win_size,
            subject=sub,
            session=ses,
            run=run,
            loader=loader
        )
        for i in np.arange(0, (L - win_size), stride)
    ]

    if train:
        run_data.segments_train = segments

    if dev:
        run_data.segments_dev = segments

    if test:
        run_data.segments_test = segments

    return
