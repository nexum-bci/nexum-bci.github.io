# Nexum One — Firmware Architecture

**v0.1** · 2026-06-21
**Scope:** EEG-Sense headband firmware + Control Box firmware + BLE protocol stack

---

## 1. System Overview

```
┌─────────────────────────────────────┐
│           EEG-Sense (nRF52832)       │
│  ┌───────┐  ┌──────┐  ┌──────────┐  │
│  │ADS1299│  │ DSP  │  │ BLE Stack│  │
│  │ Driver │→ │ CAR  │→ │ Notify   │  │
│  │       │  │ IIR  │  │ 50 Hz    │  │
│  └───────┘  └──────┘  └──────────┘  │
└────────────────┬────────────────────┘
                 │ BLE (GATT Notify)
                 ▼
┌─────────────────────────────────────┐
│        Nexum App (Phone)             │
│  ┌──────────┐  ┌──────────────────┐  │
│  │ BLE RX   │  │ CoreML/ONNX      │  │
│  │ Buffer   │→ │ EEGNet Inference │  │
│  └──────────┘  └────────┬─────────┘  │
│                         │ Intention   │
│  ┌──────────────────────▼──────────┐  │
│  │ MSK model → RL policy → CMD    │  │
│  └──────────────────────┬──────────┘  │
└─────────────────────────┬───────────┘
                          │ BLE (GATT Write)
                          ▼
┌─────────────────────────────────────┐
│       Control Box (nRF5340 + STM32)  │
│  ┌────────┐ ┌──────────┐ ┌───────┐  │
│  │BLE RX  │ │Sensor    │ │Motor  │  │
│  │+ Parse │→│Fusion    │→│FOC    │→ │
│  └────────┘ └──────────┘ └───────┘  │
│  ┌────────┐ ┌──────────┐ ┌───────┐  │
│  │Safety  │ │State     │ │BLE TX │  │
│  │Monitor │ │Estimator │ │Notify │  │
│  └────────┘ └──────────┘ └───────┘  │
└─────────────────────────────────────┘
```

---

## 2. EEG-Sense Headband Firmware (nRF52832)

### 2.1 Architecture

**RTOS:** FreeRTOS (or Zephyr RTOS if using nRF Connect SDK)
**Language:** C
**SDK:** nRF5 SDK 17.1.0 or nRF Connect SDK 2.x

### 2.2 Tasks

| Task | Priority | Period | Stack | Description |
|------|----------|--------|-------|-------------|
| `ads1299_read_task` | HIGH | 4 ms (250 Hz) | 2048 B | SPI read 8 channels from ADS1299, push to ring buffer |
| `dsp_task` | HIGH | 4 ms | 4096 B | CAR, bandpass (0.5–40 Hz), notch (50 Hz) on latest buffer |
| `ble_notify_task` | MEDIUM | 20 ms (50 Hz) | 1024 B | Packetize 27-byte data, send GATT notify |
| `impedance_check_task` | LOW | 1000 ms | 512 B | Measure electrode impedance per channel |
| `power_mgmt_task` | LOW | 100 ms | 256 B | Monitor battery, manage sleep states |
| `cmd_handler_task` | MEDIUM | Event-driven | 512 B | Handle BLE write commands from App |

### 2.3 ADS1299 Driver

```c
// Initialization sequence (power-on → DRDY interrupt → read data)
typedef struct {
    uint8_t  id;              // ADS1299 ID register (should read 0x3E)
    uint8_t  chan_count;      // 8
    uint16_t sample_rate;     // 250 SPS
    uint8_t  gain;            // 12 or 24
    uint8_t  input_mode;      // Normal electrode input
    uint8_t  bias_drive;      // DRL bias drive enabled
    uint8_t  lead_off_mode;   // Lead-off detection current
    bool     internal_ref;    // Use internal reference (4.5V)
} ads1299_config_t;

// Data format per sample: 8 channels × 3 bytes (24-bit signed), MSB first
typedef struct __attribute__((packed)) {
    int32_t ch[8];  // Sign-extended from 24-bit
    uint8_t status; // Lead-off flags + GPIO
    uint16_t seq;   // Sequence number
} eeg_sample_t;
```

### 2.4 DSP Pipeline (on nRF52832 Cortex-M4F)

```
Raw samples (8ch × 250Hz × 24bit)
  → DC offset removal (1st order HPF, fc=0.1 Hz)
  → Common Average Referencing (CAR): ch[n] -= mean(all channels)
  → Butterworth bandpass 0.5–40 Hz (4th order, cascaded biquads)
  → Notch 50 Hz (2nd order IIR)
  → Output: 8ch × 250 SPS × 16-bit (round to 16-bit to save BLE bandwidth)
```

**IIR filter implementation:** Direct Form II transposed biquad sections.
**Coefficient storage:** Pre-computed and stored in flash. Switchable filter bank for different bandwidth settings.

### 2.5 BLE GATT Service Definition

```
Service: 0xFEE0 (EEG Data Service)
  Characteristic: EEG_DATA (UUID: EEG0-001)
    Properties: Notify
    Format: 27 bytes per packet
      - 8 channels × 2 bytes (16-bit, MSB)
      - 8 bytes electrode status bits
      - 1 byte battery level (0–100%)
      - 2 byte sequence number
    
  Characteristic: IMPEDANCE (UUID: EEG0-003)
    Properties: Read, Notify
    Format: 8 channels × 2 bytes (kΩ × 10)
    
  Characteristic: CMD_RX (UUID: EEG0-004)
    Properties: Write
    Format: 1 byte command + 2 bytes parameter

Service: 0x180F (Battery Service — standard)
```

### 2.6 Power Management

| State | Current Draw | Entry Condition | Exit Condition |
|-------|-------------|-----------------|----------------|
| Active (streaming) | ~25 mA | User wearing + App connected | — |
| Idle (advertising) | ~5 mA | Power on, no connection | App connects |
| Deep sleep | ~50 µA | Power button long press | Power button press |
| Charging | N/A | USB-C plugged in | USB-C unplugged |

**Battery life (active):** 200 mAh / 25 mA ≈ 8 hours (target >4h achieved)

---

## 3. Control Box Firmware

### 3.1 Dual-Core Architecture (nRF5340 + optional STM32H743)

**Option A (Proto):** nRF5340-only
- **App core (Cortex-M33, 128 MHz):** BLE stack, command parsing, sensor fusion
- **Net core (Cortex-M33, 64 MHz):** Motor control FOC, safety monitor

**Option B (Production):** nRF5340 (BLE + sensor) + STM32H743 (motor control)
- nRF5340 handles BLE and IMU sensor fusion
- STM32H743 handles motor FOC, encoder reading, load cell ADC

### 3.2 Option B Task Map (Production Target)

#### nRF5340 App Core

| Task | Priority | Period | Description |
|------|----------|--------|-------------|
| `ble_rx_task` | HIGH | Event | Receive command from phone, parse, push to command queue |
| `imu_read_task` | HIGH | 10 ms | Read BMI270 (6-axis), push to sensor buffer |
| `sensor_fusion_task` | HIGH | 10 ms | Madgwick AHRS → hip angle, angular velocity |
| `state_tx_task` | MEDIUM | 20 ms | Packetize state vector, BLE notify to phone |
| `safety_watchdog_task` | HIGH | 5 ms | Monitor STM32 heartbeat, check limits, trigger E-stop if needed |

#### STM32H743 (Motor Control)

| Task | Priority | Period | Description |
|------|----------|--------|-------------|
| `foc_loop` | CRITICAL | 50 µs (20 kHz) | Field-Oriented Control current loop |
| `torque_controller` | HIGH | 1 ms | PI controller: torque setpoint → i_q reference |
| `encoder_read_task` | HIGH | 1 ms | SPI read AS5048A magnetic encoder |
| `loadcell_read_task` | MEDIUM | 5 ms | Read HX711 load cell amplifier |
| `cmd_dispatch_task` | HIGH | 2 ms | Pop from command queue → update torque setpoint |
| `thermal_monitor_task` | LOW | 500 ms | Read temperature sensors, throttle if >80°C |

### 3.3 FOC Motor Control

```
Control structure (cascaded loops):

Torque Cmd → [PI Torque Controller] → iq_ref → [PI Current Loop] → Vq → [SVPWM] → DRV8316
              ↑ Actual torque (load cell)         ↑ ia, ib, ic (shunt current sense)
              
iq_ref = torque_cmd / Kt           (Kt = motor torque constant, Nm/A)
id_ref = 0                          (Maximum Torque Per Ampere for surface PMSM)

Current loop: 20 kHz (50 µs period)
Torque loop:  1 kHz (1 ms period)
```

**Motor parameters (T-motor AK80-9):**
- Poles: 14 (7 pairs)
- Kt: 0.08 Nm/A (estimated; measure on test bench)
- Ke: 0.08 V/(rad/s)
- Phase resistance: 0.3 Ω (estimated)
- Phase inductance: 0.2 mH (estimated)
- Max phase current: 10 A (peak)

### 3.4 Sensor Fusion

```
IMU (BMI270):   6-axis: accel (3) + gyro (3) @ 100 Hz
Encoder (AS5048): Motor rotor angle @ 1000 Hz
Load cell (HX711): Cable tension @ 200 Hz

Fusion algorithm: Madgwick AHRS (quaternion-based)

Outputs:
  - Hip flexion angle (degrees) — from IMU + encoder cable displacement
  - Angular velocity (deg/s) — from gyro
  - Cable tension (N) — from load cell
  - Gait phase — from hip angle + angular velocity (0% = heel strike, 60% = toe off)
```

### 3.5 Safety Monitor (Independent from Motor Control)

```c
// Runs on nRF5340 app core, independent from motor control STM32
typedef struct {
    float hip_angle_max;      // 90° flexion hard limit
    float hip_angle_min;      // -20° extension hard limit
    float cable_force_max;    // 800 N mechanical limit
    float motor_temp_max;     // 125°C junction
    float enclosure_temp_max; // 48°C surface
    float current_max;        // 10A phase current
    uint32_t watchdog_timeout_ms; // 100ms — STM32 must toggle GPIO
} safety_limits_t;

// E-Stop sequence:
// 1. Set PWM duty to 0 (coast)
// 2. Assert DRV8316 nSLEEP pin (Hi-Z motor outputs)
// 3. Notify phone with error code
// 4. Blink LED red at 2 Hz
```

---

## 4. BLE Protocol Specification

### 4.1 Services and Characteristics

| Service UUID | Characteristic UUID | Properties | Name | Payload |
|-------------|---------------------|------------|------|---------|
| `0xFEE0` | `EEG0-001` | Notify | EEG_DATA | 27 bytes (8ch×2B + status×8B + batt + seq) |
| `0xFEE0` | `EEG0-003` | Read, Notify | IMPEDANCE | 16 bytes (8ch×2B, kΩ×10) |
| `0xFEE0` | `EEG0-004` | Write | CMD_RX | 3 bytes (cmd + param) |
| `0xFEE1` | `CTL0-001` | Write | CMD_TORQUE | 5 bytes (torque×2B + cmd + seq×2B) |
| `0xFEE2` | `CTL0-002` | Notify | STATE_VECTOR | 15 bytes (angle×4 + vel×4 + force×4 + motor_pos×2 + status) |
| `0xFEE2` | `CTL0-003` | Write | EMERGENCY | 2 bytes (0x454D + 0x5354 = "EMST") |
| `0x180A` | `0x2A29` | Read | Manufacturer | "Nexum" |
| `0x180A` | `0x2A26` | Read | Firmware Rev | "1.0.0" |

### 4.2 Command Types

| Byte Value | Command | Parameters |
|------------|---------|------------|
| 0x01 | TORQUE_PROFILE | 2B setpoint (0.01 Nm), 1B duration (×10ms), 2B seq |
| 0x02 | EMERGENCY_STOP | None (or 0x454D5354) |
| 0x03 | CALIBRATION_HOME | None |
| 0x04 | SET_ASSIST_LEVEL | 1B level (0–100%) |
| 0x05 | SET_MODE | 1B: 0=passive, 1=active, 2=resistive |

### 4.3 Connection Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Connection interval min | 15 ms | Lower = lower latency but higher power |
| Connection interval max | 30 ms | Acceptable for 50 Hz EEG notify |
| Slave latency | 0 | No latency tolerated for real-time control |
| Supervision timeout | 500 ms | Detect disconnection quickly |
| PHY | 2M (BLE 5.0) | Higher throughput for EEG data |
| MTU | 247 bytes | Maximum BLE 5.0 MTU |
| DLE | 251 bytes | Maximum data length extension |

---

## 5. Firmware Build & Deploy

### 5.1 Build System

| Target | Build System | Compiler | Debug Probe |
|--------|-------------|----------|-------------|
| nRF52832 (EEG) | nRF Connect SDK / Zephyr | arm-none-eabi-gcc 12.x | J-Link / nRF52 DK |
| nRF5340 (Control) | nRF Connect SDK / Zephyr | arm-none-eabi-gcc 12.x | J-Link / nRF5340 DK |
| STM32H743 | STM32CubeIDE / CMake | arm-none-eabi-gcc 12.x | ST-Link V3 |

### 5.2 OTA Update Strategy

1. **EEG headband:** Nordic DFU (Device Firmware Update) via BLE, triggered from Nexum App
2. **Control box (nRF5340):** Nordic DFU via BLE
3. **Control box (STM32H743):** STM32 receives firmware image via UART from nRF5340, writes to external flash, verifies CRC32, swaps boot slot

### 5.3 Debug Interface

- **EEG headband:** SWD (4-pin: SWCLK, SWDIO, GND, VDD) on 1.27mm pitch header, accessible without disassembly
- **Control box:** SWD on nRF5340 + SWD on STM32H743, USB-C exposes serial console via CDC ACM

### 5.4 Logging

- **During development:** RTT (Real-Time Transfer) via J-Link for zero-cost debug logging
- **During clinical testing:** Log to external flash (W25Q128, 16 MB). Circular buffer, oldest events overwritten. Download via BLE on request, erase after transfer confirmed.

---

*End of FW Architecture v0.1. Update after first PCB spin and motor bench test.*
