# Q550 v18.37 — Residual-Gradient, Normal Tilt & Moving-Level Audit

**Status on distribution:** preflight verified; the new original Q550 integration has **not** been executed. Run on the authenticated Q550 server, then return the generated `*_sendback.zip`.

## Aim

Test the hypothesis that the same diagnostic surface can **both shift in scalar level** and **change the orientation of its normal**, with neither effect assumed to vanish. The candidate surfaces remain the two frozen degree-2 surfaces from v18.33, and **are not certified material constraints**.

The v18.36 audit used `arccos(|unit(m)·unit(g)|)`, which may quantize minute angles. This version uses a projective `atan2` principal angle between a transported cotangent and the current frozen candidate gradient; it also compares full vectors and estimates the finite-difference numerical sensitivity of the source gradient.

## Mathematical construction

Let `z = (x-center)/scale` be the ten-dimensional diagnostic material coordinate and let `theta` be the clock coordinate. `C(z,theta)` denotes a **fixed** candidate fitted in earlier work. Define

```
    mu = -1
    r = dC/dxi - mu*C
    g = grad_z C
    B = dF_z/dz
```

Because Q550 has material-independent clock rate `dtheta/dxi`, and `mu` is a scalar depending only on theta, differentiation yields the exact chain-rule identity

```
    dg/dxi = (-B.T + mu*I) @ g + grad_z r .
```

To distinguish the two mechanisms, propagate separately

```
    dm/dxi = -B.T @ m,                      m(0) = g(0)
    de/dxi = (-B.T + mu*I) @ e + grad_z r, e(0) = 0
    g_reconstructed(t) = exp(mu*t)*m(t) + e(t)
```

and verify the **vector** equality against `grad_z C(y(t))` along original Q550 trajectories. The scalar-level equation is checked independently:

```
    C(t) = exp(mu*t) * ( C(0) + integral_0^t exp(-mu*s)*r(s) ds )
```

Split the residual gradient into components parallel and perpendicular to the *instantaneous* gradient `g`:

```
    q = grad_z r
    q_parallel = dot(q, unit(g))
    q_perp = q - q_parallel*unit(g)
    local_source_tilt_rate = norm(q_perp) / norm(g)
```

Nonzero `r` and nonzero `q_perp` are **mathematically compatible**. Their coexistence is measured, not imposed. They do not by themselves certify a physical normal tilt or constitutive memory. To avoid calling mere scalar level motion a physical displacement, the quantity `defect/norm(g)` is explicitly labeled a *linearized diagnostic offset*.

## Independent checks and honesty boundaries

1. `grad_z r` is obtained algebraically from the frozen quadratic-and-phase candidate and the **original SHA-pinned Q550 Jacobian**.
2. It is independently checked at four instants per trajectory by differentiating the scalar residual `r` using the **original nonlinear RHS directly**, with five-point stencils of 1e-4 and 5e-5 **in normalized coordinates**.
3. The gradient vector is also checked by a nonhomogeneous cotangent transport. This is a *consistency identity*, not an independent experimental discovery.
4. The scalar level is checked by the original field residual integral.
5. We preserve both results **within initial support**, and separately record later samples **after support exit**. The tiny v18.36 angles were mostly at the resolution limit of `arccos`; new `atan2` angles must still be checked against numerical convergence.
6. We make no claim of a privileged material metric, invariant constraint manifold, phase return, or physical torsion. The two candidate surfaces were rejected as globally invariant in previous audits.

## Data & genealogy

`inputs/v18_36_original_server_sendback.zip` is the **original authenticated** v18.36 sendback, nested with the executable genealogy back to the original ODE checkpoints. On first read, its original v18.35 archive and deeper ancestors are staged inside `.runtime/`, which is intentionally excluded from SHA manifests. The original Q550 model source is loaded from the SHA-pinned server directory; no replacement ODE is packaged.

The script exactly regenerates the original twelve seeds from fixed RNG 1836 and checks their first source, initial level, accepted attempt count and local support-exit times against v18.36.

## Requirements

Python 3.13 preferred, numpy, scipy, matplotlib, pandas; original SHA-pinned Q550 ODE at the server path used by v18.36.

## Commands on the original Q550 server

```bash
cd /root/elab1/hysteresis
unzip q550_kick203_residual_gradient_normal_tilt_v18_37_bundle.zip
cd q550_kick203_residual_gradient_normal_tilt_v18_37_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_37_server.log
```

Expected sendback in `/root/elab1/hysteresis/`:
`q550_kick203_residual_gradient_normal_tilt_v18_37_sendback.zip`.

The server computes one original reference and twelve local independent diagnostics (`13` ODE integrations), 48 direct-RHS finite-difference checks, three plots, the proof JSON, and a fresh SHA256 manifest. It does not re-integrate 400 Q550 orbital periods.

### Preflight only

```bash
bash scripts/run_preflight.sh
```

This authenticates the original v18.36 ZIP and runs mathematical tests. It **does not** produce the original v18.37 physical/model result. The sendback packager fails closed if the new Q550 integration products are missing.

## Output files

- `original_v18_37_residual_gradient_profiles.csv`: time series of direct/transported candidate normals, gradient source split, scalar level, support flags, both vector and scalar budget errors, stable angles.
- `original_v18_37_case_summary.csv`: per-trajectory first exits, initial level and tilt sources, maxima inside support, final diagnostics.
- `original_v18_37_rhs_gradient_crosscheck.csv`: two-stencil independent checks against the original RHS at four instants per case.
- `original_v18_37_proof.json`: explicitly bounded proof claims and hashes.
- Three `original_v18_37_*.png` plots.
- All Python scripts, tests, references, input sendback, dependency list, README, and SHA256 manifest are included.
