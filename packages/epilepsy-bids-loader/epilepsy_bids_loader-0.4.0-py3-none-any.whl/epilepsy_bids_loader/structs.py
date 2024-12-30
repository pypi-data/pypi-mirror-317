from numpy import ndarray
from torch import Tensor
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from collections import OrderedDict
from typing import Tuple, List, Any, Literal, Callable, Generator
from epilepsy_bids_loader.utils import Status


@dataclass
class Segment:
    smin: int
    smax: int
    subject: str
    session: str
    run: str
    loader: Any

    @property
    def size(self):
        return self.smax - self.smin

    def run_meta(self) -> Path:
        run_data: Run = self.loader.data[self.subject][self.session][self.run]
        return {
            "ref": run_data.files.tsv,
            "date_time": run_data.datetime_start_og,
            "duration": run_data.duration
        }

    def label(self):
        run_data: Run = self.loader.data[self.subject][self.session][self.run]
        y = run_data.y[self.smin : self.smax]
        y = 1 if y.any() else 0
        return y

    def time(self):
        run_data: Run = self.loader.data[self.subject][self.session][self.run]
        t = run_data.t[self.smin]
        return t

    def data(
        self,
        select: Literal["all", "random", "first"] = "all",
        overlap: float = 0.5
    ) -> Tuple[ndarray, ndarray, ndarray]:
        """
        Gets data from a segment.

        Args:
            usage (all, random, first, optional): Defaults to "all". When "all",
                returns all of the segment data. When "random", randomly
                select a window from the segment, that can extend beyond the
                segment boundaries by the overlap amount. When "first", select
                the first window of each segment.
            overlap (float, optional): The amount of overlap allowed with
                neighbouring segments as a scalar [0, 1]. Defaults to 0.5.

        Returns:
            Tuple[ndarray, ndarray, ndarray]:
            - x (1, C, L): signal data
            - y (L,): label at each sample
            - t (L,): time (secs) since start of data at each sample
        """
        run_data: Run = self.loader.data[self.subject][self.session][self.run]
        win_size = self.loader.win_size
        x_start = 0
        x_end = run_data.x.shape[2]
        overlap = int(win_size * overlap)

        if not win_size:
            raise ValueError("[segment] loader win_size is missing")

        if select == "all":
            # Returns all of the segment data
            smin = self.smin
            smax = self.smax

        elif select == "first":
            # Returns the first window of the segment
            smin = self.smin
            smax = smin + win_size

        elif select == "random":
            # Returns a random window from the segment
            from random import randint
            smin_start = max(x_start, self.smin - overlap)
            smin_end = min(x_end - win_size, self.smax - overlap)
            smin = randint(smin_start, smin_end)
            smax = smin + win_size

        else:
            raise NotImplementedError(f"[segment] unknown usage '{select}'")

        x = run_data.x[..., smin : smax]
        y = run_data.y[smin : smax]
        t = run_data.t[smin : smax]
        return (x, y, t) # Tuple[(N, C, L), (L,), (L,)]

    def plot(self, save_path: Path = None, **kwargs):
        import matplotlib.pyplot as plt
        from matplotlib.gridspec import GridSpec

        x, y, t = self.data(**kwargs)
        N, C, L = x.shape

        run_data: Run = (
            self.loader.data
            [self.subject][self.session][self.run]
        )
        ch_names = run_data.ch_names

        assert len(ch_names) == C

        fig = plt.figure(figsize=(14, (C * 0.6)))
        gs = GridSpec(nrows=C, ncols=1)
        axes = []

        for c in range(C):
            ax = fig.add_subplot(gs[c, 0], sharex=axes[0] if c > 0 else None)
            ax.plot(t, x[0, c], color="black")
            ax.set_ylabel(ch_names[c], rotation=0, labelpad=50)
            axes.append(ax)

        plt.suptitle(" ".join([self.subject, self.session, self.run]))

        if save_path:
            plt.savefig(save_path)

        else:
            plt.show(block=True)

        return


@dataclass
class SegmentJob:
    fn: Callable
    win_size: int
    stride: int
    train: bool = True
    dev: bool = True
    test: bool = True


@dataclass
class RunFiles:
    edf: str
    json: str
    tsv: str


@dataclass
class Run:
    subject: str
    session: str
    run: str
    datetime_start_og: datetime = None
    datetime_start: datetime = None
    duration: float = None
    files: RunFiles = None
    x: ndarray | Tensor = None   # (N, C, L), N=1
    y: ndarray | Tensor = None   # (L,)
    t: ndarray | Tensor = None   # (L,)
    ch_names: List[str] = None
    _is_tensor: bool = False
    segments_train: List[Segment] = None
    segments_dev: List[Segment] = None
    segments_test: List[Segment] = None


@dataclass
class Session:
    subject: str
    session: str
    datetime_start: datetime = None
    sfreq: float = None
    powerline_freq: float = None
    runs: OrderedDict[str, Run] = None

    def __getitem__(self, index):
        if self.runs is not None:
            return self.runs[index]
        raise IndexError("Runs dict is not initialised")

    def values(self):
        return self.runs.values()

    def keys(self):
        return self.runs.keys()

    def items(self):
        return self.runs.items()


@dataclass
class Subject:
    subject: str
    age: int = None
    sex: str = None
    datetime_start: datetime = None
    sessions: OrderedDict[str, Session] = None

    def __getitem__(self, index):
        if self.sessions is not None:
            return self.sessions[index]
        raise IndexError("Sessions dict is not initialised")

    def values(self):
        return self.sessions.values()

    def keys(self):
        return self.sessions.keys()

    def items(self):
        return self.sessions.items()


@dataclass
class BIDSTree:
    path: Path
    subjects: OrderedDict[str, Subject]
    sfreq: float = None

    def __len__(self):
        return len(self.subjects)

    def __getitem__(self, index):
        if self.subjects is not None:
            return self.subjects[index]
        raise IndexError("Subjects dict is not initialised")

    def values(self):
        return self.subjects.values()

    def keys(self):
        return self.subjects.keys()

    def items(self):
        return self.subjects.items()

    def apply(self,
        fn: Callable,
        carry: Any = None,
        status: Status = None,
        **kwargs
    ):
        for sub_i, (sub, sub_data) in enumerate(self.items()):
            for ses_i, (ses, ses_data) in enumerate(sub_data.items()):
                for run_i, (run, run_data) in enumerate(ses_data.items()):
                    if status:
                        status.update(" ".join([sub, ses, run]))
                    args = dict(
                        tree=self,
                        sub_i=sub_i, sub=sub, sub_data=sub_data,
                        ses_i=ses_i, ses=ses, ses_data=ses_data,
                        run_i=run_i, run=run, run_data=run_data
                    )
                    carry = fn(args, carry, **kwargs)
        return carry

    def threaded_apply(self,
        fn: Callable,
        status: Status = None,
        **kwargs
    ):
        from concurrent.futures import ThreadPoolExecutor, as_completed

        futures = []
        with ThreadPoolExecutor() as executor:
            for sub_i, (sub, sub_data) in enumerate(self.items()):
                for ses_i, (ses, ses_data) in enumerate(sub_data.items()):
                    for run_i, (run, run_data) in enumerate(ses_data.items()):
                        args = dict(
                            tree=self,
                            sub_i=sub_i, sub=sub, sub_data=sub_data,
                            ses_i=ses_i, ses=ses, ses_data=ses_data,
                            run_i=run_i, run=run, run_data=run_data
                        )
                        future = executor.submit(fn, args, **kwargs)
                        futures.append(future)

        for i, future in enumerate(as_completed(futures)):
            if status:
                status.update(f"{i + 1} of {len(futures)}")
            future.result()

        return
