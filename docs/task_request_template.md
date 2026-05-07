# Claude Code Task Request Template

> Standard format for requesting a single module or function from Claude Code.
> Following this template increases success rate and reduces back-and-forth.

---

## Why a Template

Claude Code is a strong *implementer* but works best when given:

1. **Clear goal** — what you want
2. **Bounded context** — what to read, what to ignore
3. **Concrete interface** — exact signature, types, shapes
4. **Verification command** — how to know it works
5. **Forbidden actions** — common mistakes to avoid

This template provides all five.

---

## The 8-Section Template

Copy this and fill in for each new task.

```markdown
# Task: <short descriptive title>

## 1. Goal
<one-sentence description of what the function or module does>

## 2. Context to Read
- `CLAUDE.md` (auto-loaded, you've already read it)
- `docs/<specific files relevant to this task>`
- `<any existing code files that this depends on>`

## 3. What to Implement
**File**: `<exact path, e.g., src/risk_map/fed.py>`

**Function signature**(s):
```python
def my_function(
    arg1: type1,
    arg2: type2,
) -> return_type:
    """One-line docstring."""
```

**Behaviour**: <2-4 sentences describing what it computes and why>

**Inputs**: <shapes, dtypes, ranges, units>
**Outputs**: <shapes, dtypes, ranges, units>

## 4. Interface Contract
- Must follow `docs/interface_contracts.md` for any tensor/dict shapes
- Must follow `docs/coordinate_convention.md` for any geometry
- Must use `src/shared/constants.py` for any numerical thresholds
- Must NOT modify any other module

## 5. Verification
After implementation, verify by running:

```bash
python -m src.<path.to.module>
```

This command should print `PASS` and exit 0. The `__main__` block must:
1. Load test data from <where>
2. Compute <what>
3. Verify <criterion>
4. Print clear pass/fail messages

Also add a unit test:

```bash
pytest tests/test_<module>.py -v
```

## 6. Code Style
- Type hints on every public function
- Docstrings (Google or NumPy style)
- pathlib.Path for paths
- raise ValueError with clear message; never silent failure
- No `from foo import *`
- No hard-coded numbers — use constants

## 7. Forbidden
- Do NOT modify other modules unless explicitly asked.
- Do NOT add dependencies without confirming first.
- Do NOT skip the `__main__` self-test block.
- Do NOT change the function signature without proposing first.

## 8. Reporting
After implementation:
1. Show me the full file content.
2. Show the output of `python -m <module>` (must be PASS).
3. Show the output of `pytest tests/test_<module>.py` (must be all PASS).
4. List any new dependencies added (should be ZERO normally).
```

---

## Worked Example

Here is a real task request following the template:

```markdown
# Task: Implement FED accumulation function

## 1. Goal
Compute path-integrated cumulative FED (Fractional Effective Dose)
from CO concentration along an evacuee's path.

## 2. Context to Read
- `CLAUDE.md`
- `docs/risk_indicators.md` (FED formula and threshold)
- `docs/interface_contracts.md` (RiskMap interface)

## 3. What to Implement
**File**: `src/risk_map/fed.py`

**Function signature**:
```python
def accumulate_fed(
    co_ppm_along_path: np.ndarray,  # shape (N,) in ppm
    dt_seconds: float,                # time step between path points
) -> np.ndarray:
    """Compute cumulative FED at each path point."""
```

**Behaviour**: For each step along an evacuation path, compute the
accumulated FED following ISO 13571 §7.3 simplified form:
`FED_n = FED_{n-1} + CO_n · (dt/60) / 27000`

**Inputs**:
- `co_ppm_along_path`: 1D array, length N, units ppm
- `dt_seconds`: scalar, typically 1.0 (drone replan interval)

**Outputs**:
- shape (N,) cumulative FED values, dimensionless ∈ [0, ∞)

## 4. Interface Contract
- Use `TENABILITY.FED_REFERENCE = 27000` from constants
- No external state; pure function

## 5. Verification
```bash
python -m src.risk_map.fed
```

Self-test: With constant `[CO] = 1000 ppm` for 30 minutes (`dt = 60s`,
N = 30), expected FED at end ≈ 1000 × 30 / 27000 = 1.111. Test must
verify within 0.001 of expected.

Also: `pytest tests/test_fed.py -v`

## 6. Code Style
Per CLAUDE.md.

## 7. Forbidden
- Do NOT use Purser exponent 1.036 (we use simplified form per
  decision D-008).
- Do NOT use any path-finding logic here — this function is purely
  for FED accumulation given a sequence of CO values.

## 8. Reporting
Show full file, `python -m` output, pytest output.
```

---

## Anti-Patterns to Avoid

### Anti-pattern 1: "Implement the entire risk map module"

Too broad. Break into:
- `tenability.py` (instantaneous danger)
- `fed.py` (cumulative)
- `risk_map_class.py` (abstract + 3 concrete)
- `predictive.py` (autoregress for 60s horizon)

Request each separately.

### Anti-pattern 2: "Make it generic / reusable"

Avoid. Specify the **exact** signature for our use case. We can
generalise later if needed.

### Anti-pattern 3: "Look at the codebase and figure out the best design"

Avoid. Even if Claude Code can do this, the result is unpredictable
and may conflict with our locked interfaces. Always specify the
signature.

### Anti-pattern 4: Skipping verification

Always include section 5. Without it, "implementation complete" can
mean code that doesn't even import correctly.

---

## Workflow Recommendation

1. Identify the next module from `docs/manual_v2.md` schedule.
2. Copy this template, fill in 8 sections.
3. Send to Claude Code.
4. Review the output.
5. Run the verification commands yourself.
6. If clean, commit.
7. If issues, refine and send back focused on the specific problem.

This typically yields a working module in 1–2 iterations.

---

## See Also

- `CLAUDE.md` — project context (auto-loaded)
- `docs/interface_contracts.md` — locked interfaces
- `docs/decisions.md` — past decisions
- `docs/lessons_learned.md` — known bugs to avoid
