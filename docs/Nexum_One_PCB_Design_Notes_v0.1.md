# Nexum One EEG-Sense Headband — PCB Design Notes

**v0.1** · 2026-06-21  
**Author:** EE Team · Hardware Working Group  
**Classification:** Internal — Engineering  
**Target Audience:** PCB Layout Engineer

---

## Table of Contents

1. Document Scope and Reference Documents
2. PCB Stackup Recommendation
3. Component Placement Strategy
4. Grounding Strategy
5. Routing Rules for EEG Signals
6. Power Supply Design
7. Electrode Connector Design
8. EMI/EMC Considerations
9. Flex PCB Considerations for Curved Headband
10. Key Layout Constraints and Keep-Out Zones
11. Test Points and Debug Interface
12. Appendix: Reference Schematic Fragment Guidelines

---

## 1. Document Scope and Reference Documents

### 1.1 Scope

This document provides the PCB layout engineer with specific, actionable instructions for laying out the Nexum One EEG-Sense headband PCB (and associated flex PCB for electrodes). It covers a single 8-channel dry-electrode EEG acquisition board with the following bill of materials:

- **U1:** TI ADS1299IPAG — 8-ch EEG AFE, 24-bit delta-sigma ADC
- **U2:** Nordic nRF52832-QFAA — BLE 5.0 SoC (Cortex-M4F)
- **U3:** TPS7A4700RGWT — ultra-low-noise 3.3V LDO (analog supply, 1 uVrms noise)
- **U4:** TPS7A2005PDBVR — 1.8V LDO (ADS1299 DVDD)
- **U5:** BQ24075RGTT — Li-Po linear charger with power-path management
- **Y1:** ABS05-32.768KHZ-T — 32.768 kHz RTC crystal (nRF52)
- **Y2:** NX3225SA-32MHZ — 32 MHz main crystal (nRF52)
- **ANT1:** 2450AT18A100E — Johanson 2.4 GHz chip antenna
- **J1:** TYPE-C-31-M-12 — USB-C connector (charge + data)
- **BT1:** 402030 Li-Po pouch cell, 200 mAh, 3.7V

### 1.2 Reference Documents

| Document | Purpose |
|----------|---------|
| ADS1299 Datasheet (SBAS499K) | ADC timing, analog input characteristics, recommended layout |
| nRF52832 Product Spec v1.4 | BLE RF layout guidelines, antenna matching network |
| TPS7A4700 Datasheet (SBVS219) | LDO noise spec, output capacitor ESR requirements |
| Nexum One Engineering Architecture v0.1 | System-level block diagram, data flow, latency budgets |
| Nexum One PRD v1.0 | Requirements for noise, CMRR, weight, form factor |

### 1.3 Key Performance Targets That Drive Layout Decisions

| Parameter | Target | Layout Implication |
|-----------|--------|--------------------|
| Input-referred noise | <1 uV RMS (0.5-100 Hz) | No switching noise coupling into analog inputs |
| CMRR | >100 dB at 50 Hz | Symmetrical routing for INxP/INxN pairs, guard rings |
| Weight | <80 g including battery | PCB size minimized; 4-layer not 6-layer; no unnecessary connectors |
| BLE range | >5 m through body | Antenna keep-out zone strictly enforced |
| Battery life | >4 h continuous | Low-resistance power path; no parasitic leakage |

---

## 2. PCB Stackup Recommendation

### 2.1 Stackup: 4-Layer, 0.8 mm Total Thickness

Use JLCPCB or PCBWay standard 4-layer stackup with **JLC7628 prepreg** or equivalent. Total thickness **0.8 mm** (1.0 mm also acceptable, but heavier).

| Layer | Name | Type | Thickness | Cu Weight | Notes |
|-------|------|------|-----------|-----------|-------|
| L1 | TOP | Signal + Components | 0.035 mm | 1 oz | All active components, analog routing, RF trace |
| --- | Prepreg | Dielectric (FR-4) | 0.200 mm | --- | Specify 0.2 mm prepreg for tight L1-L2 coupling |
| L2 | GND | Solid Ground Plane | 0.035 mm | 1 oz | **No split under analog section.** Continuous return path. |
| --- | Core | Dielectric (FR-4) | 0.300 mm | --- | Core thickness sets L2-L3 capacitance |
| L3 | PWR + SIG | Power + Signal | 0.035 mm | 1 oz | Power distribution traces; low-speed digital signals |
| --- | Prepreg | Dielectric (FR-4) | 0.200 mm | --- | |
| L4 | BOT | Signal + GND | 0.035 mm | 1 oz | Component landing (decoupling caps on bottom), pour for GND |

**Rationale for 4-layer over 2-layer:**
- A continuous ground plane (L2) directly under L1 is the single most important factor for EEG SNR. A 2-layer board cannot provide this.
- L3 provides dedicated power routing without cutting up the ground plane.
- 0.8 mm total keeps the board flexible enough for slight headband curvature (semi-rigid section). Do not use 1.6 mm — too stiff to conform.

**Stackup variation for flex-rigid (see Section 9):** If a rigid-flex design is used, the flex portion is 2-layer (L1/L2 only, no L3/L4), transitioning to the full 4-layer stackup in the rigid main-board region.

### 2.2 Impedance Control

| Trace | Impedance | Layer | Width (JLC7628, 1 oz) | Notes |
|-------|-----------|-------|----------------------|-------|
| BLE antenna trace | 50 Ohm single-ended | L1 (TOP) | 0.35 mm (with 0.2 mm GND clearance on both sides) | Coplanar waveguide with GND on L2 |
| SPI bus (SCLK) | Not critical (<30 MHz) | L1 or L4 | 0.25 mm minimum | Match ADS1299 SCLK--nRF52 lengths within 10 mm |

---

## 3. Component Placement Strategy

### 3.1 Partition: Analog Zone vs Digital Zone

The PCB is divided into **three zones** with a clear boundary. Crossing a zone boundary requires a bridge trace over the ground plane — never cut the ground plane.

```
                        +-------------------------------------+
                        |           HEADBOARD PCB              |
                        |                                     |
 +----------------------+   ZONE A (ANALOG -- LEFT SIDE)       |
 |                      |                                     |
 |   ANALOG REGION      |  +---------+  +------------------+  |
 |   (Left 40% of PCB)  |  |  U1     |  |  U3 (TPS7A4700)  |  |
 |                      |  | ADS1299 |  |  3.3V Analog LDO  |  |
 |                      |  |         |  |  C4, C5, C6       |  |
 |   | Electrode FPC    |  +----+----+  +------------------+  |
 |   | connector (J2)   |  +----+----+  +------------------+  |
 |   | IN1P/IN1N...     |  |  U4     |  |  REF3125 (U6)    |  |
 |   | BIAS/DRL         |  |TPS7A2005|  |  2.5V Reference  |  |
 |   | SRB1/SRB2        |  | 1.8V    |  |  C7, C8          |  |
 |                      |  +---------+  +------------------+  |
 +----------------------+                                     |
                        |  <-- GROUND BRIDGE ZONE -->         |
 +----------------------+  (No components. Solid GND pour.)   |
 |                      |                                     |
 |   DIGITAL REGION     |  +---------+  +----------+          |
 |   (Right 60% of PCB) |  |  U2     |  |  U5      |          |
 |                      |  |nRF52832 |  |BQ24075   |          |
 |                      |  |         |  |Charger   |          |
 |                      |  +----+----+  +----------+          |
 |   | BLE Antenna      |  +----+----+  +----------+          |
 |   | (ANT1, keep-out) |  | Y1,Y2   |  | J1       |          |
 |   |                  |  |Crystals |  | USB-C    |          |
 |   |  BT1 (battery    |  +---------+  +----------+          |
 |   |  connector)      |                                     |
 |                      |                                     |
 +----------------------+                                     |
                        +-------------------------------------+
```

### 3.2 Placement Rules (in order of priority)

**RULE P1 -- Analog components on Left, Digital on Right:**
- U1 (ADS1299) is the **center of the analog zone**. Place it as close to the electrode connector (J2) as physically possible. Target center-to-center distance between J2 and U1 < 15 mm.
- U3 (TPS7A4700, analog 3.3V regulator) must be within 20 mm of U1 AVDD pin. Output cap C4 (10 uF) must be <5 mm from U3 output pin.
- U4 (TPS7A2005, 1.8V ADC DVDD regulator) must be within 15 mm of U1 DVDD pin.
- U6 (REF3125, 2.5V reference) must be within 10 mm of U1 VREFP pin (pin 21 on TQFP-64).
- All decoupling caps for U1 must be on the **same layer** as U1 (L1 TOP), directly adjacent to the power pins. Do not place them on L4 bottom -- via inductance degrades decoupling at EEG frequencies where 1/f noise matters.

**RULE P2 -- BLE antenna is the most placement-critical RF element:**
- ANT1 must be at the **outer edge of the board**, with no copper (L1, L2, L3, L4) in the keep-out zone. See Section 10 for keep-out dimensions.
- nRF52832 (U2) must be positioned so that the antenna trace from pin P0.09 (ANT) to ANT1 is <25 mm and has no vias.
- The antenna region must not be under the battery (BT1). Battery GND plane parasitics detune the antenna.

**RULE P3 -- Battery and charger placement:**
- BT1 (battery connector) should be at the edge of the digital zone, oriented so the battery cable exits toward the back of the head (user comfort).
- U5 (BQ24075) must have its thermal pad (PowerPAD) connected to L2 GND with at least 6 thermal vias. Charger generates heat during CC/CV cycle -- locate away from ADS1299.
- USB-C connector J1 at board edge, right side. Keep the CC1/CC2 lines as short as possible (<20 mm) to BQ24075.

**RULE P4 -- Crystal placement for nRF52:**
- Y1 (32.768 kHz) and Y2 (32 MHz) must be placed within **5 mm** of nRF52832 XC1/XC2 pins. No other traces may cross under the crystal footprint.
- Ground pour under crystals on L1. No vias within 2 mm of crystal pads.

**RULE P5 -- Ground bridge zone:**
- A 2-3 mm wide strip across the PCB (perpendicular to the analog-digital boundary) must be **free of all components** to allow a solid copper flood connection between left and right ground regions. This strip acts as a low-impedance return path stitching the two zones.

### 3.3 Component Clearance Matrix

| From | To | Min Clearance | Reason |
|------|----|---------------|--------|
| ADS1299 | Switching regulator (any) | 15 mm | Prevent coupled switching noise into high-impedance ADC inputs |
| BLE antenna | Battery | 10 mm | Antenna detuning |
| BLE antenna | USB-C connector | 10 mm | Ground plane disruption near antenna |
| BLE antenna | ADS1299 | 20 mm | RF emissions coupling into EEG band (unlikely but conservative) |
| Crystal (Y1, Y2) | Any high-current trace | 5 mm | EMI coupling to crystal |
| SPI bus (SCLK, MOSI) | Analog INxP/INxN | 5 mm | Digital crosstalk into EEG channels |

---

## 4. Grounding Strategy

### 4.1 Single Ground Plane -- NOT Split

**There is one ground plane on L2 for the entire board.** Do NOT split the ground plane into analog and digital sections. The reasons:

1. A split ground plane creates a slot antenna that radiates digital noise. This is catastrophic for EEG -- you will see 50 Hz harmonics everywhere.
2. The ADS1299 datasheet explicitly states: "Do not split the ground plane. Use a single solid ground plane."
3. With proper component placement (Section 3), digital return currents do not flow through the analog region because the return path is directly under the signal trace.

### 4.2 Star Grounding for Analog Circuits

While the ground plane is one piece, analog signal returns must follow a **star-ground topology**:

```
                 +----------------------------------+
                 |          L2 GND PLANE             |
                 |                                  |
                 |  +------------+                   |
                 |  |  Analog    |  (Low-impedance   |
    +-----+----->  |  Star Point|   connection to    |
    | ADS |       |  |  (under   |   L2 pour)        |
    |1299 |       |  |  ADS1299) |                    |
    |     |----+  |  +-----+------+                   |
    |     |    |  |        |                          |
    +-----+    |  |        |                          |
    U1 GND pad |  |  +-----+------+                   |
    (thermal   |  |  |  Analog    |  All analog        |
     vias to   |  |  |  LDO GND   |  circuits return   |
     L2)       |  |  |  (U3 TPS)  |  to star point     |
               |  |  +------------+  via individual    |
               |  |                   traces to star   |
               |  |  +------------+  (not daisy-chained)|
               |  |  |  REF GND   |                     |
               |  |  |  (U6 REF)  |                     |
               |  |  +------------+                     |
               |  |  +------------+                     |
               |  |  |  DVDD GND  |                     |
               |  |  |  (U4 TPS)  |                     |
               |  |  +------------+                     |
               +----------------------------------------+
```

Implementation:
- Connect U1's exposed thermal pad (GND) to L2 with 9 thermal vias (3x3 grid, 0.3 mm hole). This is the analog star point.
- Connect U3 (TPS7A4700) GND pad to L2 through 4 vias directly adjacent to its PowerPAD, within 3 mm of the U1 star point.
- Connect U6 (REF3125) GND pin to L2 via a dedicated trace and via, not through a daisy chain from U3.
- Digital ground (nRF52, charger, USB-C) connects to L2 naturally through their vias. No need to segregate.

### 4.3 Thermal Pad Stitching for ADS1299

The ADS1299 TQFP-64 has an exposed PowerPAD on the bottom. This pad is **GND** and must be soldered to L1 copper and stitched to L2 ground with a 3x3 array of vias (9 total, 0.3 mm hole, 0.5 mm pitch, tented on bottom). Failure to do this will result in:
- Increased thermal resistance (ADC drift with temperature)
- Increased ground inductance (noise coupling)
- Poor mechanical reliability (pad lifts during thermal cycling)

### 4.4 Star Ground via Solder Bridge (Optional but Recommended)

For prototype boards, include a **solder-bridge jumper** between analog star ground and main ground (two adjacent 0.5 mm pads with a trace that can be cut). This allows you to:
- Measure noise with split ground during debug
- Optionally insert a ferrite bead (0 Ohm for production, 600R @ 100 MHz for debug)
- Confirm that a single ground plane is indeed optimal for your specific layout

**Production recommendation:** Close the jumper (direct copper connection). No ferrite bead.

---

## 5. Routing Rules for EEG Signals

### 5.1 ADS1299 Analog Input Routing (IN1P-IN8P, IN1N-IN8N)

Each EEG channel is a **differential pair** (INxP, INxN). The ADS1299 measures the difference INxP - INxN. All 8 channel pairs must be routed with extreme care.

```
                 TOP VIEW (L1)

    +------------------------------------------------+
    |                                                |
    |  J2 (FPC connector)                            |
    |  +----------------------------------------+    |
    |  |  1  IN1P ------------------------------>|    |
    |  |  2  IN1N ------------------------------>|    |
    |  |  3  IN2P ------------------------------>|    |
    |  |  4  IN2N ------------------------------>|    |
    |  |  5  IN3P ------------------------------>|    |
    |  |  6  IN3N ------------------------------>| U1 |
    |  |  7  IN4P ------------------------------>|ADS |
    |  |  8  IN4N ------------------------------>|1299|
    |  |  9  IN5P ------------------------------>|    |
    |  |  10 IN5N ------------------------------>|    |
    |  |  11 IN6P ------------------------------>|    |
    |  |  12 IN6N ------------------------------>|    |
    |  |  13 IN7P ------------------------------>|    |
    |  |  14 IN7N ------------------------------>|    |
    |  |  15 IN8P ------------------------------>|    |
    |  |  16 IN8N ------------------------------>|    |
    |  |  17 BIAS_OUT -------------------------->|    |
    |  |  18 SRB1 ------------------------------>|    |
    |  |  19 GND_FLEX -------------------------->|    |
    |  |  20 GND_FLEX -------------------------->|    |
    |  +----------------------------------------+    |
    |                                                |
    |  KEEP ZONE: All 16 traces routed               |
    |  on L1. No vias, no layer change.              |
    |  Total length: 8-15 mm.                        |
    +------------------------------------------------+
```

**Routing Rules for Analog Inputs:**

| Rule | Requirement | Enforcement |
|------|-------------|-------------|
| R-A1 | Route INxP and INxN as parallel traces, matched length within 0.5 mm | Manual measurement in EDA |
| R-A2 | Trace width: 0.2 mm (8 mil) | DRC rule |
| R-A3 | Spacing between P and N of same channel: 0.2 mm (edge-to-edge) | DRC rule |
| R-A4 | Spacing between different channels: 0.4 mm minimum | DRC rule |
| R-A5 | **Guard trace** on both sides of each differential pair, connected to GND | Pour copper |
| R-A6 | No 90-degree corners. Use 45-degree chamfer or arc bends only | Manual inspection |
| R-A7 | No vias on analog input traces. Ever. Stay on L1 from J2 to U1. | DRC rule |
| R-A8 | Length of all 16 traces must be within 5 mm of each other (channel-to-channel skew) | Match group constraint |

**Guard trace implementation** (Rule R-A5):

```
    L1 Copper pour: GND
    +-------------------------------------------------+
    |  GND    |  IN1P  |  GND  |  IN1N  | GND        |
    |  pour   |  0.2mm | guard |  0.2mm | pour       |
    |         |        |  0.2  |        |            |
    |         |        |  mm   |        |            |
    +-------------------------------------------------+
    Each channel pair is sandwiched by GND guard traces.
    Guard traces are connected to L2 GND via 0.3mm vias
    every 3mm.
```

### 5.2 BIAS/DRL Output Routing

The BIAS_OUT pin (pin 17 of J2) is the Driven Right Leg (DRL) output. It is an **active feedback** node that drives common-mode voltage to the reference voltage.

- Route BIAS_OUT on L1, width 0.3 mm
- Keep at least 2 mm away from any INxP/INxN trace
- Do NOT place a guard trace between BIAS and signal traces -- the guard would increase parasitic capacitance on the bias loop, degrading phase margin
- The bias electrode (connected to BIAS_OUT) is placed on the user's right mastoid or forehead (electrode 9) -- the DRL loop goes through the body and back to ADC inputs

### 5.3 SRB1/SRB2 Routing

SRB1 (pin 19 on J2) and SRB2 (pin 20 on J2) are switched reference busses. Only one SRB is needed for common reference (SRB1 active, SRB2 tied to GND via 10k resistor).

- Route SRB1 from J2 to U1 SRB1 pin (pin 19 of ADS1299 TQFP-64) with 0.3 mm trace
- Keep away from digital traces. 2 mm clearance minimum.

### 5.4 SPI Bus Routing to nRF52

The ADS1299 communicates with nRF52832 over SPI:

| Signal | ADS1299 Pin | nRF52832 Pin | Max Length | Notes |
|--------|-------------|---------------|------------|-------|
| SCLK   | 28 (SCLK)   | P0.12 (SPI_SCK) | 40 mm | Match DOUT/DOUTB within 10 mm |
| DOUT   | 30 (DOUT)   | P0.13 (SPI_MISO) | 40 mm | ADC MISO |
| DIN    | 31 (DIN)    | P0.14 (SPI_MOSI) | 40 mm | ADC MOSI |
| CS     | 29 (CS)     | P0.15 (SPI_CS) | 40 mm | Active low |
| DRDY   | 27 (DRDY)   | P0.16 (GPIO_IRQ) | 30 mm | Data ready interrupt |

- SPI traces: 0.2 mm width, 0.2 mm spacing
- No series termination resistors needed at <1 MHz SCLK (ADS1299 max SCLK = 20 MHz, we run at 8 MHz)
- Route SCLK with a **ground trace alongside** (0.2 mm guard trace between SCLK and DOUT) to minimize crosstalk from the clock into the data line

### 5.5 Lead-Off Detection (Optional, P1)

ADS1299 supports lead-off detection (current injection through electrode to check poor contact). If implemented:
- Route the LOFF drive signals (LOFF_P, LOFF_N) away from analog inputs. Minimum 1 mm clearance.
- J2 should have LOFF connections on spare FPC pins if this feature is needed.

---

## 6. Power Supply Design

### 6.1 Power Tree

```
    +---------------------------------------------------------------------+
    |                          POWER TREE                                 |
    |                                                                     |
    |   +----------+    +--------------+    +--------------------------+  |
    |   | Li-Po    |    |  U5          |    |  USB 5V (from charger)  |  |
    |   | 3.7V     |--->|  BQ24075     |--->|  (USB-C, J1)            |  |
    |   | 200mAh   |    |  Battery     |    |                          |  |
    |   | (BT1)    |    |  Charger     |    |  5V rail available only  |  |
    |   +----------+    +------+-------+    |  during charging         |  |
    |                          |            +--------------------------+  |
    |                          | BAT_OUT (3.7-4.2V)                      |
    |                          v                                          |
    |               +----------------------+                              |
    |               |   3.3V ANALOG RAIL   |   3.3V DIGITAL RAIL          |
    |               | (AVDD -- ADS1299,    |   (nRF52 VDD, SPI, misc)    |
    |               |  analog LDO ref)     |                              |
    |               |                      |                              |
    |               |  U3: TPS7A4700       |  nRF52 has integrated        |
    |               |  Input: BAT_OUT      |  DC-DC buck and LDO.        |
    |               |  Output: 3.3V        |  See Section 6.2.           |
    |               |  Iout: 200 mA max    |                              |
    |               |  Noise: 1 uVrms      |                              |
    |               +----------+-----------+                              |
    |                          |                                          |
    |                          v                                          |
    |               +----------------------+                              |
    |               |   1.8V DVDD RAIL     |                              |
    |               |                      |                              |
    |               |  U4: TPS7A2005       |                              |
    |               |  Input: AVDD_3.3V    |                              |
    |               |  Output: 1.8V        |                              |
    |               |  Iout: 50 mA         |                              |
    |               +----------------------+                              |
    |                                                                     |
    |               +----------------------+                              |
    |               |  2.5V REFERENCE      |                              |
    |               |                      |                              |
    |               |  U6: REF3125         |                              |
    |               |  Input: AVDD_3.3V    |                              |
    |               |  Output: 2.5V        |                              |
    |               |  VREFP input (U1)    |                              |
    |               +----------------------+                              |
    +---------------------------------------------------------------------+
```

### 6.2 nRF52832 Power Routing

The nRF52832 has an integrated DC-DC buck converter. This converter is a **source of switching noise** -- do not let it couple into the analog section.

**Power pin connections for nRF52:**

| Pin | Name | Connect To | Decoupling |
|-----|------|-----------|------------|
| 4   | VDD  | Digital 3.3V (from nRF52 internal LDOOUT) | 100 nF + 10 uF |
| 11  | VDD  | Digital 3.3V | 100 nF |
| 13  | DEC1 | Internal reg -- external 100 nF only | 100 nF to GND |
| 14  | DEC2 | Internal reg -- external 100 nF only | 100 nF to GND |
| 17  | DEC3 | Internal reg -- external 100 nF only | 100 nF to GND |
| 26  | VDD  | Digital 3.3V | 100 nF |
| 35  | VDD  | Digital 3.3V | 100 nF |
| 44  | VDD  | Digital 3.3V | 100 nF |
| 47  | DEC4 | Internal reg -- external 100 nF only | 100 nF to GND |
| 49  | VDD  | Digital 3.3V | 100 nF |

**Critical:** The nRF52 DC-DC inductor (L1, 10 uH, e.g., Murata LQM18PN100M00) must be placed within 5 mm of pins 18 (VDD) and 19 (DEC4 -- SW output). The inductor's AC current path goes through the VDD pin -- this is where most switching noise radiates. Place the inductor on L1 with its own GND via farm (3 vias under the inductor pad). Keep this inductor **at least 15 mm** from ADS1299.

### 6.3 Power Rail Sequencing

The ADS1299 has no strict power sequencing requirement (see datasheet Section 9.2.1.2). However, to avoid latch-up at power-on:

1. AVDD (3.3V analog) and DVDD (1.8V) can ramp simultaneously
2. VREFP (2.5V reference) should be present before or simultaneously with AVDD

Since both U3 and U4 are powered from BAT_OUT and both have enable pins tied to BAT_OUT (via 10k pull-up), they ramp together. This is acceptable.

### 6.4 Decoupling Capacitor Placement Summary

| Device | Pins | Caps | Placement Rule |
|--------|------|------|----------------|
| U1 (ADS1299) | AVDD (4 pins: 5, 11, 20, 43) | 100 nF per pin + 10 uF shared bulk | 100 nF <2 mm from each AVDD pin. 10 uF anywhere in analog zone. |
| U1 (ADS1299) | DVDD (pin 42) | 100 nF + 10 uF | 100 nF <2 mm from pin 42 |
| U1 (ADS1299) | VREFP (pin 21) | 10 uF + 100 nF | Closest decoupling on the board. <2 mm from pin. |
| U1 (ADS1299) | VREFN (pin 22) | 100 nF to GND | <3 mm |
| U3 (TPS7A4700) | IN (pin 26) | 10 uF + 100 nF | <5 mm from input pin |
| U3 (TPS7A4700) | OUT (pin 27) | 10 uF + 100 nF | <5 mm from output pin. ESR 20-500 mOhm. |
| U3 (TPS7A4700) | NR (pin 14) | 10 uF (low leakage) | 10 uF to GND. This cap sets the internal reference noise -- use X7R or film, not X5R. |
| U4 (TPS7A2005) | IN | 10 uF | <5 mm |
| U4 (TPS7A2005) | OUT | 10 uF | <5 mm |
| U6 (REF3125) | IN | 10 uF + 100 nF | <5 mm |
| U6 (REF3125) | OUT | 10 uF | <5 mm to U1 VREFP |
| U2 (nRF52) | See Section 6.2 | Per pin table | <3 mm from each VDD pin |

---

## 7. Electrode Connector Design

### 7.1 Connector Selection

Primary choice: **0.5mm pitch FPC connector, 20-pin, bottom contact, right-angle** (e.g., Hirose FH12A-20S-0.5SH or compatible Molex 52271-2079).

Rationale: FPC connector is the thinnest and lightest option for 16 signal lines + 2 bias lines + 2 spare lines. Right-angle orientation allows the flex PCB to wrap around the headband curve.

Backup: **0.5mm pitch board-to-board connector** (JAE FF08 series or Panasonic P5KS) if FPC is too fragile for prototype handling.

### 7.2 Pin Assignment (J2, FPC Connector)

| Pin | Signal | Type | Notes |
|-----|--------|------|-------|
| 1   | IN1P   | Analog input | Channel 1, positive |
| 2   | IN1N   | Analog input | Channel 1, negative |
| 3   | IN2P   | Analog input | Channel 2, positive |
| 4   | IN2N   | Analog input | Channel 2, negative |
| 5   | IN3P   | Analog input | Channel 3, positive |
| 6   | IN3N   | Analog input | Channel 3, negative |
| 7   | IN4P   | Analog input | Channel 4, positive |
| 8   | IN4N   | Analog input | Channel 4, negative |
| 9   | IN5P   | Analog input | Channel 5, positive |
| 10  | IN5N   | Analog input | Channel 5, negative |
| 11  | IN6P   | Analog input | Channel 6, positive |
| 12  | IN6N   | Analog input | Channel 6, negative |
| 13  | IN7P   | Analog input | Channel 7, positive |
| 14  | IN7N   | Analog input | Channel 7, negative |
| 15  | IN8P   | Analog input | Channel 8, positive |
| 16  | IN8N   | Analog input | Channel 8, negative |
| 17  | BIAS_OUT | Analog output | DRL drive -- active feedback |
| 18  | SRB1     | Analog I/O | Shared reference bus 1 |
| 19  | GND_FLEX | Ground    | Flex ground shield connection |
| 20  | GND_FLEX | Ground    | Flex ground shield connection |

**Pin arrangement rationale:**
- P and N of same channel are adjacent (pins 1-2, 3-4, etc.) -- makes it easy to route as paired traces
- Bias and SRB are at the end (far from the first channel) -- their larger voltage swing will not couple into channel 1
- Two GND pins at the far end provide a low-impedance ground connection from the flex to the main board
- Spare pins: if you need lead-off detection or additional bias electrodes, the 20-pin connector has capacity

### 7.3 Flex-to-Electrode Routing (on the Flex PCB)

The flex PCB that connects J2 to the 8 dry electrodes must implement the following:

```
                   FLEX PCB LAYOUT (unrolled, top view)

    +-------------------------------------------------------------+
    |                                                             |
    |  J2 (to main board)          Electrode pads (P1-P8)         |
    |  +----------+                                                |
    |  |       1-->----------------------------------------------P1|
    |  |       2-->----+                                      P2  |
    |  |       3-->----+------------------------------------------|
    |  |       4-->----+                                      P3  |
    |  |       5-->----------------------------------------------|
    |  |       6-->----+                                      P4  |
    |  |       7-->----+------------------------------------------|
    |  |       8-->----+                                      P5  |
    |  |       9-->----------------------------------------------|
    |  |      10-->----+                                      P6  |
    |  |      11-->----+------------------------------------------|
    |  |      12-->----+                                      P7  |
    |  |      13-->----------------------------------------------|
    |  |      14-->----+                                      P8  |
    |  |      15-->----+------------------------------------------|
    |  |      16-->----+                                          |
    |  |      17-->-----BIAS (to separate electrode or mast.)     |
    |  |      18-->-----SRB1 (daisy chain to all electrode refs)  |
    |  |      19-->GND shield                                     |
    |  |      20-->GND shield                                     |
    |  +----------+                                                |
    |                                                             |
    |  <=========================================================>|
    |   ~120-160 mm (fits across forehead from temple to temple)   |
    +-------------------------------------------------------------+
```

**Flex PCB specifications:**

| Parameter | Value | Notes |
|-----------|-------|-------|
| Substrate | Polyimide (PI), 1 oz copper | Standard flex material |
| Total thickness | 0.2 mm max | Must be thin enough to bend around forehead curve |
| Layer count | 2 layers | L1: signal, L2: GND pour |
| Copper weight | 1 oz (0.035 mm) | For mechanical durability |
| Trace width | 0.15 mm (6 mil) | Minimum reliable for 1 oz flex |
| Trace spacing | 0.15 mm (6 mil) | Minimum reliable |
| Surface finish | ENIG (immersion gold) | Required for FPC connector insertion cycles |
| Bend radius (min) | 5 mm (static), 25 mm (dynamic) | Headband is static bend -- radius OK |

**Critical flex rule:** The ground plane on L2 of the flex must have a **solid copper pour** under all analog signal traces. No gaps. Stitch the flex ground to the main board ground through J2 pins 19-20.

### 7.4 ESD Protection on J2

Each electrode pin (INxP, INxN) on J2 must have an ESD protection diode close to the connector (within 5 mm):

- Part: **TI ESD321DPYR** or **Nexperia PESD5V0S1BL** (bidirectional, 0.4 pF capacitance)
- Connect between the signal line and GND
- Ultra-low capacitance is critical: >5 pF of capacitance on the analog input creates a voltage divider with the electrode impedance (10-100 kOhm dry contact), attenuating the EEG signal

**Do NOT use standard TVS diodes with >10 pF capacitance (e.g., SMAJ5.0A).** They will kill your EEG signal. Must be <1 pF.

---

## 8. EMI/EMC Considerations

### 8.1 Critical Noise Paths (Ranked)

| Rank | Path | Mechanism | Coupling | Mitigation |
|------|------|-----------|----------|------------|
| 1 | nRF52 DC-DC --> ADS1299 analog inputs | Inductive coupling from inductor | Switching noise at ~2 MHz harmonics | Physical separation (15 mm min). Oriented so inductor B-field axis is perpendicular to analog zone. |
| 2 | SPI bus (SCLK) --> Analog IN traces | Capacitive crosstalk | SCLK 8 MHz edges capacitively coupled into high-Z (>1 MOhm) analog inputs | 5 mm clearance between SPI and analog. Guard trace on SPI. |
| 3 | USB-C VBUS (5V charging) --> Analog | Burst charging current creates GND potential bounce | Charger switching (if BQ24075 is in thermal regulation) | Separate charger GND return path to L2. Do not share with analog. |
| 4 | BLE RF (2.4 GHz) --> EEG | RF rectification at ADC input ESD diodes | RF envelope detected as DC offset drift | Antenna 20 mm from ADS1299. Shield can over analog section if needed. |

### 8.2 Shielding

**Prototype:** No shield can. The target is 80g total including battery, and a shield can adds 5-10g. Rely on layout discipline instead.

**Production V2 (if noise measurements show need):**
- Use a **tin-plated steel shield can** over the analog zone (U1 + U3 + U6 + J2 area)
- Dimensions: approximately 25 x 20 mm, 3 mm height
- The shield can must make contact with L2 GND through a fence of vias on the can footprint (0.5 mm vias at 1 mm pitch along the can perimeter)
- Solder the can to the shield ring during assembly

**For prototype** -- include the **shield can footprint** on the PCB (as a keep-out zone with a via fence ring) even if you do not populate the can. This gives you the option to add a shield in V1.1 without a board respin.

### 8.3 Ferrite Bead on USB-C

Place a ferrite bead (e.g., **Murata BLM18AG121SN1D**, 120 Ohm @ 100 MHz) in series with the USB-C VBUS line, close to J1. This suppresses conducted emissions from the charging cable into the board.

### 8.4 Common-Mode Choke on Battery

Not required for prototype. The battery is a floating source, not connected to mains. If conducted emissions from the charger are problematic, add a 100 nF capacitor from VBAT to GND near the battery connector.

### 8.5 PCB Edge and Shield Ring

Run a **guard ring** around the entire PCB perimeter:

- L1: 1 mm wide copper trace connected to GND, on all 4 edges of the PCB
- Stitch with vias to L2 GND every 5 mm
- This ring acts as a low-impedance shield that intercepts fringing fields at the PCB edge

---

## 9. Flex PCB Considerations for Curved Headband

### 9.1 Architecture: Two-Piece Rigid + Flex

The headband has a curved form factor (fits on forehead at hairline). A single rigid PCB cannot follow this curve. Two approaches:

**Option A: Rigid-flex (recommended for V1 prototype)**
- One rigid section (20 x 30 mm) containing all active electronics (U1-U6, J1, ANT1, Y1, Y2)
- One flex section extending from J2 across the forehead holding the 8 electrodes
- Flex is permanently attached to the rigid section through J2 FPC connector (not bonded -- allows replacement)

**Option B: Semi-rigid PCB (alternative for prototype simplicity)**
- Use 0.8 mm thick FR-4 (thinnest standard). The board can flex slightly along its length if the long axis is along the headband curve.
- Risk: traces may crack under repeated flexing. Acceptable for prototype (10-20 bend cycles).

**Recommendation:** Go with **Option A** (rigid-flex with FPC connector). This is the correct engineering choice and the FPC connector cost is negligible (3 RMB). Option B is a false economy that will cause board cracking failure.

### 9.2 Headband Mechanical Integration

```
                     +------------------------------+
                     |       USER'S FOREHEAD         |
                     |   (viewed from above)          |
                     |                                |
                     |   E1  E2  E3  E4  E5  E6  E7 E8|
                     |   |   |   |   |   |   |   |   | |
                     |   +---+---+---+---+---+---+---+ |
                     |       FLEX PCB strip            |
                     |            |                    |
                     |       J2 (FPC connector)        |
                     |            |                    |
                     |    +------+------+              |
                     |    |  MAIN PCB   |              |
                     |    |  (rigid)    |              |
                     |    |             |              |
                     |    |  U1 ADS1299 |              |
                     |    |  U2 nRF52   |              |
                     |    |  U3 TPS7A   |              |
                     |    |  U4 TPS7A   |              |
                     |    |  U5 Charger |              |
                     |    |  ANT1       |              |
                     |    +------+------+              |
                     |           |                     |
                     |       BT1 (battery)             |
                     |       200 mAh Li-Po             |
                     |       (behind flex PCB)         |
                     +------------------------------+
                           (not to scale)
```

**Key mechanical constraints:**
- The main rigid PCB should be positioned at the **right temple** area (for right-handed user -- where the watch/BLE antenna has best clearance from the head)
- Battery (BT1) goes on the **left temple** area -- counterweight to balance the PCB weight
- Flex PCB runs across the forehead from temple to temple, underneath the TPU shell
- Electrode pads (E1-E8) are spaced **15-20 mm apart** (center-to-center), matching the 10-20 EEG system positions for the frontal montage (Fp1, Fp2, Fz, F3, F4, F7, F8, FCz -- or optimized placement for MRCP detection)

### 9.3 Flex PCB Strain Relief

At the J2 connector junction:
- The flex PCB must have a **strain relief tab** (5 mm extension beyond the connector insertion line) with adhesive backing
- A thin (0.5 mm) FR-4 or polyimide stiffener on the back of the flex at the connector area prevents the flex from creasing at the connector edge
- The flex-to-rigid transition must not create a sharp angle -- use a 5 mm minimum bend radius

### 9.4 Mounting Holes

The rigid PCB needs 4 mounting holes (2 mm diameter, stainless steel, with GND-connected pads):

| Hole | Location | Function |
|------|----------|----------|
| H1 | Top-left of PCB | Screw into headband TPU shell |
| H2 | Top-right of PCB | Screw into headband TPU shell |
| H3 | Bottom-left (near J2) | Additional anchor, near electrode connector |
| H4 | Bottom-right (near J1) | USB-C strain relief anchor |

---

## 10. Key Layout Constraints and Keep-Out Zones

### 10.1 Board Outline and Dimensions

- **Rigid PCB size:** 50 mm x 20 mm (maximum). This is the space budget for all active electronics.
- **Flex PCB strip:** 120-160 mm long (from temple-to-temple), 12 mm wide.
- **Board shape:** Rectangular with rounded corners (R2 mm). No board cutouts needed for prototype.

If 50 x 20 mm is too tight (it will be tight), extend to 60 x 22 mm before going to 6 layers. The weight impact of slightly larger PCB (0.5g) is less than the cost and complexity of 6-layer.

### 10.2 Antenna Keep-Out Zone

The Johanson 2450AT18A100E chip antenna requires a strict keep-out zone:

```
    TOP VIEW
    +-----------------------------------------------------+
    |                                                     |
    |  +----------+                                       |
    |  |          |    +---------------------+             |
    |  |   nRF52  |    |  KEEP-OUT ZONE      |             |
    |  |   (U2)   |--->|                     |             |
    |  |          |    |  No copper on L1-L4  |             |
    |  +----------+    |  7 x 10 mm           |   ANT1     |
    |                  |  (from antenna       |   +--+     |
    |                  |   center point)      |   |  |     |
    |                  +----------------------+   +--+     |
    |                                                     |
    |  <----- 5 mm min clearance to board edge ---------->|
    |                                                     |
    +-----------------------------------------------------+
    |                                                     |
    |  SIDE VIEW                                          |
    |  +---------------------------------------------+    |
    |  |  PCB (L1-L4)                                |    |
    |  |  <--- 5 mm keep-out -> no GND planes        |    |
    |  +---------------------------------------------+    |
    |                           ^                         |
    |                    ANT1   |                         |
    |                    is     |                         |
    |                    here   |                         |
    +-----------------------------------------------------+
```

**Keep-out dimensions (from ANT1 center):**
- Lateral (parallel to PCB edge): 7 mm minimum
- Vertical (away from PCB edge): 10 mm minimum
- Below antenna (L2-L4): No copper for 5 mm in all directions
- Board edge clearance: antenna must be at the PCB edge, and 5 mm beyond the edge must be clear of any metal (battery, wires, enclosure)

### 10.3 nRF52 RF Matching Network

Between U2 pin P0.09 (ANT) and ANT1, include a Pi-matching network (C10, L2, C11) positioned within 5 mm of the antenna:

| Component | Value (calculated) | Notes |
|-----------|-------------------|-------|
| C10 (series) | 1.0 pF (NPO/C0G) | Tune after first board |
| L2 (shunt)   | 2.2 nH (0402)     | Tune after first board |
| C11 (series) | 1.0 pF (NPO/C0G) | Tune after first board |

**Initial values** are based on the Johanson antenna datasheet typical application. **These MUST be tuned** when the first prototype boards come back -- antenna impedance depends on enclosure, battery proximity, and headband shape. Leave the matching network populated with 0-Ohm jumpers initially, then replace with calculated values after network analyzer measurements.

### 10.4 Thermal Management Keep-Outs

- U5 (BQ24075 charger): The area around U5 must not have any temperature-sensitive components (electrolytic caps, plastic connectors) within 5 mm. Charger can reach 85 degC during fast charge.
- nRF52 DC-DC inductor: No plastic components (connectors, switches) within 3 mm. The inductor core can reach 100 degC under heavy BLE TX duty cycle.

### 10.5 Via and Pad Minimum Requirements

| Feature | Minimum | Preferred |
|---------|---------|-----------|
| Via hole diameter | 0.3 mm | 0.3 mm (no smaller -- JLCPCB standard) |
| Via pad diameter | 0.6 mm | 0.6 mm |
| Trace width (signal) | 0.15 mm (6 mil) | 0.2 mm (8 mil) |
| Trace width (power) | 0.25 mm (10 mil) | 0.4 mm (16 mil) |
| Clearance (trace-to-trace) | 0.15 mm (6 mil) | 0.2 mm (8 mil) |
| Clearance (trace-to-pad) | 0.15 mm (6 mil) | 0.2 mm (8 mil) |
| Silkscreen text height | 0.8 mm | 1.0 mm |
| Silkscreen line width | 0.15 mm | 0.15 mm |

---

## 11. Test Points and Debug Interface

### 11.1 Required Test Points

Install the following test points on L1 (0.8 mm diameter bare copper pad, no solder mask, with a 0.6 mm hole for probe hook). These are essential for bring-up:

| Ref | Signal | TP Label | Purpose |
|-----|--------|----------|---------|
| TP1 | BAT_OUT (3.7-4.2V) | VBAT | Battery voltage measurement |
| TP2 | AVDD_3V3 | +3V3_A | Analog 3.3V rail (from U3) |
| TP3 | DVDD_1V8 | +1V8_D | ADC digital 1.8V rail (from U4) |
| TP4 | VREF_2V5 | VREF | ADC reference voltage |
| TP5 | GND | GND | Ground reference for all measurements |
| TP6 | SCLK | SCLK | SPI clock (logic analyzer probe) |
| TP7 | DRDY | DRDY | ADC data ready (trigger for acquisition) |
| TP8 | IN1P | CH1_P | Channel 1 input (signal injection) |
| TP9 | IN1N | CH1_N | Channel 1 negative input |
| TP10 | BIAS_OUT | BIAS | DRL drive output |

**Test point arrangement:** Place TP1-TP5 in a row (2.54 mm pitch) at the board edge, so they can be accessed with a pogo-pin fixture or multimeter probes while the headband is worn. TP6-TP10 can be smaller and placed near their respective components.

### 11.2 Debug Connector -- SWD (J3)

An **Arm Serial Wire Debug (SWD)** connector is mandatory. Use a 6-pin 1.27 mm pitch shrouded header (e.g., Samtek FTSH-105-01-L-D or Harwin M50-3600542):

| Pin | Signal | nRF52 Pin | Color (cable) |
|-----|--------|-----------|---------------|
| 1   | SWD_CLK | P0.25 | Yellow |
| 2   | SWD_IO  | P0.24 | Blue |
| 3   | GND     | ---    | Black |
| 4   | SWO     | P0.18 (optional trace) | Green |
| 5   | VTG (3.3V output) | nRF52 VDD | Red |
| 6   | RESET   | P0.21 (optional) | White |

**Connector placement:** Edge of digital zone, near U2. This allows programming and debugging with a J-Link or DAPLink adapter while the headband is worn.

**SWO (pin 4):** The Serial Wire Output trace must be routed on L1 with a 22 Ohm series resistor (R_SWO, 0402) placed within 5 mm of the nRF52 pin. Optional but highly recommended for printf-over-SWO debugging.

### 11.3 UART Debug (J4)

A 4-pin 1.27 mm header for UART debug output from nRF52:

| Pin | Signal | nRF52 Pin |
|-----|--------|-----------|
| 1   | TXD    | P0.06 |
| 2   | RXD    | P0.08 |
| 3   | GND    | --- |
| 4   | VTG    | nRF52 VDD (3.3V) |

This provides console output during firmware development. Baud rate: 115200 or 921600.

### 11.4 Production Test Points

For automated production testing (flying probe or bed-of-nails), add the following additional test points on L4 (bottom side):

| TP | Signal | Purpose |
|----|--------|---------|
| TP11 | USB_D+ | USB data line continuity |
| TP12 | USB_D- | USB data line continuity |
| TP13 | BLE_TX (P0.09) | RF power measurement (conducted) |

**BLE conducted RF test:** Add a U.FL coaxial connector (e.g., Hirose U.FL-R-SMT-1) on the antenna trace, between the matching network and ANT1. Connect with a 0-Ohm resistor that can be removed to isolate the antenna for conducted measurements. This is optional for prototype but mandatory for production (FCC/CE certification requires conducted RF power measurement).

### 11.5 Programming Header (J5 -- Optional)

If the SWD connector is too large for the final form factor, include a 2x3 0.5 mm pitch FPC connector footprint (unpopulated) as a secondary programming interface:

| Pin | Signal | nRF52 Pin |
|-----|--------|-----------|
| 1   | SWD_CLK | P0.25 |
| 2   | VDD     | nRF52 VDD |
| 3   | SWD_IO  | P0.24 |
| 4   | GND     | --- |
| 5   | RESET   | P0.21 |
| 6   | GND     | --- |

---

## 12. Appendix: Reference Schematic Fragment Guidelines

These are layout-derived constraints that should be reflected in the schematic:

### 12.1 ADS1299 Configuration Resistors

| Resistor | Placement | Value | Purpose |
|----------|-----------|-------|---------|
| R_BIAS (R1) | Between BIAS_OUT and bias electrode (in flex) | 51 kOhm | Bias resistor -- limits DRL current |
| R_SRB (R2) | Between SRB1 and GND | 10 kOhm | SRB pulldown |
| R_LEADOFF (R3-R10) | Per channel, in series with INxP/INxN | 0 Ohm (populate if needed) | Lead-off detection resistors |

### 12.2 Filtering Components

- **Anti-aliasing filter:** Per channel, place a 2-pole passive RC low-pass filter (R = 1.5 kOhm, C = 1 uF, fc = 106 Hz) between the connector and ADS1299 input. This is the **analog anti-aliasing filter** -- mandatory. Hardware: R11-R26 (16 resistors, 0402) and C11-C18 (8 capacitors, 0603). Fit within the 15 mm connector-to-ADS1299 routing corridor.
- **Bias feedback filter:** RC filter on BIAS_OUT (R = 10 kOhm, C = 100 nF, fc = 159 Hz) to limit the bias loop bandwidth and improve stability.

### 12.3 Power-On Indication

LED D1 (green, 0603) on digital 3.3V rail, driven by nRF52 GPIO (P0.17) through 1 kOhm series resistor. Place near U2. LED D2 (red, 0603) on BAT_OUT for charging indication, driven by BQ24075 CHG pin through 1 kOhm resistor.

---

*End of PCB Design Notes v0.1. This document captures layout-critical decisions frozen for the v0.1 prototype. If any specification changes (stackup, placement, grounding approach), update this document before the PCB layout is routed.*
