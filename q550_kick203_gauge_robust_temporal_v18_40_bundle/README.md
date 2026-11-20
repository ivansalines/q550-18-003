# Q550 v18.40 — Gauge-Robust Source Rotation & Temporal Resolution Audit

## Scientific question

The original v18.39 Q550 source response produced diagnostic full-vector turns of
54.49° and 61.68° for phase-blind surface cases while an earlier scalar projection
sometimes flipped without the full vector inverting. Here we measure **when** the
v18.39 odd residual-gradient response rotates within the authenticated diagnostic
support, whether a scalar projection is crossing zero, and the dependence of the
reported rotation on **declared** transport conventions.

**These are neither physical material torsion angles nor newly certified material
metrics or invariant constraints.** The nominal `kappa0` is unchanged. There is
no claim that the parent results represent a physical phase-space return.

## Original server use

```bash
cd /root/elab1/hysteresis
unzip q550_kick203_gauge_robust_temporal_v18_40_bundle.zip
cd q550_kick203_gauge_robust_temporal_v18_40_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_40_server.log
```

Upload `../q550_kick203_gauge_robust_temporal_v18_40_sendback.zip`.

The preflight can be run with `bash scripts/run_preflight_v18_40.sh`. It does
**not** run the original Q550 ODE, and cannot generate a valid v18.40 sendback.
The original Q550 ODE remains an authentic SHA-pinned external server dependency
(under the original /root/elab1/hysteresis history) and is not replaced with
synthetic physics. Missing source or changed hashes fail closed.

## Design and measurement

* SHA-authenticate all 115 original v18.39 output/source files in the exact parent
  server sendback ZIP, stage its authentic v18.38 parent, and recursively use all
  the established v18.34–39 checkpoint loaders. Copy the original v18.39 driver
  exactly into a new versioned driver and extend it; initial seeds, perturbation
  scaling, projection, `DOP853` tolerances, `kappa0`, and 1e-5 xi window are unchanged.
* Reintegrate the same **60 original Q550 seed trajectories plus one baseline**;
  verify all original v18.39 9D endpoint source vectors and scalar replay. The
  frozen v18.39 coordinates and original case indices are authoritative.
* Inspect 14 nonuniform fractions of the **common within-support** interval,
  including fine early fractions 1/128 and 1/64, plus 33 uniform odd-response
  times. Never conflate a right-censored trajectory with an observed exit.
* At each time map each perturbation's transverse source minimally to the common
  alpha=0 normal. Compare with the initial 9D frame using (a) direct
  normal-to-normal minimal rotation and (b) incremental minimal rotations on
  separately sampled 8/64 interval grids. The latter are different transport
  conventions and **not generally related by a mere common coordinate change**.
* Independently express the same vectors in instantaneous Householder charts
  and in an arbitrarily twisted `SO(9)` coordinate chart. **Undo** the explicit
  basis rotations before comparing directions and require numerical closure.
  Angles from unaligned coordinates must NOT be interpreted as physical flips.
* Record full odd-source turn vs time, amplitude gain, projected scalar sign,
  level-source association, observer crossing *brackets* (not invented exact
  crossings), and nested temporal total angular travels on 4/8/16/32 intervals.
* Test failure scenarios in deterministic synthetic **math-only** cases;
  no synthetic result is labeled `ORIGINAL_Q550_*`.

## Important semantics

The 9D tangent basis is defined by the normalized material coordinates inherited
from v18.39. No privileged physical metric or torsion connection has been
established. Direct and incremental transports may disagree because they make
different comparisons between tangent planes. Coordinate rotations on the same
tangent plane must agree exactly after alignment. The first-exit search remains
numerical, not a rigorous interval-arithmetic support guarantee.

## Outputs

- `results/original_v18_40_proof.json` — server-only proof and genealogy.
- `results/original_v18_40_temporal_sources.csv` — 12 x 14 time samples.
- `results/original_v18_40_gauge_comparison.csv` — transport convention and coordinate closure.
- `results/original_v18_40_family_summary.csv` — endpoint replication and projected crossings.
- `results/original_v18_40_resolution.csv` — 4,8,16,32 time-grid total angular paths.
- Three figures, reproducible generator code, tests, English README,
  `ENVIRONMENT.json` and a SHA256 manifest.

All comments and documentation are in English. Original code dependency hashes
remain anchored to the historical server. The user-visible scientific results
must be drawn only after the new original Q550 server sendback is received.
