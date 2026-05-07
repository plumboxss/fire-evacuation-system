# Decision Log

> Each major project decision logged with date, decision, alternatives,
> and rationale. Append-only — past decisions are not edited.

---

## D-001: Single floor, not multi-floor

**Date**: Project inception
**Decision**: Building is a single floor only.
**Alternatives**: Multi-floor with stairwells; high-rise.
**Rationale**: Multi-floor doubles or triples computational cost in FDS,
introduces stairwell evacuation modelling, and risks scope blow-up.
Single floor is sufficient to demonstrate the dynamic-vs-static
path-planning value proposition.

---

## D-002: Mesh resolution 0.5 m

**Date**: Project inception
**Decision**: Cell size 0.5 m × 0.5 m × 0.5 m → 60 × 40 × 6 SLCF grid.
**Alternatives**: 0.2 m (150 × 100 × 15 cells) for higher fidelity.
**Rationale**: 0.2 m would make FDS scenarios take 8–10× longer to run
(~40+ CPU-hours per scenario). 30 scenarios at that rate would
consume the entire RunPod budget. 0.5 m is sufficient for spatial
features at human-evacuation scale (room widths, corridor widths).

---

## D-003: Maze-style building, not simple rectangle

**Date**: Week 3
**Decision**: Maze-style layout with multiple rooms, intersections,
central courtyard, and 2 end-exit doors.
**Alternatives**: Single corridor with fire at one end.
**Rationale**: A simple rectangle makes Dijkstra near-optimal — defeats
the purpose of comparing dynamic vs static planners. Maze structure
ensures Dijkstra and dynamic planners produce visibly different
paths under fire spread.

---

## D-004: SLCF region (60×40×6) ≠ FDS MESH (100×80×8)

**Date**: Week 3 (after fdsreader bug discovery)
**Decision**: FDS MESH includes 10 m external buffer for ventilation
boundary conditions; SLCF extracts only the building footprint.
**Alternatives**: Make FDS MESH = SLCF region (no buffer).
**Rationale**: Without external buffer, FDS treats building edges as
hard walls, distorting smoke/heat transport near doors. With buffer,
ventilation boundaries are physically reasonable. The model only
sees the SLCF region — buffer is invisible to ML.

---

## D-005: Three indicators (T, V, CO), not full toxic suite

**Date**: Week 1
**Decision**: ML predicts only Temperature, Visibility, CO.
**Alternatives**: Add HCN, irritant gases, radiant heat flux.
**Rationale**: ISO 13571 §5–7 designates these three as the dominant
indicators for typical residential fires. Adding more channels increases
model complexity without proportional benefit. Documented in
`risk_indicators.md` as conservative simplification.

---

## D-006: Visibility uses inverse normalisation

**Date**: Week 2
**Decision**: `V_norm = 1 − clip(V/30, 0, 1)`. Higher value = more dangerous.
**Alternatives**: Direct normalisation, or treat visibility as separate
sign convention.
**Rationale**: Keeps all 3 model output channels with the same
"high = dangerous" semantics, simplifying loss functions and risk
score computation. Documented prominently in `interface_contracts.md`.

---

## D-007: ConvLSTM as baseline, PI-FNO as primary

**Date**: Week 1
**Decision**: Train ConvLSTM (3D extension) as baseline; PI-FNO as
primary model.
**Alternatives**: Use only PI-FNO (less work but no comparison baseline).
**Rationale**: A baseline is necessary to demonstrate "PI-FNO beats X"
in EXP-FIRE-001. ConvLSTM is a natural choice because it's the
prior-art deep-learning sequence-prediction architecture for grid data.

---

## D-008: FED constant 27000 (not Purser exponent)

**Date**: Week 4
**Decision**: Use simplified FED formula
`FED = (Δt_min/27000) · Σ CO_ppm` instead of Purser's
`FED = Σ ([CO]^1.036) · Δt / C_t`.
**Alternatives**: Full Purser formula with exponent.
**Rationale**: Simplification preserves the linear-time-integral
structure that allows efficient path-integrated FED computation.
The exponent matters most at very high concentrations, which we
already saturate via clipping. ISO 13571 §7.3 references the
27000 ppm·min reference dose.

---

## D-009: FED threshold 0.3 (sensitive population)

**Date**: Week 4
**Decision**: `FED_THRESHOLD = 0.3` for the danger criterion.
**Alternatives**: 1.0 (healthy adults).
**Rationale**: Real evacuations include elderly, children, people with
respiratory conditions. ISO 13571 §7.3 explicitly recommends 0.3 for
sensitive populations. NFPA 130 (transit) also uses 0.3.

---

## D-010: VECTOR=.TRUE. forbidden on SLCF

**Date**: Week 5 (after fdsreader bug)
**Decision**: All SLCF lines must NOT have `VECTOR=.TRUE.`.
**Alternatives**: Use `VECTOR=.TRUE.` for vector field outputs (wind, etc.)
**Rationale**: `VECTOR=.TRUE.` + `CELL_CENTERED=.TRUE.` causes
`fdsreader` to fail with array broadcast errors on slice loading.
This was discovered the hard way during initial data validation.
Logged separately in `lessons_learned.md`.

---

## D-011: Training data 30 scenarios, not 100+

**Date**: Project inception
**Decision**: 24 train / 3 val / 3 OOD = 30 total.
**Alternatives**: 100+ scenarios for stronger generalisation guarantees.
**Rationale**: At ~1 CPU-hour per scenario × 30 = 30 CPU-hours.
RunPod budget supports this comfortably. 100+ would consume budget
without proportional benefit at student-team timeline. Standard
practice in surrogate ML for CFD literature.

---

## D-012: HRR variation 4 levels, not continuous

**Date**: Week 4
**Decision**: HRR ∈ {500, 1000, 1500, 2000} kW.
**Alternatives**: Continuous HRR sampling.
**Rationale**: Discrete levels simplify scenario indexing and OOD
construction. The 4 levels span a factor of 4× in fire intensity,
which is enough to test if the model interpolates within and
extrapolates beyond.

---

## D-013: Single Crazyflie drone for PyBullet, not swarm

**Date**: Week 1
**Decision**: PyBullet integration uses 1 drone.
**Alternatives**: Multi-drone swarm.
**Rationale**: Swarm coordination is a separate research problem.
A single drone is sufficient to demonstrate end-to-end use of the
risk map for evacuation guidance.

---

## D-014: Replan period 30 s for dynamic planner

**Date**: Week 11 (proposed)
**Decision**: `DynamicPredictivePlanner` re-plans every 30 s.
**Alternatives**: Replan every step; replan never.
**Rationale**: Replan-every-step is computationally wasteful (PI-FNO
inference at 10 Hz adds up) and doesn't change the path much.
Replan never reduces dynamic planner to static planner. 30 s aligns
with 60 s prediction horizon (replan halfway through horizon).

---

## How to add a decision

When making a major scope or interface decision:

1. Write a new section here labeled `D-NNN`.
2. Date, Decision (one line), Alternatives, Rationale.
3. Keep concise — 3–5 sentences for rationale.
4. Update `CLAUDE.md` constraints if the decision changes them.
5. Commit with message `decisions: D-NNN - <one-line summary>`.
