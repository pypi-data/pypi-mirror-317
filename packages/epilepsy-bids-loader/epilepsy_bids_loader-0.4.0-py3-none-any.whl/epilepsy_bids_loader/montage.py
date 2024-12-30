
class Montage:

    # This is the same as epilepsy2bids
    # From https://github.com/esl-epfl/epilepsy2bids/blob/main/src/epilepsy2bids/eeg.py#L47
    ELECTRODES_10_20 = [
        "Fp1",
        "F3",
        "C3",
        "P3",
        "O1",
        "F7",
        "T3",
        "T5",
        "Fz",
        "Cz",
        "Pz",
        "Fp2",
        "F4",
        "C4",
        "P4",
        "O2",
        "F8",
        "T4",
        "T6",
    ]

    # This is the same as epilepsy2bids
    # https://github.com/esl-epfl/epilepsy2bids/blob/main/src/epilepsy2bids/eeg.py#L27
    # Parasagittal first, followed by temporal
    BIPOLAR_DBANANA = [
        # Parasagittal chain (left)
        "Fp1-F3",
        "F3-C3",
        "C3-P3",
        "P3-O1",

        # Temporal chain (left)
        "Fp1-F7",
        "F7-T3",
        "T3-T5",
        "T5-O1",

        # Midline
        "Fz-Cz",
        "Cz-Pz",

        # Parasagittal chain (right)
        "Fp2-F4",
        "F4-C4",
        "C4-P4",
        "P4-O2",

        # Temporal chain (right)
        "Fp2-F8",
        "F8-T4",
        "T4-T6",
        "T6-O2",
    ]

    # Modified from BIPOLAR_DBANANA:
    # - Channel names are the same
    # - Channel order follows ACNS LB-18.1 (DOI: 10.1097/WNP.0000000000000317)
    # - Chains ordered left to right
    BIPOLAR_LB_18_1 = [
        # Temporal chain (left)
        "Fp1-F7",
        "F7-T3",
        "T3-T5",
        "T5-O1",

        # Parasagittal chain (left)
        "Fp1-F3",
        "F3-C3",
        "C3-P3",
        "P3-O1",

        # Midline
        "Fz-Cz",
        "Cz-Pz",

        # Parasagittal chain (right)
        "Fp2-F4",
        "F4-C4",
        "C4-P4",
        "P4-O2",

        # Temporal chain (right)
        "Fp2-F8",
        "F8-T4",
        "T4-T6",
        "T6-O2",
    ]

    @staticmethod
    def as_10_20(ch):
        synonym_channels = {
            "T7": "T3",
            "T8": "T4",
            "P7": "T5",
            "P8": "T6"
        }
        if ch.upper() in synonym_channels:
            return synonym_channels[ch.upper()]

        else:
            return ch