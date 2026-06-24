# DragoTurkey Helper

A lightweight, polished PyQt5 desktop application for Dragodinde / AutoHotkey users to configure hotkeys, preview saved settings and generate a ready-to-run script. This project is designed for Windows desktop use and demonstrates a practical workflow with local JSON configuration, custom Qt widgets and a small text-utility surface for quick transformations.

## Key Highlights
- Save and manage attract, repel and toggle shortcuts from a simple settings flow.
- Generate an AutoHotkey script from the stored configuration with one click.
- Modern, readable dark UI with custom panels, shortcut capture fields and status feedback.
- Lightweight developer utilities: reusable text helpers and pytest coverage for core string transformations.

## Features
- First-run flow that guides the user to configure shortcuts before using the main screen.
- Shortcut capture widgets for attract, repel and toggle actions.
- Persisted JSON configuration stored in `app_config.json`.
- Main dashboard that displays the currently saved settings and lets the user regenerate the script.
- AutoHotkey script generation to a configurable folder, with a fallback save dialog when no folder is set.
- Two utility pages for quick text operations: reverse text and swap case.
- Pytest coverage for the pure helper functions in `text_utils.py`.

## Demonstration
@TODO: SCREENSHOTS of the settings page, main dashboard, script generation flow and the text utility pages showcasing the UI and features.

You can also find a demo video here: @TODO.

## Tech Stack
- Python 3
- PyQt5
- JSON for local configuration storage
- AutoHotkey script generation
- pytest for tests

## Prerequisites
- Python 3.x installed on your machine
- PyQt5 available through `pip`
- Optional: AutoHotkey installed to run the generated script
- Recommended editor: VS Code or PyCharm

## Quick Start

1. Clone the repo
   git clone <your-repo-url>

2. Install dependencies
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt

3. Run the app
   python main.py

You can also build a standalone Windows executable with PyInstaller using the scripts in `commands-pwsh.txt` or `build_py.py`.

## Developer utilities
Small helper functions exist in `text_utils.py` to keep the UI logic simple and testable:

- `reverse_text(s)`
  - Returns the reversed version of the input string and handles `None` safely.
- `swap_case(s)`
  - Swaps upper and lower case characters and handles `None` safely.

Use these helpers for reproducible unit tests or when extending the text utility pages.

## Project Structure (important files)
- `main.py` — application entry point, window setup and stacked-page navigation.
- `config.py` — load/save helpers for `app_config.json` and first-run state.
- `text_utils.py` — pure text transformation helpers used by the UI pages.
- `ui/main_menu.py` — landing page with navigation to settings and regeneration.
- `ui/settings_page.py` — shortcut capture and configuration save flow.
- `ui/main_page.py` — displays saved settings and generates the AutoHotkey script.
- `ui/reverse_text_page.py` — text reversal demo page.
- `ui/swap_case_page.py` — case-swapping demo page.
- `dark_theme.qss` — application theme stylesheet.
- `ressources/` — icons and images used by the interface.
- `tests/test_text_utils.py` — unit tests for the core string helpers.

## What this project demonstrates
This section is targeted to quickly show the concrete technical skills and practices you can evaluate when reviewing the repository:

- PyQt5 proficiency
  - Widget-based desktop UI with stacked navigation, custom forms and readable layout composition.
  - Event-driven interactions for shortcut capture, validation and script generation.

- Local configuration & data handling
  - Simple JSON persistence for user settings with a first-run bootstrap flow.
  - Defensive loading and saving logic to keep the app resilient to malformed config files.

- UI / UX craftsmanship
  - Dark themed interface with panels, badge-like labels and clear hierarchy.
  - Usability-focused elements such as shortcut capture, validation messages and one-click regeneration.

- Code separation & maintainability
  - Pure helper functions isolated in `text_utils.py` and covered by tests.
  - Clear separation between config handling, page logic and app bootstrap.

- Developer productivity & testing readiness
  - Small, deterministic helper functions that are easy to unit test.
  - PyInstaller build scripts and shell commands for packaging a distributable Windows app.

- Attention to detail for production-quality apps
  - Configurable output folder, fallback save dialog and graceful error handling around file generation.
  - Consistent UI state management across the first-run, settings and main dashboard screens.

## How to validate these skills quickly
- Run the app and complete the settings page to verify shortcut capture, validation and persistence.
- Open the main dashboard to confirm the saved shortcuts and the generated script path are displayed correctly.
- Inspect `config.py` to see the JSON persistence flow and first-run state management.
- Review `ui/settings_page.py` and `ui/main_page.py` to evaluate widget composition, validation and script generation.
- Run `pytest` to validate the core helper functions in `tests/test_text_utils.py`.

## Contributing
- Open an issue for bugs or feature requests.
- Fork the repo, create a feature branch and send a PR with a clear description and screenshots.
- Keep formatting consistent and add tests where relevant.

## Contact
Erwan Rossignol — erwan@hotmail.ch  
Project repository: https://github.com/E-Rossignol/dragoturkey_helper
