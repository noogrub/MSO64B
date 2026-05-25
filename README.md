# MSO64B

Concise Tektronix MSO64B working notes for CREATE lab use.

This repository preserves small, repeatable oscilloscope tasks as HOWTOs and scripts. The goal is to keep MSO64B knowledge available to the lab after individual students graduate, without relying on one person as the permanent menu expert.

## Working method

Use PyVISA with the pure-Python backend `pyvisa-py` for scripted control.

Confirmed CREATE bench resource:

```text
TCPIP::192.168.1.11::INSTR
```

Confirmed instrument identity:

```text
TEKTRONIX,MSO64B,C062498,CF:91.1CT FV:2.16.15-release.3490
```

## Repository layout

```text
howtos/       Short task-focused instructions
scripts/      Small Python utilities for repeatable instrument actions
notes/        Lab context and project-level notes
img/          Local retrieved images; ignored by git
requirements.txt
```

## Starting point

Begin with:

```text
howtos/001_setup_pyvisa_connection.md
howtos/003_save_screen_image.md
howtos/004_retrieve_screen_image.md
```

The confirmed screenshot path is:

```text
SAVE:IMAGE "C:/CREATE_test.png"
FILESystem:READFile "C:/CREATE_test.png"
local output: img/CREATE_test.png
```

## Official Tektronix documentation

Official Tektronix documentation is the source of truth for instrument limits, command syntax, and remote-control behavior.

- [5/6 Series MSO Programmer Manual, including MSO64](https://download.tek.com/manual/5_6-Series-MSO54-MSO56-MSO58-MSO58L-MSO64-Programmer-Manual_EN-US_077130505.pdf)
- [5/6 Series MSO Printable Help, including MSO64](https://download.tek.com/manual/5-6-Series-MSO-MSO54-MSO56-MSO58LP-MSO64-Printable-Help_EN-US_077130303.pdf)

This repository should link to vendor documentation rather than storing local copies of Tektronix PDFs.

## Intended audience

This repository is for CREATE lab members who need practical MSO64B procedures during bench work. It favors clear text, reproducible commands, and small examples over menu memorization.
