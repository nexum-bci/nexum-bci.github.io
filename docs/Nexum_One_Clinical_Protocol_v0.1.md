# Nexum One — Pre-Clinical Study Protocol Outline

**Version 0.1** · 2026-06-21
**Author:** Zirui Zhao · Architecture
**Classification:** Internal — Clinical
**References:** [PRD v1.0](Nexum_One_PRD_v1.0.md), [Engineering Architecture v0.1](Nexum_One_Engineering_Architecture_v0.1.md)

---

## Table of Contents

1. Study Design
2. Inclusion / Exclusion Criteria
3. Primary Endpoint
4. Secondary Endpoints
5. Sample Size Justification
6. Study Procedure
7. Data Collection Plan
8. Safety Monitoring and Adverse Event Reporting
9. Statistical Analysis Plan
10. Ethical Considerations (IRB Pathway in China)

---

## 1. Study Design

### 1.1 Design Overview

**Type:** Prospective, single-arm, pre-post feasibility study.

**Phase:** Pre-clinical (pilot) — corresponds to NMPA clinical trial Phase I / feasibility stage. Not intended for pivotal efficacy claim. Intended to generate safety data, performance characterization, and effect size estimates for future sample size planning.

**Design Rationale:**
- Single-arm is appropriate at this stage because: (a) the sham condition for a wearable robot is difficult to blind effectively, and (b) the primary goal is characterizing system behavior and detecting signal (proof-of-mechanism), not proving superiority.
- Pre-post comparison (each subject serves as their own baseline) maximizes statistical power with limited sample size.
- A randomized crossover design (device ON vs device OFF) could be considered as a secondary analytic approach within the same cohort.

**Reference Designs:**
- Ekso GT feasibility study: single-arm, n=15, pre-walk vs powered-walk (Kressler et al., 2014, JNER).
- ReWalk pivotal trial: prospective, non-randomized, n=50, pre-post on walking endurance (Esquenazi et al., 2012, Am J Phys Med Rehabil).
- HAL (Cyberdyne) pre-market clinical study in Japan: single-arm, n=30, pre-post on gait parameters (Kawamoto et al., 2013).

### 1.2 Study Duration

| Item | Duration |
|------|----------|
| Total study duration | 8 months |
| Recruitment period | 3 months |
| Each subject's participation | 4 weeks |
| Training sessions per subject | 8 sessions (2 sessions/week × 4 weeks) |
| Evaluation sessions | Pre-training (baseline) + Post-training (week 4) |

### 1.3 Study Sites

Single-site or multi-site (2–3 sites):
- **Primary site:** Rehabilitation hospital or university hospital rehab department (e.g., 中国康复研究中心, 宣武医院, or 华山医院康复科)
- **Secondary site (optional):** Another tier-1 rehab center to demonstrate generalizability
- **Tertiary site (optional):** Community rehab center for home-use feasibility subset (n=5)

---

## 2. Inclusion / Exclusion Criteria

### 2.1 Inclusion Criteria

1. **Age:** 22–75 years inclusive
2. **Diagnosis:**
   - **Cohort A — Stroke (n=15):** Unilateral hemiparesis due to ischemic or hemorrhagic stroke, ≥6 months post-stroke (chronic stage)
   - **Cohort B — Incomplete SCI (n=15):** Traumatic or non-traumatic SCI, AIS C or D, neurological level C4–L2, ≥6 months post-injury
3. **Functional status:** Able to stand with or without assistance for ≥30 seconds; able to walk at least 10 m with walker/cane (with or without assistance)
4. **Cognitive status:** Mini-Mental State Examination (MMSE) ≥24; able to follow 3-step commands
5. **Cortical function preserved:** Detectable Bereitschaftspotential (BP) or movement-related cortical potential (MRCP) during screening EEG (at least 50% detection rate over 20 self-paced foot-lift trials)
6. **Skin integrity:** Intact skin at all points of contact with the device
7. **Informed consent:** Able and willing to provide written informed consent

### 2.2 Exclusion Criteria

1. **Complete SCI:** AIS A or B (no preserved motor function below lesion)
2. **Bilateral stroke or brainstem stroke** involving motor cortex bilaterally
3. **Severe spasticity:** Modified Ashworth Scale (MAS) ≥3 in hip flexors or extensors
4. **Fixed joint contracture:** Hip flexion contracture >20 degrees; knee flexion contracture >15 degrees
5. **Uncontrolled epilepsy:** Seizure within the past 6 months
6. **Cardiovascular instability:** Uncontrolled hypertension (SBP >160 or DBP >100 mmHg at rest); recent myocardial infarction (<3 months); symptomatic orthostatic hypotension
7. **Orthopedic contraindications:** Lower extremity fracture within past 6 months; severe osteoporosis (T-score ≤ −3.0)
8. **Pressure ulcers:** Stage ≥2 at any device contact point
9. **Severe sensory impairment:** Inability to detect device pressure or position changes
10. **Pregnancy** or planning pregnancy during study period
11. **Concurrent participation** in another interventional clinical trial
12. **Scalp conditions** affecting EEG electrode contact (wounds, psoriasis, dermatitis at electrode sites)
13. **Metal implants** in the head (intracranial electrodes, clips) — relative exclusion; case-by-case evaluation
14. **Body weight** >100 kg (exosuit sizing limit)

### 2.3 Screening Failure Definition

Subject is considered a screening failure if:
- Cannot tolerate EEG headband for ≥10 min during screening
- MRCP not detectable in ≥50% of screening trials
- Cannot complete baseline 10MWT due to safety concern

---

## 3. Primary Endpoint

### 3.1 Co-Primary Endpoints (Dual: Safety + Performance)

The study has two co-primary endpoints, reflecting the pre-clinical nature of this investigation.

#### Endpoint 1 — Safety: Serious Adverse Device Events (SADE)

**Definition:** Proportion of subjects experiencing a serious adverse device event (SADE) during the 4-week study period.

**SADE criteria (per ISO 14155:2020):**
- Device-related fall resulting in fracture or head injury
- Device-related skin injury ≥ Grade 2 (per CTCAE v5.0) — blistering, ulceration, or infection
- Device-related electrical shock or burn
- Any adverse event leading to hospitalization, life-threatening condition, or death

**Success threshold:** Zero SADEs (upper bound of 95% CI ≤10% for n=30)

#### Endpoint 2 — Performance: Intention Detection Accuracy

**Definition:** Area Under the Receiver Operating Characteristic Curve (AUC-ROC) for single-trial movement intention detection during walking.

**Measurement method:**
- Ground truth: sEMG from rectus femoris (ipsilateral to intended movement) as surrogate marker of actual movement initiation
- Detection target: Nexum One's intention detection algorithm output (binary: intention / no intention) in 200 ms sliding windows
- Aggregate across all strides from all evaluation sessions

**Success threshold:** AUC >0.80 (lower bound of one-sided 95% CI ≥0.75) in the overall cohort.

**Rationale:** Single-trial BP detection AUC of 0.75–0.85 is state-of-the-art in lab settings (Lew et al., 2012; Jiang et al., 2015). During gait, expect 0.70–0.80. Setting threshold at 0.75 is realistic for a first-in-human study.

---

## 4. Secondary Endpoints

| # | Endpoint | Measure | Instrument / Method | Timepoint |
|---|----------|---------|---------------------|-----------|
| S1 | Gait speed | Change in 10-Meter Walk Test (10MWT), comfortable pace | Stopwatch, 10 m marked walkway | Baseline → Week 4 |
| S2 | Walking endurance | Change in 6-Minute Walk Test (6MWT) | Stopwatch, 30 m marked walkway | Baseline → Week 4 |
| S3 | Functional mobility | Change in Timed Up and Go (TUG) test | Stopwatch, chair, 3 m walk | Baseline → Week 4 |
| S4 | Lower limb motor function | Change in Fugl-Meyer Assessment — Lower Extremity (FMA-LE) | Qualified assessor (blinded to device settings) | Baseline → Week 4 |
| S5 | Balance | Change in Berg Balance Scale (BBS) | Qualified assessor (blinded) | Baseline → Week 4 |
| S6 | Spatiotemporal gait parameters | Change in step length symmetry ratio, stride time variability | Gait analysis mat (GAITRite or equivalent) or instrumented walkway | Baseline → Week 4 |
| S7 | Muscle activation | Change in sEMG envelope amplitude (rectus femoris, biceps femoris, tibialis anterior, gastrocnemius) during gait | Wireless sEMG (Delsys Trigno or equivalent), synchronized with gait events | Baseline → Week 4 |
| S8 | User satisfaction | Quebec User Evaluation of Satisfaction with Assistive Technology (QUEST 2.0) | Questionnaire | Week 4 |
| S9 | System usability | System Usability Scale (SUS) | Questionnaire | Week 1, Week 4 |
| S10 | Cognitive load | NASA-TLX (Task Load Index) score during device use | Questionnaire | Week 1, Week 4 |
| S11 | Device experience | Proportion of sessions where device provided meaningful assistance (user-reported "helped me walk") | Binary question after each session | Per session |
| S12 | False positive rate | FP rate = unintended assistance events / total strides | Algorithm log analysis | Per session |
| S13 | False negative rate | FN rate = missed intentions / total attempted strides | Algorithm log + sEMG verification | Per session |
| S14 | End-to-end latency | Latency from EEG onset marker to torque application at hip | System clock synchronization (EEG → phone → motor) | Weekly |

---

## 5. Sample Size Justification

### 5.1 Sample Size Calculation

**Target: n=30** (15 stroke + 15 incomplete SCI).

#### For Primary Endpoint 1 (Safety):
- Zero SADE in n=30 subjects. Using the "rule of three" (Hanley & Lippman-Hand, 1983): upper bound of 95% CI for adverse event rate = 3/n = 3/30 = 10%.
- This is an acceptable safety risk profile for a first-in-human pre-clinical study of a non-invasive wearable device.
- n=30 is consistent with early feasibility studies for similar devices: Ekso (n=15), ReWalk pivotal (n=50), HAL pre-market (n=30).

#### For Primary Endpoint 2 (AUC ≥0.75):
- Assumptions: expected AUC = 0.83, null hypothesis AUC = 0.75, one-sided α = 0.05, power = 0.80.
- Using Hajian-Tilaki's method for AUC sample size: n ≈ 24–30 subjects across both cohorts.
- Accounting for 15% attrition: target enrollment n=30 yields n=25–26 evaluable subjects.

#### For Secondary Endpoints (Exploratory):
- n=30 provides 80% power to detect a standardized effect size d=0.55 (medium effect) in pre-post comparison of gait speed (10MWT), at α=0.05 two-tailed.
- This is adequate for generating effect size estimates to power a future pivotal trial, but NOT adequate for definitive efficacy claims.

### 5.2 Comparison to Prior Device Studies

| Device | Study Type | n | Primary Endpoint | Outcome |
|--------|-----------|---|------------------|---------|
| Ekso GT | Feasibility, single-arm | 15 | Safety + gait parameters | SADE=0; gait speed improved |
| ReWalk | Pivotal, non-randomized | 50 | 6MWT, 10MWT | 6MWT +55 m (p<0.001) |
| HAL (Cyberdyne) | Pre-market, single-arm | 30 | FMA-LE, gait speed | FMA-LE +4.2 points; 10MWT +0.08 m/s |
| Indego | Feasibility, crossover | 27 | 6MWT, 10MWT | 6MWT +28 m in powered mode |
| Our study | Feasibility, single-arm | 30 | Safety + AUC; 10MWT/6MWT (exploratory) | — |

---

## 6. Study Procedure

### 6.1 Overall Flow

```
Screening Visit → Baseline Assessment → Training Phase (8 sessions) → Post-Training Assessment → 30-Day Safety Follow-up
     ↓                    ↓                                       ↓                            ↓
   Day -7 to -1           Day 0                                 Week 1–4                   Week 8
```

### 6.2 Visit Schedule

| Visit | Time | Activities | Duration |
|-------|------|-----------|----------|
| V0 — Screening | Day −14 to −1 | Informed consent, medical history, vitals, screening EEG (MRCP detection), 10MWT screening, skin assessment | 90 min |
| V1 — Baseline | Day 0 | Full motor assessment (FMA-LE, BBS, 10MWT, 6MWT, TUG), GAITRite, sEMG, setup time measurement, device fitting, comfort assessment | 120 min |
| V2 — Training Session 1 | Week 1, Day 1 | Device donning, system calibration, supervised gait training (15 min device ON + 15 min rest) | 60 min |
| V3 — Training Session 2 | Week 1, Day 3–4 | Supervised gait training with device (20 min device ON), NASA-TLX, SUS | 60 min |
| V4 — Training Session 3 | Week 2, Day 1 | Gait training (25 min), parameter adjustment, optional community ambulation | 60 min |
| V5 — Training Session 4 | Week 2, Day 3–4 | Gait training (30 min), stair negotiation training (if safe), adverse event check | 60 min |
| V6 — Training Session 5 | Week 3, Day 1 | Gait training (30 min), obstacle negotiation | 60 min |
| V7 — Training Session 6 | Week 3, Day 3–4 | Gait training (30 min), increasing speed trials | 60 min |
| V8 — Training Session 7 | Week 4, Day 1 | Final training + user satisfaction (QUEST 2.0) | 60 min |
| V9 — Post-Training Eval | Week 4, Day 3–4 | Full motor assessment (identical to V1), GAITRite, sEMG, physiological cost index, SUS, device log download | 120 min |
| V10 — Safety Follow-up | Week 8 (±3 days) | Phone call or in-person: adverse event check, device return confirmation | 15 min |

### 6.3 Training Protocol Details

Each training session follows a structured progression:

1. **Baseline setup (10 min):**
   - Don EEG headband, verify electrode impedance <50 kΩ per channel
   - Don NeuroSuit hip module, verify cable routing and comfort
   - System calibration: EEG baseline recording (30 s eyes open, 30 s eyes closed)
   - Body-weight support (overhead harness) for fall safety during all sessions

2. **Calibration walk (5 min):**
   - Walk with device in passive (zero-torque) mode to collect baseline gait parameters
   - User-specific AI model initializes based on passive-walk EEG features

3. **Adaptive training (20–30 min):**
   - Device provides assistive torque based on detected movement intention
   - Therapist provides verbal cues and manual guidance as needed
   - Rest breaks every 10 minutes or as requested
   - Distance or duration targets increase across sessions

4. **Cool-down (5 min):**
   - Passive mode walking or seated rest
   - Device doffing, skin inspection

### 6.4 Device State Conditions (For Comparison)

At the end of each training session (starting Session 3), a 5-minute comparison walk is performed:

| Condition | Description |
|-----------|-------------|
| Device OFF | Suit worn, motors powered down (passive assistance only — no torque) |
| Device ON | Full closed-loop: EEG → AI → torque assistance |

The order is randomized across sessions to control for fatigue effects. The therapist and subject are not blinded (device OFF is obvious), but the assessor for outcome measures is blinded to condition order.

---

## 7. Data Collection Plan

### 7.1 Data Types and Frequency

| Data Category | Variables | Collection Frequency | Storage Format | Responsible |
|--------------|-----------|---------------------|----------------|-------------|
| **Demographics** | Age, sex, height, weight, diagnosis, onset date, lesion level (SCI), lesion side (stroke) | Once at V0 | CRF (paper/electronic) | Site coordinator |
| **Medical history** | Comorbidities, medications, prior surgeries, fall history | Once at V0 | CRF | Site coordinator |
| **EEG** | 8-channel raw EEG (250 Hz, 24-bit), impedance per channel | Every session | `.edf` + compressed `.npz` | Algorithm team |
| **sEMG** | 4-channel (RF, BF, TA, GASTRO) raw EMG (2000 Hz) | V1, V9 (full); V2–V8 (spot check) | `.edf` | Algorithm team |
| **IMU** | Hip angle, angular velocity, trunk orientation (100 Hz) | Every session | `.csv` | Firmware team |
| **Motor data** | Torque setpoint, actual torque, motor current, cable force (200 Hz) | Every session | `.csv` | Firmware team |
| **Intention log** | Detection timestamps, confidence scores, false positive/negative flags | Every session | `.json` | Algorithm team |
| **Gait parameters** | Step length, step time, double support %, cadence, symmetry indices | V1, V9 (GAITRite); V2–V8 (IMU-based estimate) | `.csv` | Clinical team |
| **Clinical assessments** | 10MWT, 6MWT, TUG, FMA-LE, BBS, MAS | V1, V9 | CRF + video recording (optional) | Clinical team |
| **Skin assessment** | Erythema, pressure marks, blistering (photographed) | Every session | CRF + photo (`.jpg`) | Site coordinator |
| **Adverse events** | Type, severity, relation to device, action taken | Every session, plus V10 (retrospective) | CRF + SAE form within 24h | Site coordinator |
| **User feedback** | QUEST 2.0, SUS, NASA-TLX, device experience (binary) | As per visit schedule | CRF / questionnaire | Site coordinator |
| **System log** | Battery level, BLE packet loss rate, CPU load, error codes | Every session, per-session summary | `.json` | System team |

### 7.2 Data Management

- **Primary database:** REDCap or local equivalent (e.g., 临床研究电子数据采集系统 by 国家药品监督管理局)
- **Data quality:** Double-entry verification for primary endpoints; automated range checks; query resolution within 72 hours
- **Data ownership:** Nexum (Bones & Manifold). De-identified data may be shared with academic collaborators under DTA.
- **Data retention:** 10 years (per GCP guidelines). EEG raw data stored as `.edf` for future re-analysis. Anonymized dataset to be deposited in a public repository (e.g., PhysioNet, OpenNeuro, or 科学数据银行) after primary publication.

### 7.3 De-identification Protocol

- Direct identifiers (name, ID number, phone, hospital record number) stripped at source
- Subject assigned 6-digit random Study ID at enrollment
- EEG/sEMG recordings labeled with Study ID only (date offset by random number of days)
- Linking file stored in encrypted, access-controlled database, separate from clinical data

---

## 8. Safety Monitoring and Adverse Event Reporting

### 8.1 Definitions (per ISO 14155:2020)

| Term | Definition |
|------|-----------|
| **AE** — Adverse Event | Any untoward medical occurrence in a subject, whether or not related to the device |
| **ADE** — Adverse Device Event | AE related to the use of the Nexum One device (including misuse or off-label use) |
| **SADE** — Serious Adverse Device Event | ADE that leads to death, serious deterioration in health (life-threatening, requires hospitalization, causes permanent impairment), or requires intervention to prevent permanent impairment |
| **UADE** — Unanticipated Adverse Device Effect | ADE of a type not previously described in the risk management file (ISO 14971) or IFU |

### 8.2 Expected Adverse Events (Based on Risk Analysis)

| Risk | Severity | Probability | Expected Rate |
|------|----------|-------------|---------------|
| Skin abrasion/redness from suit friction | Mild–Moderate | High | 20–40% of subjects |
| Electrode discomfort (pressure points on scalp) | Mild | Medium | 15–25% |
| Fall during walking (harnessed) | Mild (no injury) | Medium | 10–20% |
| Skin pressure mark >30 min duration | Mild | Medium | 10–15% |
| Muscle soreness (unaccustomed gait pattern) | Mild | High | 30–50% |
| Dizziness or orthostatic intolerance | Mild | Low | 5–10% |
| Anxiety or claustrophobia from device | Mild | Low | 3–5% |
| Battery overheating (enclosure >48°C) | Moderate | Low | <1% |
| Cable breakage during use (sudden loss of assistance) | Mild | Low | <1% |

### 8.3 Safety Monitoring Plan

| Mechanism | Description | Frequency |
|-----------|-------------|-----------|
| **Pre-session safety check** | Device integrity inspection (cable, connector, battery), subject self-report of any issue since last visit | Each session |
| **Post-session skin assessment** | Systematic skin inspection at all contact points; documented with body diagram + photo | Each session |
| **Falls log** | Any fall (regardless of injury) documented: circumstances, harness status, injury, follow-up | Each incident |
| **Safety pause** | If any single subject experiences ≥2 falls (even harnessed), suspend enrollment for DSMB review | Per event |
| **Device event log** | Continuous recording of system faults, over-current events, emergency stops, watchdog resets | Continuous |

### 8.4 Adverse Event Reporting Procedures

| AE Type | Reporting Requirement | Responsible | Timeline |
|---------|----------------------|-------------|----------|
| Mild AE (Grade 1) | Document in CRF; continue device use | Site coordinator | Within 72 hours |
| Moderate AE (Grade 2) | Document in CRF; suspend device use until resolved | PI | Within 24 hours |
| Severe AE (Grade ≥3) | Document in CRF; file SAE form; notify sponsor; notify IRB | PI + Sponsor | Within 24 hours |
| SADE | All of the above + pause enrollment; convene DSMB if needed | PI + Sponsor + DSMB | Immediate (phone) + 24h (written) |
| UADE | All SADE procedures + file amendment to regulatory authority | Sponsor | Within 72 hours |

### 8.5 Stopping Rules

The study will be paused for DSMB review if ANY of the following occur:

1. **Any SADE** (device-related death, fracture, grade ≥3 skin injury, electrical shock, hospitalization)
2. **≥2 falls resulting in injury** (fracture, head injury, laceration requiring sutures)
3. **≥3 subjects experience Grade ≥2 skin injury** at device contact points
4. **≥2 subjects withdraw** due to device intolerance (pain, anxiety, discomfort)
5. **Cumulative device-related AE rate exceeds 50%** of enrolled subjects

### 8.6 Data Safety Monitoring Board (DSMB)

- Composition: 1 rehabilitation physician (independent of study), 1 biostatistician, 1 neuro-engineer (independent, affiliated with academic institution)
- Meeting schedule:
  - Pre-study: review protocol, approve safety plan
  - Interim: after n=10 subjects complete 2-week milestone
  - Ad-hoc: if stopping rule triggered
- The DSMB has authority to recommend study suspension, modification, or termination to the IRB.

---

## 9. Statistical Analysis Plan

### 9.1 Analysis Populations

| Population | Definition | Primary Analysis |
|------------|-----------|------------------|
| **Intent-to-Treat (ITT)** | All enrolled subjects who signed consent | Safety analysis (endpoint 1) |
| **Per-Protocol (PP)** | All subjects who completed ≥6/8 training sessions + final evaluation | Performance analysis (endpoint 2) and secondary endpoints |
| **Safety Population** | All subjects who used device at least once | Adverse event rate |

### 9.2 Primary Endpoint Analysis

#### Endpoint 1 (Safety):
- **Method:** Proportion of subjects with SADE, with exact 95% CI (Clopper-Pearson method).
- **Hypothesis:** H0: p ≥ p₀ vs H1: p < p₀, where p₀ = 0.10 (acceptable upper bound).
- **Decision rule:** If zero SADE observed and n ≥ 30, the upper bound of 95% CI <10%, meeting the threshold.

#### Endpoint 2 (AUC):
- **Method:** Pooled AUC-ROC across all subjects, computed using all strides from all evaluation sessions. Standard error estimated via bootstrapping (2000 resamples, stratified by subject).
- **Hypothesis:** H0: AUC ≤ 0.75 vs H1: AUC > 0.75 (one-sided α = 0.05).
- **Subgroup analysis:** Separate AUC for stroke vs SCI; separate AUC for walking initiation vs other classes (sit-to-stand, stop).

### 9.3 Secondary Endpoint Analysis

| Endpoint | Analysis Method | Covariates | Missing Data |
|----------|----------------|------------|--------------|
| 10MWT change | Paired t-test (or Wilcoxon signed-rank if normality violated) | Age, baseline gait speed, lesion type | Last observation carried forward (LOCF) sensitivity |
| 6MWT change | Same as above | Same | Same |
| TUG, FMA-LE, BBS | Same as above | Same | Same |
| sEMG envelope change | Mixed-effects model (fixed: time; random: subject, session) | Lesion type | Mixed model handles missing |
| Gait symmetry | Paired t-test on symmetry ratio | — | LOCF |
| QUEST 2.0, SUS | Descriptive: mean ± SD, median [IQR] | — | Analysis only on completers |

All secondary endpoints are **exploratory and hypothesis-generating**. No multiplicity adjustment is applied. Results will be reported as effect sizes with 95% CI, not p-values for significance testing.

### 9.4 Subgroup Analyses (Exploratory)

- Stroke vs SCI: compare treatment effect sizes
- High lesion (above T10) vs low lesion (T10–L2) in SCI cohort
- Hemorrhagic vs ischemic stroke
- Age groups: <50 vs 50–75
- EEG signal quality: high SNR (≥3 dB) vs low SNR (<3 dB)

### 9.5 Sample Size Re-estimation

After n=15 subjects complete the study, an interim analysis (blinded to treatment allocation) will be conducted to:
1. Estimate variability of primary endpoints
2. Confirm that AUC variability is within expected range (±0.08)
3. If AUC variability is substantially higher than expected (>±0.12), the total n may be increased to 40–50 to maintain power

---

## 10. Ethical Considerations (IRB Pathway in China)

### 10.1 Regulatory Framework

This study falls under the following Chinese regulations:

| Regulation | Scope | Applicable Clause |
|------------|-------|-------------------|
| 《医疗器械临床试验质量管理规范》(GCP) 2022版 | All medical device clinical trials | Full compliance required |
| 《涉及人的生物医学研究伦理审查办法》2016版 | Human subjects research ethics | Full compliance required |
| 《医疗器械注册与备案管理办法》2021版 | Device registration | Supporting data for NMPA submission |
| 《创新医疗器械特别审查程序》2018版 | Innovative device fast track | Study design compatible with innovative device requirements |
| 《个人信息保护法》2021版 | Personal data protection | Patient data handling procedures |

### 10.2 IRB Approval Pathway

**Step 1 — Select the IRB / Ethics Committee**

For a pre-clinical feasibility study, the study can proceed under **IRB approval** (not yet NMPA clinical trial filing, since this is pre-market feasibility). Options ranked by feasibility:

| IRB Option | Advantages | Disadvantages | Recommended For |
|------------|-----------|---------------|-----------------|
| **Hospital Ethics Committee (e.g., 宣武医院 伦理委员会)** | Fastest (4–8 weeks); known process; PI's institution | Results may not be accepted by NMPA directly; need GCP-compliant EC | **Primary choice** for feasibility study |
| **University IRB (e.g., Tsinghua/SEU)** | Fast (4–6 weeks); academic collaborators | May not have medical device review experience | Secondary site choice |
| **National-level clinical trial platform (e.g., 国家康复辅具研究中心)** | NMPA-recognized; results directly usable for registration | Slower (8–12 weeks); more documentation | For pivotal trial (Phase 2) |

**Step 2 — Prepare IRB Submission Package**

Required documents per 《医疗器械临床试验质量管理规范》:

| Document | Responsible |
|----------|-------------|
| IRB application form (伦理审查申请表) | Sponsor (Nexum) |
| Study protocol (version 0.1, dated) | Sponsor |
| Investigator's Brochure (IB) — device description, pre-clinical data, safety data, risk analysis | Sponsor |
| Informed Consent Form (ICF) — Chinese language, Grade 6 readability | Sponsor + PI |
| Case Report Forms (CRF) | Sponsor |
| Device description and intended use document | Sponsor |
| ISO 14971 risk management file (summary for IRB) | Sponsor |
| Investigator's CV and GCP training certificate | PI |
| Insurance certificate for clinical trial subjects | Sponsor |
| Device quality inspection certificate (出厂检验报告) | Sponsor |

**Step 3 — Informed Consent Process**

- Written informed consent in Mandarin Chinese (simplified characters)
- Read-aloud option for subjects with low literacy
- Cooling-off period: minimum 24 hours between information delivery and signing
- Surrogate consent allowed if subject cannot write (witness signs on behalf) per 《民法典》
- Video recording of consent process recommended for subjects with aphasia

**Step 4 — Special Ethical Considerations**

1. **Vulnerable population:** Stroke and SCI patients may have cognitive or communication impairments. Consent capacity must be assessed by a qualified physician independent of the study. For subjects with reduced capacity, family member consent + subject assent required.

2. **Placebo/sham issue:** No sham device group. Rationale documented: (a) sham condition for a wearable device cannot be effectively blinded, (b) the study objective is feasibility/safety, not efficacy. This is ethically acceptable per WHO CIOMS guidelines.

3. **Fall risk:** Continuous overhead harness safety system. Study staff at 1:1 ratio during all sessions. Falls will be documented but not concealed.

4. **Data privacy:** All personal data processed per 《个人信息保护法》 and 《数据安全法》. EEG data is considered sensitive personal information under Chinese law. De-identification protocol per Section 7.3.

5. **Compensation:** Subject stipend of ¥500 per completed session (total ¥5,000 for full participation). Travel reimbursement at ¥0.8/km or public transportation fare. Insurance coverage: ¥500,000 per subject for clinical trial injury (per 《药物临床试验质量管理规范》 — analogous standard for devices).

6. **Right to withdraw:** Subject may withdraw at any time without consequences for their clinical care. Withdrawn subjects will not be replaced in the analysis (ITT handles missing data).

### 10.3 Registration

- Study registered in Chinese Clinical Trial Registry (中国临床试验注册中心, ChiCTR) prior to enrollment
- World Health Organization International Clinical Trials Registry Platform (WHO ICTRP) secondary registration

### 10.4 Publication Policy

- Primary analysis: intended for peer-reviewed journal (e.g., Journal of NeuroEngineering and Rehabilitation, Frontiers in Neuroscience, or Chinese Journal of Rehabilitation Medicine)
- Negative results will be published equally to positive results
- Authorship: Principal Investigator (first author), Nexum CTO/CEO (senior author), key contributors per ICMJE criteria

---

## Appendix A — References

1. Kressler J, Thomas CK, Field-Fote EC, et al. (2014). "Understanding therapeutic benefits of overground gait training using a powered exoskeleton after incomplete SCI." *J Neuroeng Rehabil*, 11:158.
2. Esquenazi A, Talaty M, Packel A, Saulino M. (2012). "The ReWalk powered exoskeleton to restore ambulatory function to individuals with thoracic-level motor-complete spinal cord injury." *Am J Phys Med Rehabil*, 91(11):911–21.
3. Kawamoto H, Kambayashi K, Nakata Y, et al. (2013). "Pilot study of locomotion improvement using hybrid assistive limb with walking intention." *Adv Robot*, 27(10):783–93.
4. Hanley JA, Lippman-Hand A. (1983). "If nothing goes wrong, is everything all right? Interpreting zero numerators." *JAMA*, 249(13):1743–5.
5. Hajian-Tilaki K. (2014). "Sample size estimation in diagnostic test studies of biomedical informatics." *J Biomed Inform*, 48:193–204.
6. ISO 14155:2020 — Clinical investigation of medical devices for human subjects — Good clinical practice.
7. Lew E, Chavarriaga R, Silvoni S, Millán J del R. (2012). "Detection of self-paced reaching movement intention from EEG signals." *Front Neuroeng*, 5:13.

## Appendix B — Assessment Schedule Matrix

| Assessment | V0 Screen | V1 Base | V2 | V3 | V4 | V5 | V6 | V7 | V8 | V9 Eval | V10 FU |
|------------|:---------:|:-------:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:-------:|:------:|
| Informed consent | ✓ | | | | | | | | | | |
| Medical history | ✓ | | | | | | | | | | |
| Vitals | ✓ | ✓ | | ✓ | | ✓ | | ✓ | | ✓ | |
| MMSE | ✓ | | | | | | | | | | |
| Screening EEG (MRCP) | ✓ | | | | | | | | | | |
| FMA-LE | | ✓ | | | | | | | | ✓ | |
| BBS | | ✓ | | | | | | | | ✓ | |
| 10MWT | ✓ (screen) | ✓ | | | | | | | | ✓ | |
| 6MWT | | ✓ | | | | | | | | ✓ | |
| TUG | | ✓ | | | | | | | | ✓ | |
| GAITRite | | ✓ | | | | | | | | ✓ | |
| sEMG (full) | | ✓ | | | | | | | | ✓ | |
| sEMG (spot) | | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | | |
| EEG system test | | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | | |
| Device training | | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | | |
| Device ON/OFF comparison | | | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | |
| Skin assessment | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | |
| AE check | | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| QUEST 2.0 | | | | | | | | | ✓ | | |
| SUS | | | | ✓ | | | | | | ✓ | |
| NASA-TLX | | | | ✓ | | | | | | ✓ | |
| Device experience | | | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | |
| System log download | | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | |
| Physiological cost index | | ✓ | | | | | | | | ✓ | |

---

*End of Clinical Protocol v0.1. This is a living draft — update after regulatory consultation and IRB feedback.*
