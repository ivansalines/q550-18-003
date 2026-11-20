# Q550 v18.38 — Coupled Level–Normal Transport & Local Scaling Audit

## Research question

Do normalized signed level transport and oriented normal tilt show reproducible *joint* local response to symmetric perturbations of the same frozen diagnostic surface? A nonzero correlation is not sufficient. Test transfer from small perturbations to held-out larger ones, across postures and surface candidates.

## Frozen scope / provenance

- The original physical-model parameter `kappa0` is **unchanged** from v18.37 (the server's SHA-pinned Q550 ODE). The newly proposed geometric expression for `kappa0` is **not substituted** into this audit and is not a certified law.
- `inputs/v18_37_original_server_sendback.zip` is the authentic parent, SHA256-pinned in `ENVIRONMENT.json`; the loader verifies **each member** and stages nested original v18.36 and earlier checkpoints under `.runtime`.
- The two diagnostic surfaces are the previously selected phase-dependent and phase-blind quadratic candidates with `mu=-1`. Neither is a certified physical material constraint.
- All distances, signed normals, gradients, tangent directions, and angles use explicitly declared *normalized material coordinates*. There is no privileged material metric.

## Protocol

1. Reconstruct and SHA-validate original parent and exact prior baseline seeds; reject mismatch before doing new integrations.
2. For each surface, three anchors (xi=3.5, 4.0, 4.5), and two seed branches, compute an initial tangent to the frozen candidate and move symmetrically along it with five multipliers `[-1,-1/3,0,+1/3,+1]` (60 new Q550 local trajectories). Reproject **each** candidate onto the *same* `C=0`; check material radius and phase support before integrating. Generate the reference base trajectory once (61 total integrations).
3. Integrate each trajectory with the original SHA-pinned ODE and the cotangent/defect variation system. Resolve the individual support exit with dense interpolation.
4. For each five-seed family, evaluate sources at time zero and at **half the earliest support-exit time**, so every comparison stays inside the diagnostic support.
5. Measure signed normalized scalar rate `r/||g||`, signed normal-rate component along the predeclared tangent, accumulated level normal offset, and stable signed tilt against homogeneous cotangent transport.
6. Fit the response only to `[-1/3,0,+1/3]`; test transfer to held-out `[-1,+1]`. The fitted direction, scale and sign are **not** chosen using the holdout futures.
7. Record both gains and failures. Reconstruct level and vector budgets and refuse packaging if the original Q550 experiment was not completed.

## Command on the original server

```bash
cd /root/elab1/hysteresis
unzip q550_kick203_coupled_level_normal_scaling_v18_38_bundle.zip
cd q550_kick203_coupled_level_normal_scaling_v18_38_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_38_server.log
```

Return:
`/root/elab1/hysteresis/q550_kick203_coupled_level_normal_scaling_v18_38_sendback.zip`

Offline authenticity + synthetic math preflight only:
`bash scripts/run_preflight.sh`

## Important limitations

- There is no original Q550 ODE available in this construction environment. **No new original v18.38 nonlinear result is claimed by the preflight.** The server must perform all new original solves.
- The surfaces are selected diagnostic fits and may fail actual invariance. The transported homogeneous normal is a reference construction, not a physical material surface.
- A scalar level offset and angular tilt use different normalization and response scales; do **not** merge them into a metric-invariant scalar without further justification.
- `kappa0` is held fixed. A separate, later parameter-rebuild study is required to assess the newly proposed geometric form; archived orbits cannot be silently reused with a changed parameter.
- Avoid claiming causality from correlation between `r` and `grad(r)`; the joint algebraic dependence is known. The transfer error and posture robustness are the only additional empirical diagnostics.

## Genealogy / files

`scripts/` contains all original derived audit source (new and inherited functional reconstruction); `inputs/` pins the full original parent ZIP; `tests/` has independent synthetic mathematics and negative controls; `results/` is separated into preflight and original server outputs; `SHA256SUMS_OUTPUT.json` is the manifest; `ENVIRONMENT.json` pins source hashes and original version. Python dependencies are in `requirements.txt`.
