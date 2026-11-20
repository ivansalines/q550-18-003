# Q550 — v18.43 Analytic Source-Jet & Precision Separation Audit

This bundle is self-contained for script genealogy, **except** the pinned original Q550 ODE implementation remains on the original server; its SHA is verified by the ancestral loader and the source state/checkpoints are retrieved through the authenticated nested sendback chain. An unmodified v18.42 original server sendback is embedded under `inputs/` and its SHA256 is checked. All historical scripts necessary to reconstruct the original analysis are included.

## Scope and scientific limits

The original v18.42 curvature five-point routine contained `ss=dd5@dd5` rather than `ss=d5@d5`; therefore its exported curvature columns were invalid. The authentic v18.42 parent is **not** rewritten. v18.43 uses a corrected independent curvature formula, and audits its convergence rather than asserting an intrinsic torsion.

For a polynomial phase candidate C(z,θ), with normalized material z, gradient g=∇_z C, Lie defect r=L_F C−μ C, projected source p=(I−nnᵀ)∇_z r/||g|| and n=g/||g||, v18.43 applies the chain rule to compute the first time derivative of p. The evolution includes the entire model Jacobian and phase derivatives, not two finite differences of the output samples.

**Important qualification:** \(\dot B\), the directional time derivative of the model Jacobian, uses a 5-point numerical derivative of the original Jacobian at off-orbit Euler displacements. The derivative of the chart is also numerically differentiated along analytically computed normal jets. Thus the first source jet is **semi-analytic, not an exact symbolic Hessian/second variation**. Its step-size stability is recorded for 3 different normalized steps. The second jet differentiates that first jet once; it is independently compared with the corrected 5-point second difference of dense original source data.

The normalized material metric and moving 9D frame are declared diagnostic conventions. The candidate surface is not an invariant material constraint. Phase is carried explicitly as state θ and its difference, not as a Q550 winding certificate. No kappa0 changes are made.

## Input/outputs and runtime

On original Linux host (`/root/elab1/hysteresis`):

```bash
unzip q550_kick203_source_jet_precision_v18_43_bundle.zip
cd q550_kick203_source_jet_precision_v18_43_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_43_server.log
```

Produces sibling `q550_kick203_source_jet_precision_v18_43_sendback.zip`. No 400-orbit regeneration. Fresh Q550 work: 1 original dense anchor replay + 36 independent local 11D material seed flows + 12 independent original anchor reference flows = **49 original integrations**. The 12 families use ±1/3 and 0 from unchanged v18.42 seeds, four parent within-support time windows, 5 flow-jet milestones per family, 3 directional Jacobian steps, and corrected second derivative comparisons at 8,16,32 subdivisions (144 rows).

Main results:
- `original_v18_43_source_first_jets.csv` (60)
- `original_v18_43_second_jet_windows.csv` (144)
- `original_v18_43_directional_step_stability.csv` (120)
- `original_v18_43_family_summary.csv` (12)
- - `original_v18_43_solver_step_diagnostics.csv` (48; DOP853 adaptive step sizes and evaluations, diagnostic only)
- Original proof and two plots; frozen parent archive, all scripts/tests and SHA256 manifest.

### Preflight only

`bash scripts/run_preflight_v18_43.sh` authenticates the original v18.42 and its older nested original checkpoints without any original Q550 integrations. `scripts/pack_sendback_v18_43.py` **must fail** after preflight alone.

Requires `numpy`, `scipy`, `matplotlib`, Python 3.10+ (Python 3.13 preferred). All documents and script comments in English. No claims about an exact material metric, physical torsion, phase winding, or certified invariant surface.
