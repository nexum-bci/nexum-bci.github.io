# Nexum One — Integration & Test Plan

**v0.1** · 2026-06-21

---

## 1. Test Philosophy

**Failing fast is the goal.** The first integrated prototype will almost certainly not work well — it tells us _what to fix_. Each test phase has a single pass/fail criterion. If it fails, we fix before moving on.

**Hardware-in-the-loop (HIL) from day 1.** Before the mechanical prototype exists, the control box firmware is tested against a simulated plant model.

---

## 2. Test Phases

```
Phase 0: Subsystem Bench Tests (Month 1–2)
Phase 1: Wired Integration (Month 2–3)
Phase 2: Wireless Integration (Month 3–4)
Phase 3: Wearable Prototype (Month 4–5)
Phase 4: Human Subject Testing (Month 5–6)
```

---

## 3. Phase 0: Subsystem Bench Tests

### T0.1 — EEG Signal Quality (Week 1–4)

**Setup:**
- ADS1299 eval board + OpenBCI dry electrodes
- Signal generator (JDS6600) → resistor divider → µV-level sine
- 5 healthy subjects, sitting, eyes open/closed

**Test Procedure:**
1. Place 8 dry electrodes at Cz, C3, C4, FCz, FC3, FC4, Pz, P3 (10-20 system)
2. Record 5 min resting state (eyes open / eyes closed alternating)
3. Record 5 min with cue-based ankle dorsiflexion (intentional movement)
4. Measure electrode-skin impedance (target: <500 kΩ per channel)

**Pass Criteria:**
- Input-referred noise <1 µV RMS (0.5–100 Hz)
- CMRR >100 dB at 50 Hz
- Visible alpha rhythm (8–12 Hz) at Cz during eyes-closed
- Impedance <500 kΩ on ≥6/8 channels within 2 min of placement

### T0.2 — Motor + Cable Bench Test (Week 2–5)

**Setup:**
- T-motor AK80-9 + DRV8316 eval board + STM32H743 Nucleo
- Bowden cable (PTFE-lined) + S-type load cell
- Cable routed through 3D-printed hip joint simulator

**Test Procedure:**
1. Characterize motor: measure Kt, Ke, phase R/L with LCR meter
2. FOC current loop tuning: step response to 1A i_q step (target: <2ms settling)
3. Torque control: command 0–10 Nm ramp, measure load cell vs setpoint
4. Bowden cable efficiency: measure output force / input force at 0°, 30°, 60°, 90° bend
5. Cable friction hysteresis: load→unload cycle, measure deadband
6. Endurance: 10,000 cycles at 8 Nm, measure efficiency degradation

**Pass Criteria:**
- Torque rise time (0→8 Nm) <60 ms
- Torque accuracy ±0.5 Nm steady state
- Cable efficiency >70% at ≤30° bend
- <5% efficiency degradation after 10,000 cycles

### T0.3 — BLE Throughput Test (Week 3–4)

**Setup:**
- nRF52832 DK (simulates EEG headband)
- nRF5340 DK (simulates control box)
- iPhone SE (test device)

**Test Procedure:**
1. nRF52832 streams 27-byte packets at 50 Hz (simulating EEG data rate)
2. nRF5340 sends 15-byte state vector at 50 Hz
3. Phone sends 5-byte torque commands at 50 Hz
4. Measure packet loss, latency, and jitter over 30 min

**Pass Criteria:**
- Packet loss <0.1%
- One-way latency (TX→RX app-level) <15 ms p95
- No disconnections in 30-minute test

### T0.4 — IMU Accuracy Test (Week 3)

**Setup:**
- BMI270 on breakout board + STM32H743 Nucleo
- 3D-printed test fixture on servo-controlled tilt platform

**Test Procedure:**
1. Static accuracy: place IMU at known angles (0°, 30°, 60°, 90°), measure error
2. Dynamic accuracy: sinusoidal rotation 0.5–3 Hz, measure tracking error
3. Gyro drift: record 30 min stationary, measure accumulated drift
4. Sensor fusion (Madgwick): compare fused quaternion vs ground truth

**Pass Criteria:**
- Static angle error <1°
- Dynamic tracking error <2° RMS at 1 Hz
- Gyro drift <0.5°/minute
- Fusion settling time <2s from any orientation

---

## 4. Phase 1: Wired Integration (Bench, No Wearable)

**Goal:** Prove data flows end-to-end: EEG → Phone → Motor → Force. Not wearable yet.

**Setup:**
- EEG headband PCB V1 (or ADS1299 eval board if PCB not ready)
- BLE to phone
- Phone running minimal Nexum App (just: receive EEG → simple threshold detector → send torque cmd)
- nRF5340 DK connected to DRV8316 eval board + T-motor
- Motor under no-load bench test (spool winding cable against test spring)

**Test Procedure:**
1. Place EEG electrodes on subject (sitting)
2. Subject performs cued ankle dorsiflexion (or imagined stepping)
3. Observe: does motor spin when subject intends to move?
4. Measure E2E latency: EEG signal trace → BLE packet timestamp → motor encoder response

**Pass Criteria:**
- Motor actuates within 200ms of EEG cue onset (at least once — this is a smoke test)
- System does not crash or disconnect during 60-minute test
- Emergency stop works: motor stops <50ms after button press

---

## 5. Phase 2: Wireless Integration

**Same as Phase 1, but:**
- EEG headband is fully wireless (not eval board with USB)
- Control box is battery-powered (not bench supply)
- Phone not connected to debugger

**Additional Test:**
- Battery life: stream EEG + motor under simulated gait load (8W avg) → measure time to 20% SoC

**Pass Criteria:**
- Battery life >4h at average 8W draw
- No BLE disconnections in 4-hour test
- E2E latency <200ms, measured with photodiode on motor and EEG signal trigger

---

## 6. Phase 3: Wearable Prototype

**Setup:**
- Full system: wireless EEG headband + NeuroSuit (3D-printed hip anchors + compression garment + control box)
- 5 healthy subjects
- Treadmill walking at 3 km/h

**Test Procedure:**
1. Subject dons system (timed, unassisted after first training)
2. Walk on treadmill for 10 min with system in "monitor-only" mode (no assistance)
3. Walk for 10 min with EEG-triggered assistance (conservative: 3 Nm, short duration)
4. Walk for 10 min with sEMG+IMU assistance (EEG disabled, sEMG-triggered)
5. Post-wear survey: comfort, perceived control, "would you wear this daily?"

**Measurements:**
- EEG signal quality during walking (SNR at Cz), compared to sitting baseline
- Don/doff time
- Skin pressure at hip anchors (pressure mapping film)
- Enclosure temperature after 30 min
- Cable force tracking accuracy vs setpoint

**Pass Criteria:**
- Don/doff <3 min (single person)
- No skin irritation after 30 min
- Enclosure surface <48°C
- ≥3/5 subjects report "feels like I'm in control" (not "robot is pushing me")
- EEG SNR during walking ≥3 dB (at Cz, 0.5–40 Hz band, relative to sitting baseline)

---

## 7. Phase 4: Human Subject Testing (Pre-Clinical)

### T4.1 — EEG Decoding Accuracy (5 healthy subjects)

**Protocol:**
1. Subjects walk on treadmill at 3 km/h
2. Cue-based paradigm: "walk" / "stop" cues at random intervals
3. Record 8-ch EEG + IMU + gait phase
4. Offline: train EEGNet on first 70% of data, test on remaining 30%
5. Metrics: sensitivity, specificity, AUC for "walk" vs "stop" classification

**Pass Criteria:**
- Sensitivity ≥75% (correctly detects intention to walk)
- Specificity ≥90% (does NOT falsely detect intention)
- AUC ≥0.80
- Detection latency <500ms from Bereitschaftspotential onset

### T4.2 — Assist-as-Needed Validation (5 healthy subjects)

**Protocol:**
1. Subjects walk on treadmill at 3 km/h, 5 min each condition:
   - No suit (baseline)
   - Suit passive (no assistance)
   - Constant assistance (5 Nm)
   - EEG-triggered assistance (5 Nm, correct timing only)
   - Sham assistance (5 Nm at random, wrong timing)
2. Measure: metabolic cost (VO2, indirect calorimetry), gait symmetry (IMU), perceived effort (Borg scale)

**Pass Criteria:**
- Metabolic cost: EEG-triggered < passive (p<0.1 exploratory)
- EEG-triggered perceived effort significantly lower than sham (p<0.05)
- No adverse events (falls, skin abrasion, muscle strain)

### T4.3 — 30-Minute Usability (5 healthy subjects)

**Protocol:**
1. Subject performs: sit→stand→walk 10m→turn→walk back→sit. Repeat for 30 min.
2. Record: completion rate, subjective fatigue, any system faults

**Pass Criteria:**
- 5/5 subjects complete 30 min
- Zero system faults (disconnections, unexpected stops, torque anomalies)
- Mean SUS (System Usability Scale) >70

---

## 8. Test Equipment Checklist

| Equipment | Purpose | Estimated Cost (¥) |
|-----------|---------|--------------------|
| Rigol DS1054Z oscilloscope | Signal debug, timing | 2,500 |
| JDS6600 signal generator | EEG simulator | 1,200 |
| S-type load cell 1000N + HX711 | Cable force measurement | 800 |
| Korad KA3005D PSU | Bench power | 1,500 |
| Fluke 17B+ multimeter | Voltage/current/resistance | 600 |
| LCR meter (cheap) | Motor phase characterization | 500 |
| Photodiode + scope | E2E latency measurement | 100 |
| Pressure mapping film (Fujifilm Prescale) | Skin pressure | 500/pack |
| COSMED K5 (or rent) | VO2 measurement | ~50,000 (rent) |
| 3D-printed test fixtures | Various | 500 (material) |
| Treadmill (gym access or buy) | Walking test | 5,000 (used) |

---

## 9. Test Data Management

- All test data stored in structured format: `test_reports/YYYY-MM-DD/<test_id>/`
- Raw data (EEG, IMU, motor): HDF5 or NPZ format
- Metadata: JSON with subject ID, date, configuration, pass/fail
- Scripts under `tests/` directory for automated analysis
- Git-tracked: test scripts and analysis code (NOT raw data — too large)

---

*End of Test Plan v0.1. Update after Phase 0 bench tests.*
