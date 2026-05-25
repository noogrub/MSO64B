
# HOWTO 003: Save an MSO64B Screen Image

## Purpose

Save the current MSO64B screen image using PyVISA and the documented SCPI command `SAVE:IMAGE`.

This procedure saves the image on the oscilloscope filesystem.

## Required setup

- PyVISA access confirmed with `howtos/001_setup_pyvisa_connection.md`
- MSO64B screen showing the view to capture

## Script

```text
scripts/mso64b_save_image.py
```

## Command

```powershell
python scripts/mso64b_save_image.py --label probe-comp-ch2
```

## Default behavior

Default VISA resource:

```text
TCPIP::192.168.1.11::INSTR
```

Default scope-side output directory:

```text
C:/
```

Default generated filename pattern:

```text
YYYYMMDD-HHMMSS_mso64b_<label>.png
```

Example generated scope-side path:

```text
C:/20260525-183742_mso64b_probe-comp-ch2.png
```

## Exact output path

To force a specific scope-side filename:

```powershell
python scripts/mso64b_save_image.py --scope-path "C:/CREATE_test.png"
```

## Confirmed CREATE result

The save command reports success when `*OPC?` returns `1`.

Example:

```text
Connected to: TEKTRONIX,MSO64B,C062498,CF:91.1CT FV:2.16.15-release.3490
Sending: SAVE:IMAGE "C:/20260525-183742_mso64b_probe-comp-ch2.png"
*OPC? response: 1
Saved screen image on scope: C:/20260525-183742_mso64b_probe-comp-ch2.png
```

## Retrieve next

Use `howtos/004_retrieve_screen_image.md` to list files on the scope and retrieve the saved PNG.
