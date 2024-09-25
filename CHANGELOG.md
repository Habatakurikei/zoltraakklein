# Zoltraak Klein Changelog

## [Unreleased]
- Upgrade `YAMLManager` class for debug.
- Full revision of compilers and architects.

## [1.0.7] - 2024-09-25
### Changed
- Requirement of LLMMaster updated to 0.5.0 and capped until the next major update.
- Revised Python version requirement to 3.10 or later to adapt to the latest LLMMaster.

## [1.0.6] - 2024-08-30
### Changed
- Corrected architect "video_from_presentation.py" to avoid error of access permission for moviepy work file.

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
