# Risk Indicators and Tenability Thresholds

> Reference document for tenability analysis.
> All thresholds are drawn from **ISO 13571:2012** and the
> **SFPE Handbook of Fire Protection Engineering** (5th ed.).

---

## Korean Glossary (한국어 용어 정리)

| English | 한국어 |
|---------|-------|
| Tenability | 거주가능성 / 인명안전조건 |
| Fractional Effective Dose (FED) | 누적유효노출량 |
| Available Safe Egress Time (ASET) | 가용피난시간 |
| Required Safe Egress Time (RSET) | 요구피난시간 |
| Wayfinding | 피난동선 인식 / 길 찾기 |
| Incapacitation | 행동불능 |

---

## Overview

Three instantaneous indicators and one cumulative indicator are used:

| Indicator | Symbol | Type | Source |
|-----------|--------|------|--------|
| Temperature | T | Instantaneous | ISO 13571 §5.2 |
| Visibility | V | Instantaneous | ISO 13571 §5.4 |
| CO concentration | [CO] | Instantaneous | SFPE Handbook Table 2-6.3 |
| Fractional Effective Dose | FED_CO | Cumulative | ISO 13571 §7.3 |

---

## Thresholds

### Temperature

| Level | °C | Notes |
|-------|----|-------|
| Safe | ≤ 30 °C | Sustained exposure negligible risk |
| Danger | ≥ 60 °C | Threshold for humid-air convective heating causing incapacitation (ISO 13571 Table 1) |

Normalisation (used by models):

```
T_norm = (T_celsius − 20) / 1180,   clipped to [0, 1]
```

Range: 20 °C → 0.0; 1200 °C → 1.0. Domain motivated by FDS output range.

Danger score (used by risk map):

```
d_T = clip((T − 30) / (60 − 30), 0, 1)
```

This is a linear ramp: 30 °C → 0.0; 60 °C → 1.0.

### Visibility

| Level | m | Notes |
|-------|---|-------|
| Safe | ≥ 10 m | Occupants can locate exit signs unaided |
| Danger | ≤ 3 m | Wayfinding severely impaired; disorientation likely |

References: ISO 13571 §5.4; SFPE Handbook Ch. 2-6 (Purser).

**Inverse mapping**: unlike T and CO, *higher* raw visibility means
*safer*. The normalised value is therefore inverse:

```
V_norm = 1 − clip(V / 30, 0, 1)
```

Range: 30+ m → 0.0; 0 m → 1.0.

Danger score:

```
d_V = clip((10 − V) / (10 − 3), 0, 1)
```

This is a linear ramp: 10 m → 0.0; 3 m → 1.0; saturates beyond.

### CO Concentration (Instantaneous)

| Level | ppm | Notes |
|-------|-----|-------|
| Safe | ≤ 100 ppm | Slight effect on sensitive individuals after prolonged exposure |
| Danger | ≥ 1400 ppm | Headache, dizziness, incapacitation risk within minutes (SFPE Table 2-6.3) |

Normalisation (used by models):

```
CO_norm = log1p(CO_ppm) / log1p(5000),   clipped to [0, 1]
```

Log scale chosen because CO hazard is non-linear and spans several
orders of magnitude.

Danger score:

```
d_CO_inst = clip((CO − 100) / (1400 − 100), 0, 1)
```

---

## Fractional Effective Dose (FED) — CO

The FED accounts for **time-integrated exposure** and is the appropriate
indicator for predicting incapacitation along an evacuation path.

### Formula (ISO 13571 §7.3, simplified)

For a single occupant moving through the field:

```
FED_CO(t) = ∫₀ᵗ [CO](τ) / 27000 dτ          (with [CO] in ppm·min)
```

Equivalently in discrete time with frame interval Δt = 10 s:

```
FED_CO(t_n) = (Δt_min / 27000) · Σ_{k=0..n} CO_ppm[k]
            = (1/6 / 27000) · Σ_{k=0..n} CO_ppm[k]
```

where `Δt_min = 10 / 60 = 1/6` minutes.

### Why 27000?

The constant **27000 ppm·min** is the ISO 13571 reference dose for
incapacitation in an average healthy adult. This corresponds to:

```
FED = 1.0 ⟹ ~50% of healthy adults incapacitated.
FED = 0.3 ⟹ ~10% of sensitive individuals incapacitated.
```

We use the simplified form (without the Purser exponent `n = 1.036`)
because:

1. The exponent matters most at very high concentrations, which we
   already saturate via clipping.
2. The simplified form preserves the linear-time-integral structure
   that lets us compute FED along a path with low overhead.

### Threshold for this project

| Population | FED threshold |
|------------|---------------|
| Normal (healthy adults) | 1.0 |
| **Sensitive (used in this project)** | **0.3** |

The sensitive-population threshold (FED = 0.3) is specified in
**ISO 13571:2012 §7.3** and is adopted here because real evacuations
include elderly, children, and individuals with respiratory conditions.

### Path-integrated FED

For a moving occupant whose position at time `t` is `x(t)`:

```
FED_path = (Δt_min / 27000) · Σ_t CO_ppm(x(t), t)
```

This is the metric used by EXP-PATH-001 to compare static vs dynamic
evacuation paths.

---

## Aggregated Danger Score

The risk map combines per-cell instantaneous indicators into a single
scalar `d ∈ [0, 1]`:

```
d_total = clip(0.4 · d_T + 0.4 · d_V + 0.2 · d_CO_inst, 0, 1)
```

Default weights (modifiable in `configs/risk_map.yaml`):

| Component | Weight | Rationale |
|-----------|--------|-----------|
| Temperature (d_T) | **0.4** | Direct life-safety, fast-acting |
| Visibility (d_V) | **0.4** | Wayfinding-critical, drives decisions |
| CO instantaneous (d_CO_inst) | **0.2** | Slow accumulation; cumulative FED handles this better |

Cumulative FED is **separately tracked**, not folded into `d_total`,
because it is path-dependent and applies per occupant rather than
per cell.

---

## Implementation Reference

```python
from src.shared.constants import TENABILITY
from src.risk_map.tenability import compute_danger_score   # Wk 10
from src.risk_map.fed import accumulate_fed                # Wk 10
```

The `TENABILITY` dataclass exports:

```python
TENABILITY.T_SAFE_C        = 30.0
TENABILITY.T_DANGER_C      = 60.0
TENABILITY.V_SAFE_M        = 10.0
TENABILITY.V_DANGER_M      = 3.0
TENABILITY.CO_SAFE_PPM     = 100.0
TENABILITY.CO_DANGER_PPM   = 1400.0
TENABILITY.FED_REFERENCE   = 27000.0   # ppm·min
TENABILITY.FED_THRESHOLD   = 0.3       # sensitive population
TENABILITY.WEIGHT_T        = 0.4
TENABILITY.WEIGHT_V        = 0.4
TENABILITY.WEIGHT_CO       = 0.2
```

---

## Out-of-Scope Hazards

The following are **explicitly excluded** from this project (see
`docs/decisions.md` for rationales):

- **HCN** (hydrogen cyanide) — no FDS data available
- **Irritant gases** (acrolein, HCl) — out of scope
- **Radiant heat flux** — only convective temperature considered
- **Multi-component FED** — CO only
- **Hyperventilation due to elevated CO₂** — not modelled

These omissions make our tenability estimates **conservative under-estimates**
in some respects (we may miss some hazards) and **conservative over-estimates**
in others (we use sensitive-population thresholds). The net effect is
documented to be small (within 15%) for typical residential fire scenarios
per Purser's review work.

---

## Sources

1. **ISO 13571:2012** — *Life-threatening components of fire — Guidelines
   for the estimation of time available for escape using fire data.*
2. **SFPE Handbook of Fire Protection Engineering, 5th ed.**, Ch. 63,
   "Combustion Toxicity," Purser & McAllister, 2016.
3. **NFPA 130** for transit applications (referenced for FED 0.3 sensitive
   threshold confirmation).
4. **Purser, D. A.** "Toxicity assessment of combustion products."
   SFPE Handbook (3rd ed.), Ch. 2-6, 2002.
