# Nexum One — NMPA Regulatory Strategy

**Version 0.1** · 2026-06-21
**Author:** Zirui Zhao · Architecture
**Classification:** Internal — Regulatory / Confidential
**References:** [PRD v1.0](Nexum_One_PRD_v1.0.md), [Engineering Architecture v0.1](Nexum_One_Engineering_Architecture_v0.1.md), [Clinical Protocol v0.1](Nexum_One_Clinical_Protocol_v0.1.md)

---

## Table of Contents

1. Classification Rationale
2. Innovative Device Fast-Track Pathway Requirements
3. Predicate Device Analysis
4. Technical Standard Checklist
5. Required Testing
6. Clinical Evaluation Pathway
7. Estimated Timeline
8. Key Risks
9. Budget Estimate for Regulatory Work
10. Recommended Regulatory Consultant Qualifications

---

## 1. Classification Rationale

### 1.1 Classification Determination

Nexum One is a **combination product** comprising three elements with different NMPA classification characteristics:

| Component | Nature | Standalone Class | Combined Class Rationale |
|-----------|--------|-----------------|-------------------------|
| **EEG headband** | Non-invasive neurophysiological recording device (脑电采集设备) | Class II (non-invasive, not implantable, no energy delivery to patient) | The combined product's risk is bounded by the highest-risk component. Since no component delivers significant energy to the patient and the system is non-invasive, the overall risk profile is consistent with Class II. |
| **Hip exosuit (Bowden cable-driven)** | Rehabilitation training device / walking aid (康复训练设备 / 步行辅助) | Class II (powered, non-invasive, external body-worn, no bone fixation) | |
| **AI inference software** | Decision-support / intention-detection software (决策支持软件 / 意图识别) | Class II (provides clinically significant information for treatment decision, but in a "assist-as-needed" role, not autonomous diagnosis) | |

### 1.2 Class II Justification (Why Not Class III)

Nexum One should be classified as **Class II (第二类医疗器械)** based on the following rationale:

| Criterion | Nexum One Status | Class II Threshold | Risk of Class III |
|-----------|-----------------|-------------------|------------------|
| **Invasiveness** | Entirely non-invasive — electrodes contact intact skin only; no percutaneous or implanted components | Non-invasive → Class I–II | If classified as active implantable → Class III (not applicable) |
| **Energy delivery to patient** | Mechanical torque at hip (<15 Nm); electrical stimulation: NONE | Passive/non-harmful → Class I–II | If E-stim combined → Class III |
| **Duration of use** | Intermittent (rehab sessions, <4h/day), not continuous 24/7 | Short-term (<30 days) → Class I–II; Long-term → Class II–III | If classified as life-supporting → Class III |
| **Effect on patient** | Assist-as-needed; patient initiates; device augments, does not replace physiological function | Therapy aid → Class II | If autonomous diagnostic/therapeutic decision → Class III |
| **Biological risk** | Skin contact only; no breach of skin barrier | External surface → Class I–II | If implantable → Class III |

**Key argument for Class II:** Nexum One does **not**:
- Deliver electrical stimulation to the brain or nerves (not a neural stimulator)
- Penetrate the skin or body cavity (not invasive)
- Make autonomous clinical decisions (the AI provides **assistance recommendations**, not diagnoses)
- Sustain vital physiological functions (not life-supporting)

### 1.3 Classification Reference (existing NMPA examples)

| Product | NMPA Class | Nexum One Parallel |
|---------|-----------|-------------------|
| 程天科技 UGO (powered lower-limb exoskeleton for rehab) | Class II (valid) | Same mechanical category; Nexum One adds EEG but EEG alone is Class II |
| 大艾外骨骼 (DAAI exoskeleton, powered walking aid) | Class II | Same |
| 博睿康 Neuro-EEG (脑电图机) | Class II | EEG component equivalent |
| NEOFECT Smart Glove (rehabilitation robot) | Class II | Similar combined "sensor + actuator" paradigm |
| 强脑科技 (BrainCo) 智能义肢 | Class II | EEG-controlled prosthesis — precedent for EEG-based actuation as Class II |
| YBrain Cerebro (BCI rehabilitation system) | Class II | Direct precedent: EEG + exoskeleton/powered orthosis combination |

**Recommendation:** File a **分类界定申请** (Classification Determination Application) to NMPA before proceeding with full regulatory submission. This is a pre-submission inquiry that:
- Takes 20–30 working days for a formal response
- Provides binding classification determination
- Eliminates downstream risk of re-classification
- Estimated cost: ¥10,000–20,000 (via NMPA administrative service)

**Fallback position:** If NMPA determines Class III (e.g., due to "BCI + motor actuation" being considered a novel combination with no precedent), the submission pathway changes significantly:
- Must conduct a full clinical trial (not just clinical evaluation via CER)
- Requires GCP-compliant multi-site trial (at least 2 sites)
- Timeline extends by 12–18 months
- Regulatory cost increases by ¥2,000,000–3,000,000

---

## 2. Innovative Device Fast-Track Pathway Requirements

### 2.1 创新医疗器械特别审查程序 (Innovative Medical Device Special Review Procedure)

This is a fast-track program established by NMPA Order No. 83 (2018 revision) for devices that meet ALL of the following criteria:

| Criterion # | Requirement | Nexum One Status | Evidence Needed |
|-------------|-------------|-------------------|-----------------|
| **1. Patent ownership** | Applicant holds core technology invention patent (发明专利); patent is granted or at least in substantive examination; the patent covers the core structure/mechanism of the device | Core patents: nerve-muscle intention decoding method, EEG + force feedback closed-loop control, Bowden-cable suit architecture | Pat. 1: "基于脑电和肌电融合的运动意图识别方法" (filing date); Pat. 2: "鲍登线驱动髋关节助力外骨骼结构" (filing date); Patent assignment from inventor to Nexum company |
| **2. Domestic debut** | The product has not been marketed in China previously; there is no identical or equivalent product approved in China | No EEG + exosuit combination product has been NMPA-approved. Individual components (EEG, exoskeleton) exist separately, but the combined "neural reconnection AI system" is novel in the Chinese market | Market research report confirming no identical product; PubMed/CNKI literature search showing no approved product of this combination |
| **3. Significant clinical advantage** | The product has clear clinical advantages over existing treatments (better efficacy, safety, convenience, or cost) | Intended advantages: (a) EEG-based intention enables faster, more natural gait initiation vs postural-shift-based exoskeletons; (b) non-invasive BCI avoids surgical risk of implantable systems; (c) 80%+ cost reduction vs imported exoskeletons | Clinical literature comparing intention detection latency; cost-benefit analysis; expert review letter from 2–3 tertiary hospital rehabilitation directors |
| **4. Substantial R&D investment** | The applicant has performed substantial R&D in China, including design, testing, and preliminary validation | Prototype BOM ≥¥200k; team of 8 engineers × 6 months; pre-clinical study (n=30) | R&D documentation; prototype photos/videos; pre-clinical data; R&D expense summary audited by accountant |

### 2.2 Innovative Application Procedure

```
Application Submission → Formal Review (CMDE, 5 working days) → Expert Review (60 working days) → Decision (10 working days)
       ↓                         ↓                            ↓                          ↓
    Materials to               Check                      Panel of 3–5                Final
    CMDE (Center for           completeness               experts from                 notification
    Medical Device             and fee                    clinical + technical
    Evaluation)                                           fields
```

**Total review time for innovative designation:** Approximately **75 working days** (~15 weeks).

### 2.3 Benefits of Innovative Device Status

1. **Priority review:** Registration application is reviewed within 60 working days (vs standard 120+ working days)
2. **Dedicated communication channel:** Direct dialogue with CMDE reviewers during the evaluation process
3. **Streamlined clinical evaluation:** May accept clinical evaluation report (CER) instead of full clinical trial, if sufficient evidence of safety and efficacy exists
4. **Conditional approval pathway:** Can obtain conditional registration with commitment to post-market clinical study (上市后临床研究)
5. **No extra cost:** The innovative device review fee is the same as standard registration (¥72,300 for Class II in 2024); additional fee only for expert panel if required

### 2.4 Timeline and Probability

| Item | Optimistic | Realistic | Probability of Success |
|------|-----------|-----------|----------------------|
| Classification determination (分类界定) | 1 month | 2 months | 90% (Class II) |
| Innovative device application (创新医疗器械特别审查) | 4 months | 6 months | 60% (given BCI novelty — depends on patent strength and expert panel impression) |
| Alternative: Standard Class II path (no innovation designation) | N/A | 8–10 months longer for review | 100% fallback |

**Recommendation:** File classification determination AND innovative device application simultaneously — the applications are independent and both benefit from early submission.

---

## 3. Predicate Device Analysis

### 3.1 Direct Competitors (NMPA-Registered Products)

| Product | Manufacturer | NMPA Registration No. | Class | Intended Use | Key Technology | Analysis for Nexum One |
|---------|-------------|----------------------|-------|-------------|----------------|------------------------|
| **UGO康复训练外骨骼** | 程天科技 (ChengTian Tech) | 浙械注准2021219xxxx (verify exact number) | II | Lower limb rehabilitation training for stroke/SCI patients | Powered hip-knee exoskeleton; IMU-based gait phase detection; pre-programmed assistance profiles | **Closest predicate** for mechanical structure. Can reference safety data (falls, skin, joint ROM limits). No EEG — intentional difference to claim novelty. |
| **大艾外骨骼康复机器人** | 大艾科技 (DAAI Tech) | 京械注准2021219xxxx (verify) | II | Walking aid for SCI/hemiplegia patients | Motor-driven hip/knee; multi-mode training; body-weight support interface | **Predicate for torque levels and joint safety limits.** Clinical data on 10MWT and 6MWT outcomes can support Nexum One's performance claims. |
| **杭州程天Waker外骨骼** | 程天科技 | 浙械注准2022219xxxx | II | Gait training | Similar to UGO, lighter version | Reference for home-use safety documentation. |
| **NEOFECT智能康复手套** | NEOFECT (Korea/NMPA filing) | 国械注进2022xxxxxx | II | Hand rehabilitation for stroke | sEMG + IMU intent detection; game-based training | **Predicate for sensor-based intent detection software** (SaMD component). Reference for AI-based assisted training software certification pathway. |
| **BrainCo智能仿生义肢** | 强脑科技 (BrainCo) | 国械注准2022xxxxxx | II | Prosthesis control for amputees | EEG + sEMG pattern recognition for motor intent | **Closest predicate for EEG-based motor control.** BrainCo's Class II designation for EEG-controlled prosthesis is the strongest regulatory precedent for Nexum One's EEG-to-actuation paradigm. |

### 3.2 Predicate Device Mapping for Substantial Equivalence

For the clinical evaluation report (CER), Nexum One should claim substantial equivalence via a **modular comparison**:

| Subsystem | Predicate | Basis of Equivalence |
|-----------|-----------|---------------------|
| **Mechanical safety** (joint limits, torque range, cable safety, suit attachment) | UGO / DAAI exoskeleton | Same mechanical principles; comparable torque and ROM limits; same patient population; same clinical environment |
| **EEG acquisition** (electrode type, amplification, filtering) | BrainCo prosthetic / Conventional EEG (博睿康, 理邦) | Industry-standard ADS1299-based EEG; BrainCo's precedent confirms Class II for motor-control EEG |
| **Intention detection software** | BrainCo pattern recognition / NEOFECT intent detection | SaMD with similar risk profile (assist-as-needed, not autonomous); comparable input data (EEG + sEMG) |
| **Combined system** | Novel — no direct predicate | Argument for innovative device classification; CER uses component-level equivalence for safety and performance modules |

### 3.3 Key Differences from Predicates (To Be Addressed in CER)

1. **EEG + exosuit combination** — No predicate product has this exact combination. Address this through: (a) demonstrating each component's safety individually via predicate equivalence, (b) showing that the combination does not create new safety risks not already covered by component-level risk analysis.

2. **Closed-loop AI adaptation** — None of the predicate devices have real-time, subject-specific model adaptation. Address this by: (a) positioning the AI as "assistance level adjustment" (which is a feature of many Class II devices), not "autonomous diagnostic/control" (which would be Class III); (b) limiting the AI to providing percentage-assistance modification (scaling factor), not generating new torque patterns.

---

## 4. Technical Standard Checklist

### 4.1 Mandatory Standards for Class II Medical Devices

| Standard | Title | Applicable To | Nexum One Status |
|----------|-------|--------------|------------------|
| **GB 9706.1-2020** | Medical electrical equipment — Part 1: General requirements for basic safety and essential performance (equivalent to IEC 60601-1:2012, 3rd edition) | Full system (control box, battery, motor drive) | **Must comply.** Key clauses: leakage current (8.7), dielectric strength (8.8), mechanical hazards (9), temperature limits (11), marking/labels (7). |
| **YY 9706.102-2021** | Medical electrical equipment — Electromagnetic compatibility (equivalent to IEC 60601-1-2:2014) | Full system | **Must comply.** Emissions (Group 1, Class B) → CISPR 11; immunity → Table 4/9 requirements. |
| **IEC 62304 / YY/T 0664-2020** | Medical device software — Software life cycle processes | Nexum App, AI inference module, firmware | **Mandatory for SaMD.** Software safety classification for Nexum One: likely **Class B** (can lead to injury if defective — incorrect torque level could cause fall). Determine software safety class early. |
| **ISO 14971 / YY/T 0316-2016** (updated to YY/T 14971-2022) | Medical devices — Application of risk management | Full system | **Mandatory.** Risk management file must cover all components: electrical, mechanical, software, biological, usability. |
| **IEC 62366 / YY/T 1474-2016** | Medical devices — Application of usability engineering | Full system (especially don/doff, emergency stop, alarm management) | **Mandatory.** Usability testing required: 15 representative users (mix of patients and therapists) for summative evaluation. |
| **ISO 13485 / YY/T 0287-2017** | Quality management systems | Manufacturing facility / QMS | **Mandatory.** Must have ISO 13485 QMS in place before submission (or at least under implementation with 3 months of internal audit records). |
| **GB/T 25000.51-2016** | Software product quality | Nexum App, AI inference | **Required for software quality measurement.** Functional suitability, reliability, usability, efficiency, maintainability, portability. |
| **YY 9706.108-2021** | Alarm systems (equivalent to IEC 60601-1-8) | Device alarms (battery low, motor fault, EEG disconnect) | **Must comply** if alarm functionality is included. |

### 4.2 Recommended Standards (Best Practice)

| Standard | Title | Rationale |
|----------|-------|-----------|
| **YY/T 0933-2014** | Rehabilitation robots — General safety requirements | Directly applicable to exoskeleton structure; covers joint limits, emergency stop, speed limiting |
| **YY/T 1635-2018** | Exoskeleton gait rehabilitation robot — Technical requirements | More specific than YY/T 0933; for CE marking reference |
| **GB/T 36001-2018** | EEG measurement equipment — General technical requirements | For EEG headband component |
| **IEC 62304 Class B documentation** | Software lifecycle documentation | Required for SaMD — ensures traceability from requirements to tests |
| **ISO 10993-10 / GB/T 16886.10** | Biological evaluation — Sensitization | For skin-contact materials in suit and headband |
| **ISO 10993-5 / GB/T 16886.5** | Biological evaluation — Cytotoxicity | Same as above |
| **ISO 10993-1 / GB/T 16886.1** | Biological evaluation framework | Overall biocompatibility strategy for skin-contact materials |

---

## 5. Required Testing

### 5.1 Type Testing (型式检验)

Type testing must be performed at an NMPA-accredited testing laboratory (国家药品监督管理局认可的检验机构). The test plan covers the following areas:

| Test Category | Standard | Key Tests | Estimated Cost (¥) | Duration |
|--------------|----------|-----------|-------------------|----------|
| **Electrical Safety** | GB 9706.1-2020 | Leakage current (normal + single fault), dielectric strength, protective earth, input power, temperature rise, enclosure protection (IP22) | 80,000–120,000 | 4–6 weeks |
| **EMC** | YY 9706.102-2021 | Radiated emissions (30 MHz–1 GHz), conducted emissions (150 kHz–30 MHz), ESD (±8 kV contact, ±15 kV air), radiated RF immunity, conducted RF immunity, power frequency magnetic field, voltage dips/interruptions | 60,000–100,000 | 4–6 weeks |
| **Mechanical Safety** | GB 9706.1 + YY/T 0933 | Joint angle limiting verification, emergency stop function, cable force limit, structural integrity under static load | 30,000–50,000 | 2–4 weeks |
| **Software Evaluation** | GB/T 25000.51 | Functional testing (all user stories), performance testing (latency, throughput), reliability testing (stress test), usability inspection | 50,000–80,000 | 6–8 weeks |
| **Biocompatibility** | GB/T 16886 series | Skin irritation (patch test, GB/T 16886.10), cytotoxicity (GB/T 16886.5), sensitization (GB/T 16886.10) — testing on representative materials from suit + headband | 40,000–60,000 | 4–6 weeks (accelerated: 2 weeks for cytotoxicity) |
| **Battery Safety** | GB 9706.1 (battery section) + GB 31241 (portable Li-ion) | Overcharge test, overdischarge test, short circuit test, external short circuit, crush test (limited scope for medical device) | 20,000–30,000 | 2–3 weeks |
| **Environmental** | GB 9706.1 (environmental) | Operating temperature (10–40°C), humidity (20–80%), vibration, transport simulation | 15,000–25,000 | 2–3 weeks |
| **Total (Type Testing)** | | | **¥295,000–465,000** | **12–16 weeks (parallel execution)** |

### 5.2 Recommended Testing Laboratories

| Laboratory | Location | Accreditation | Advantages | Lead Time |
|------------|----------|--------------|------------|-----------|
| **国家药品监督管理局医疗器械技术审评中心 (CMDE)** — not a testing lab but coordinating body | Beijing | NMPA | Final reviewer — use their listed labs |
| **中国食品药品检定研究院 (中检院, CFDI)** | Beijing | NMPA, CNAS | Most authoritative; accepted by all provinces | 6–8 weeks scheduling |
| **上海医疗器械检验研究院** | Shanghai | NMPA, CNAS | Faster turnaround; good for software testing | 4–6 weeks |
| **北京医疗器械检验研究院** | Beijing | NMPA, CNAS | Similar to Shanghai; preferred for northern sites | 4–6 weeks |
| **深圳医疗器械检测中心** | Shenzhen | NMPA, CNAS | Fastest in southern China; good for electronics | 3–5 weeks |

**Recommendation:** Start with Shanghai or Beijing institute for EMC + electrical safety (longest lead time items). Negotiate parallel testing for mechanical + biocompatibility + software at different labs simultaneously.

### 5.3 Type Testing Schedule

```
Month 1      Month 2      Month 3      Month 4      Month 5      Month 6
─────────────────────────────────────────────────────────────────────────────
Electrical Safety ──────────────────────────►
EMC ───────────────────────────────────►
Mechanical ──────────►
Software Eval ─────────────────────────────────────────►
Biocompatibility ──────────►
Battery ──────►
Environmental ──►
          Report compilation ────────────────────►
```

**Critical path:** EMC and Software evaluation have the longest durations and highest risk of re-test. Start these first.

---

## 6. Clinical Evaluation Pathway

### 6.1 Pathway Selection

For NMPA Class II devices, there are three possible clinical evaluation pathways:

| Pathway | Description | Suitable For Nexum One? | Risk Level |
|---------|-------------|------------------------|------------|
| **Pathway A — Waiver (免于进行临床试验)** | Device is listed on NMPA's "豁免临床试验目录" (exemption list). Requires only clinical evaluation report (CER) with literature + predicate comparison. | **No.** Nexum One's EEG + exosuit combination is not on any current exemption list. Individual components (EEG, exoskeleton) may be listed, but the combined system requires clinical data. | Low if on list |
| **Pathway B — Clinical Evaluation Report (CER)** | CER based on: (a) predicate device clinical data, (b) published literature, (c) own pre-clinical study data. Does not require de novo clinical trial. | **Yes — primary target.** If CER + pre-clinical (n=30) data + predicate equivalence is accepted. Supported by innovative device fast-track review if granted. | Medium |
| **Pathway C — Clinical Trial (临床试验)** | Full GCP-compliant clinical trial, multi-site, randomized or well-controlled design. | **Fallback.** Required only if NMPA determines CER insufficient. More likely for Class III devices, or if BCI component is considered novel enough to require de novo clinical evidence. | High |

**Recommended strategy:** Target **Pathway B** (CER + pre-clinical study), with clear contingency planning for Pathway C.

### 6.2 CER Structure (Pathway B)

The Clinical Evaluation Report must follow NMPA's 《医疗器械临床评价技术指导原则》(2021 revision):

| Section | Content | Source |
|---------|---------|--------|
| **1. Device description** | Nexum One system composition, intended use, indications, contraindications, technical specifications | PRD v1.0, Engineering Architecture v0.1 |
| **2. Clinical claims** | Claims about safety, performance, and clinical benefit | PRD v1.0 (user needs table) |
| **3. Predicate device analysis** | Modular equivalence mapping to UGO, DAAI, BrainCo, NEOFECT (see Section 3 of this document) | Literature + NMPA databases |
| **4. Literature review** | Systematic review of published clinical data for: (a) EEG-based intention detection, (b) powered exoskeleton gait training, (c) combined BCI-robot systems | PubMed, CNKI, Cochrane 10-year search |
| **5. Pre-clinical study data** | Nexum One pre-clinical study results (n=30, safety + performance) | Clinical Protocol v0.1 + study report |
| **6. Risk-benefit analysis** | Summarize risks identified in ISO 14971 HFMEA, compare to clinical benefits from literature + pre-clinical data | Risk management file |
| **7. Conclusions** | The clinical evidence demonstrates that the device is safe and effective for its intended use | Summary |
| **8. Post-market surveillance plan** | Plans for continued monitoring after market entry | Regulatory team |

### 6.3 Literature Review Strategy (CER Section 4)

| Topic | Search Strategy | Expected Yield | Key Papers |
|-------|-----------------|----------------|------------|
| EEG-based gait intention detection | "EEG movement intention" AND "gait" AND "rehabilitation" | 30–50 papers | Jiang et al. (2015) on BP detection during walking; Shurlea et al. (2015) on foot movement intention from EEG |
| Exoskeleton gait training efficacy | "powered exoskeleton" AND "gait training" AND "stroke/SCI" | 100+ papers | Esquenazi et al. (2012) — ReWalk pivotal; Louie et al. (2015) — exoskeleton meta-analysis; Fisahn et al. (2016) |
| BCI + exoskeleton combined | "brain-computer interface" AND "exoskeleton" AND "rehabilitation" | 15–30 papers | Donati et al. (2016) — BCI + exoskeleton for SCI; Bundy et al. (2017) — EEG exoskeleton feasibility |
| Nexum One specific | Search in CNKI for Chinese exoskeleton clinical data (程天科技, 大艾科技 clinical publications) | 5–15 Chinese papers | ChengTian UGO clinical study publications; DAAI clinical outcome reports |

### 6.4 NMPA Consultation Mechanism (咨询)

Before finalizing the CER, Nexum should request a **pre-submission meeting** (医疗器械注册申报前咨询) with CMDE. This is a formal mechanism where:

- Nexum presents the device description, predicate comparison, and clinical evaluation plan
- CMDE reviewers provide written feedback on whether the proposed CER approach is acceptable
- Feedback is non-binding but highly indicative of eventual approval

**Timeline:** Pre-submission meetings are offered quarterly; application deadline 1 month before meeting.

---

## 7. Estimated Timeline

### 7.1 Overall Regulatory Timeline (Optimistic: ~18 months)

```
Phase 1: Pre-Engagement (Month 1–4)
├── Classification determination (分类界定) .......................... 2 months
├── Innovative device application preparation ..................... 2 months
├── ISO 13485 QMS implementation ................................. 4 months (ongoing)
├── Risk management file (ISO 14971) ............................. 3 months
└── Regulatory consultant onboarding .............................. 1 month

Phase 2: Testing (Month 3–8)
├── Type testing — electrical safety (GB 9706.1) .................. 2 months
├── Type testing — EMC (YY 9706.102) ............................. 2 months
├── Type testing — mechanical safety ............................. 2 months
├── Biocompatibility (GB/T 16886) ................................ 2 months
└── Software evaluation (GB/T 25000.51) .......................... 3 months

Phase 3: Clinical Evaluation (Month 4–12)
├── Pre-clinical study (IRB + recruitment + data collection) ....... 6 months
├── CER writing + literature review .............................. 3 months
└── CER finalization (incorporate clinical study results) .......... 1 month

Phase 4: Submission (Month 12–18)
├── Submission dossier compilation ............................... 2 months
├── Formal review (形式审查) ...................................... 5 working days
├── Technical review (技术审评) — standard: 120 working days ....... 6 months
│   └── (With innovation fast-track: 60 working days) ............ 3 months
├── Supplementary materials (发补) ................................ 2 months
├── Expert review (专家评审, if needed) ........................... 1 month
└── Registration certificate issuance ............................ 1 month

TOTAL: 18 months (20–24 months with supplements)
```

### 7.2 Gantt Chart Summary

```
Month:  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
        │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │
Class det│██│██│  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │
Innovativ│  │  │██│██│██│██│  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │
QMS set  │  │██│██│██│██│  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │
Risk mgmt│  │██│██│██│  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │
Type test│  │  │  │██│██│██│██│██│  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │
Clin stud│  │  │  │  │██│██│██│██│██│██│██│██│  │  │  │  │  │  │  │  │  │  │  │
CER write│  │  │  │  │  │  │  │  │  │██│██│██│  │  │  │  │  │  │  │  │  │  │  │
Dossier  │  │  │  │  │  │  │  │  │  │  │  │██│██│  │  │  │  │  │  │  │  │  │  │
Submission│  │  │  │  │  │  │  │  │  │  │  │  │  │██│  │  │  │  │  │  │  │  │  │
Review   │  │  │  │  │  │  │  │  │  │  │  │  │  │  │██│██│██│██│██│██│  │  │  │
Supplement│  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │██│██│  │  │  │  │
Approval  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │██│  │  │
```

---

## 8. Key Risks

### 8.1 Risk Register for Regulatory Pathway

| # | Risk | Probability | Impact | Mitigation | Contingency |
|---|------|------------|--------|------------|-------------|
| **R1** | NMPA classifies Nexum One as Class III (novel BCI device) | Medium | High (timeline +12–18 months; cost +¥2–3M) | Pre-submission classification determination (分类界定); strong Class II rationale document; legal argument referencing BrainCo precedent | Accept Class III path; shift to full clinical trial; raise additional funding for regulatory work |
| **R2** | Innovative device application rejected | Medium–High | Medium (lose fast-track, timeline +4–6 months) | Ensure strong patent portfolio; obtain expert letters from 2–3 academic thought leaders; document clinical advantage in writing | Proceed with standard Class II path — timeline impact manageable |
| **R3** | Type testing failure — EMC or electrical safety | Medium | Medium (re-test takes 4–8 weeks) | Pre-compliance testing at non-certified lab before formal submission; design margin (e.g., 6 dB margin on EMC); retain EMC consultant | Budget for 2 rounds of formal testing; ensure design allows quick fixes (shield can, ferrite bead, filter redesign) |
| **R4** | SaMD (AI software) reclassified as Class III | Low–Medium | High (software pathway changes entirely) | Limit AI role to "assistance level adjustment" — does not make autonomous clinical decisions; ensure IEC 62304 Class B documentation is rigorous; avoid claims of "diagnosis" in labeling | Re-label software as "patient-specific parameter tuning tool" rather than "clinical decision support" |
| **R5** | Pre-clinical study fails to meet safety endpoint | Low | Critical (device redesign or study restart) | Robust risk management before study; thorough bench testing of all failure modes; conservative inclusion criteria; DSMB review at n=10 interim | Pause submission; redesign the specific safety-critical sub-system; conduct additional bench tests |
| **R6** | Clinical evaluation (CER) rejected — requires full clinical trial | Medium | High (timeline +12 months; cost +¥1.5–2M) | CER must be comprehensive — cover all predicate data + literature + own study data; pre-submission meeting to validate CER approach with CMDE before final submission | Switch to Pathway C; leverage pre-clinical site relationships to accelerate multi-site trial setup |
| **R7** | ISO 13485 certification delayed | Medium | Medium (cannot submit without QMS) | Start QMS implementation early (Month 1); hire experienced QMS consultant; use ISO 13485:2016 template from medical device industry partner | Submit with QMS under implementation + certification audit scheduled within 3 months (NMPA may accept) |
| **R8** | Biocompatibility test failure (skin irritation) | Low | Medium | Pre-screen all skin-contact materials with ISO 10993 test lab before finalizing design; obtain material certificates from fabric supplier; keep 3 candidate materials for each contact surface | Switch to alternative material with existing biocompatibility certification; accelerate re-test (2 weeks) |

### 8.2 Critical Risk: BCI Novelty and Clinical Trial Requirement

This is the single highest regulatory risk for Nexum One. The issue:

**Problem:** NMPA has limited experience reviewing BCI-based medical devices. The regulatory framework for "neural reconnection systems" does not exist as a defined category. Reviewers may lack familiarity with EEG intention-detection technologies and may default to requiring a full clinical trial.

**Evidence for optimistic outcome:**
- BrainCo's 智能仿生义肢 (EEG-controlled prosthetic hand) was approved as Class II without a full clinical trial — establishing a precedent for EEG-based motor control
- Multiple EEG-only devices (脑电图机, 博睿康, 理邦) are Class II with only CER
- The exosuit mechanical component has established predicates (UGO, DAAI)

**Risk reduction strategies:**
1. **Pre-submission meeting** — the single most effective risk mitigation. Present the proposed CER pathway to CMDE and secure feedback before investing in a full submission.
2. **Engage a BCI-experienced NMPA consultant** who has worked on BrainCo's submission or similar products.
3. **Academic endorsement** — obtain a letter from a Chinese BCI expert (e.g., Prof. 高上凯 at Tsinghua, or Prof. 明东 at Tianjin University) explaining that the technology is well-established in literature and not experimental.
4. **Limit clinical claims** — position the device as "gait training aid with adaptive assistance," not "intention-driven neural reconnection system," to reduce perceived novelty risk.

---

## 9. Budget Estimate for Regulatory Work

### 9.1 Direct Regulatory Costs

| Item | Estimated Cost (¥) | Notes |
|------|-------------------|-------|
| **Classification determination** | 10,000–20,000 | Application fee + legal service if filed via agent |
| **Innovative device application** | 30,000–50,000 | Application fee + patent analysis + expert letter procurement |
| **Type testing (all categories)** | 300,000–500,000 | 4–6 accredited lab tests; includes re-test contingency |
| **Biocompatibility testing** | 50,000–80,000 | GB/T 16886 series |
| **Software evaluation** | 60,000–100,000 | GB/T 25000.51 |
| **ISO 13485 certification** | 80,000–120,000 | Certification body audit + preparation (NQA/TÜV/SGS) |
| **Clinical study (pre-clinical, n=30)** | 500,000–1,000,000 | IRB fees, subject stipends, site fees, insurance, data management |
| **CER writing** | 100,000–200,000 | Consultant fees for literature review + writing + translation |
| **Registration fee** | 72,300 | NMPA fixed fee for Class II (as of 2024) |
| **Submission dossier preparation** | 50,000–100,000 | Documentation compilation, format conversion, QC |
| **Supplement (发补) response** | 30,000–80,000 | Additional testing or documentation on reviewer request |
| **Post-market surveillance plan** | 20,000–40,000 | PV system setup + annual reporting mechanism |
| **Total direct costs** | **¥1,302,300–2,390,000** | |

### 9.2 Regulatory Personnel Costs

| Role | Time Required | Cost (¥) |
|------|--------------|----------|
| **Regulatory consultant (full-time)** | 12–18 months | 500,000–750,000 |
| **QMS specialist** | 6 months (initial setup) | 200,000–350,000 |
| **Clinical research coordinator** | 8 months | 160,000–240,000 |
| **Legal counsel (medical device regulatory)** | On retainer | 100,000–200,000 |
| **Total personnel costs** | | **¥960,000–1,540,000** |

### 9.3 Grand Total

| Category | Low Estimate (¥) | High Estimate (¥) |
|----------|-----------------|-------------------|
| Direct costs | 1,302,300 | 2,390,000 |
| Personnel costs | 960,000 | 1,540,000 |
| **Total** | **¥2,262,300** | **¥3,930,000** |

**Recommended budget allocation:** ¥3,000,000 (approximately USD $420,000 at 2026 exchange rate).

**Significant budget risks:**
- If full clinical trial (Pathway C) is required: add ¥1,500,000–2,000,000
- If 2 rounds of type testing needed: add ¥200,000–300,000
- If re-classification as Class III: add ¥2,000,000–3,000,000

---

## 10. Recommended Regulatory Consultant Qualifications

### 10.1 Consultant Requirements

| Criteria | Minimum Requirement | Preferred |
|----------|-------------------|-----------|
| **Experience** | ≥5 years in NMPA medical device registration | ≥10 years; ≥5 Class II device submissions |
| **Track record** | ≥3 successful Class II submissions to NMPA | ≥1 successful exoskeleton or BCI submission |
| **Exoskeleton experience** | Familiarity with YY/T 0933, GB 9706.1 for powered exoskeletons | Direct experience with UGO or DAAI submission |
| **AI/software experience** | Knowledge of IEC 62304, GB/T 25000.51 | Experience with SaMD classification negotiation |
| **Language** | Fluent Chinese (written) + English (technical documents) | NMPA review documentation drafting experience in Chinese |
| **Location** | Beijing preferred (near CMDE); Shanghai acceptable | Possibility for in-person meetings with CMDE within 48h |
| **Network** | Familiar with CMDE reviewers and process | Personal relationships with rehabilitation device reviewers |

### 10.2 Recommended Regulatory Consulting Firms in China

| Firm | Headquarters | Exoskeleton Experience | BCI/AI Experience | Estimated Rate |
|------|-------------|----------------------|-------------------|----------------|
| **江苏煜博医疗科技** | Nanjing | Yes (worked with rehab robot companies) | Moderate | ¥1,500–2,500/day |
| **北京华睿卓信** | Beijing | Yes (worked with ChengTian UGO team) | Moderate | ¥2,000–3,000/day |
| **上海祺晟医疗** | Shanghai | Limited | Limited (but strong SaMD) | ¥1,500–2,500/day |
| **深圳迈瑞思** | Shenzhen | Yes (general medical device) | Limited | ¥1,200–2,000/day |
| **TÜV Rheinland (China)** | Shanghai/Beijing | Yes (ISO 13485 + CE) | Strong AI regulatory | ¥3,000–5,000/day |
| **BSI China** | Shanghai | Yes | Strong AI/software | ¥3,000–5,000/day |

**Recommendation:** Hire a hybrid team:
1. **Primary regulatory consultant** from a Chinese firm with exoskeleton submission experience (either 煜博 or 华睿卓信) — this person handles the day-to-day submission work, communicates with testing labs, manages the dossier
2. **Specialized SaMD/AI consultant** — part-time, for the software evaluation and CER sections related to AI
3. **Backup:** TÜV or BSI for ISO 13485 certification and international harmonization (if CE marking is also planned)

### 10.3 Consultant Work Plan

| Month | Consultant Tasks | Deliverable |
|-------|-----------------|-------------|
| **M1–2** | Classification determination application; QMS gap analysis; risk management file template | Application submitted; QMS gap report |
| **M3–4** | Innovative device application; type testing lab selection + scheduling; IEC 62304 gap analysis | Innovative application submitted; test lab booked |
| **M5–6** | QMS implementation support; type testing supervision (pre-compliance before official); IRB package review | QMS ready for audit; pre-compliance test report |
| **M7–8** | CER literature review initiation; clinical protocol refinement; test lab management (re-test if needed) | Literature review outline; clinical study active |
| **M9–10** | CER draft writing; dossier template; ISO 13485 certification audit support | CER draft v1; dossier template ready |
| **M11–12** | CER finalization (incorporate clinical study results); dossier compilation | Submission-ready dossier |
| **M13–15** | Submission + review period liaison; supplement response preparation | Supplement response within 60-day deadline |
| **M16+** | Expert review support (if needed); certificate receipt | Registration certificate |

---

## Appendix A — Key Chinese Regulatory Terminology Reference

| English | Chinese | Abbreviation | Notes |
|---------|---------|-------------|-------|
| National Medical Products Administration | 国家药品监督管理局 | NMPA | Formerly CFDA |
| Center for Medical Device Evaluation | 医疗器械技术审评中心 | CMDE | NMPA's device review arm |
| China Food and Drug Administration Institute | 中国食品药品检定研究院 | CFDI | Testing lab |
| Class II medical device | 第二类医疗器械 | Class II | Moderate risk |
| Classification determination | 分类界定 | 分类界定 | Pre-submission classification |
| Innovative medical device special review | 创新医疗器械特别审查程序 | 创新通道 | Fast-track pathway |
| Type testing | 型式检验 | 型检 | Mandatory product testing |
| Clinical evaluation report | 临床评价报告 | CER | Literature + predicate analysis |
| Clinical trial | 临床试验 | 试验 | De novo patient study |
| Clinical trial exemption | 免于进行临床试验目录 | 豁免目录 | Devices not requiring separate clinical trial |
| Quality management system | 质量管理体系 | QMS | ISO 13485-based |
| Risk management | 风险管理 | RM | ISO 14971-based |
| Registration certificate | 医疗器械注册证 | 注册证 | Market approval document |
| Supplement / deficiency response | 发补 | 发补 | Reviewer request for additional data |

## Appendix B — Checklist: Readiness for Submission

Before submitting the registration dossier, verify the following items are complete:

- [ ] Classification determination letter confirming Class II (分类界定通知书)
- [ ] Innovative device approval (if filed and approved)
- [ ] GB 9706.1 type test report (full pass)
- [ ] YY 9706.102 EMC test report (full pass)
- [ ] GB/T 16886 biocompatibility test report (skin contact materials)
- [ ] GB/T 25000.51 software evaluation report
- [ ] ISO 13485 certification (or scheduled audit within 3 months)
- [ ] ISO 14971 risk management file (complete, reviewed, signed)
- [ ] IEC 62304 software lifecycle documentation (Class B level)
- [ ] IEC 62366 usability engineering file (including summative evaluation report)
- [ ] Clinical Evaluation Report (CER) — reviewed by CMDE pre-submission if possible
- [ ] Pre-clinical study report (n=30)
- [ ] Device labeling: IFU (使用说明书), packaging labels, quick-start guide (Chinese)
- [ ] Production quality inspection certificate (出厂检验报告)
- [ ] Post-market surveillance plan (上市后监督计划)
- [ ] Authorization letter from patent holder (if patent not owned by applicant)

---

*End of Regulatory Strategy v0.1. This is a living draft — update after CMDE consultation and regulatory consultant input.*
