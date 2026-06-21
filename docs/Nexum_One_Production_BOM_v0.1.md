# Nexum One — Production BOM & Supplier Guide

**v0.1** · 2026-06-21
**Note:** Prices are indicative (qty 1–10 for prototype, qty 100+ for production). RMB prices for China supply chain. All suppliers are publicly listed — no pre-existing commercial relationships unless noted.

---

## 1. EEG-Sense Headband BOM

### 1.1 Electronics

| # | Item | MPN | Supplier | Proto Price (¥) | Prod Price (¥ @100) | Source |
|---|------|-----|----------|-----------------|---------------------|--------|
| 1 | 8-ch EEG AFE | TI ADS1299IPAG | TI / Mouser / DigiKey | 180 | 120 | [mouser.com](https://www.mouser.com) |
| 2 | BLE SoC | nRF52832-QFAA | Nordic / LCSC / Taobao | 25 | 15 | [lcsc.com](https://www.lcsc.com) |
| 3 | 3.3V LDO | TPS7A4700RGWT | TI | 45 | 28 | mouser.com |
| 4 | 1.8V LDO (ADC DVDD) | TPS7A2005PDBVR | TI | 8 | 5 | lcsc.com |
| 5 | 32.768 kHz Crystal | ABS05-32.768KHZ-T | Abracon | 5 | 2.5 | lcsc.com |
| 6 | 32 MHz Crystal (BLE) | NX3225SA-32MHZ | NDK | 8 | 4 | lcsc.com |
| 7 | Chip Antenna (2.4 GHz) | 2450AT18A100E | Johanson | 12 | 6 | lcsc.com |
| 8 | Battery (Li-Po 3.7V 200mAh) | 402030 pouch | Generic / LCSC | 30 | 18 | lcsc.com |
| 9 | Battery Charger | BQ24075RGTT | TI | 12 | 7 | mouser.com |
| 10 | USB-C Connector | TYPE-C-31-M-12 | Korean Hroparts / LCSC | 3 | 1.5 | lcsc.com |
| 11 | Passives (R/C/L) | 0402/0603 | Yageo / Murata / Samsung | 50 | 25 | lcsc.com |
| **Subtotal** | | | | **~378** | **~232** | |

### 1.2 Dry Electrodes

| # | Item | Spec | Supplier | Proto Price | Notes |
|---|------|------|----------|-------------|-------|
| 1 | Dry comb electrode ×8 | Ag/AgCl coated, spring-loaded, 10mm pin length | OpenBCI-compatible / Custom PCB fab | ¥160 (buy) or ¥80 (DIY) | Start with OpenBCI ($20/ch), move to custom in V2 |
| 2 | Electrode flex PCB | 8-ch custom flex for headband curve | JLCPCB flex service | ¥300/10pcs | Requires PCB design |

### 1.3 Mechanical

| # | Item | Material | Supplier / Method | Proto Price |
|---|------|----------|-------------------|-------------|
| 1 | Headband shell | TPU 95A (flexible) or elastic fabric | 3D print TPU / garment factory | ¥50 |
| 2 | Electrode housing | ABS-like resin | 3D print SLA | ¥100/set |
| 3 | Strap (adjustable) | Elastic webbing + velcro | Local tailor / 1688.com | ¥20 |

**EEG-Sense Total (proto): ~¥700** | **EEG-Sense Total (prod @100): ~¥400**

---

## 2. Control Box BOM

### 2.1 Main PCB

| # | Item | MPN | Supplier | Proto (¥) | Prod @100 (¥) |
|---|------|-----|----------|-----------|---------------|
| 1 | MCU | STM32H743ZIT6 | ST / LCSC | 120 | 75 |
| 2 | BLE Module | nRF5340-QKAA | Nordic / LCSC | 50 | 32 |
| 3 | IMU | BMI270 | Bosch / LCSC | 18 | 10 |
| 4 | Motor Driver ×2 | DRV8316CRGZT | TI / Mouser | 60 | 38 |
| 5 | Magnetic Encoder ×2 | AS5048A-HTSP | ams / Mouser | 80 | 50 |
| 6 | Load Cell AFE | HX711 | Avia / LCSC | 8 | 4 |
| 7 | Flash (external) | W25Q128JVSIQ | Winbond / LCSC | 8 | 5 |
| 8 | Power Management IC | BQ25713RSNR (USB-C PD) | TI / Mouser | 35 | 22 |
| 9 | Battery Monitor | BQ76952 (or BQ4050) | TI / Mouser | 45 | 28 |
| 10 | 3.3V Buck Converter | TPS62130ARGTT | TI | 15 | 8 |
| 11 | 5V Boost | TPS61089RNRR | TI | 12 | 7 |
| 12 | Motor supply (12V rail) | TPS54824RNVR | TI | 20 | 12 |
| 13 | USB-C PD Controller | STUSB4500QTR | ST / Mouser | 15 | 9 |
| 14 | Passives + connectors | — | LCSC | 80 | 40 |
| **Subtotal** | | | | **~566** | **~340** |

### 2.2 Motor (×2)

| # | Item | Spec | Supplier | Proto (¥) | Prod @100 (¥) |
|---|------|------|----------|-----------|---------------|
| 1 | BLDC Motor (proto) | T-motor AK80-9 or AK60-6 | Taobao / T-motor official | 700 | N/A (temp) |
| 2 | BLDC Motor (production) | Maxon EC-i 40 60W (or custom) | Maxon / distributor | 2,200 | 1,500 |
| 3 | Gear reducer (if needed) | Planetary 1:4–1:6 | T-motor / Maxon | 300 | 200 |
| 4 | Spool mechanism | Custom machined aluminum | Local CNC shop / 3D print proto | 100 (print) | 40 (machined) |

### 2.3 Battery

| # | Item | Spec | Supplier | Proto (¥) | Prod @100 (¥) |
|---|------|------|----------|-----------|---------------|
| 1 | 21700 cells ×6 | Samsung 50E 5000mAh / Molicel P42A | 1688.com / battery distributor | 180 | 120 |
| 2 | BMS PCB | 6S, 25A, balance charging | Custom PCB + TI BQ76952 | 200 | 80 |
| 3 | Nickel strip + wiring | — | 1688.com | 20 | 10 |
| 4 | Heat shrink wrap | PVC 150mm | 1688.com | 5 | 2 |

### 2.4 Enclosure

| # | Item | Material | Supplier / Method | Proto (¥) | Prod @100 (¥) |
|---|------|----------|-------------------|-----------|---------------|
| 1 | Top shell | 6061 aluminum CNC | Local CNC shop | 200 | 60 |
| 2 | Bottom shell | 6061 aluminum CNC | Local CNC shop | 150 | 50 |
| 3 | Thermal pad | 3W/mK silicone pad 2mm | 1688.com | 10 | 3 |
| 4 | Belt clip | Injection molded ABS+PC | 3D print → injection mold | 20 (print) | 5 (molded) |
| 5 | Gasket (IP22) | Silicone O-ring | 1688.com | 5 | 1 |

**Control Box Total (proto): ~¥2,400** | **Control Box Total (prod @100): ~¥1,700** (with T-motor)
**Control Box Total (prod @100): ~¥3,500** (with Maxon motor)

---

## 3. NeuroSuit BOM

| # | Item | Spec | Supplier / Method | Proto (¥) | Prod @100 (¥) |
|---|------|------|-------------------|-----------|---------------|
| 1 | Carbon fiber hip anchor ×2 | 2mm CF plate, CNC cut | Local CF fabrication shop (Nanjing/Suzhou) | 800 | 350 |
| 2 | Bowden cable ×2 | PTFE-lined bicycle brake cable, 1.5m | Shimano / Jagwire / 1688.com | 30 | 15 |
| 3 | Cable sheath ×2 | PTFE tube 4mm OD | 1688.com | 20 | 8 |
| 4 | Cable termination kit ×2 | Aluminum crimp ends | 1688.com | 10 | 3 |
| 5 | Compression garment (custom) | Nylon-spandex blend, medical grade | Garment factory (minimum order 100 pcs) | 500 (sample) | 120 |
| 6 | sEMG fabric electrodes ×8 | Silver-plated nylon knit | Smart textile supplier (e.g., Myant, AdvanPro) | 400 | 200 |
| 7 | Snap connectors (for sEMG) | Stainless steel micro-snaps | 1688.com | 20 | 8 |
| 8 | Waist belt | Nylon webbing + quick-release buckle | 1688.com | 30 | 12 |
| 9 | Cable routing guides | 3D printed TPU clips | 3D print → injection mold | 20 | 5 |
| 10 | Load cell (inline tension) ×2 | S-type 100kg with amplifier | Taobao / AliExpress | 200 | 80 |
| **NeuroSuit Total (proto): ~¥2,030** | **NeuroSuit Total (prod @100): ~¥800** |

---

## 4. Total System BOM Summary

| Module | Proto BOM (¥) | Prod BOM @100 (¥) | Prod BOM @1000 (¥ est.) |
|--------|---------------|--------------------|----------------------|
| EEG-Sense Headband | 700 | 400 | 280 |
| Control Box (T-motor) | 2,400 | 1,700 | 1,200 |
| NeuroSuit | 2,030 | 800 | 550 |
| Packaging + Manual + Accessories | 150 | 80 | 50 |
| **Total (Home version)** | **~5,280** | **~2,980** | **~2,080** |
| Clinical version add-ons | +500 | +300 | +200 |
| **Total (Clinical version)** | **~5,780** | **~3,280** | **~2,280** |

**Note:** Clinical version adds: therapist tablet pre-loaded, spare electrode set, docking station, hard case.

---

## 5. Key Suppliers — China Supply Chain

| Category | Supplier | Location | Notes |
|----------|----------|----------|-------|
| PCB Fab + Assembly | JLCPCB / PCBWay | Shenzhen | Prototype and small batch; 4-layer minimum for EEG |
| Component distribution | LCSC (立创商城) | Shenzhen | Most electronic components |
| Motor (proto) | T-motor (老虎动力) | Shenzhen | AK series BLDC, available on Taobao |
| Motor (production) | Maxon / Faulhaber distributor | Shanghai / online | Medical-grade certification |
| Carbon fiber fabrication | 碳纤维加工厂 (local) | Nanjing / Suzhou / Dongguan | Custom CF plate cutting |
| Garment factory | 服装厂 (medical textile) | Shaoxing / Guangzhou | Minimum order typically 100–500 pcs |
| sEMG textile electrodes | AdvanPro / Myant / 国内纺织电极厂 | Shenzhen / HK | Sample quantities available |
| 3D printing (proto) | Bambu Lab P1S (in-house) | — | TPU, PETG, PLA materials |
| CNC machining | 嘉立创CNC / 本地CNC厂 | Shenzhen / Nanjing | Aluminum enclosure, CF cutting |
| Li-ion battery pack | 电池PACK厂 (custom) | Shenzhen / Dongguan | 6S 21700 with BMS |
| Injection mold (production) | 模具厂 | Dongguan / Kunshan | For enclosure, clips, electrode housing |

---

## 6. Prototype Tooling Budget (¥)

| Item | Cost | Notes |
|------|------|-------|
| Bambu Lab P1S 3D printer | 4,000 | Fast prototyping, TPU/PETG/PLA |
| Rigol DS1054Z oscilloscope | 2,500 | 4-ch, 50 MHz |
| Korad KA3005D power supply | 1,500 | 30V, 5A |
| Soldering station (Hakko or similar) | 800 | FX-888D |
| Multimeter (Fluke 17B+) | 600 | True RMS |
| JDS6600 signal generator | 1,200 | EEG simulator input |
| Hand tools + consumables | 2,000 | Cutters, strippers, solder, flux |
| ESD mat + wrist strap | 200 | Basic ESD protection |
| **Total tooling** | **~12,800** | One-time |

---

## 7. Cost Reduction Roadmap

| Phase | Action | BOM Target |
|-------|--------|------------|
| Proto (now) | Off-the-shelf components, 3D printed parts | ¥5,280 |
| EVT (M3–M6) | Custom PCBs, simplified mechanical, bulk components | ¥3,500 |
| DVT (M6–M12) | Custom motor, injection molded parts, optimized PCB | ¥2,500 |
| PVT (M12+) | Full production tooling, second-source components | ¥2,080 |
| Scale (1000+) | Automated assembly, bargaining power, die-shrink ICs | <¥1,800 |

---

*All prices exclude VAT and shipping. Update quarterly as supply chain develops.*
