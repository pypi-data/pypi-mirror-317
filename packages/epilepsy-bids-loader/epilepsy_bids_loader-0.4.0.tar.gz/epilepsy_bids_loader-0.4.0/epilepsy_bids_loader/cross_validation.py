import torch
from torch import Tensor
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from typing import Tuple, List, Dict, Literal, Generator, Callable

from epilepsy_bids_loader import Segment
from epilepsy_bids_loader import Status, ZScoreScaler
from epilepsy_bids_loader import batch_segments_with_prefetch


@dataclass
class CVFold:
    train: List[Segment]
    dev: List[Segment]
    test: List[Segment]


@dataclass
class TestBatch:
    run: str
    ref: Path
    date_time: datetime
    duration: float
    segments: List[Segment] = field(default_factory=list)
    batches: Generator[Tuple[Tensor, Tensor, Tensor], None, None] = None

    def __len__(self):
        return len(self.batches)

    def __iter__(self):
        return iter(self.batches)

    def close(self):
        return self.batches.close()

    def append_segment(self, seg: Segment):
        self.segments.append(seg)
        return

    def create_batches(
        self,
        batch_size: int,
        prefetch: int
    ):
        self.batches = batch_segments_with_prefetch(
            segments=self.segments,
            batch_size=batch_size,
            select="first",
            prefetch=prefetch
        )
        return


@dataclass
class CrossValidation:
    method: Literal["subject_specific", "subject_independent"]
    folds: List[CVFold] = field(default_factory=list)

    def __len__(self):
        return len(self.folds)

    def append(self, fold: CVFold):
        self.folds.append(fold)
        return

    def _train_batch_default(
        self,
        fold: int,
        batch_size: int,
        prefetch: int,
        **kwargs
    ) -> Generator[Tuple[Tensor, Tensor, Tensor], None, None]:
        """
        Standard training batching process
        - Use all bckg, repeat sz, randomise
        """
        from random import sample
        segments: List[Segment] = self.folds[fold].train

        # Balanced selection of sz and bckg segments
        sz_segs = [
            seg for seg in segments
            if seg.label() == 1
        ]
        bckg_segs = [
            seg for seg in segments
            if seg.label() == 0
        ]
        segments = (
            bckg_segs
            + sz_segs * (len(bckg_segs) // len(sz_segs))
        )

        # Randomise
        segments = sample(segments, k=len(segments))

        batches = batch_segments_with_prefetch(
            segments=segments,
            batch_size=batch_size,
            select="random",
            prefetch=prefetch
        )
        return batches

    def train_batch(
        self,
        fold: int,
        method: Literal["default"],
        batch_size: int,
        prefetch: int = 10,
        **kwargs
    ) -> Generator[Tuple[Tensor, Tensor, Tensor], None, None]:
        """
        Generates batches of training samples.
        - Override this method to extend functionality.
        - Supports prefetching.

        Args:
            fold (int): The cross validation fold number.
            method (str): Batching method to use.
            batch_size (int): Size of the N dimension.
            prefetch (int, optional): Number of batches to prefetch.
                Defaults to 10.

        Yields:
            Generator[Tuple[Tensor, Tensor, Tensor], None, None]:
            - x: (N, C, L)
            - y: (N,)
            - t: (N,)
        """
        _batch_fn = {
            "default": self._train_batch_default,
            # TODO Extend options here as needed
        }[method]
        return _batch_fn(
            fold=fold,
            batch_size=batch_size,
            prefetch=prefetch,
            **kwargs
        )

    def test_batch_by_run(
        self,
        fold: int,
        batch_size: int,
        ds_type: Literal["dev", "test"],
        prefetch: int = 10,
    ) -> Dict[Tuple[str, str, str], TestBatch]:
        """
        Generates batches of test samples grouped by run.
        - Supports prefetching.

        Args:
            fold (int): The cross validation fold number.
            batch_size (int): Size of the N dimension.
            ds_type (str): Retrieve samples from either "dev" or "test" sets.
            prefetch (int, optional): Number of batches to prefetch.
                Defaults to 10.

        Returns:
            Dict[Tuple[str, str, str], TestBatch]:
            - Keys for run as (sub, ses, run)
            - TestBatch yields:
                - x: (N, C, L)
                - y: (N,)
                - t: (N,)
        """
        segments: List[Segment] = getattr(self.folds[fold], ds_type)

        # Organise segments by run
        batches: Dict[str, TestBatch] = {}
        for seg in segments:
            sub = seg.subject
            ses = seg.session
            run = seg.run
            key = (sub, ses, run)
            if key not in batches:
                run_meta = seg.run_meta()
                batches[key] = TestBatch(
                    run=run,
                    ref=run_meta["ref"],
                    date_time=run_meta["date_time"],
                    duration=run_meta["duration"]
                )
            batches[(sub, ses, run)].append_segment(seg)

        # Create batched data by run
        for test_batch in batches.values():
            test_batch.create_batches(
                batch_size=batch_size,
                prefetch=prefetch
            )
        return batches

    def fit_scaler(
        self,
        fold: int
    ) -> ZScoreScaler:
        """
        Fits a ZScoreScaler on the training data of a particular fold.

        Args:
            fold (int): The cross validation fold number.

        Returns:
            ZScoreScaler: The fitted scaler.
        """
        status = Status("[loader] fitting z-score scaler on training data")
        x = torch.concatenate(
            [
                seg.data("all")[0] # (1, C, L)
                for seg in self.folds[fold].train
            ],
            axis=2
        ) # (1, C, L+)
        scaler = ZScoreScaler()
        scaler.fit(x)
        status.done()
        return scaler