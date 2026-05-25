# MSO64B

Concise Tektronix MSO64B working notes for CREATE lab use.

This repository preserves small, repeatable oscilloscope tasks as HOWTOs and scripts. The goal is to keep MSO64B knowledge available to the lab after individual students graduate, without relying on one person as the permanent menu expert.

The working pattern is simple:

- One bench task
- One short HOWTO
- One small script when useful
- One lab-meeting-ready explanation

The first target is Ethernet communication with the instrument. Once that works, later notes can cover screenshots, waveform export, edge triggering, pulse-width triggering, and FieldNet_PLL capture examples.

## Repository layout

```text
howtos/     Short task-focused instructions
scripts/    Small Python utilities for repeatable instrument actions
notes/      Lab context and project-level notes
```

## Starting point

Begin with:

```text
howtos/001_connect_and_identify_scope.md
scripts/mso64b_id.py
```

That first task verifies that a computer can communicate with the MSO64B over Ethernet and ask the instrument to identify itself using the SCPI command `*IDN?`.

## Intended audience

This repository is for CREATE lab members who need practical MSO64B procedures during bench work. It favors clear text, reproducible commands, and small examples over menu memorization.
