# HOWTO 004: Retrieve an MSO64B Screen Image

## Purpose

Retrieve a file from the MSO64B filesystem using PyVISA and the documented SCPI command `FILESystem:READFile`.

This procedure copies the image saved by `SAVE:IMAGE` from the scope to the local computer.

## Required setup

- PyVISA access confirmed with `howtos/001_setup_pyvisa_connection.md`
- A scope-side image saved with `howtos/003_save_screen_image.md`

## Script

```text
scripts/mso64b_retrieve_file.py
```

## Command

```powershell
python scripts/mso64b_retrieve_file.py
```

Default VISA resource:

```text
TCPIP::192.168.1.11::INSTR
```

Default scope-side input path:

```text
C:/CREATE_test.png
```

Default local output path:

```text
img/CREATE_test.png
```

The `img/` directory is ignored by git.

## Confirmed result

The retrieved file opens as a valid PNG image of the MSO64B display.

The confirmed test image showed the probe-comp waveform on CH2, roughly 0 to 250 mV, with the display set to 400 us/div.

## Command pair

To save and retrieve the current screen:

```powershell
python scripts/mso64b_save_image.py
python scripts/mso64b_retrieve_file.py
```
