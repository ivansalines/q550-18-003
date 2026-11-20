# v18.38.1 — Authentic v18.36 seed genealogy repair

## Failure corrected
The Q550 v18.38 original runner tried to read
`number_of_seed_attempts` from `original_v18_37_case_summary.csv`.
That column belongs to `original_v18_36_joint_support_cases.csv`.

## Scope of patch
- `scripts/original_coupled_scaling_v18_38.py`: load the actual v18.36
  case and attempt ledger using the already pinned `read_parent_v37()`;
  verify the v18.37 case exists; reject missing, nonidentical or corrupt
  v18.36 attempts *before* new nonlinear integrations.
- `scripts/seed_genealogy_v18_38.py`: strict replay of deterministic
  seed attempt count, flags, scaled displacement and normalized radius.
- `scripts/run_on_server.sh`: include the new regression-test file.
- `tests/test_seed_genealogy_v18_38.py`: seven additional negative and
  positive cases.

The original Q550 ODE, source kappa0, candidates, samplers, tolerances,
fit logic and scientific interpretation are unchanged. The original
v18.37 ZIP and nested v18.36 sendback remain unchanged and SHA pinned.

## Server execution
From `/root/elab1/hysteresis`, unzip this hotfix with `unzip -o`.
Then cd into the original v18.38 bundle and rerun `bash scripts/run_on_server.sh`.

**No original v18.38 Q550 run was performed in this build environment.**
