from pathlib import Path
from typing import List, Dict
import re

from epilepsy_bids_loader import Run, Subject
from epilepsy_bids_loader import BIDSLoader
from epilepsy_bids_loader import CVFold, CrossValidation
from epilepsy_bids_loader import Status, read_yaml


class ManifestBIDSLoader(BIDSLoader):

    def __init__(
        self,
        data_path: str | Path,
        manifest_path: str | Path,
        enforce_chronology: bool,
        allowed_subjects: List[str] = None,
    ) -> None:
        super().__init__(
            data_path=data_path,
            enforce_chronology=enforce_chronology,
            allowed_subjects=allowed_subjects
        )
        self.load_and_check_manifest(manifest_path)
        return

    def load_and_check_manifest(self, manifest_path: Path):

        manifest = read_yaml(manifest_path)

        assert "subject_specific" in manifest.keys()
        assert "subject_independent" in manifest.keys()

        sub_spec = manifest["subject_specific"]
        for sub, cv_folds in sub_spec.items():
            assert re.match(r"^sub-\d{2}$", sub)

            for i, (fold, datasets) in enumerate(cv_folds.items()):
                assert fold == f"fold-{i:02d}"

                for ds_type in ["train", "dev", "test"]:
                    assert ds_type in datasets.keys()

                    for ses, runs in datasets[ds_type].items():
                        assert re.match(r"^ses-\d{2}$", ses)

                        for run in runs:
                            assert re.match(r"^run-\d{2}$", run)

        self.sub_spec: Dict[str, Dict[str, Dict[str, Dict[str, List[str]]]]] = \
            sub_spec

        sub_ind = manifest["subject_independent"]
        for i, (fold, datasets) in enumerate(sub_ind.items()):
            assert fold == f"fold-{i:02d}"

            for ds_type in ["train", "dev", "test"]:
                assert ds_type in datasets.keys()

                for sub in datasets[ds_type]:
                    assert re.match(r"^sub-\d{2}$", sub)

        self.sub_ind: Dict[str, Dict[str, List[str]]] = sub_ind

        return

    def _get_sub_spec_folds(
        self,
        cv: CrossValidation,
        sub: str
    ) -> CrossValidation:
        """
        Time-series cross validation (TSCV) for subject specific models
        based on specified manifest.

        Args:
            sub (str): Subject identifier.

        Returns:
            CrossValidation: CV object.
        """
        assert cv.method == "subject_specific"

        sub_data: Subject = self.data.subjects[sub]
        manifest = self.sub_spec[sub]

        runs: Dict[str, Dict[str, Run]] = {
            ses: {
                run: run_data
                for run, run_data in ses_data.items()
            }
            for ses, ses_data in sub_data.items()
        }
        status = Status("[loader] subject specific CV ...")
        for fold in range(len(manifest)):
            status.update(f"fold {fold}/{len(runs) - 1}")
            fold_manifest = manifest[f"fold-{fold:02d}"]
            cv.append(CVFold(
                train=[
                    seg
                    for _ses, _runs in fold_manifest["train"].items()
                    for _run in _runs
                    for seg in runs[_ses][_run].segments_train
                ],
                dev=[
                    seg
                    for _ses, _runs in fold_manifest["dev"].items()
                    for _run in _runs
                    for seg in runs[_ses][_run].segments_dev
                ],
                test=[
                    seg
                    for _ses, _runs in fold_manifest["test"].items()
                    for _run in _runs
                    for seg in runs[_ses][_run].segments_test
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
        Leave-one-out (subject) cross validation for subject independent models
        based on specified manifest.

        Returns:
            CrossValidation: CV object.
        """
        assert cv.method == "subject_independent"

        subs: Dict[str, Subject] = {
            sub: sub_data
            for sub, sub_data in self.data.items()
        }
        manifest = self.sub_ind
        status = Status("[loader] subject independent CV ...")
        for fold in range(len(manifest)):
            status.update(f"fold {fold}/{len(subs)}")
            fold_manifest = manifest[f"fold-{fold:02d}"]
            cv.append(CVFold(
                train=[
                    seg
                    for _sub in fold_manifest["train"]
                    for _ses_data in subs[_sub].values()
                    for _run_data in _ses_data.values()
                    for seg in _run_data.segments_train
                ],
                dev=[
                    seg
                    for _sub in fold_manifest["dev"]
                    for _ses_data in subs[_sub].values()
                    for _run_data in _ses_data.values()
                    for seg in _run_data.segments_dev
                ],
                test=[
                    seg
                    for _sub in fold_manifest["test"]
                    for _ses_data in subs[_sub].values()
                    for _run_data in _ses_data.values()
                    for seg in _run_data.segments_test
                ]
            ))
        status.done()
        return cv
