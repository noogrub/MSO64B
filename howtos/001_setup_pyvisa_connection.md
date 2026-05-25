# HOWTO 001: Set Up PyVISA Access to the MSO64B

## Purpose

Verify that Python can communicate with the Tektronix MSO64B through PyVISA.

## Required setup

- Tektronix MSO64B powered on
- Aria connected to the CREATE instrument switch
- Aria Ethernet address configured on the `192.168.1.x` subnet
- Python environment with `pyvisa` and `pyvisa-py`

## Install requirements

From the repository root:

```powershell
python -m pip install -r requirements.txt
```

## Confirm PyVISA backend

```powershell
python -c "import pyvisa; rm=pyvisa.ResourceManager('@py'); print(rm); print(rm.list_resources())"
```

Confirmed CREATE result:

```text
Resource Manager of Visa Library at py
('TCPIP::192.168.1.11::INSTR', 'TCPIP::192.168.1.11::hislip0,4880::INSTR')
```

## Confirm instrument identity

```powershell
python -c "import pyvisa; rm=pyvisa.ResourceManager('@py'); scope=rm.open_resource('TCPIP::192.168.1.11::INSTR'); scope.timeout=5000; print(scope.query('*IDN?'))"
```

Confirmed CREATE result:

```text
TEKTRONIX,MSO64B,C062498,CF:91.1CT FV:2.16.15-release.3490
```

## What this proves

The control computer can reach the MSO64B through the documented VISA-style interface.

Use this PyVISA path for scripts in this repository.
