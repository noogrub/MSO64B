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
python scripts/mso64b_save_image.py
```

Default VISA resource:

```text
TCPIP::192.168.1.11::INSTR
```

Default scope-side output path:

```text
C:/CREATE_test.png
```

## Confirmed CREATE result

```text
Connected to: TEKTRONIX,MSO64B,C062498,CF:91.1CT FV:2.16.15-release.3490
Sending: SAVE:IMAGE "C:/CREATE_test.png"
*OPC? response: 1
Saved screen image on scope: C:/CREATE_test.png
```

## Notes

This HOWTO intentionally stops at saving the image on the oscilloscope.

File readback to the computer should be added only after the readback procedure is confirmed cleanly through PyVISA and documented separately.
