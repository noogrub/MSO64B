# HOWTO 005: Run the Local MSO64B Bench UI

## Purpose

Run a local browser UI for quick MSO64B screenshot capture and retrieval.

The UI runs only on localhost:

```text
http://127.0.0.1:5000
```

## Required setup

- PyVISA access confirmed with `howtos/001_setup_pyvisa_connection.md`
- Python requirements installed from `requirements.txt`
- Aria connected to the CREATE MSO64B network

## Install requirements

```powershell
python -m pip install -r requirements.txt
```

## Run the UI on Windows

Double-click:

```text
run_mso64b_ui.bat
```

Then open:

```text
http://127.0.0.1:5000
```

## Run the UI from PowerShell

```powershell
python scripts/mso64b_ui.py
```

## Features in this first version

- Shows instrument identity
- Lists files in the scope-side directory
- Captures and retrieves a screenshot in one click
- Retrieves a selected scope-side file
- Displays local retrieved images from `img/`

## Design note

The UI calls reusable functions in:

```text
mso64b/instrument.py
mso64b/naming.py
mso64b/config.py
```

This keeps the instrument-control code separate from the UI layer. A later FastAPI or WebSocket UI can reuse the same modules.
