# HOWTO 001: Connect and Identify the MSO64B

## Purpose

Verify Ethernet communication with the Tektronix MSO64B.

This task asks the oscilloscope to identify itself using the SCPI command:

```text
*IDN?
```

A successful response confirms that the computer can reach the instrument over the network and that the instrument accepts SCPI commands.

## When to use this

Use this before any scripted MSO64B work.

This is the first check when:

- setting up a new computer
- moving to a different bench network
- confirming the scope IP address
- preparing to capture screenshots or waveform data
- teaching another lab member how scripted instrument access begins

## Required setup

- Tektronix MSO64B powered on
- Ethernet connected
- MSO64B IP address or hostname known
- Python 3 available on the control computer

## Script

```text
scripts/mso64b_id.py
```

## Command

From the repository root:

```bash
python scripts/mso64b_id.py --host 192.168.x.x
```

Replace `192.168.x.x` with the MSO64B IP address.

If the scope uses a non-default raw socket SCPI port:

```bash
python scripts/mso64b_id.py --host 192.168.x.x --port 4000
```

## Expected result

The script should print an identity string from the instrument. The exact response depends on the installed hardware and firmware.

A typical response includes:

```text
TEKTRONIX,<model>,<serial>,<firmware>
```

## What this teaches

The MSO64B can be treated as a network instrument.

Once the identity query works, later tasks can use the same communication path to capture screenshots, save waveform data, and configure repeatable measurements.

## Troubleshooting

If the script times out:

- Confirm the scope is powered on.
- Confirm the Ethernet cable or lab network path.
- Confirm the IP address.
- Confirm that the control computer can reach the scope with `ping` if ICMP is allowed.
- Confirm that the selected TCP port is correct for the scope configuration.

If the connection is refused:

- The scope may not have raw socket SCPI enabled.
- The port may be different from the default used by the script.
- The network may block the connection.

## FieldNet_PLL relevance

This is the first repeatability check for using the MSO64B as part of FieldNet_PLL bench work.

A working identity query gives us a stable starting point for later PLL capture procedures.
