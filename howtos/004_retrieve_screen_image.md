
# HOWTO 004: Retrieve an MSO64B Screen Image

## Purpose

List or retrieve files from the MSO64B filesystem using PyVISA and the documented SCPI commands `FILESystem:DIR?` and `FILESystem:READFile`.

This procedure copies an image saved by `SAVE:IMAGE` from the scope to the local computer.

## Required setup

- PyVISA access confirmed with `howtos/001_setup_pyvisa_connection.md`
- A scope-side image saved with `howtos/003_save_screen_image.md`

## Script

```text
scripts/mso64b_retrieve_file.py
```

## List files on the scope

```powershell
python scripts/mso64b_retrieve_file.py --list
```

Default scope-side directory:

```text
C:/
```

To list a different scope-side directory:

```powershell
python scripts/mso64b_retrieve_file.py --list --scope-dir "C:/Temp"
```

## Retrieve a named file

```powershell
python scripts/mso64b_retrieve_file.py --scope-path "C:/20260525-183742_mso64b_probe-comp-ch2.png"
```

By default, the local file is written to:

```text
img/<same-filename>
```

Example:

```text
img/20260525-183742_mso64b_probe-comp-ch2.png
```

The `img/` directory is ignored by git.

## Exact local output path

```powershell
python scripts/mso64b_retrieve_file.py --scope-path "C:/CREATE_test.png" --output "img/CREATE_test.png"
```

## Confirmed result

The retrieved file opens as a valid PNG image of the MSO64B display.

The confirmed test image showed the probe-comp waveform on CH2, roughly 0 to 250 mV, with the display set to 400 us/div.

## Command sequence

Typical save/list/retrieve workflow:

```powershell
python scripts/mso64b_save_image.py --label probe-comp-ch2
python scripts/mso64b_retrieve_file.py --list
python scripts/mso64b_retrieve_file.py --scope-path "C:/YYYYMMDD-HHMMSS_mso64b_probe-comp-ch2.png"
```
