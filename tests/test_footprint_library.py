from __future__ import annotations

import pytest

from hw_codesign.footprint_library import canonical_footprint_geometry

_CASES = {
    "Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal": {
        "sha256": "3b8d7da3cae5114ec83022a759a78925113bc2eeec100ea447594f6d8687e4b8",
        "body": (-4.47, -3.675, 4.47, 3.675),
        "copper": (-4.82, -4.255, 4.82, 1.975),
        "courtyard": (-5.32, -4.76, 5.32, 4.18),
        "pad_forms": 22,
        "pad_numbers": frozenset({
            "A1", "A4", "A5", "A6", "A7", "A8", "A9", "A12",
            "B1", "B4", "B5", "B6", "B7", "B8", "B9", "B12", "SH",
        }),
    },
    "Package_TO_SOT_SMD:SOT-23-5": {
        "sha256": "455a3f7c3e5eb5b8847eaa5df23e18651e78ab9f75afd09a0883758a0d901761",
        "body": (-0.8, -1.45, 0.8, 1.45),
        "copper": (-1.8, -1.25, 1.8, 1.25),
        "courtyard": (-2.05, -1.7, 2.05, 1.7),
        "pad_forms": 5,
        "pad_numbers": frozenset({"1", "2", "3", "4", "5"}),
    },
    "Package_TO_SOT_SMD:SOT-23-6": {
        "sha256": "f341c73aac9dcb553456f68bf3fee3d26eb14acf6d8a1cae82b50418fe1d71ca",
        "body": (-0.8, -1.45, 0.8, 1.45),
        "copper": (-1.8, -1.25, 1.8, 1.25),
        "courtyard": (-2.05, -1.7, 2.05, 1.7),
        "pad_forms": 6,
        "pad_numbers": frozenset({"1", "2", "3", "4", "5", "6"}),
    },
    "Package_DFN_QFN:QFN-56-1EP_7x7mm_P0.4mm_EP3.2x3.2mm": {
        "sha256": "516b5c14ad87b1a5ef29c098b603ec48c6bd9cefe21e8d479613cacf18458d8b",
        "body": (-3.5, -3.5, 3.5, 3.5),
        "copper": (-3.875, -3.875, 3.875, 3.875),
        "courtyard": (-4.13, -4.13, 4.13, 4.13),
        "pad_forms": 70,
        "pad_numbers": frozenset(str(number) for number in range(1, 58)),
    },
    "Package_SO:SOIC-8_5.3x5.3mm_P1.27mm": {
        "sha256": "cc86a7083c9df1c1bf808dfa469e913d446455fd7ab7a7941e18681b80e8b9b5",
        "body": (-2.65, -2.65, 2.65, 2.65),
        "copper": (-4.4, -2.23, 4.4, 2.23),
        "courtyard": (-4.65, -2.9, 4.65, 2.9),
        "pad_forms": 8,
        "pad_numbers": frozenset(str(number) for number in range(1, 9)),
    },
    "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm": {
        "sha256": "7648bca15399a8bd7856b5da6a1d2bc3a87049dc63958f8e8a3ab7409941a8e4",
        "body": (-1.6, -1.25, 1.6, 1.25),
        "copper": (-1.8, -1.45, 1.8, 1.45),
        "courtyard": (-2.1, -1.75, 2.1, 1.75),
        "pad_forms": 4,
        "pad_numbers": frozenset({"1", "2", "3", "4"}),
    },
    "Connector_IDC:IDC-Header_2x05_P2.54mm_Vertical": {
        "sha256": "b605d7a816a5b5681d09bd120b547ac748d74440e7d55a8371007b9c53afb092",
        "body": (-3.18, -5.1, 5.72, 15.26),
        "copper": (-0.85, -0.85, 3.39, 11.01),
        "courtyard": (-3.68, -5.6, 6.22, 15.76),
        "pad_forms": 10,
        "pad_numbers": frozenset(str(number) for number in range(1, 11)),
    },
    "Resistor_SMD:R_0603_1608Metric": {
        "sha256": "7190ac4a00125b807e54129ef0d87d87f2a658eeb74d025a7028203419b09f23",
        "body": (-0.8, -0.4125, 0.8, 0.4125),
        "copper": (-1.225, -0.475, 1.225, 0.475),
        "courtyard": (-1.48, -0.73, 1.48, 0.73),
        "pad_forms": 2,
        "pad_numbers": frozenset({"1", "2"}),
    },
    "Capacitor_SMD:C_0402_1005Metric": {
        "sha256": "0403382fc4583ed510b461b1fa4a36dfaec6f4c0d9b1a67e6b0027837a54e1b5",
        "body": (-0.5, -0.25, 0.5, 0.25),
        "copper": (-0.76, -0.31, 0.76, 0.31),
        "courtyard": (-0.91, -0.46, 0.91, 0.46),
        "pad_forms": 2,
        "pad_numbers": frozenset({"1", "2"}),
    },
    "Capacitor_SMD:C_0603_1608Metric": {
        "sha256": "fe0dbfefbb181a0466f93a8de52d84ba7b00fcd9acdbb69575f4128a0af4e405",
        "body": (-0.8, -0.4, 0.8, 0.4),
        "copper": (-1.225, -0.475, 1.225, 0.475),
        "courtyard": (-1.48, -0.73, 1.48, 0.73),
        "pad_forms": 2,
        "pad_numbers": frozenset({"1", "2"}),
    },
}


@pytest.mark.parametrize("library_id", _CASES)
def test_vendored_kicad_footprint_has_pinned_canonical_pad_geometry(library_id: str):
    expected = _CASES[library_id]
    geometry = canonical_footprint_geometry(library_id)

    assert geometry is not None
    assert geometry.sha256 == expected["sha256"]
    assert geometry.body_extent == pytest.approx(expected["body"])
    assert geometry.copper_extent == pytest.approx(expected["copper"])
    assert geometry.courtyard_extent == pytest.approx(expected["courtyard"])
    assert geometry.pad_forms == expected["pad_forms"]
    assert frozenset(geometry.numbered_pads) == expected["pad_numbers"]
