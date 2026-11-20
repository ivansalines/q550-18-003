# Q550 v18.42 — Second-Derivative Noise Floor & Time-Window Scaling Audit

## Question and motivation

Authentic v18.41 found 12 nearly planar, nearly affine odd residual-gradient
responses over extremely short within-support windows, while central second-
difference estimates of curvature became unstable as the mesh was refined.
This experiment separates the **geometric chord signal** from the **numerical
second-derivative estimator**. It does not certify intrinsic material torsion.

The diagnostic vector remains the original phase-(in)dependent cofactor
candidate's **odd full 9D transverse residual-gradient response** in the
same DECLARED normalized Euclidean material metric and minimal moving frame
used in v18.39–v18.41. **Original kappa0 is unchanged**. No material
constraint, invariant surface or material gauge is newly certified.

## Server execution

```bash
cd /root/elab1/hysteresis
unzip q550_kick203_second_derivative_noise_window_v18_42_bundle.zip
cd q550_kick203_second_derivative_noise_window_v18_42_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_42_server.log
```

Send back:
`/root/elab1/hysteresis/q550_kick203_second_derivative_noise_window_v18_42_sendback.zip`

The historical Q550 ODE scripts are **SHA-pinned external dependencies** on
the original server; no substitute ODE is embedded or used for original
scientific claims. The exact v18.41 ORIGINAL sendback and its complete older
ancestry are included under `inputs/`.

## Executable audit

1. Verify SHA256 of the exact v18.41 original server archive, CRC-check the
   ZIP, validate 137 individual manifest members, confirm its original
   integration proof, stage nested v18.40 archive and validate all earlier
   checkpoint tiers `standard` and `tight`.
2. Reconstruct the same base orbit anchors at xi 3.5, 4.0 and 4.5, both
   candidate surfaces and both branches. Reuse the authenticated deterministic
   seed stream and identical DOP853, pinned ODE, support criteria and normal
   transport, including the v18.36–v18.38 hotfix genealogy.
3. Run the original **61 Q550 integrations**, replay the v18.38–v18.41
   baseline outputs, and fail closed if v18.41's endpoint angles or
   endpoint-defined plane/chord statistics change unexpectedly.
4. On the accepted common within-support time horizon `Tcase`, evaluate 129
   source vectors `v(s)` at uniform `s=t/Tcase`. Compute chord departures,
   endpoint turn and endpoint-plane departure in FOUR NESTED windows
   `s∈[0, 1], [0, 1/2], [0,1/4], [0,1/8]`. Keep a FIXED reference scale
   for all four windows, and fit an explicit `error ∝ window^p` diagnostic.
   Under a smooth *resolved* nonzero `v''`, one would expect chord error
   scaling close to `window^2`, but small noise may dominate.
5. At each window midpoint, compare **three-point second difference**,
   **five-point second difference**, and **quartic seven-point least-squares**
   acceleration with three step sizes (`window/8`, `/16`, `/32`) in the
   *dimensionless variable* `s=t/Tcase`. Compare perpendicular acceleration
   to the local vector velocity as a Euclidean curve-curvature diagnostic.
   ALL acceleration/curvature estimates are explicitly NON-certified.
6. Independently cross-check the **first derivative only** using a local
   symmetric Euler-jet shift along the ORIGINAL ODE RHS, compared with the
   dense-solution temporal derivative. This is NOT an analytical Hessian,
   analytical second variation, or proof of a true derivative of the
   residual-gradient vector.
7. For the two PREDECLARED high-angle cases (phase-blind, xi=3.5 and
   xi=4.0, branch 0), rerun the original ODE for the exact same baseline
   and ±1/3 seeds at 10x **coarser** and 10x **tighter** error tolerances,
   for **12 additional actual original integrations**. Compare the
   9D source responses, absolute chord signals and endpoint directions
   throughout the four windows; report an **empirical tolerance noise
   sensitivity**, not an interval or precision bound.
8. Package reports only after **73 actual original Q550 integrations**
   and exact expected output counts. `run_preflight_v18_42.sh` never
   integrates original Q550 or produces an original science proof.

## Expected outputs

- `results/original_v18_42_proof.json` — ORIGINAL-only proof, authenticated
  parent, 73 original solves, diagnostic limitations and replay checks.
- `results/original_v18_42_odd_vector_profiles.csv` — 1548 source samples,
  full 9D components and v18.41 replay geometry.
- `results/original_v18_42_window_scaling.csv` — 48 window results.
- `results/original_v18_42_second_derivative_stencils.csv` — 144 stencil
  comparisons, acceleration and curvature estimates.
- `results/original_v18_42_family_summary.csv` — 12 family reports and
  window-scaling slopes.
- `results/original_v18_42_tolerance_noise.csv` — 16 comparisons from
  additional ORIGINAL tolerance-ladder integrations.
- Three PNG plots for window scaling, stencil disagreement, and empirical
  solver tolerance floor.
- All source and historical scripts, reference modules, original parent ZIP,
  dependency declaration, SHA256 manifest and server log (if supplied).

## Interpretive limits

The dynamic support is a numerically scanned ball, NOT an interval enclosure.
The time interval is extraordinarily short (often ~1e-6 in xi), and the
residual-gradient candidate surface is NOT established as an invariant.
The 9D material metric and tangent frame are explicit conventions, not
physical invariants. Solver tolerance variation and finite-difference
stencil disagreement do not provide mathematically rigorous error bounds.
If the second derivative fails to converge, the conclusion must be
**curvature unresolved**, not 'torsion observed'.

All code comments and technical documentation are in English.
