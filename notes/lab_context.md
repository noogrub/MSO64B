# Lab Context

This repository supports practical Tektronix MSO64B use in the CREATE lab.

The immediate project driver is FieldNet_PLL work. MSO64B notes should be added when the bench work creates a real need for a scope capability.

The repo is public so colleagues can read and reuse the notes. Keep procedures concise, reproducible, and safe for shared lab use.

## Working rule

When FieldNet_PLL needs a scope capability, add the smallest useful note for that capability.

Each note should answer:

1. What task does this perform?
2. When should a lab member use it?
3. What command or front-panel action is required?
4. What result should they expect?
5. What does this teach about the MSO64B?

## Interface rule

Use PyVISA with `pyvisa-py` for scripted control.

Confirmed CREATE bench resource:

```text
TCPIP::192.168.1.11::INSTR
```

## Style

Use direct technical prose. Prefer documented SCPI commands through PyVISA, filenames, and observable results. Avoid relying on memory of touch-screen menu locations when a script or saved setup can make the task repeatable.

## Early task sequence

Planned early tasks:

1. Set up PyVISA access to the MSO64B.
2. Connect Aria to the CREATE instrument network.
3. Save the current screen image on the MSO64B using `SAVE:IMAGE`.
4. Retrieve the saved screen image using `FILESystem:READFile`.
5. Export a waveform for Python analysis.
6. Configure a basic edge trigger.
7. Configure a pulse-width trigger.

These tasks should be added as the bench work needs them.
