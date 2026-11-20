# v18.39 — Full Tangent-Plane Source Rotation & Coupled Transport Audit

## Scientific question

The original v18.38 showed poor or posture-dependent held-out prediction by a
**single signed tangent observer**. Is its failure caused by genuine changes in
the complete normalized material transverse residual source, or by source
rotation outside that observer's one-dimensional projection?

This version transports and compares the complete **10D material transverse
source**, expressed with a common orthonormal **9D diagnostic tangent frame**.
It measures both the instantaneous source and the small actual transported
normal-tilt vector. Separately records the signed scalar observer from v18.38.

## Original Q550 experiment

- Original ODE/solver is SHA256-pinned in ancestral v18.31 code on the server.
- No change to original kappa0. The proposed geometric alternative is **not**
  silently introduced into this experiment.
- 2 frozen diagnostic candidate surfaces, 3 xi anchors (3.5, 4, 4.5), 2
  deterministic independent baseline seeds = 12 families.
- 5 on-surface symmetric amplitudes each: -1,-1/3,0,+1/3,+1 = 60
  true original Q550 integrations, plus authentic base orbit reference.
- Same normalized coordinate metric, initial seeds, ODE, phase, support
  radius, right-censored exit handling, original integrator and tolerances as
  the previous version. Common observation time is half the earliest supported
  horizon (or half the observation window if all right censored).
- Verify the complete v18.38 **authentic 108-file SHA256 manifest**, entire
  original archive including hotfixes, and its nested ancestral checkpoints.
- Fail closed if scalar replay differs from v18.38, support exit class changes,
  source projection identity fails, or common frame fails norm preservation.

## Measured vectors, normalized material gauge

Set `g = grad_z C`, `r=L_F C - mu C`, `gr=grad_z r` and
`P_g=I - gh gh^T`, `gh=g/||g||`. The full instantaneous angular source is
`omega = P_g gr / ||g||` (ten components, tangent to g).

The transported normal direction is compared to the actual grad(C) with a
stable atan2 **tangent angle vector**, not arccos. For each family construct a
frozen deterministic 9D Householder basis at the alpha=0 initial normal;
transport it to the alpha=0 common-time normal by the **minimum Euclidean
rotation**. At either moment, each perturbed sample's own tangent source is
minimally rotated into that baseline tangent frame. This yields comparable
9D coefficients with no loss of the vector norm under the declared gauge.

**Crucial caveat:** Minimum Euclidean frame transport is a chosen observer,
not the mechanical/material connection, and this does not prove intrinsic
normal torsion, a physical material metric, or invariant constraint.

## Tests and interpretation

Fit the odd response from +/-1/3, hold out +/-1. The complete 9D vector
predictive error is compared to the v18.38 single-direction signed source
error. Report inner-to-outer odd-vector gain, odd-vector turn, even curvature,
source norm and fraction captured by the old scalar observer, and the full
vector association with scalar level source. Compare the within-support
initial-to-common 9D odd-vector rotation against sign flips in the old
observer. A scalar sign flip accompanying full-vector alignment is **not**
proof of material torsion; it can be an observer-projection effect.

Zero or near-zero odd vectors have **undefined** turning direction, not zero
rotation. Five points per case limit statistical confidence and no universal
constitutive law is inferred from correlations.

## Server

```bash
cd /root/elab1/hysteresis
unzip q550_kick203_full_tangent_source_rotation_v18_39_bundle.zip
cd q550_kick203_full_tangent_source_rotation_v18_39_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_39_server.log
```

This writes alongside the bundle directory:
`q550_kick203_full_tangent_source_rotation_v18_39_sendback.zip`

Do not run the server script on a machine missing the original SHA256-pinned
ODE. `bash scripts/run_preflight.sh` checks archival lineage and synthetic
math identities only. `scripts/pack_sendback_v18_39.py` cannot pack preflight
in place of an original server result.

## Reproducible genealogy

`inputs/v18_38_original_server_sendback.zip` is the original immutable server
sendback including executed v18.38.1/v18.38.2 hotfixes, code, results,
manifest and original nested ancestors. This bundle includes all scripts
necessary to perform this new run plus the full script ancestry. Runtime
`.runtime/` stages authenticated nested parent inputs and is excluded from
sendback. SHA256SUMS_OUTPUT.json covers inputs, code, README, results and
figures. Python preferred 3.13, NumPy, SciPy, Matplotlib.

All documentation and source comments are in English. Scientific calibration
is local and diagnostic, not a claimed physical law or certified constraint.
