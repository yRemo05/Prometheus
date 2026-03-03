# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-02-26
### Added
- New directory structure with `src/` folder for better organization.
- `Manager.py`, `Utils.py`, and `Corrector.py` modules.
- `config.json` for project configuration.


### Changed
- Prometheus used to keep all windows in the same cahce which wasn't a really good idea if the user wanted switch windows. Now the windows are kept track of with the manager.

### Fixed
- Fixed the issue where the last word tracker logic would prevent the second word from being corrected if 2 last words were the same.