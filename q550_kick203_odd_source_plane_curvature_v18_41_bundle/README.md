# Q550 v18.41 — Odd-Source Response Plane & Curvature Audit

## Scientific question

The **authentic** v18.40 Q550 data show a 54.4917-degree odd-source
response turn at phase-blind xi=3.5, branch 0, and a 61.6789-degree turn
at phase-blind xi=4.0, branch 0. Their sampled angular paths were equal
to their endpoint turns to rounding. Does the normalized direction occupy
only the 2-plane spanned by its first and last 9D vectors? Is the RAW odd
response almost a straight chord between the same two endpoints? These
are **different** geometric questions.

No result here claims intrinsic material torsion, a material metric, or
an invariant constraint surface. The material scaling, metric, support,
and normal-transport convention are exactly the DECLARED diagnostics of
v18.39/v18.40. Nominal kappa0 is NOT changed or re-estimated.

## Run on the original server

```bash
cd /root/elab1/hysteresis
unzip q550_kick203_odd_source_plane_curvature_v18_41_bundle.zip
cd q550_kick203_odd_source_plane_curvature_v18_41_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_41_server.log
```

Send back the file:

`/root/elab1/hysteresis/q550_kick203_odd_source_plane_curvature_v18_41_sendback.zip`

The complete earlier v18.40 ORIGINAL Q550 sendback, including authentic
v18.39 and older archive genealogy, is stored unmodified under `inputs/`.
The old Q550 ODE is **not** included as an invented replacement: its
SHA-pinned scripts remain external dependencies on the original server.
Unrecognized or changed upstream original inputs fail closed.

## Design

1. SHA-256 validate the exact v18.40 server sendback ZIP and all its 121
   manifest members, verify `ORIGINAL_Q550_GAUGE_ROBUST_SOURCE_TEMPORAL_COMPLETED`,
   stage its nested original v18.39 ZIP, then recursively authenticate v18.39–
   v18.34 and both historical checkpoint tiers. Run `frozen_preflight_v18_41.py`
   without any new Q550 integrations.
2. Recreate exactly the 12 families and the 5 alpha perturbations per family
   (60 original Q550 trajectories plus one base integration). Preserve original
   seed stream, pinned RHS and Jacobian, kappa0, candidate surfaces, phase,
   DOP853 tolerances and support rules.
3. Replay v18.40 scalar, vector and 32-interval turning results with explicit
   tolerances. Stop immediately on discrepancies or on any loss of numerical
   diagnostic support.
4. On a uniform 129-point temporal grid over each case's **common accepted
   within-support** horizon, follow the odd response of the normalized
   transverse residual-gradient source in the common 9D tangent coordinates.
5. Construct the unique (except degenerate endpoints) **endpoint-only**
   two-plane from the normalized first and last response vectors. Measure
   orthogonal leakage for ALL intermediate samples. No intermediate data
   may be used to refit that plane.
6. Measure separately the deviation of the **raw unnormalized odd vector**
   from the straight affine interpolation of its two raw endpoints. A
   spherical direction may turn greatly while the raw vector moves almost
   along a segment; this possibility is tested directly.
7. Separately estimate raw Euclidean curvature and directional geodesic
   curvature on the unit 8-sphere. These use numerical second differences;
   first/last two samples are excluded and low-speed nodes are invalidated.
   They are diagnostics, not bounded curvature certificates.
8. Repeat plane, chord, angular-path and curvature statistics on nested
   grids 16, 32, 64 and 128; record grid sensitivity and the sign/amount
   of backtracking in the endpoint-plane coordinate.
9. Apply an arbitrary **time-dependent** SO(9) coordinate rotation and
   undo it explicitly; require the recovered physical 9D coordinates to
   agree before interpretation. No comparison of unaligned coordinate
   systems is described as gauge-invariant.

No interpolation of a phase-space "return" is used. No rerun of 400
original orbit periods is required by these local dense-solution checks.

## Expected ORIGINAL-only results

- `results/original_v18_41_proof.json` — 61 original Q550 integrations,
  parent authenticated, replay discrepancies and method semantics.
- `results/original_v18_41_plane_profiles.csv` — 12 x 129 temporal samples;
  plane departure, affine-chord residual, direction turn, curvature.
- `results/original_v18_41_family_summary.csv` — 12 endpoint-plane and
  convergence summaries.
- `results/original_v18_41_curvature_resolution.csv` — 12 x 4 nested
  grids, including geodesic and raw curvature diagnostics.
- Three PNG plots generated from the original CSV, plus the replayed
  v18.40 results, frozen preflight, all executable Python source,
  dependency declaration, SHA256 manifest and exact parent ZIP.

## Reproducibility and limitations

- `bash scripts/run_preflight_v18_41.sh` checks historical ancestry and
  runs **15 independent synthetic geometry/transport regression tests**.
  Preflight does not run the original Q550 ODE, produce scientific results,
  or permit a sendback to be packed.
- `python3 scripts/pack_sendback_v18_41.py` refuses to pack without actual
  v18.41 ORIGINAL Q550 proof and all required output counts.
- Support exit is a numerically scanned diagnostic boundary (with right
  censoring), not a rigorous interval-arithmetic enclosure.
- The numerical curvature of tiny source-response vectors may be sensitive
  to temporal resolution and derivative noise. Do not interpret small
  curvature coefficients as a physical law without grid stability.
- Endpoint-plane occupancy does **not** imply an invariant 2D subspace
  of the 10D material dynamics, nor does an affine 9D source response
  imply physical straight-line motion.

All source-code comments and technical documentation are in English.
