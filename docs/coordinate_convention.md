# Coordinate Convention

> **Single source of truth** for all spatial coordinates used in the project.
> Consult this document before writing any geometry or tensor indexing code.

---

## Coordinate Systems

The project uses two coordinate systems that must always stay in sync.

### 1. World Space (metres)

| Property | Value |
|----------|-------|
| Units | **Metres** (SI). Never millimetres. |
| Origin | Building corner **(0, 0, 0)** |
| X axis | Points along the 30 m building length (East) |
| Y axis | Points along the 20 m building width (North) |
| Z axis | Points upward (vertical, Z-up convention) |
| Extent | X ∈ [0, 30], Y ∈ [0, 20], Z ∈ [0, 3] |

Any point outside this extent is **out-of-bounds** and treated as
maximum danger (see `RiskMap.query`).

### 2. Grid Space (integer cell indices)

| Property | Value |
|----------|-------|
| Shape | **(60, 40, 6)** — (nx, ny, nz) |
| Cell size | **0.5 m × 0.5 m × 0.5 m** |
| Index origin | Cell (0, 0, 0) has its corner at world (0, 0, 0) |
| Index range | ix ∈ [0, 59], iy ∈ [0, 39], iz ∈ [0, 5] |

Cell centre of (ix, iy, iz):

```
x_centre = (ix + 0.5) × 0.5
y_centre = (iy + 0.5) × 0.5
z_centre = (iz + 0.5) × 0.5
```

World-to-grid conversion (floor division):

```
ix = floor(x / 0.5)
iy = floor(y / 0.5)
iz = floor(z / 0.5)
```

---

## Tensor Layout

Model tensors follow PyTorch convention with the batch dimension first:

```
Input  tensor: (B, 5, 60, 40, 6)
Output tensor: (B, 3, 60, 40, 6)
```

**Axis order**: `[batch, channel, X, Y, Z]`

The spatial axes **directly correspond** to world axes:
- Tensor dimension 2 (size 60) ↔ X axis (0 → 30 m)
- Tensor dimension 3 (size 40) ↔ Y axis (0 → 20 m)
- Tensor dimension 4 (size  6) ↔ Z axis (0 → 3 m)

Accessing a specific cell with NumPy/PyTorch:

```python
field_tensor[batch, channel, ix, iy, iz]
```

---

## FDS ↔ Project Alignment

FDS uses the same Z-up, metres convention. When extracting slice data:

1. Confirm FDS `&MESH` extents match (0, 30, 0, 20, 0, 3).
2. FDS slice dimensions should be 60 × 40 × 6 after extraction.
3. Do **not** transpose axes — the FDS (X, Y, Z) order is the same as
   the project tensor order.

---

## PyBullet Alignment (Week 12)

PyBullet uses a right-handed coordinate system with Z-up by default.
To align:

- Building floor is at Z = 0 in both systems.
- Scale factor: 1.0 (both use metres).
- No rotation required — axes are identical.
- PyBullet body origin at world (0, 0, 0) = building corner.

---

## Common Mistakes

| Mistake | Correct approach |
|---------|-----------------|
| Using millimetres | Always use metres |
| 0.2 m resolution (150 × 100 × 15) | Always use 0.5 m (60 × 40 × 6) |
| (B, C, Z, Y, X) axis order | Always (B, C, X, Y, Z) |
| Origin at building centre | Origin at corner (0, 0, 0) |
| `os.path.join` for paths | `pathlib.Path` |

---

## Code Reference

```python
# All conversion functions live here:
from src.shared.coordinates import world_to_grid, grid_to_world, is_in_bounds

# Constants (never hard-code these):
from src.shared.constants import GRID_SHAPE, DOMAIN_SIZE_M, CELL_SIZE_M
# GRID_SHAPE   = (60, 40, 6)
# DOMAIN_SIZE_M = (30.0, 20.0, 3.0)
# CELL_SIZE_M  = 0.5
```
