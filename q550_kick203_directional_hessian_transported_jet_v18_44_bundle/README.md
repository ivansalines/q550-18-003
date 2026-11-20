# Q550 — v18.44: Directional Hessian & Transported Source-Jet Audit

**Status before execution on original Q550 server:** `PREFLIGHT ONLY`. This archive contains **no** new original v18.44 Q550 result. **Synthetic test count: 13**, and only those have been executed locally. The original v18.43 scientific server sendback is preserved in `inputs/v18_43_original_server_sendback.zip` and authenticated by SHA256 down to all 147 manifested parent members. The historical Python genealogy and original input checkpoints are retained in the nested sendback chain. Previous scripts are retained unmodified as functional executable ancestry, except the v18.44 run script, which replaces the inherited current runner. The original Q550 model is still loaded from SHA256-pinned Python dependencies on the server.

## Aim

The v18.42/42.1 scalar curvature calculation exposed a specific source-code bug in the curvature denominator, and v18.43 showed a reproducible first source jet but an unstable numerical second jet. This audit **does not claim an exact symbolic Hessian or certify material curvature**. It separates:

1. The contracted directional Hessian `[(L_F B)^T g]` constructed from a five-point directional difference of the **pinned analytic Jacobian** `DF`, compared with the same contraction formed using two independent four-point first-difference operators on the **original RHS** `F` in normalized 11D coordinates. The RHS mixed derivative is fourth-order in each displacement, but still numerical. Report three RHS displacements (`0.006`, `0.018`, `0.036`) and three Jacobian-direction targets (`0.0005`, `0.002`, `0.008`). Agreement is *numerical cross-validation*, not physics independence.
2. The exact chain-rule source-jet formula for the **candidate diagnostic surface** `C` given the contracted Hessian source, including the tangent projector derivative and the dependence on the original unwrapped phase.
3. The **analytic Fréchet differential** of the declared minimal-rotation chart, isolating (a) source derivative, (b) own-normal alignment change and (c) base/reference transport. This replaces the v18.43 *finite normal-chart derivative* and is checked against it.
4. Reproduction of the **original v18.43** 9D source and semi-analytic jet on matched, authenticated cases. No phase-modulo return is interpreted as a material recurrence.

### Identities

Writing `z_i=(y_i-center_i)/scale_i`, `F_z=F_material/scale`, `B=D_z F_z`, `g=grad_z C`, and `w=(F_z, F_theta)`:

`[(L_F B)^T g]_j = D^2_z [g · F_z](w,e_j)` with `g` held constant in the right-hand contraction. The Jacobian construction differentiates `B` in the full normalized 11D direction; the mixed-RHS construction differentiates the scalar weighted original field. The two share the original model but not the numerical derivative calculation.

The full first-jet formula follows the frozen v18.43 polynomial/phase candidate differentiation and substitutes each independently computed Hessian contraction into `grad_z r dot` before projecting the source into the moving material tangent 9D chart.

**No physical metric, material constraint, source invariance, symbolic Hessian or second derivative accuracy is certified.** Derivative probes may leave the candidate `C=0` level, as required to probe an ambient derivative. This does not make those probes new physical trajectories. All 36 temporal observations are on original trajectories within the authenticated local support, with the original seed and parent time horizon.

## Run on the SHA-pinned original server

```bash
cd /root/elab1/hysteresis
unzip q550_kick203_directional_hessian_transported_jet_v18_44_bundle.zip
cd q550_kick203_directional_hessian_transported_jet_v18_44_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_44_server.log
```

Preferred Python: `python3.13`; fallback `python3`. Requires `numpy`, `scipy`, `matplotlib`. Optional explicit `--base-root` points to the same authenticated original Q550 model scripts as v18.43; the default is provided by its pinned historical wrapper. Original default solver: DOP853, `rtol=3e-12`, `atol=3e-13`, `max_step=2.5e-7`.

The script reconstructs 49 original integrations (one anchor collection, 36 local trajectories, 12 phase-matched references). For 12 diagnostic families, three times `s ∈ {0.125,0.5,1}` and three material amplitudes `±1/3,0`, it audits 324 original independent Hessian contraction comparisons and 36 transported 9D source-jet comparisons, with 48 original solver-step records. All are *source candidates*, not certified invariant manifolds.

Output, if and only if the original run is successful:

- `results/original_v18_44_hessian_dual_contractions.csv` — 324 records, complete 10D contracted vectors for both pathways and all probe choices.
- `results/original_v18_44_transported_source_jets.csv` — 36 records, 9D source and two jets, source/own-normal/reference-frame transport, old v18.43 cross-checks.
- `results/original_v18_44_family_summary.csv` — 12 families, comparison summaries.
- `results/original_v18_44_solver_diagnostics.csv` — 48 phase-matched diagnostic solver records.
- `results/original_v18_44_proof.json` — original Q550 completion/limits/identity counts.
- Three original plotted comparisons, SHA256 manifest, all historical scripts, nested original sendback.

Successful sendback: `../q550_kick203_directional_hessian_transported_jet_v18_44_sendback.zip`.

## Reproducibility and safeguards

Preflight (no new Q550 integrations): `bash scripts/run_preflight_v18_44.sh`.

The packager **fails closed** without 49 completed original Q550 integrations and their result files. The original `v18.43` parent ZIP is embedded byte-for-byte with its SHA256 verified; all earlier generations are staged from authenticated historical archives. No old `kappa0` or source coefficients have been edited. Numerical dual-Hessian disagreement is reported rather than silently passed as exact.

**Known limits:** one common normalized Euclidean diagnostic metric; no symbolic higher derivatives of the original Q550 model; numerical mixed differences can be affected by cancellation and finite-difference truncation; no material stiffness certification from adaptive step counts. The fact that the dynamic Jacobian is SHA-pinned does not make its finite directional derivative exact.
