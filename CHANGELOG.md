# Zoltraak Klein Changelog

## [1.0.5] - 2024-08-29
### Changed
- Removed USER_DIR as the work directory path from "config.py", then added `work_dir` as a ZK member variable.
- Added new argument `work_dir` for `__init__` method of ZoltraakKlein class.

## [1.0.4] - 2024-08-28
### Changed
- Corrected architects "architect_common.py", "mermaid_chart.py" and "marp_presentation.py" to call external command suitable for the OS.
- Corrected "mermaid_chart.py" to adapt to Posix systems case by adding "puppeteer-config.json".
- Amended files in rosetta folder.

## [1.0.3] - 2024-08-24
### Changed
- Fully revised architect "voice_voicevox.py" to reduce the load on the system.
- Corrected spelling error in the "architect_description.json" file.

## [1.0.2] - 2024-08-23
### Changed
- Corrected bug of file copy error in the "epub.py" and "epub_picture.py" architect.
- Revised compiler and image generation prompts for picture book
- Amended files in rosetta folder.

## [1.0.1] - 2024-08-21
### Changed
- For architect "epub.py" and "epub_picture.py", corrected bug of recording file name to the menu.
- `takt_time` changed from list to dictionary.

## [1.0.0] - 2024-08-19
### Changed
- Formal release of Zoltraak Klein

## [0.1.0] - 2024-07-14
### Added
- Demo version of Zoltraak Klein
