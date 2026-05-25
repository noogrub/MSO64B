# Gotchas

This file preserves bench lessons that should not clutter the short HOWTOs.

Keep each entry concise. A HOWTO should remain a clean path through one task. Gotchas belong here when they explain why a simple task may fail in practice.

## Probe-comp signal can disappear at ps/div time scale

The MSO64B probe-comp signal is a 1 kHz square wave.

A 1 kHz signal has a 1 ms period. If the horizontal scale is left at a few ps/div, the waveform will not look like a square wave.

Working setup observed on the CREATE MSO64B:

```text
Signal: MSO64B probe-comp output
Channel: CH2
Horizontal scale: 400 us/div
Trigger mode: Normal
Trigger source: CH2
Trigger type: Edge
Observed waveform: roughly 0 to 250 mV square wave
```

## Probe-comp ground is not the small female ground hole

The small female ground hole on the MSO64B front panel is not the probe-comp ground reference for ordinary passive-probe compensation.

For the probe-comp square wave, use the PROBE COMP terminals:

```text
Probe ground lead -> upper PROBE COMP ground tab
Probe tip -> lower 1 kHz PROBE COMP signal tab
```

The small female ground connector is for ESD/wrist-strap grounding.

## Passive probe needs a real ground lead

A passive probe without a usable ground lead is not a good probe-comp test setup.

It may show apparent noise because the signal has no proper return path.

Use a probe with a proper ground lead or an appropriate accessory for the MSO64B probe-comp terminals.
