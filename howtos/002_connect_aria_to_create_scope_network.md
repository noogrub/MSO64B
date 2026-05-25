# HOWTO 002: Connect Aria to the CREATE MSO64B Network

## Purpose

Connect Aria to the local CREATE instrument network through a docking station and verify communication with the Tektronix MSO64B.

This HOWTO documents a confirmed working bench setup.

## Confirmed bench result

Date recorded: 2026-05-25

Computer:

```text
Aria
```

Dock Ethernet adapter reported by Windows:

```text
Name: Ethernet 3
InterfaceDescription: Realtek USB GbE Family Controller
Status: Up
LinkSpeed: 1 Gbps
```

MSO64B network identity:

```text
Instrument: Tektronix MSO64B
Hostname: MSO64B-C062498
IP address: 192.168.1.11
Serial: C062498
Firmware: 2.16.15-release.3490
```

Successful PyVISA identity response:

```text
TEKTRONIX,MSO64B,C062498,CF:91.1CT FV:2.16.15-release.3490
```

## Network context

The CREATE scope switch appears to be a local instrument network with no DHCP server.

When Aria first connected through the docking station, Windows assigned a link-local address:

```text
169.254.41.109
```

That indicated that the physical Ethernet link was present, but no DHCP address was assigned.

## Step 1: Confirm the dock Ethernet adapter

In PowerShell:

```powershell
Get-NetAdapter
```

Confirmed adapter:

```text
Ethernet 3    Realtek USB GbE Family Controller    Up    1 Gbps
```

## Step 2: Assign Aria a static IPv4 address

Use PowerShell as Administrator:

```powershell
New-NetIPAddress -InterfaceAlias "Ethernet 3" -IPAddress 192.168.1.12 -PrefixLength 24
```

This places Aria on the same `/24` subnet as the MSO64B at `192.168.1.11`.

## Step 3: Ping the MSO64B

```powershell
ping 192.168.1.11
```

Confirmed result:

```text
Pinging 192.168.1.11 with 32 bytes of data:
Reply from 192.168.1.11: bytes=32 time<1ms TTL=64
Reply from 192.168.1.11: bytes=32 time=1ms TTL=64
Reply from 192.168.1.11: bytes=32 time=1ms TTL=64
Reply from 192.168.1.11: bytes=32 time=1ms TTL=64

Ping statistics for 192.168.1.11:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 0ms, Maximum = 1ms, Average = 0ms
```

## Step 4: Verify PyVISA access

Follow:

```text
howtos/001_setup_pyvisa_connection.md
```

Confirmed VISA resources:

```text
TCPIP::192.168.1.11::INSTR
TCPIP::192.168.1.11::hislip0,4880::INSTR
```

Use this resource for the scripts in this repository:

```text
TCPIP::192.168.1.11::INSTR
```

## What this proves

The complete control path works:

```text
Aria -> dock Ethernet -> CREATE switch -> MSO64B -> PyVISA resource
```

## Notes

Wi-Fi can remain enabled while using the dock Ethernet interface for the scope network. Aria can use Wi-Fi for internet access and `Ethernet 3` for the local MSO64B subnet at the same time.

The linked Tektronix Programmer Manual in the README may not match the installed firmware exactly. The confirmed CREATE scope firmware is:

```text
2.16.15-release.3490
```
