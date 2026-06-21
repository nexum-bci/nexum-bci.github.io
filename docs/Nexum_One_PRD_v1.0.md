# Nexum One — Product Requirements Document

**Version 1.0** · 2026-06-21
**Author:** Zirui Zhao · Architecture
**Classification:** Internal — Engineering

---

## 1. Product Definition

Nexum One is a **neural reconnection AI system** for lower-limb motor function reconstruction. It reads motor intention from the brain (non-invasive EEG), generates personalized assistance strategies (MSK digital twin + RL), and executes assistive torque at the hip joint (Bowden cable-driven NeuroSuit).

**Target population:** Stroke survivors and incomplete SCI patients with preserved cortical function but impaired motor execution.

**Regulatory classification:** NMPA Class II innovative medical device.

---

## 2. User Needs → Engineering Requirements

| # | User Need | Engineering Requirement | Verification Method |
|---|-----------|------------------------|---------------------|
| U1 | "I want to walk when I intend to walk" | System detects movement intention ≥75% sensitivity, ≥90% specificity | EEG decoding benchmark on 5 subjects |
| U2 | "I don't want to feel like a robot is pushing me" | Torque rise time <60ms, torque ripple <±0.5 Nm | Load cell measurement on test bench |
| U3 | "I want to wear it without help" | Don/doff time <3 min, single person | Timed test with 5 naive users |
| U4 | "I don't want to look like a patient" | Suit resembles athletic compression wear; no visible rigid frame | User perception survey (n≥20) |
| U5 | "I want to use it for my full rehab session" | Battery life ≥4h continuous use at avg 8W draw | Battery discharge test with simulated load |
| U6 | "I'm worried about skin irritation" | All skin-contact materials ISO 10993-10 certified; no pressure points >32 mmHg | Pressure mapping + biocompatibility cert |
| U7 | "I need to see my progress" | App shows daily step count, assistance level trend, muscle activation symmetry | Usability test with 5 patients + 3 therapists |
| U8 | "My condition changes — the device should adapt" | AI model adapts within first 10 min of each session; strategy differs week-to-week | Pre/post adaptation comparison over 4 weeks |

---

## 3. Functional Requirements

### 3.1 EEG Acquisition
| ID | Requirement | Priority | Target |
|----|------------|----------|--------|
| EEG-01 | Acquire 8-channel EEG at ≥250 SPS, 24-bit resolution | P0 | Must |
| EEG-02 | Input-referred noise <1 µV RMS (0.5–100 Hz) | P0 | Must |
| EEG-03 | CMRR >100 dB at 50 Hz | P0 | Must |
| EEG-04 | Electrode-skin impedance measurement per channel (range: 1 kΩ–1 MΩ) | P1 | Should |
| EEG-05 | On-board preprocessing: CAR, 0.5–40 Hz bandpass, 50 Hz notch | P0 | Must |
| EEG-06 | Wireless transmission (BLE 5.0) of preprocessed data to phone | P0 | Must |
| EEG-07 | Headband weight ≤80g, don in <30s without assistance | P0 | Must |
| EEG-08 | Operate with dry electrodes (no gel, no skin prep) | P0 | Must |

### 3.2 Motor Control
| ID | Requirement | Priority | Target |
|----|------------|----------|--------|
| MOT-01 | Continuous assist torque: 8 Nm at hip joint | P0 | Must |
| MOT-02 | Peak assist torque: 15 Nm for 3s | P0 | Must |
| MOT-03 | Torque control bandwidth ≥10 Hz | P0 | Must |
| MOT-04 | Torque accuracy ±0.5 Nm steady-state | P1 | Should |
| MOT-05 | Emergency stop: motor power cut within 50ms of fault detection | P0 | Must |
| MOT-06 | Cable force sensor: inline load cell ±1% FS accuracy, 200 Hz | P1 | Should |

### 3.3 AI Inference
| ID | Requirement | Priority | Target |
|----|------------|----------|--------|
| AI-01 | Movement intention detection latency <55ms (from BLE RX to command TX) | P0 | Must |
| AI-02 | Intention classes: "walk", "stop", "stand up", "sit down", "rest" | P0 | Must |
| AI-03 | False positive rate <10% (assistance when user did NOT intend) | P0 | Must |
| AI-04 | False negative rate <25% (no assistance when user DID intend) | P1 | Should |
| AI-05 | Model personalization: adaptation within first 10 min of session | P0 | Must |
| AI-06 | On-device inference (CoreML / ONNX on phone, no cloud dependency for real-time) | P0 | Must |

### 3.4 Safety
| ID | Requirement | Priority | Target |
|----|------------|----------|--------|
| SAF-01 | Three-level degradation: EEG+sEMG → sEMG+IMU → passive support (no sudden stop) | P0 | Must |
| SAF-02 | Joint angle limit: hip flexion ≤90°, hip extension ≤20° (mechanical hard stop) | P0 | Must |
| SAF-03 | Cable force limit: 800N mechanical fuse | P0 | Must |
| SAF-04 | Over-temperature protection: motor driver junction <125°C; enclosure surface <48°C | P0 | Must |
| SAF-05 | Battery: overcharge/overdischarge/short-circuit protection (BMS) | P0 | Must |
| SAF-06 | IEC 60601-1 (medical electrical equipment safety) compliance | P1 | Should |

### 3.5 Software
| ID | Requirement | Priority | Target |
|----|------------|----------|--------|
| SW-01 | Nexum App: iOS 18+ and Android 15+ | P0 | Must |
| SW-02 | Therapist dashboard: view 20+ patients, remote progress monitoring | P1 | Should |
| SW-03 | Data processing: raw physiological signals processed locally; only de-identified model improvements uploaded | P0 | Must |
| SW-04 | Session log: date, duration, steps, assistance level, anomalies | P0 | Must |
| SW-05 | Weekly progress report: auto-generated PDF for patient + clinician | P1 | Should |

---

## 4. Non-Functional Requirements

| Category | Requirement | Target |
|----------|-------------|--------|
| Reliability | MTBF (electronics) | >5,000 hours |
| Durability | Motor cycles before replacement | >10^6 cycles |
| Durability | Cable cycles before replacement | >5×10^5 cycles |
| Durability | Suit wash cycles (fabric) | >100 machine wash cycles |
| Environment | Operating temperature | 10–40°C |
| Environment | Operating humidity | 20–80% RH non-condensing |
| Environment | IP rating | IP22 (control box); IPX4 (suit) |
| Maintainability | Battery replacement | User-replaceable, <1 min |
| Maintainability | Electrode replacement | >500 uses per electrode set |
| Maintainability | Firmware update | OTA via Nexum App |
| Usability | Learning time (first use) | <15 min with therapist guidance |
| Usability | Setup time (subsequent uses) | <3 min |
| EMC | Emissions | CISPR 11 Group 1 Class B |
| EMC | Immunity | IEC 60601-1-2 |

---

## 5. What Nexum One is NOT (Scope Boundaries)

- **NOT a full-body exoskeleton** — hip joint only in V1. Knee/ankle are V2+.
- **NOT for complete paralysis** — requires preserved cortical motor function. If patient cannot form movement intention, EEG-based approach will not work.
- **NOT for cognitive impairment** — requires ability to follow basic instructions.
- **NOT for pediatric use** — adult sizing only in V1 (waist 65–145 cm, thigh 40–80 cm).
- **NOT a replacement for physical therapy** — it's a tool that enables more therapy with less therapist supervision.
- **NOT implantable** — entirely non-invasive.

---

## 6. Competitive Benchmark Targets

| Metric | Nexum One Target | EksoNR | ReWalk Personal 6.0 | HAL Lower Limb |
|--------|-----------------|--------|---------------------|----------------|
| System weight | <2.5 kg | ~25 kg | ~13.5 kg | ~12 kg |
| E2E latency | <185 ms | N/A (button control) | N/A (posture shift) | ~300 ms (EMG) |
| Setup time | <3 min | 5–10 min | 5–10 min | 10–15 min |
| Price (clinical) | $18,000 | $75,000–95,000 | $85,000–100,000 | $60,000–80,000 |
| Price (home) | $3,999 + $499/yr | N/A | $70,000+ | N/A |
| Intent detection | EEG + sEMG | None | Tilt sensor | sEMG only |
| Personalization | AI (MSK+RL) | Manual parameter adjustment | Manual | Pre-programmed modes |
| Data network effect | Yes (federated) | No | No | No |

---

## 7. Phase 0 Success Criteria (Prototype)

The first prototype is successful if ALL of the following are demonstrated:

1. **Data flow completeness** — EEG signal acquired, transmitted via BLE, decoded to movement intention, converted to motor torque, applied to hip joint. At least once. Doesn't need to be accurate yet.
2. **E2E latency <200ms** — Measured on bench with simulated EEG signal (signal generator feeding ADS1299 input).
3. **Torque control ±1 Nm** — At steady state, no-load bench test.
4. **Wearable for 30 min** — No skin irritation, no electrode detachment, enclosure temperature <48°C.
5. **EEG detectable during walking** — On ≥3/5 healthy subjects, Bereitschaftspotential visible in ≥50% of strides at Cz electrode.

---

*End of PRD v1.0. Update after Phase 0 prototype results.*
