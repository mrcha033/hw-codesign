# Vendored KiCad footprint attribution

These files originate from snapshots of the KiCad 10.0.3 standard footprint
library installed locally. The ESP32 snapshot was recorded on 2026-07-14; the
remaining snapshots were recorded on 2026-07-18. The RP2040 QFN footprint is a
documented exception: its exposed-pad via array is an hw-codesign extension
aligned with Raspberry Pi's official Minimal-KiCAD reference design.

- Upstream: https://gitlab.com/kicad/libraries/kicad-footprints
- License: Creative Commons CC-BY-SA 4.0 with the KiCad libraries exception;
  see `LICENSE.md` in this directory.

| Upstream library file | Vendored file | SHA-256 |
| --- | --- | --- |
| `Capacitor_SMD.pretty/C_0402_1005Metric.kicad_mod` | `C_0402_1005Metric.kicad_mod` | `0403382fc4583ed510b461b1fa4a36dfaec6f4c0d9b1a67e6b0027837a54e1b5` |
| `Capacitor_SMD.pretty/C_0603_1608Metric.kicad_mod` | `C_0603_1608Metric.kicad_mod` | `fe0dbfefbb181a0466f93a8de52d84ba7b00fcd9acdbb69575f4128a0af4e405` |
| `Connector_IDC.pretty/IDC-Header_2x05_P2.54mm_Vertical.kicad_mod` | `IDC-Header_2x05_P2.54mm_Vertical.kicad_mod` | `b605d7a816a5b5681d09bd120b547ac748d74440e7d55a8371007b9c53afb092` |
| `Connector_USB.pretty/USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal.kicad_mod` | `USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal.kicad_mod` | `3b8d7da3cae5114ec83022a759a78925113bc2eeec100ea447594f6d8687e4b8` |
| `Crystal.pretty/Crystal_SMD_3225-4Pin_3.2x2.5mm.kicad_mod` | `Crystal_SMD_3225-4Pin_3.2x2.5mm.kicad_mod` | `7648bca15399a8bd7856b5da6a1d2bc3a87049dc63958f8e8a3ab7409941a8e4` |
| `Package_DFN_QFN.pretty/QFN-56-1EP_7x7mm_P0.4mm_EP3.2x3.2mm.kicad_mod` | `QFN-56-1EP_7x7mm_P0.4mm_EP3.2x3.2mm.kicad_mod` | `516b5c14ad87b1a5ef29c098b603ec48c6bd9cefe21e8d479613cacf18458d8b` |
| `Package_SO.pretty/SOIC-8_5.3x5.3mm_P1.27mm.kicad_mod` | `SOIC-8_5.3x5.3mm_P1.27mm.kicad_mod` | `cc86a7083c9df1c1bf808dfa469e913d446455fd7ab7a7941e18681b80e8b9b5` |
| `Package_TO_SOT_SMD.pretty/SOT-23-5.kicad_mod` | `SOT-23-5.kicad_mod` | `455a3f7c3e5eb5b8847eaa5df23e18651e78ab9f75afd09a0883758a0d901761` |
| `Package_TO_SOT_SMD.pretty/SOT-23-6.kicad_mod` | `SOT-23-6.kicad_mod` | `f341c73aac9dcb553456f68bf3fee3d26eb14acf6d8a1cae82b50418fe1d71ca` |
| `RF_Module.pretty/ESP32-S3-WROOM-1.kicad_mod` | `ESP32-S3-WROOM-1.kicad_mod` | `d0cfbb31fef0c47396c0d061ec5a3bff60f0567d8d4ea8dd4769c84f52bd656f` |
| `Resistor_SMD.pretty/R_0603_1608Metric.kicad_mod` | `R_0603_1608Metric.kicad_mod` | `7190ac4a00125b807e54129ef0d87d87f2a658eeb74d025a7028203419b09f23` |

The snapshots are retained so generation is deterministic and does not
silently change with the workstation's installed KiCad library version.

The RP2040 extension uses nine 0.60 mm plated pads with 0.35 mm drills on a
1.275 mm square grid, plus the reference design's four 1.084435 mm paste
apertures centered at +/-0.6375 mm, matching `RP2040-QFN-56.kicad_mod` in Raspberry Pi's
[Minimal-KiCAD reference archive](https://pip-assets.raspberrypi.com/categories/814-rp2040/documents/RP-008296-DS-1-Minimal-KiCAD.zip)
(archive SHA-256
`5af8f5acd52a521a93ae6ba4986a4e0cbfaefca5454223cfddf91b37e975b21f`).
This source alignment does not qualify the selected board fabricator or its
via-in-pad assembly process.
