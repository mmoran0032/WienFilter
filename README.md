Wien Filter Monitor
===================

Terminal-based monitoring and control program for the St. GEORGE Wien Filter at
the Nuclear Science Lab at Notre Dame. The program allows simple monitoring of
both high voltage electrostatic plates and control over their values through
a friendly interface.


Overview
--------

St. GEORGE (Strong Gradient Electromagnetic Online Recoil separator for capture
Gamma ray Experiments) is a recoil separator in the NSL designed to study (α,γ)
reactions prevalent in astrophysical environments. The Wien Filter (henceforth
**WF**) is a velocity filter consisting of cross electric and magnetic fields.
Since the particles have already been filtered for their momentum, selecting a
velocity within the separator means that the WF acts as a mass filter,
transmitting the desired recoils and performing the final rejection of the beam
particles.

The magnets within St. GEROGE are controlled via a separate power supply, and
this includes the dipole magnet for the WF. The electrostatic plates are
controlled by two separate high voltage (**HV**) power supplies which set the
electric field within the WF. This is the only electrostatic element within St.
GEORGE.

When setting the WF for an experiment, the electric and magentic fields are set
to transmit the desired particles to the end of the separator, based on the beam
energy and desired recoil products.


Monitor Backend
---------------

The WF Monitor (`wf.py`) communicates with the HV power supplies through TCP
sockets via a serial server located within the St. GEORGE target room and behind
the Notre Dame firewall. For safety, the actual hosts and ports are not made
public.

Most commands query internal register values or change values held within those
registers. The `WFcontroller` handles passing those actual commands to the
`WFmodel`, while the user can input easy commands that are interpretted.


Limits
------

Nominal voltage limits for the power supplies are ±110 kV on each plate. A
hardware current limit was set at ±1 uA. Values outside of these limits should
be rejected by the power supply itself.


Debugging
---------

If need be, raw commands can be sent to either HV power supply. Since these are
just the actual commands that interface with the supplies, any command available
in the FuG Elektronik technical manual can be sent. Some helpful commands are
listed below, with *x = 0* being the voltage register and *x = 1* the current
register. All registers can be queried by appending a `?` after the register
name, and can be set by appending a value (unless the register is *Read Only*).

- `>Sx`: register set value

- `>SxA?`: actual value, integrated (Read Only)

- `>Mx?`: monitor value, non-integrated (Read Only)

- `>SxB`: ramp function type

- `>KS?`: power supply status (Read Only)

- `>DON?`: output release status (Read Only)

- `Fy`: release (`1`) or turn off (`0`) power supply output
