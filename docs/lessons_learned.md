# Lessons Learned

> Concrete bugs, gotchas, and surprises encountered during the project.
> Each entry documents the symptom, root cause, and fix to prevent
> repeat occurrences.

---

## L-001: fdsreader broadcast error on `VECTOR=.TRUE.` slices

**Symptom**:

```
ValueError: could not broadcast input array from shape (61,41,8)
into shape (61,41,7)
```

When calling `slc.to_global(return_coordinates=True)` on a SLCF that
was generated with both `VECTOR=.TRUE.` and `CELL_CENTERED=.TRUE.`.

**Root cause**:

`fdsreader` cannot correctly compute the cell-centered slice dimensions
when `VECTOR=.TRUE.` is set on the FDS SLCF. There appears to be an
off-by-one or stride mismatch internally. This is a known limitation
of the `fdsreader` library and not a bug in our code.

**Fix**:

Always omit `VECTOR=.TRUE.` from SLCF lines used by ML pipeline.
We only need scalar fields (T, V, CO), not vector fields like velocity.

```fortran
# DO NOT USE:
&SLCF QUANTITY='TEMPERATURE',
      VECTOR=.TRUE.,            ! <-- this line breaks fdsreader
      CELL_CENTERED=.TRUE.,
      ID='Temperature', XB=...

# USE:
&SLCF QUANTITY='TEMPERATURE',
      CELL_CENTERED=.TRUE.,
      ID='Temperature',
      XB=0.0,30.0, 0.0,20.0, 0.0,3.0/
```

**Status**: Fixed. Documented in `CLAUDE.md` and `coordinate_convention.md`.

---

## L-002: FDS MESH must be larger than SLCF region

**Symptom**:

When MESH `XB` was set to (0, 30, 0, 20, 0, 3), smoke and heat near the
end-exit doors behaved oddly — temperatures dropped sharply right at
the door, gradients looked wrong.

**Root cause**:

FDS treats MESH boundaries as walls unless explicitly told otherwise.
A door defined right at the MESH edge has nowhere for smoke to escape.

**Fix**:

Extend MESH 10 m beyond building footprint on each side:
- MESH XB: `[-10, 40] × [-10, 30] × [0, 4]`
- SLCF XB: `[0, 30] × [0, 20] × [0, 3]`  (building only)
- Models train on the SLCF region; the buffer is invisible to ML.

**Status**: Fixed. Documented in `CLAUDE.md` and `coordinate_convention.md`.

---

## L-003: Visibility direction is opposite of T and CO

**Symptom**:

Initial training run had loss decreasing for T and CO channels but
*increasing* for visibility. Later, peak danger error gave wrong
direction in the test set.

**Root cause**:

Raw visibility in metres: **higher value is safer** (you can see further).
Raw temperature: **higher value is more dangerous**.
If both are normalised the same way, the loss function is fighting itself.

**Fix**:

Normalise visibility with **inverse mapping**:

```python
V_norm = 1 - np.clip(V_metres / 30.0, 0, 1)
```

So high raw visibility (safe) maps to low normalised value (≈ 0.0),
matching the convention "high normalised = dangerous" used for T and CO.

**Status**: Fixed. Documented prominently in `CLAUDE.md`,
`coordinate_convention.md`, and `interface_contracts.md`.

---

## L-004: Cell-centered indexing offset by 0.25 m, not 0

**Symptom**:

Drone positions queried at world coordinate (0, 0, 0) returned `nan`
or 1.0 (out-of-bounds), even though that's the corner of the building.

**Root cause**:

Cell (0, 0, 0) of the SLCF grid has its **centre** at world (0.25, 0.25, 0.25),
not at (0, 0, 0). Any query at (0, 0, 0) is technically outside the
last-cell-bounds of the interpolator, so the `bounds_error=False`
fallback kicks in.

**Fix**:

When converting world → grid index, account for the cell-centered offset:

```python
# WRONG:
ix = int(world_x / 0.5)

# CORRECT:
ix = int((world_x - 0.25) / 0.5)
```

Use `scipy.interpolate.RegularGridInterpolator` constructed from
the actual cell centres returned by `fdsreader.to_global(return_coordinates=True)`,
which automatically handles the offset.

**Status**: Documented. Pattern enshrined in `coordinate_convention.md`.

---

## L-005: HDF5 mask should be float, not bool

**Symptom**:

When loading the building mask via `h5py`, broadcasting it into a
PyTorch tensor produced `dtype=torch.uint8` and silently ruined
gradient flow when used as input.

**Root cause**:

PyTorch tensors with `uint8` dtype cannot be cast to `float32` via
`.float()` if the source HDF5 dataset was stored as `bool`. The result
is technically valid but loses gradients.

**Fix**:

Save the mask as `np.float32` directly:

```python
mask = mask_array.astype(np.float32)  # 0.0 or 1.0
hf.create_dataset("mask", data=mask)
```

Then reading it produces `float32` tensors directly.

**Status**: Captured as a convention in `interface_contracts.md`.

---

## L-006: PyTorch DataLoader with num_workers > 0 needs `if __name__ == '__main__'`

**Symptom**:

On Windows or in some Linux configurations, training with
`DataLoader(num_workers=4)` resulted in:

```
RuntimeError: An attempt has been made to start a new process before
the current process has finished its bootstrapping phase.
```

**Root cause**:

DataLoader workers are spawned via `multiprocessing.spawn` on Windows.
Without `if __name__ == '__main__'`, the child process re-imports the
main script, recursively spawning workers.

**Fix**:

Always wrap training entry points:

```python
if __name__ == '__main__':
    train_main()
```

This is already required by our coding conventions, so it's
double-enforced.

**Status**: Fixed by convention, validated in `train_conv_lstm.py` template.

---

## L-007: `to_global()` time alignment is approximate

**Symptom**:

`temp_slc.times` returned values like `[0.0, 10.001, 19.998, 30.002, ...]`
rather than exactly `[0, 10, 20, 30, ...]`. Indexing by computed time
(e.g., `slc[15]` for t=150) returned the wrong frame in some cases.

**Root cause**:

FDS time stepping is adaptive (CFL-controlled). `DT_SLCF` controls
output frequency but actual output times can drift slightly.

**Fix**:

Use `np.searchsorted` to find the closest output index:

```python
target_times = np.arange(0, 301, 10)  # [0, 10, ..., 300]
indices = np.searchsorted(temp_slc.times, target_times)
indices = np.clip(indices, 0, len(temp_slc.times) - 1)
grid_aligned = grid[indices]  # shape (31, 60, 40, 6)
```

**Status**: Documented in `coordinate_convention.md` `to_global()` pattern.

---

## L-008: PyBullet drone collision with floor

**Symptom** (anticipated for Week 12):

Drone falls through the floor at simulation start.

**Likely root cause**:

The Crazyflie URDF has a small collision radius. PyBullet's default
contact margin is 0.001 m. If drone spawn height is < 0.001 m, it can
phase through the floor.

**Planned fix**:

Spawn drone at z = 0.5 m (above the floor by 0.5 m) and explicitly
set its mass to a small value. Use `setAdditionalSearchPath` to load
URDF correctly.

**Status**: Open. Will be addressed in Week 12 when integration begins.

---

## How to add a lesson

When you encounter and fix a bug worth remembering:

1. Add a new section labeled `L-NNN`.
2. Symptom (literal error or behaviour observed).
3. Root cause (why it happened).
4. Fix (the actual change that resolved it).
5. Status (Fixed / Open / Workaround).
6. Cross-reference docs that were updated.

Keep entries concise — 3–8 sentences each. Append-only.
