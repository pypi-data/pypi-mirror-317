import torch
import numpy as np
import pandas as pd
from pandas import DataFrame
from pathlib import Path
from typing import Tuple, List, Any, Literal

from epilepsy_bids_loader import SegmentJob
from epilepsy_bids_loader import Run, RunFiles, Session, Subject
from epilepsy_bids_loader import BIDSTree
from epilepsy_bids_loader import CVFold, CrossValidation
from epilepsy_bids_loader import Status
from epilepsy_bids_loader import read_json
from epilepsy_bids_loader import Montage


def load_bids_tree(
    data_path: str | Path,
    allowed_subjects: List[str] = None
) -> BIDSTree:
    data_path = Path(data_path)
    subject_meta = (
        pd.read_csv(
            data_path.joinpath("participants.tsv"),
            sep="\t",
            index_col="participant_id"
        )
        .to_dict("index")
    )

    # Generate a catalogue of available data within the data path
    tree = BIDSTree(
        path=data_path,
        subjects={ subject.name: Subject(
            subject=subject.name,
            age=subject_meta[subject.name]["age"],
            sex=subject_meta[subject.name]["sex"],

            sessions={ session.name: Session(
                subject=subject.name,
                session=session.name,

                runs={ run_name: Run(
                    subject=subject.name,
                    session=session.name,
                    run=run_name,
                    files=RunFiles(
                        edf=edf_file,
                        json=json_file,
                        tsv=tsv_file
                    ))
                    for run_name, edf_file, json_file, tsv_file in (
                        (
                            edf.stem.split("_")[-2],
                            edf,
                            json,
                            tsv
                        )
                        for edf in sorted(session.joinpath("eeg").iterdir())
                        if edf.is_file() and edf.name.endswith(".edf")

                        for json in session.joinpath("eeg").iterdir()
                        if (
                            json.is_file() and json.name.endswith(".json")
                            and json.stem == edf.stem
                        )

                        for tsv in session.joinpath("eeg").iterdir()
                        if (
                            tsv.is_file() and tsv.name.endswith(".tsv")
                            and (
                                edf.stem.split("_")[:-1]    # *eeg.edf
                                == tsv.stem.split("_")[:-1] # *events.tsv
                            )
                        )
                    )
                })
                for session in sorted(subject.iterdir())
                if session.is_dir() and session.name.startswith("ses-")
            })
            for subject in sorted(data_path.iterdir())
            if subject.is_dir() and subject.name.startswith("sub-")
        }
    )

    if allowed_subjects is not None:
        tree.subjects = {
            sub: sub_data
            for sub, sub_data in tree.subjects.items()
            if sub in allowed_subjects
        }

    assert len(tree) > 0, "[loader] Did not load any subjects!"
    return tree


def load_events(
    tree: BIDSTree,
    enforce_chronology: bool
) -> DataFrame:
    """
    Reads event annotations, updates the tree in place then returns events
    as a dataframe.

    Args:
        tree (BIDSTree): A BIDSTree, this will be modified in-place.
        enforce_chronology (bool): Some datasets will only provide time,
            so that the datetime does not follow chronological order
            between successive runs within each session.
            This should be True for Siena and False for CHB-MIT.

    Returns:
        DataFrame: of events.
    """
    events = []
    last_datetime_end = None

    def _load_events(args, last_datetime_end, events):
        sub = args["sub"]
        sub_data: Subject = args["sub_data"]
        ses = args["ses"]
        ses_data: Session = args["ses_data"]
        run = args["run"]
        run_i = args["run_i"]
        run_data: Run = args["run_data"]

        run_files = run_data.files
        event_file = run_files.tsv
        event = (
            pd.read_csv(
                event_file,
                sep="\t",
                parse_dates=["dateTime"]
            )
            .assign(
                subject=sub,
                session=ses,
                run=run,
                file=event_file.name
            )
        )
        datetime_start_og = event["dateTime"].min()
        datetime_start = datetime_start_og
        duration = event["recordingDuration"].min()
        # NOTE: Duration should be the same for all event entries

        if run_i == 0:
            last_datetime_end = datetime_start

        if enforce_chronology:
            while datetime_start < last_datetime_end:
                print(
                    f"[loader] event chronology"
                    f" {' '.join([sub, ses, run])}"
                )
                datetime_start += pd.Timedelta(days=1)

        event["dateTime"] = datetime_start
        event["dateTimeOriginal"] = datetime_start_og
        event["endDateTime"] = (
            datetime_start
            + pd.to_timedelta(event["recordingDuration"], unit="s")
        )
        last_datetime_end = event["endDateTime"].max()
        events.append(event)

        # NOTE: mutates tree information
        run_data.datetime_start_og = datetime_start_og
        run_data.datetime_start = datetime_start
        run_data.duration = duration
        if not ses_data.datetime_start:
            ses_data.datetime_start = datetime_start
        if not sub_data.datetime_start:
            sub_data.datetime_start = datetime_start

        return last_datetime_end

    tree.apply(fn=_load_events, carry=last_datetime_end, events=events)

    events = pd.concat(events, ignore_index=True)

    # Convert event onset, event offset and record end to datetime
    events["onsetDateTime"] = (
        events["dateTime"]
        + pd.to_timedelta(events["onset"], unit="s")
    )
    events["offsetDateTime"] = (
        events["onsetDateTime"]
        + pd.to_timedelta(events["duration"], unit="s")
    )
    events = (
        events
        .sort_values(by=["subject", "session", "dateTime"])
        .reset_index(drop=True)
        .set_index(["subject", "session", "run"])
    )
    return events


def load_data(
    tree: BIDSTree,
    events: DataFrame,
):
    from pyedflib import EdfReader
    from datetime import datetime

    def _load_data(
        args: dict,
        carry: Any,
        events: DataFrame
    ):

        tree: BIDSTree = args["tree"]
        sub = args["sub"]
        sub_data: Subject = args["sub_data"]
        ses = args["ses"]
        run = args["run"]
        run_data: Run = args["run_data"]
        run_files = run_data.files

        # Read meta data
        meta = read_json(run_files.json)
        sfreq = meta["SamplingFrequency"]
        duration = meta["RecordingDuration"]
        n_channels = meta["EEGChannelCount"] # C
        n_steps = int(sfreq * duration) # L

        # Perform sfreq checks
        if tree.sfreq == None:
            tree.sfreq = sfreq

        else:
            assert tree.sfreq == sfreq, "[loader] sfreq mismatch"

        # Load EDF and read the signal
        edf = EdfReader(str(run_files.edf))
        x = np.stack([
            edf.readSignal(chn=c)
            for c in range(edf.signals_in_file)
        ])
        assert x.shape == (n_channels, n_steps)

        # Read channel names
        ch_names = edf.getSignalLabels()

        # Get start time from EDF
        datetime_start = datetime(
            year=edf.startdate_year,
            month=edf.startdate_month,
            day=edf.startdate_day,
            hour=edf.starttime_hour,
            minute=edf.starttime_minute,
            second=edf.starttime_second,
            microsecond=edf.starttime_subsecond
        )
        assert datetime_start == run_data.datetime_start_og, \
            "[loader] datetime_start in edf does not match tsv"

        # Load event annotations
        run_evt = events.loc[[(sub, ses, run)]]

        # Generate labels
        y = np.zeros(n_steps, dtype=int)
        for _, evt in run_evt.iterrows():
            if not evt["eventType"].startswith("sz"): # Not seizure
                continue
            assert evt["recordingDuration"] == duration, \
                "[loader] duration in edf does not match tsv"
            y_onset = int(sfreq * evt["onset"])
            y_duration = int(sfreq * evt["duration"])
            y[y_onset : y_onset + y_duration] = 1

        # Generate timestamps
        secs_start = (datetime_start - sub_data.datetime_start).seconds
        t = np.linspace(
            start=secs_start,
            stop=secs_start + duration,
            num=n_steps,
            endpoint=False
        )

        run_data.x = x[np.newaxis, ...] # (N, C, L), N=1
        run_data.y = y
        run_data.t = t
        run_data.ch_names = ch_names

        return carry

    status = Status("[loader] loading data ...")
    tree.apply(
        fn=_load_data,
        carry=None,
        status=status,
        events=events
    )
    status.done()
    return


def check_valid_bipolar_montage(
    montage: List[str],
    electrodes: List[str] = Montage.ELECTRODES_10_20,
    unipolar_electrodes: List[str] = ["AVG", "REF"]
) -> bool:
    """
    Checks whether the supplied montage is a valid bipolar montage. Assumptions:
    - Channel has format {from_channel}-{to_channel}.
    - Channel names will be converted to 10-20 nomenclature.
    - Either from_channel or to_channel must be from the supplied electrodes.
    - If to_channel is from unipolar_electrodes, will return False.

    Args:
        montage (List[str]): Montage list of two hyphen separated channels.
        electrodes (List[str], optional): Truth electrode (channel) names.
            Defaults to Montage.ELECTRODES_10_20.

    Returns:
        bool: _description_
    """
    # Convert montage names to upper case
    electrodes = [ch.upper() for ch in Montage.ELECTRODES_10_20]
    montage = [ch.upper() for ch in montage]

    # Check that the supplied montage is a valid bipolar montage
    # Will throw AssertionError if channels are invalid
    for ch in montage:
        from_ch, to_ch = ch.split("-")
        from_ch = Montage.as_10_20(from_ch)
        to_ch = Montage.as_10_20(to_ch)

        assert from_ch in electrodes, f"[montage] invalid channel: {from_ch}"

        if to_ch in unipolar_electrodes:
            return False

        assert to_ch in electrodes, f"[montage] invalid channel: {to_ch}"

    return True


def convert_montage_names(montage: List[str]) -> List[Tuple[str, str]]:
    """
    Converts a list of {from_ch}-{to_ch} to a tuple of (from_ch, to_ch)
    in the 10-20 nomenclature.

    Args:
        montage (List[str]): Montage list of two hyphen separated channels.

    Returns:
        List[Tuple[str, str]]: Montage of channles as a tuple.
    """
    _montage = []
    for ch in montage:
        from_ch, to_ch = ch.split("-")
        from_ch = Montage.as_10_20(from_ch).upper()
        to_ch = Montage.as_10_20(to_ch).upper()
        _montage.append((from_ch, to_ch))
    return _montage


class BIDSLoader():

    def __init__(
        self,
        data_path: str | Path,
        enforce_chronology: bool,
        allowed_subjects: List[str] = None
    ) -> None:
        self.data_path = Path(data_path)
        self.data = load_bids_tree(
            data_path=data_path,
            allowed_subjects=allowed_subjects
        )
        self.events = load_events(
            tree=self.data,
            enforce_chronology=enforce_chronology
        )
        self.win_size: int | None = None # Populated in self.segment()
        return

    def load(self):
        load_data(tree=self.data, events=self.events)
        return

    def to_bipolar(self, montage: List[str] = Montage.BIPOLAR_LB_18_1):

        check_valid_bipolar_montage(montage)

        def _to_bipolar(
            args: dict,
            carry: Any,
            montage: List[str]
        ):
            run_data: Run = args["run_data"]
            ch_names = run_data.ch_names
            N, C, L = run_data.x.shape
            assert len(ch_names) == C

            # Check whether current channels are uni or bipolar
            is_bipolar = check_valid_bipolar_montage(ch_names)

            # Convert ch_names, montage to 10-20 nomenclature and uppercase
            ch_names = convert_montage_names(ch_names)
            montage = convert_montage_names(montage)

            if not is_bipolar:
                # Reference unipolar to bipolar
                ch_data = {
                    from_ch : run_data.x[:, i, :]
                    for i, (from_ch, to_ch) in enumerate(ch_names)
                }
                new_x = []
                new_ch_names = []
                for (from_ch, to_ch) in montage:
                    if from_ch in ch_data and to_ch in ch_data:
                        new_x.append(ch_data[from_ch] - ch_data[to_ch]) # (N, L)

                    else:
                        print(
                            f"[montage] missing {from_ch}-{to_ch}, using zeros"
                        )
                        new_x.append(np.zeros((N, L)))

                    new_ch_names.append("-".join([from_ch, to_ch]))
                    continue

            else:
                # Reorder bipolar
                ch_data = {
                    (from_ch, to_ch) : run_data.x[:, i, :]
                    for i, (from_ch, to_ch) in enumerate(ch_names)
                }
                new_x = []
                new_ch_names = []
                for (from_ch, to_ch) in montage:
                    if (from_ch, to_ch) in ch_data:
                        new_x.append(ch_data[(from_ch, to_ch)])

                    else:
                        print(
                            f"[montage] missing {from_ch}-{to_ch}, using zeros"
                        )
                        new_x.append(np.zeros((N, L)))

                    new_ch_names.append("-".join([from_ch, to_ch]))
                    continue

            new_x = np.stack(new_x, axis=1) # (N, C, L)
            assert (N, len(montage), L) == new_x.shape

            run_data.x = new_x
            run_data.ch_names = new_ch_names
            return

        status = Status(f"[loader] converting to bipolar montage ...")
        self.data.apply(
            fn=_to_bipolar,
            montage=montage,
            status=status
        )
        status.done()
        return

    def filt_fir(
        self,
        freqs: List[int] = [0.5, 40],
        fs: int = 256,
        numtaps: int = 384,
        window: str = "hamming",
        pass_zero: Literal["bandpass", "lowpass", "highpass", "bandstop"] \
            = "bandpass",
        **kwargs
    ):
        from scipy.signal import firwin, filtfilt

        def _filt(args: dict):
            run_data = args["run_data"]
            run_data.x = filtfilt(
                b=firwin(
                    fs=fs,
                    numtaps=numtaps,
                    cutoff=freqs,
                    window=window,
                    pass_zero=pass_zero,
                    **kwargs
                ),
                a=1.0,
                x=run_data.x, # (N, C, L)
                axis=2
            )
            return

        status = Status(f"[loader] fir filter {pass_zero} {freqs} ...")
        self.data.threaded_apply(
            fn=_filt,
            status=status
        )
        status.done()
        return

    def _segment(
        self,
        method: str,
        win_size: int,
        seg_jobs: List[SegmentJob],
        **kwargs
    ) -> Tuple[float, float]:
        from epilepsy_bids_loader import get_segment_stats

        status = Status(f"[loader] segmenting {method} ...")
        for job in seg_jobs:
            assert win_size == job.win_size
            self.data.apply(
                fn=job.fn,
                carry=None,
                loader=self,
                win_size=job.win_size,
                stride=job.stride,
                train=job.train,
                dev=job.dev,
                test=job.test,
                **kwargs
            )
        status.done()
        self.win_size = win_size

        # Calculate segment statistics
        seg_size_stats = self.data.apply(
            fn=get_segment_stats,
            carry=[]
        )
        seg_size_mean = np.mean(seg_size_stats)
        seg_size_stddev = np.std(seg_size_stats)
        print(
            f"[loader] seg size stats: "
            f"mean {seg_size_mean:.2f}, "
            f"stddev {seg_size_stddev:.2f}"
        )
        return seg_size_mean, seg_size_stddev

    def segment(
        self,
        win_size: int,
        stride: int,
        method: Literal["fixed"],
        **kwargs
    ) -> Tuple[float, float]:
        assert win_size is not None, "[loader] win_size is missing"
        assert stride is not None, "[loader] stride is missing"
        assert method is not None, "[loader] seg method is missing"

        if method == "fixed":
            from epilepsy_bids_loader import fixed_segmentation
            seg_jobs = [
                SegmentJob(
                    fn=fixed_segmentation,
                    win_size=win_size,
                    stride=stride,
                    train=True,
                    dev=True,
                    test=True
                )
            ]

        # TODO: Extend with other methods here

        else:
            raise NotImplementedError()

        return self._segment(
            method=method,
            win_size=win_size,
            seg_jobs=seg_jobs,
            **kwargs
        )

    def _get_sub_spec_folds(
        self,
        cv: CrossValidation,
        sub: str
    ) -> CrossValidation:
        """
        Time-series cross validation (TSCV) for subject specific models.
        - Train on run(i), test on run(i + 1), then increment i++
        - Number of folds is len(runs) - 1

        Args:
            sub (str): Subject identifier.

        Returns:
            CrossValidation: CV object.
        """
        assert cv.method == "subject_specific"

        sub_data: Subject = self.data.subjects[sub]
        runs: List[Run] = [
            run_data
            for ses_data in sub_data.values()
            for run_data in ses_data.values()
        ]
        status = Status("[loader] subject specific CV ...")
        for i in range(len(runs) - 1):
            status.update(f"fold {i}/{len(runs) - 1}")
            cv.append(CVFold(
                train=[
                    seg
                    for _run in runs[: i + 1]
                    for seg in _run.segments_train
                ],
                dev=[
                    # TODO
                ],
                test=[
                    seg
                    for seg in runs[i + 1].segments_test
                ]
            ))
        status.done()
        return cv

    def _get_sub_indp_folds(
        self,
        cv: CrossValidation,
        **kwargs
    ) -> CrossValidation:
        """
        Leave-one-out (subject) cross validation for subject independent models.
        - Train on all subjects except one.
        - Test on the left out subject.

        Returns:
            CrossValidation: CV object.
        """
        assert cv.method == "subject_independent"

        subs: List[Subject] = [sub_data for sub_data in self.data.values()]
        status = Status("[loader] subject independent CV ...")
        for i, leave_out in enumerate(subs):
            status.update(f"fold {i}/{len(subs)}")
            cv.append(CVFold(
                train=[
                    seg
                    for sub in subs if sub.subject != leave_out.subject
                    for ses in sub.values()
                    for run in ses.values()
                    for seg in run.segments_train
                ],
                dev=[
                    # TODO
                ],
                test=[
                    seg
                    for ses in leave_out.values()
                    for run in ses.values()
                    for seg in run.segments_test
                ]
            ))
        status.done()
        return cv

    def get_folds(
        self,
        cv: CrossValidation,
        sub: str = None
    ) -> CrossValidation:
        """
        Get cross validation folds.
        - subject_specific: uses time-series cross validation (TSCV).
        - subject_independent: uses leave-one-out subject.

        Args:
            cv (CrossValidation): Either subject_specific or
                subject_independent.
            sub (str, optional): Subject to select if using subject_specific
                and is ignored in subject_independent. Defaults to None.

        Returns:
            CrossValidation: CV object.
        """
        _get_folds = {
            "subject_specific": self._get_sub_spec_folds,
            "subject_independent": self._get_sub_indp_folds
        }[cv.method]
        return _get_folds(cv=cv, sub=sub)

    def to_tensor(self, dtype=torch.float32):
        def _to_tensor(
            args: dict,
            carry: Any = None,
            **kwargs
        ):
            import gc
            run_data: Run = args["run_data"]

            x = run_data.x.copy()
            y = run_data.y.copy()
            t = run_data.t.copy()
            del run_data.x, run_data.y, run_data.t
            gc.collect()

            run_data.x = torch.tensor(x, dtype=dtype)
            run_data.y = torch.tensor(y, dtype=dtype)
            run_data.t = torch.tensor(t, dtype=dtype)
            run_data._is_tensor = True

            del x, y, t
            gc.collect()
            return carry

        status = Status(f"[loader] convert to {dtype} ...")
        self.data.apply(
            fn=_to_tensor,
            carry=None,
            status=status
        )
        status.done()
        return