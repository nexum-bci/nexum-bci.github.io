# Nexum One — Engineering Architecture Document

**Draft v0.1** · 2026-06-21  
**Author:** Architecture Working Group  
**Classification:** Internal — Engineering

---

## Table of Contents

1. System Architecture and Data Flow
2. Technical Specifications to Lock Down First
3. Component Selection Guidance
4. Critical Engineering Risks (Ranked)
5. First Prototype Build Plan
6. Appendix: Communication Protocol Summary

---

## 1. System Architecture and Data Flow

### 1.1 High-Level Overview

Nexum One is a closed-loop neural reconnection system with four physical nodes and one logical control loop:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        NEXUM ONE SYSTEM                             │
│                                                                     │
│  ┌──────────────┐    BLE     ┌──────────────┐    BLE     ┌───────┐ │
│  │  EEG-Sense   │◄──────────►│  Nexum App   │◄──────────►│Control│ │
│  │  Headband    │   (EEG)    │  (Phone)     │  (Cmds)    │ Box   │ │
│  │  (80g, 8ch)  │            │  AI Inference │            │       │ │
│  └──────────────┘            │  + UI + Log   │            │       │ │
│                              └──────┬───────┘            │       │ │
│                                     │                    │       │ │
│                                     │ Wired (UART)       │       │ │
│                                     ▼                    │       │ │
│                              ┌──────────────┐            │       │ │
│                              │   Control     │◄───────────┘       │ │
│                              │   Box         │                    │ │
│                              │  (Waist)      │                    │ │
│                              │  MCU + IMU    │                    │ │
│                              │  + Motor Drv  │                    │ │
│                              │  + Battery    │                    │ │
│                              └───┬───┬───────┘                    │ │
│                                  │   │                            │ │
│                          Motor   │   │ IMU                        │ │
│                          (PWM)   │   │ (I2C)                      │ │
│                                  ▼   ▼                            │ │
│                              ┌──────────────┐                     │ │
│                              │  NeuroSuit   │                     │ │
│                              │  Hip Module  │                     │ │
│                              │  Bowden Cable│                     │ │
│                              │  + Force Sen │                     │ │
│                              └──────────────┘                     │ │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 Detailed Data Flow (EEG to Force Feedback)

The system operates in five stages, forming a closed loop:

#### Stage 1: Neural Signal Acquisition (EEG-Sense Headband)

| Step | Action | Component | Output |
|------|--------|-----------|--------|
| 1.1 | Dry electrodes (8 channels, Cz/C3/C4/FCz/FC3/FC4/Pz/P3/P4 or optimized montage) pick up cortical potentials | Ag/AgCl or Ag/AgCl-coated dry comb electrodes | Analog signal: 1–100 µV, DC–100 Hz |
| 1.2 | Instrumentation amplifier + anti-aliasing filter (0.1–100 Hz analog bandpass) | TI ADS1299 (internal PGA + filter) | Analog, gain=12 or 24 |
| 1.3 | 24-bit delta-sigma ADC, 250–500 SPS per channel | ADS1299 internal ADC | Digital: 8 × 24-bit samples @ 250–500 Hz |
| 1.4 | Common Average Referencing (CAR), bandpass (0.5–40 Hz digital), notch (50 Hz) | nRF52832 MCU | Preprocessed 8-channel data buffer |
| 1.5 | Packetize + transmit over BLE (Notify, 20 ms interval, 5 packets per interval) | nRF52832 BLE radio | BLE GATT characteristic updates |

**Raw BLE throughput:** 8 ch × 250 Hz × 3 bytes = 48,000 bps (48 kbps)  
**Compressed (optional):** 16-bit resolution → 32 kbps, well within BLE 5.0 capacity (2 Mbps PHY).

#### Stage 2: Intention Decoding (Nexum App on Phone)

| Step | Action | Component | Output |
|------|--------|-----------|--------|
| 2.1 | Receive BLE packets from headband | Phone BLE stack | 200 ms sliding buffer (50–100 samples per channel) |
| 2.2 | Feature extraction: power spectral density (mu/beta bands), spatial patterns, CSP | CoreML / ONNX runtime | Feature vector (32–64 dim), updated every 40 ms |
| 2.3 | Inference: CNN or Transformer model trained on MRCP (movement-related cortical potentials) | Neural network accelerator (ANE/GPU) | Intention probability [0–1], intended action class, onset timestamp |
| 2.4 | Intention fusion with IMU context (gait phase, hip angle) received from control box | App fusion layer | Refined assistance command + timing |

**Target inference latency:** < 50 ms per window.  
**Detection window:** Readiness potential onset detected ~500 ms before intended movement.

#### Stage 3: Command Relay (Phone → Control Box)

| Step | Action | Component | Output |
|------|--------|-----------|--------|
| 3.1 | Encode assistance command (desired torque profile, timing, duration) | App command encoder | Compact binary command (8–16 bytes) |
| 3.2 | Transmit over BLE to control box | Phone BLE stack | BLE GATT write |
| 3.3 | Receive, parse, prioritize command | nRF5340 / MCU on control box | Motor control setpoint |

#### Stage 4: Motor Actuation (Control Box + NeuroSuit)

| Step | Action | Component | Output |
|------|--------|-----------|--------|
| 4.1 | Compute motor current from torque setpoint (PI loop with feedforward) | STM32 MCU (M4/M7) | PWM duty cycle |
| 4.2 | Drive BLDC motor (Field-Oriented Control, PWM 20–50 kHz) | TI DRV8316 / TMC6300 + 3-phase bridge | Phase currents to motor |
| 4.3 | Motor rotates → spool winds → Bowden cable shortens | Maxon EC-i 40 or equivalent BLDC | Linear cable displacement |
| 4.4 | Cable tension transfers to hip module → hip flexion/extension assistance | Bowden sheath + sliding mechanism | Assistive torque at hip joint (~5–15 Nm) |
| 4.5 | Cable tension sensor (inline load cell or hall-effect) reads actual force | Strain gauge / MLX91206 | Analog/digital tension feedback |

#### Stage 5: State Feedback + Loop Closure

| Step | Action | Component | Output |
|------|--------|-----------|--------|
| 5.1 | IMU reads hip angle, angular velocity, trunk orientation | BMI270 (6-axis IMU) on control box | Quaternion + Euler angles @ 100 Hz |
| 5.2 | Motor encoder reads actual position/velocity | Magnetic encoder (AS5048 or TLE5012) | Rotor angle @ 1 kHz |
| 5.3 | Force sensor reads cable tension | Strain gauge amplifier (HX711 or INA) | Tension value @ 200 Hz |
| 5.4 | MCU fuses sensor data → computes state estimate | Sensor fusion (Mahony/Madgwick + complimentary filter) | Hip angle, gait phase, cable force |
| 5.5 | State sent to phone via BLE for logging + AI model adaptation | BLE GATT notify | State packet @ 50 Hz |
| 5.6 | Phone adapts personalization model based on user response history | App background ML pipeline | Updated model weights |

**Total closed-loop latency budget (target):**

| Stage | Component | Latency Budget |
|-------|-----------|----------------|
| Stage 1 | EEG acquisition + preprocessing + BLE TX | < 40 ms |
| Stage 2 | Phone BLE RX + inference + command generation | < 55 ms |
| Stage 3 | BLE command TX → Control box RX | < 20 ms |
| Stage 4 | Motor control loop + Bowden cable mechanical response | < 60 ms |
| Stage 5 | Sensor acquisition + state estimation | < 10 ms |
| **Total** | **EEG → Force feedback** | **< 185 ms** |

**Note:** For the prototype phase, a simplified data flow is recommended: run inference on a Raspberry Pi 5 or Jetson Nano **inside** the control box (wired to the motor controller), eliminating phone latency and BLE double-hop. See Section 5 for details.

---

## 2. Technical Specifications to Lock Down First

The following parameters must be frozen before any detailed design begins. Changes after freeze will cascade across multiple subsystems.

### 2.1 EEG Acquisition

| Parameter | Target | Rationale / Trade-off |
|-----------|--------|-----------------------|
| Number of channels | 8 | Minimum for source localization of MRCP; more channels = higher BLE bandwidth, higher power, higher cost |
| Sampling rate | 250 SPS per channel | MRCP content < 10 Hz; 250 SPS satisfies Nyquist with margin; higher rates waste power |
| ADC resolution | 24 bit | Required for µV-level signals; ADS1299 native |
| Input range | ±4.5 mV (programmable) | Dry electrodes have larger DC offsets; need headroom |
| Input noise | < 1 µV RMS (0.5–100 Hz) | MRCP is 5–10 µV; SNR > 10 dB minimum |
| CMRR | > 100 dB | 50 Hz common-mode rejection critical |
| EEG bandwidth | 0.3–40 Hz | MRCP is DC-slow; 0.3 Hz HPF is practical trade-off vs drift |
| Common reference | Driven Right Leg (DRL) or bipolar | DRL improves CMRR but adds electrode; evaluate in Phase 1 |

### 2.2 Real-Time Latency Budget

| Parameter | Target | Who owns it |
|-----------|--------|-------------|
| EEG acquisition to BLE packet | < 40 ms | EE / FW team |
| BLE RX to inference output | < 55 ms | ML / App team |
| BLE command to motor start | < 20 ms | FW team |
| Motor max response time (0–rated torque) | < 60 ms | ME / FW team |
| **End-to-end latency (EEG → movement)** | **< 200 ms** | **System** |
| Target: user-perceptible delay threshold | < 100 ms (transparent) to 200 ms (acceptable) | — |

**This is the single most important specification.** Every subsystem must be designed to meet their individual allocation. We will measure E2E latency in the first integration milestone.

### 2.3 Motor and Mechanical

| Parameter | Target | Notes |
|-----------|--------|-------|
| Continuous assist torque | 8 Nm | ~30% of typical hip flexion torque during gait |
| Peak assist torque | 15 Nm (3 sec) | Sit-to-stand, stair ascent |
| Torque control bandwidth | > 10 Hz | Smooth assistance during gait cycle |
| Force control accuracy | ±0.5 Nm | Too coarse → feels wrong; too fine → overengineered |
| Cable stroke | 150 mm | Typical hip flexion ROM in gait (~35 deg) |
| Cable force (peak) | 800 N | Based on 15 Nm at 20 mm lever arm |
| Bowden sheath bend radius (min) | 50 mm | Tighter bends increase friction nonlinearly |
| System weight (NeuroSuit + Control Box) | < 2.5 kg | User tolerance for rehab session |

### 2.4 Power and Battery

| Parameter | Target | Notes |
|-----------|--------|-------|
| Battery capacity | 48 Wh (1,250 mAh @ 38.4 V / 5,000 mAh @ 9.6 V) | Li-ion 4–6S, depending on motor voltage |
| Continuous power draw | ~8–12 W | MCU + BLE + IMU ~1 W; motor + driver ~7–11 W average |
| Peak power draw | ~50 W (3 sec) | Motor peak torque + acceleration |
| Battery life, continuous use | > 4 hours | One rehab session |
| Charging time | < 2 hours | USB-C PD (20 V / 3 A input) |
| Battery type | Li-ion 18650 or pouch | 18650 for prototype (cheap, safe, replaceable) |

**Critical trade-off:** Motor voltage vs battery cells. Higher voltage (36–48 V) enables lower current for same power (smaller wires, less I²R loss, faster motor response), but requires more series cells (10S–12S → heavier). Recommended: **6S Li-ion (21.6 V nominal)** — balances motor response with pack weight (~350 g for 48 Wh).

### 2.5 Mechanical Form Factor

| Parameter | Target |
|-----------|--------|
| Control box dimensions | 120 × 80 × 30 mm (wallet-sized) |
| Control box weight | < 400 g (including battery) |
| Hip module width | < 100 mm lateral (does not interfere with arm swing) |
| Suit total don/doff time | < 3 min |

---

## 3. Component Selection Guidance

### 3.1 EEG Front-End Chip

The EEG front-end is the single most critical component for signal quality. Only three chips are viable for this application:

| Chip | Pros | Cons | Recommendation |
|------|------|------|----------------|
| **TI ADS1299** | Industry standard for dry EEG; 8-channel, 24-bit, integrated PGA + bias drive + lead-off detection; extensive reference designs (OpenBCI, etc.) | Relatively high power (5 mW/ch); limited input bandwidth; ~$18/chip | **Default choice.** Lowest risk, most community support, known by EE hiring target |
| TI ADS1299-4 | 4-channel version of above | Only 4 channels; would need 2 chips for 8 channels | Not recommended |
| TI ADS131M08 | Lower power (0.5 mW/ch); 24-bit; 8-channel simultaneous | Fewer EEG-specific features (no bias drive); less community reference | Consider for V2 power optimization |
| Maxim MAX30001 | Ultra-low power; single-channel for ECG | Not suitable for multichannel EEG | Out |

**Decision: ADS1299 for prototype and V1 production.**

#### Dry Electrodes

| Type | Pros | Cons |
|------|------|------|
| Ag/AgCl coated comb (g.tec g.GAMMAcap) | Known performance; CE marked | ~$150/channel; proprietary |
| OpenBCI Dry Electrode | Proven in research; ~$20/ch | Lower SNR than wet; requires skin prep |
| Custom PCB spring-loaded pins | Cheap (~$1/ch); design freedom | Unproven; contact impedance varies |
| BrainProducts ActiCAP dry | Medical grade | Expensive; BCI-oriented |

**Prototype recommendation:** Start with OpenBCI compatible dry comb electrodes ($20/ch × 8 = $160). Move to custom spring-loaded pins in V2 after impedance testing.

### 3.2 IMU

| Chip | Pros | Cons | Choice |
|------|------|------|--------|
| **BMI270 (Bosch)** | 6-axis, low power (0.6 mA), integrated step detector, 3×3 mm | No magnetometer | **Primary choice** — low power, small, well-documented, cheap |
| ICM-20948 (TDK) | 9-axis (includes magnetometer), 3×3 mm, 0.7 mA | Yaw drift still problematic indoors; extra complexity | Consider if heading estimate needed |
| LSM6DSO (ST) | 6-axis, 0.55 mA, 2.5×2.5 mm | Slightly less mature library ecosystem | Backup |

**Decision: BMI270 for the control box.** Add a second BMI270 on the thigh segment if bilateral hip angle needed (V2).

### 3.3 BLE Module

| Chip | Pros | Cons | Choice |
|------|------|------|--------|
| **Nordic nRF52832** | 512 KB flash, 64 KB RAM, Cortex-M4F (64 MHz) — can run simple preprocessing on-chip; mature SDK; BLE 5.0; ~$3 | Limited RAM for complex inference | **EEG headband** — adequate for data pipeline |
| **Nordic nRF5340** | Dual-core: Cortex-M33 app + M33 network; 1 MB flash, 512 KB RAM; BLE 5.3; ~$5 | Overkill for headband | **Control box** — enough for motor control + sensor fusion |
| Nordic nRF52840 | 1 MB flash, 256 KB RAM, USB; ~$4 | More than needed for headband | Fallback for control box |
| TI CC2652R7 | Good RF, 352 KB RAM; ~$4 | Smaller ecosystem than Nordic | Not recommended |

**Decision:**
- **EEG-Sense headband:** nRF52832 (SDK + preprocessing capability is sufficient)
- **Control box:** nRF5340 (dual-core enables separation of motor control + BLE stack)

### 3.4 MCU / Main Processor

This is the hardest decision. The "right" choice depends on **where inference runs**:

#### Option A: Inference on Phone (Prototype Fast Path)

| Component | Role | Selection |
|-----------|------|-----------|
| Control box MCU | Motor control + IMU + BLE relay | **nRF5340** (already selected; M33 core is sufficient for FOC + sensor fusion) |
| Phone | AI inference + UI | **Any modern iPhone / Android** (CoreML / TFLite / ONNX) |

**Pros:** Fastest to prototype; no embedded ML engineering; leverages phone GPU/ANE.  
**Cons:** BLE double-hop adds latency; requires phone always present; phone dependency is a product risk for Home version.

#### Option B: Edge Inference on Control Box (Production Target)

| Component | Role | Selection |
|-----------|------|-----------|
| Control box MCU | Motor control + sensor fusion | **STM32H743** (Cortex-M7 @ 480 MHz, 2 MB flash, 1 MB RAM) or **NXP RT1064** |
| ML accelerator | Real-time EEG inference | **Kendryte K230** (RISC-V dual-core + NPU, 1 TOPS) or **STM32N6** (Neural-ART accelerator) |
| BLE | Communication | nRF5340 (separate from inference MCU via UART/SPI) |

**Pros:** No phone required; lower E2E latency; works standalone as a medical device.  
**Cons:** Significantly more firmware complexity; NPU integration risk.

### 3.5 Motor Driver

| Driver | Pros | Cons | Choice |
|--------|------|------|--------|
| **TI DRV8316** | 3-phase BLDC driver, 4.5–60 V, 5 A RMS, integrated current sensing (sense-less FOC), SPI interface, ~$5 | No integrated MOSFET RDS(on) monitoring | **Primary** for prototype (matched with Maxon EC-i 40) |
| Trinamic TMC6300 | Ultra-quiet (StealthChop2), 2–11 V, 1.2 A RMS | Low voltage limits motor selection | Too low voltage for our torque needs |
| TI DRV8301 | 6–60 V, up to 60 A; used in many robotics projects | Larger package; more external components | Overkill for prototype |
| AMT49400 (Allegro) | Integrated FOC, 4.5–36 V, 2 A | Less flexible than TI | Backup |

**Decision: TI DRV8316** for prototype. It has the voltage range (up to 60 V → supports 6S battery), sufficient current (5 A continuous), and integrated current sensing eliminates external shunt resistors.

### 3.6 Motor

| Motor | Pros | Cons | Choice |
|-------|------|------|--------|
| **Maxon EC-i 40 (60 W)** | Medical-grade, 0.15 Nm continuous at 4,000 RPM, 42 mm diameter, 150 g, hall sensors available | ~$300 each | **V1 Production choice** — too expensive for prototype |
| T-motor AK80-9 (or similar) | ~$100, 0.5 Nm at ~2,000 RPM, 12 V, integrated encoder | Not medical grade; larger (60 mm) | **Prototype choice** — cheap, available, easy to integrate |
| Faulhaber 3863H024C | Excellent torque density, 12 V, ~$500 | Very expensive; long lead times | Consider for V2 if weight is critical |
| Custom BLDC (wound in-house) | Theoretically optimal | Massive development effort; not realistic | Out of scope |

**Decision for prototype:** **T-motor AK80-9 (or AK60-6 for higher torque)** — $80–120 each, available on Taobao with < 1 week lead time, 12 V or 24 V versions, integrated hall encoder. Acceptable for functional prototype. Upgrade to Maxon EC-i 40 for clinical validation.

### 3.7 Battery

| Pack config | Nominal V | Energy | Weight (est.) | Motor suitability | Recommendation |
|-------------|-----------|--------|---------------|-------------------|----------------|
| 4S Li-ion (14.8 V) | 14.8 V | 44 Wh (3,000 mAh) | ~280 g | Limited (low voltage) | Minimum viable |
| **6S Li-ion (22.2 V)** | **22.2 V** | **50 Wh (2,250 mAh)** | **~360 g** | **Good** | **Primary choice** |
| 10S Li-ion (36 V) | 36 V | 54 Wh (1,500 mAh) | ~480 g | Excellent | Weight penalty |

**Decision: 6S Li-ion, 21700 cells** (Samsung 50E or similar, 5,000 mAh per cell → 6 × 5,000 mAh at 22.2 V). Custom pack with BMS (TI BQ76952 or similar).

---

## 4. Critical Engineering Risks (Ranked by Severity)

### RISK 1: Dry EEG Signal Quality During Movement

**Severity:** CRITICAL | **Probability:** HIGH | **Mitigation Cost:** HIGH

| Factor | Detail |
|--------|--------|
| Problem | Dry electrodes are 10–100× noisier than wet/gel electrodes. Motion artifacts (cable sway, electrode shift, muscle EMG crosstalk) are in the same frequency band as MRCP (0.1–10 Hz). A user walking creates massive movement artifacts. |
| Impact | If dry EEG SNR < 3 dB during gait, intention decoding is impossible and the product cannot function. This is an existential risk. |
| Mitigation | (1) Optimize electrode mechanical design: spring-loaded pins with independent suspension; (2) Adaptive noise cancellation using IMU reference (accelerometer on headband); (3) Active noise suppression via DRL circuit; (4) Artifact rejection algorithm (MARA, FASTER) running in preprocessing; (5) Fallback: if gait artifacts are insurmountable, detect intention from gaze or residual EMG instead. |
| Phase to address | **Immediately.** Day 1 of prototype: electrode test rig with motion simulator. Do not proceed past month 1 without quantified SNR under motion. |

### RISK 2: Real-Time Intention Decoding Latency and Accuracy

**Severity:** CRITICAL | **Probability:** MEDIUM | **Mitigation Cost:** HIGH

| Factor | Detail |
|--------|--------|
| Problem | Bereitschaftspotential (BP) is only 5–10 µV peak. Single-trial detection from 8 channels is at the edge of what's been demonstrated in literature (single-trial BP detection accuracy ~70–80% in controlled lab settings). Real-time, during gait with artifacts: accuracy likely drops below useful threshold. |
| Impact | False positives (assistance when user didn't intend) → feels uncontrollable, safety risk. False negatives (no assistance when intended) → user abandons device. |
| Mitigation | (1) Use sliding-window deep learning (EEGNet, shallow ConvNet) trained on user-specific data; (2) Multi-modal fusion: cue from IMU (weight shift precedes step) provides second signal; (3) Active personalization: model adapts in first 10 minutes of each session; (4) Conservative threshold: prioritize specificity over sensitivity in early versions; (5) FDA strategy: position as "assist-as-needed" rather than "intent-controlled" for initial clearance. |
| Phase to address | **Month 1–3.** Algorithm development + data collection from first 5 able-bodied subjects. |

### RISK 3: Bowden Cable Friction and Control Nonlinearity

**Severity:** HIGH | **Probability:** HIGH | **Mitigation Cost:** MEDIUM

| Factor | Detail |
|--------|--------|
| Problem | Bowden cable friction increases nonlinearly with sheath curvature. Efficiency can drop to 40–70%. Cable stretch under load introduces hysteresis. This makes precise torque control very difficult. |
| Impact | "Slop" in assistance feels unnatural. If friction varies with hip angle during gait, the controller must compensate dynamically — hard to model. |
| Mitigation | (1) Minimize sheath bends: route cable in straightest possible path; (2) Use PTFE-lined Bowden sheath (low friction); (3) Closed-loop force control with inline load cell (compensates for friction); (4) Model friction as function of sheath angle (empirically characterize); (5) Alternative: direct-drive motor at hip (heavier but more controllable) — keep as risk mitigation strategy. |
| Phase to address | **Month 2–4.** Build cable test bench to characterize friction vs. bend radius vs. load. |

### RISK 4: System Integration Complexity

**Severity:** HIGH | **Probability:** MEDIUM | **Mitigation Cost:** MEDIUM

| Factor | Detail |
|--------|--------|
| Problem | Five subsystems (EEG headband, phone app, control box, motor, suit mechanical) must work together. Each has independent development dependencies (FW, EE, ME, ML). Integration typically reveals timing bugs, protocol mismatches, power sequencing issues, and mechanical interference. |
| Impact | Integration phase extends beyond schedule; single point of failure in any subsystem blocks entire system test. |
| Mitigation | (1) Define communication protocols **before** any coding begins (see Appendix); (2) Build integration test harness in Month 1; (3) Weekly integration tests from Month 2; (4) Hardware-in-the-loop (HIL) test bench for control box firmware before mechanical prototype exists; (5) Designate one person as **integration lead** with authority to block (not just flag) changes that break compatibility. |
| Phase to address | **Month 1 (protocol definition) + ongoing.** |

### RISK 5: Battery Life Under Real Use

**Severity:** MEDIUM | **Probability:** MEDIUM | **Mitigation Cost:** LOW

| Factor | Detail |
|--------|--------|
| Problem | Motor actuation power depends on gait pattern, user weight, and assistance level. Worst-case (heavy user, high assist, frequent sit-stand) may draw 25+ W, draining a 48 Wh battery in < 2 hours. |
| Impact | Clinical viability: a rehab session should be 45–60 min minimum. 2 hours is acceptable. < 1 hour is not. |
| Mitigation | (1) Measure real power draw on first motorized prototype; (2) Use low-power states between strides; (3) Increase battery capacity to 60 Wh if needed (~+100 g, acceptable trade-off); (4) Charging dock that enables hot-swap batteries for clinic use. |
| Phase to address | **Month 4–5**, after first integrated system test. |

### RISK 6: Thermal Management

**Severity:** MEDIUM | **Probability:** LOW–MEDIUM | **Mitigation Cost:** LOW

| Factor | Detail |
|--------|--------|
| Problem | Motor driver + battery + MCU in a waist-mounted enclosure (120 × 80 × 30 mm) with limited airflow. Motor driver (DRV8316) at 5 A can dissipate 2–3 W. Battery internal resistance adds heat during peak draw. |
| Impact | Overheating → throttling → reduced assistance; worst case: thermal shutdown mid-session. |
| Mitigation | (1) Thermally couple driver to aluminum enclosure; (2) Add thermal pad + heat spreader; (3) Measure junction temperatures in worst-case test; (4) Software current limit at 80°C enclosure temperature. |
| Phase to address | **Month 4**, during enclosure design. |

### RISK 7: Regulatory (NMPA Class II)

**Severity:** MEDIUM (product) / HIGH (timeline) | **Probability:** MEDIUM | **Mitigation Cost:** MEDIUM

| Factor | Detail |
|--------|--------|
| Problem | NMPA Class II medical device requires: ISO 13485 QMS, usability engineering (IEC 62366), software lifecycle (IEC 62304), risk management (ISO 14971), clinical evaluation. None of these are built into a prototype-first engineering approach. Retrospective compliance is expensive. |
| Impact | Clinical trial delayed 6–12 months if design history file must be reconstructed. |
| Mitigation | (1) Hire NMPA regulatory consultant **before** prototype (Month 0); (2) Maintain design history file from Day 1; (3) Document all design decisions with rationale; (4) Use certified components (ISO 10993) where possible; (5) Target "innovative medical device" fast-track designation. |
| Phase to address | **Month 0–ongoing.** Regulatory is a schedule-critical path item. |

---

## 5. First Prototype Build Plan

### 5.1 Guiding Principles

1. **Reduce latency risk first:** The biggest unknown is whether dry EEG can work during gait. Test this in Month 1 with a wired EEG + motion simulator, before any wireless or mechanical work.
2. **Phone as inference engine (Phase 1):** Skip embedded ML for now. Phone processing lets us iterate the AI model rapidly without firmware updates.
3. **Off-the-shelf motor for prototype:** Do not design custom motor. Buy T-motor for first prototype.
4. **3D print everything mechanical:** CNC/carbon fiber for production, not for early prototypes.
5. **Failing fast is the goal:** The first integrated prototype (Month 3) will almost certainly not work well. That's fine — it tells us what to fix.

### 5.2 Buy vs Build vs Outsource

| Item | Decision | Vendor / Method | Estimated Cost (¥) | Timeline |
|------|----------|-----------------|-------------------|----------|
| **EEG Front-End** | Buy | ADS1299 evaluation module + custom carrier board | 8,000 | Week 2 |
| **Dry Electrodes (8)** | Buy | OpenBCI compatible dry comb electrodes | 1,500 | Week 1 |
| **EEG Headband PCB + Assembly** | Build | Custom PCB (ADS1299 + nRF52832 + power) | 20,000 (first batch of 10) | Week 4–8 |
| **BLE Module** | Buy | Nordic nRF52832 DK (dev kit) × 2 | 1,500 | Week 1 |
| **BLE Module** | Buy | Nordic nRF5340 DK × 2 | 1,200 | Week 1 |
| **IMU** | Buy | Bosch BMI270 breakout | 200 | Week 1 |
| **Motor (BLDC)** | Buy | T-motor AK80-9 (× 2, one spare) | 3,000 | Week 2 |
| **Motor Driver** | Buy | TI DRV8316 eval module + custom board | 4,000 | Week 3 |
| **Motor Driver PCB** | Build | Custom carrier for DRV8316 + STM32H743 | 15,000 | Week 4–8 |
| **MCU Dev Board** | Buy | STM32H743 Nucleo | 800 | Week 1 |
| **Battery (6S)** | Buy | Custom 6S Li-ion pack from 18650 seller | 3,000 | Week 4 |
| **BMS** | Buy | TI BQ76952 evaluation module | 1,500 | Week 4 |
| **Load Cell (tension)** | Buy | S-type load cell 1000 N + HX711 | 800 | Week 3 |
| **Hip Joint Mech** | Build | 3D printed (PLA/ABS) + aluminum shaft | 2,000 (materials) | Week 4–6 |
| **Carbon Fiber Anchor** | Outsource | Local CNC shop (carbon fiber plate + hip belt frame) | 10,000 | Week 6–8 |
| **Suit Fabric** | Outsource | Local tailor / garment factory (custom webbing + neoprene) | 5,000 | Week 6–8 |
| **Bowden Cable + Sheath** | Buy | Standard bicycle brake cable (PTFE-lined) — cheap, available | 200 | Week 2 |
| **Control Box Enclosure** | Build | 3D printed (PETG) for prototype; CNC aluminum for V2 | 1,000 (3D print) | Week 5–7 |
| **Force Sensor (cable)** | Build | Inline load cell mount (3D print + strain gauge) | 500 | Week 5 |
| **Phone (for test)** | Buy | Used iPhone SE (hardware ML test device) | 2,500 | Week 1 |
| **Oscilloscope** | Buy | Rigol DS1054Z (4-ch, 50 MHz) | 2,500 | Week 1 |
| **Power supply** | Buy | Korad KA3005D (30 V, 5 A) | 1,500 | Week 1 |
| **Signal generator** | Buy | JDS6600 (EEG simulator for test) | 1,200 | Week 2 |
| **Tooling** | Buy | Soldering station, multimeter, hand tools | 3,000 | Week 1 |
| **3D Printer** | Buy | Bambu Lab P1S (fast prototyping) | 4,000 | Week 1 |
| **Contingency** | — | — | 93,300 | — |
| | | | **¥200,000 total** | |

**Total: ~¥200,000** (approximately ¥107,000 in direct BOM + test equipment + ~¥93,000 contingency for PCB respins, mechanical redesigns, and unexpected costs). This leaves ¥1,800,000 for: 6 months of team salary, clinical fees, office/lab space, and regulatory consulting.

### 5.3 Team Allocation (8 People, 6 Months)

| Role | Headcount | Focus (Month 1–3) | Focus (Month 3–6) |
|------|-----------|-------------------|-------------------|
| **EE Hardware Lead** | 1 | EEG headband PCB design + electrode test rig + debugging | Headband V2, EMC testing |
| **Embedded Firmware** | 1 | BLE protocol, motor control firmware, sensor drivers | Control loop tuning, sensor fusion |
| **Mechanical Engineer** | 1 | Bowden cable test bench, hip joint CAD, suit integration | Design for manufacturing, carbon fiber parts |
| **Algorithm / ML** | 1 | EEG data collection pipeline, model training on BP detection | Real-time inference on phone, personalization |
| **System Integration** | 1 | Protocol spec, integration test harness, HIL bench | E2E validation, certification prep |
| **Product / PM** | 1 | User testing coordination, requirements management | Clinician interviews, Home vs Clinical spec |
| **Clinical / Regulatory** | 1 | IRB prep, NMPA innovation device application | Clinical protocol design, ISO 13485 gaps |
| **Industrial Designer** | 1 | Wearable ergonomics, headband form factor, suit aesthetics | Production-ready industrial design |

### 5.4 6-Month Development Timeline

```
Month 01 | Month 02 | Month 03 | Month 04 | Month 05 | Month 06
─────────────────────────────────────────────────────────────────────
EEG TEST    │         │         │         │         │
RIG ───────►│         │         │         │         │
 (Wired)    │ PCB V1  │         │         │         │
            │ ───────►│ FW+TEST │         │         │
            │         │ ───────►│  PCB V2 │         │
            │         │         │  ──────►│ INTEGR. │
            │CABLE    │         │         │ ───────►│
MOTOR TEST  │BENCH    │ PROTOT. │         │         │
BENCH ─────►│────────►│ SUIT V1 │ ME V2   │ E2E     │
            │         │ ───────►│────────►│ TEST ──►│
            │ML DATA   │         │         │         │
            │COLLECT   │ MODEL   │ ON-PHONE│ TUNE    │
BP ALGO     │────────►│ TRAIN ─►│ TEST ──►│ ───────►│
            │         │         │         │         │
PROTOCOL    │ INTEG.  │         │         │         │
SPEC ──────►│ HIL     │ SUBSYS  │ E2E V1  │ E2E V2  │
            │ ───────►│ TEST ──►│ TEST ──►│ ───────►│
            │         │         │         │         │
            │ IRB     │         │ CLIN    │         │
REGULATORY  │ SUBMIT  │  NMPA   │ DATA    │ REPORT  │
───────────►│────────►│ ───────►│ COLLECT │────────►│
```

**Key Milestones:**

| Month | Milestone | Deliverable |
|-------|-----------|-------------|
| M1 | EEG feasibility confirmed | SNR report: dry EEG under motion ≥ 3 dB |
| M1 | Communication protocol frozen | Proto spec document signed by all teams |
| M2 | Motor + cable characterization done | Torque control transfer function; friction model |
| M2 | Headband PCB V1 assembled | 8-channel wireless EEG streaming to phone |
| M3 | First integrated prototype (lab bench) | Signals: EEG→Phone→Motor→Force. Not wearable yet. |
| M4 | Wearable prototype assembled | Headband + control box + suit fully integrated, tethered only for debug |
| M4 | ML model achieves > 75% BP detection AUC on 5 subjects | Offline evaluation on collected dataset |
| M5 | Real-time intention decoding on phone | < 200 ms E2E latency verified on test bench |
| M5 | IRB approved for pilot clinical study | Can begin recruitment |
| M6 | E2E validation: 5 healthy subjects, 3 stroke patients | Latency < 200 ms, torque accuracy < ±0.5 Nm, no SAEs |
| M6 | NMPA innovative device application submitted | Decision within 60 days |

### 5.5 Prototype Success Criteria

A successful first prototype must demonstrate:

1. **Data flow completeness:** EEG signal acquired, transmitted, decoded, and converted to motor torque — no matter how poorly — at least once.
2. **E2E latency < 200 ms:** Measured on bench with simulated EEG signal.
3. **Torque control accuracy < ±1 Nm:** At steady state, under no-load bench test.
4. **Wearable for 30 minutes:** No skin irritation, no electrode detachment, no overheating.
5. **EEG detectable during walking:** On at least 3/5 healthy subjects, MRCP visible in at least 50% of strides.

---

## 6. Appendix: Communication Protocol Summary

To avoid the most common integration failure (protocol mismatch), the following interfaces are defined upfront:

### 6.1 EEG Headband → Phone (BLE)

| Parameter | Value |
|-----------|-------|
| Transport | BLE GATT Notify |
| Service UUID | `0xFEE0` (custom) |
| Characteristic | `EEG_DATA` (UUID: `EEG0-001`) |
| Packet format | 8 channels × 3 bytes (24-bit signed) + 1 byte status + 2 byte sequence = **27 bytes per packet** |
| Packet interval | 20 ms (50 Hz update) |
| Battery characteristic | `BATT_LEVEL` (UUID: `EEG0-002`), 1 byte, 0–100% |

### 6.2 Phone → Control Box (BLE)

| Parameter | Value |
|-----------|-------|
| Transport | BLE GATT Write |
| Service UUID | `0xFEE1` (custom) |
| Characteristic | `CMD_TORQUE` (UUID: `CTL0-001`) |
| Packet format | 2 byte torque setpoint (0.01 Nm resolution) + 1 byte command type + 2 byte sequence = **5 bytes** |
| Command types | 0x01: torque profile (setpoint + duration), 0x02: emergency stop, 0x03: calibration home |

### 6.3 Control Box → Phone (BLE)

| Parameter | Value |
|-----------|-------|
| Transport | BLE GATT Notify |
| Service UUID | `0xFEE2` (custom) |
| Characteristic | `STATE_VECTOR` (UUID: `CTL0-002`) |
| Packet format | 4-byte hip angle (float, degrees) + 4-byte angular velocity + 4-byte cable force (N) + 2-byte motor position + 1-byte status = **15 bytes**, @ 50 Hz |

### 6.4 Wired Internal (Control Box Internals)

| Interface | Protocol | Pins | Baud / Speed |
|-----------|----------|------|-------------|
| MCU ↔ Motor Driver | SPI / PWM | SCK, MOSI, MISO, CS + 2 PWM | 10 MHz SPI, 50 kHz PWM |
| MCU ↔ IMU | I2C | SCL, SDA | 400 kHz |
| MCU ↔ Force Sensor | Analog (ADC) / I2C | AIN or I2C | 12-bit, 200 Hz |
| MCU ↔ BLE Module | UART | TX, RX, RTS, CTS | 921600 baud |

---

*End of document. This is a living draft — update as specifications are validated or changed.*
