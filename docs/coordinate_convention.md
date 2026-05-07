# Coordinate Convention

> **Single source of truth** for all spatial coordinates used in the project.
> Consult this document before writing any geometry or tensor indexing code.

---

## Two Grids — Critical Distinction

This project uses **two different grids** that must not be confused.

### Grid 1: FDS MESH (computational domain)

What FDS simulates internally. Includes external buffer for ventilation
boundary conditions.

| Property | Value |
|----------|-------|
| Cells | **100 × 80 × 8** |
| Extent | **[−10, 40] × [−10, 30] × [0, 4] m** |
| Resolution | 0.5 m × 0.5 m × 0.5 m |
| Buffer | 10 m on −X, +X, −Y, +Y |

We do **not** train on this grid. It exists so FDS has clean boundaries.

### Grid 2: SLCF Region (model-visible)

What `&SLCF` extracts. This is the actual learnable region.

| Property | Value |
|----------|-------|
| Cells | **60 × 40 × 6** |
| Extent | **[0, 30] × [0, 20] × [0, 3] m** |
| Resolution | 0.5 m × 0.5 m × 0.5 m (cell-centered) |
| Cell shape | `(nx, ny, nz)` |

**Models always operate on the SLCF region, never the MESH.**

---

## World Space Conventions (SLCF region)

| Property | Value |
|----------|-------|
| Units | **Metres** (SI). Never millimetres or feet. |
| Origin | Building corner **(0, 0, 0)** at the floor |
| X axis | Along the 30 m building length |
| Y axis | Along the 20 m building width |
| Z axis | Vertical (Z-up convention) |
| Range | X ∈ [0, 30], Y ∈ [0, 20], Z ∈ [0, 3] |

Any point outside this range is **out-of-bounds** and treated as
maximum danger by `RiskMap.query()`.

---

## Cell-Centered Indexing

The SLCF data is **cell-centered**, not corner-aligned. This matters for
coordinate conversion.

For grid index `(ix, iy, iz)`:

```
x_centre = ix × 0.5 + 0.25     for ix in [0, 60)   → [0.25, 0.75, ..., 29.75]
y_centre = iy × 0.5 + 0.25     for iy in [0, 40)   → [0.25, 0.75, ..., 19.75]
z_centre = iz × 0.5 + 0.25     for iz in [0,  6)   → [0.25, 0.75, ...,  2.75]
```

World-to-grid conversion:

```python
ix = int((world_x - 0.25) / 0.5)   # cell that "owns" this point
iy = int((world_y - 0.25) / 0.5)
iz = int((world_z - 0.25) / 0.5)
```

For **continuous queries** (drone position → risk lookup), use
`scipy.interpolate.RegularGridInterpolator` with `method='linear'`,
not nearest-neighbour. This gives smooth gradients along drone trajectories.

---

## Tensor Layout

Model tensors follow PyTorch convention with batch first:

```
Input  tensor: (B, 5, 60, 40, 6)
Output tensor: (B, 3, 60, 40, 6)
```

**Axis order**: `[batch, channel, X, Y, Z]`

The spatial axes **directly correspond** to world axes:
- Tensor dimension 2 (size 60) ↔ X axis (0 → 30 m)
- Tensor dimension 3 (size 40) ↔ Y axis (0 → 20 m)
- Tensor dimension 4 (size  6) ↔ Z axis (0 → 3 m)

Cell access:
```python
field_tensor[batch, channel, ix, iy, iz]
```

---

## fdsreader Integration Pattern (CRITICAL)

This is the standard pattern. Copy verbatim into any module that
loads FDS data.

```python
import fdsreader
from pathlib import Path

sim = fdsreader.Simulation(str(Path(fds_dir)))

# Filter to the slices we want
temp_slc = sim.slices.filter_by_quantity("TEMPERATURE")[0]
vis_slc  = sim.slices.filter_by_quantity("SOOT VISIBILITY")[0]
co_slc   = sim.slices.filter_by_quantity("CARBON MONOXIDE VOLUME FRACTION")[0]

# Returns (T, nx, ny, nz) array AND coordinate dict in world metres.
grid, coords = temp_slc.to_global(return_coordinates=True)

# coords['x'] = [0.25, 0.75, ..., 29.75]   ← cell centres in world metres
# Because origin is aligned, these ARE the world coordinates.
# No transformation, no scaling, no axis swap.
```

### Pre-conditions for this pattern to work

1. SLCF `XB` matches the learnable region: `0,30, 0,20, 0,3`
2. `CELL_CENTERED=.TRUE.` is set on the SLCF
3. `VECTOR=.TRUE.` is **NOT** set (causes fdsreader broadcast bug)

If any of these fail, `to_global()` will raise an error or produce
garbage. See `docs/lessons_learned.md` for the actual bug encountered.

### Time axis handling

```python
# slc.times has the actual FDS output times — may not be exactly
# 0, 10, 20, ..., 300 due to floating-point.

target_times = np.arange(0, 301, 10)  # 31 frames
indices = np.searchsorted(temp_slc.times, target_times)
indices = np.clip(indices, 0, len(temp_slc.times) - 1)
grid_aligned = grid[indices]   # shape (31, 60, 40, 6)
```

---

## FDS ↔ PyBullet Alignment

FDS and PyBullet both use right-handed, Z-up, metre-based coordinates.

**No transformation is needed** between them, provided:
- FDS `&MESH` origin matches PyBullet URDF origin (both at world (0, 0, 0))
- PyBullet building URDF places the building corner at (0, 0, 0)

Verification (Week 12):

```python
# Drone position from PyBullet, in world metres directly:
drone_pos, _ = pybullet.getBasePositionAndOrientation(drone_id)

# Risk lookup uses the same coordinates:
danger = risk_map.query(np.array(drone_pos), t=current_sim_time)
```

If `risk_map.query()` returns 1.0 for clearly-inside-building drone
positions, the coordinate alignment is broken. Debug in this order:

1. Is `coords['x'][0]` returned by fdsreader equal to `0.25`?
2. Is the SLCF `XB` set to `0,30, 0,20, 0,3`?
3. Is the URDF building corner at world (0, 0, 0)?
4. Is the drone position in metres (not millimetres or feet)?
5. Is `risk_map`'s `bounds_error=False, fill_value=1.0` set in the
   underlying interpolator?

---

## Common Mistakes — Hall of Shame

| Mistake | Correct approach |
|---------|-----------------|
| Using millimetres anywhere | Always metres |
| 0.2 m grid (150 × 100 × 15) | Always 0.5 m (60 × 40 × 6) |
| `(B, C, Z, Y, X)` axis order | Always `(B, C, X, Y, Z)` |
| Origin at building centre | Origin at corner (0, 0, 0) |
| `os.path.join` for paths | `pathlib.Path` |
| `cell_corner = ix * 0.5` | `cell_centre = ix * 0.5 + 0.25` |
| Using MESH grid (100×80×8) | Use SLCF region (60×40×6) |
| `VECTOR=.TRUE.` on SLCF | Omit; causes fdsreader bug |
| Transposing FDS output axes | Already in (T, X, Y, Z) order |

---

## Code Reference

```python
# All conversion functions live here:
from src.shared.coordinates import (
    world_to_grid,
    grid_to_world,
    is_in_bounds,
    cell_centres,
)

# Constants (never hard-code these):
from src.shared.constants import (
    GRID_SHAPE,         # = (60, 40, 6)
    DOMAIN_SIZE_M,      # = (30.0, 20.0, 3.0)
    CELL_SIZE_M,        # = 0.5
    MESH_SHAPE,         # = (100, 80, 8)   ← FDS computational
    MESH_EXTENT_M,      # = ((-10, 40), (-10, 30), (0, 4))
)
```

If you need values not in the list above, propose adding them to
`constants.py` rather than inlining them.
