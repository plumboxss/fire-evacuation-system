# Risk Indicators and Tenability Thresholds

> Reference document for tenability analysis.
> All thresholds are drawn from **ISO 13571:2012** and the
> **SFPE Handbook of Fire Protection Engineering** (5th ed.).

---

## Overview

Three instantaneous indicators and one cumulative indicator are used:

| Indicator | Symbol | Type | Source |
|-----------|--------|------|--------|
| Temperature | T | Instantaneous | ISO 13571, §5.2 |
| Visibility | V | Instantaneous | ISO 13571, §5.4 |
| CO concentration | [CO] | Instantaneous | SFPE Handbook, Table 2-6.3 |
| Fractional Effective Dose — CO | FED | Cumulative | ISO 13571, §7.3 |

---

## Thresholds

### Temperature

| Level | °C | Notes |
|-------|----|-------|
| Safe | ≤ 30 °C | Sustained exposure negligible risk |
| Danger | ≥ 60 °C | Threshold for humid-air convective heating causing incapacitation (ISO 13571, Table 1) |

Normalisation: linear ramp between 30 °C (→ 0.0) and 60 °C (→ 1.0).

### Visibility

| Level | m | Notes |
|-------|---|-------|
| Safe | ≥ 10 m | Occupants can locate exit signs unaided |
| Danger | ≤ 3 m | Wayfinding severely impaired; disorientation likely |

Reference: ISO 13571 §5.4; SFPE Handbook Chapter 2-6, Purser.

**Inverse mapping**: unlike temperature and CO, *higher* raw visibility
means *safer*. The normalised value is therefore `1 − clip(V/30, 0, 1)`.

### CO Concentration (Instantaneous)

| Level | ppm | Notes |
|-------|-----|-------|
| Safe | ≤ 100 ppm | Slight effect on sensitive individuals after prolonged exposure |
| Danger | ≥ 1400 ppm | Headache, dizziness, and incapacitation risk within minutes (SFPE Table 2-6.3) |

Normalisation: log-scale `log1p(ppm) / log1p(5000)`.
Log scale is used because CO hazard is non-linear and spans several orders of magnitude.

---

## Fractional Effective Dose — CO (Cumulative)

The FED accounts for **time-integrated exposure** and is appropriate for
predicting incapacitation along an evacuation path.

### Purser's CO Model (SFPE Handbook, 3rd ed., Chapter 2-6)

```
FED_CO = Σ [CO]^n × Δt / C_t
```

Where:
- `[CO]` = CO concentration in ppm at each time step
- `n = 1.036` (dose-response exponent for CO)
- `Δt` = time step duration in minutes
- `C_t` = reference concentration × time product (SFPE Table 2-6.4)

### Incapacitation Threshold

| Population | FED threshold |
|------------|---------------|
| Normal (healthy adults) | 1.0 |
| **Sensitive (used in this project)** | **0.3** |

The sensitive-population threshold (FED = 0.3) is specified in
**ISO 13571:2012, Section 7.3** and is adopted here because occupants
in a real evacuation may include elderly, children, or individuals with
respiratory conditions.

---

## Aggregated Danger Score

A single danger score d ∈ [0, 1] is computed per cell:

```
d = w_T × d_T + w_V × d_V + w_CO × d_CO
```

Default weights (see `configs/risk_map.yaml`):

| Component | Weight |
|-----------|--------|
| Temperature | 0.4 |
| Visibility | 0.4 |
| CO | 0.2 |

Each component danger is computed as a linear ramp between the safe
and danger thresholds, clipped to [0, 1].

---

## Implementation Reference

```python
from src.shared.constants import TENABILITY
from src.risk_map.tenability import compute_danger_score  # Week 12
from src.risk_map.fed import accumulate_fed               # Week 12

# TENABILITY constants:
# TENABILITY.T_SAFE_C     = 30.0
# TENABILITY.T_DANGER_C   = 60.0
# TENABILITY.V_SAFE_M     = 10.0
# TENABILITY.V_DANGER_M   = 3.0
# TENABILITY.CO_SAFE_PPM  = 100.0
# TENABILITY.CO_DANGER_PPM = 1400.0
# TENABILITY.FED_THRESHOLD = 0.3
```

---

## Out-of-Scope Hazards

The following are **explicitly excluded** from this project:

- HCN (hydrogen cyanide) — no FDS data available
- Irritant gases (acrolein, HCl) — out of scope
- Radiant heat flux — only convective temperature considered
- Multi-component FED — CO only
