# v18.38.2 — Observed support exit vs right-censored residence

## Original Q550 server failure

After successful v18.38.1 genealogy verification and one completed five-trajectory
family, a later run returned `NO_EXIT_OBSERVED` from the existing
`flow_normal_math_v18_36.first_exit()` helper. The original v18.38 code
mistakenly demanded that EVERY trajectory cross the diagnostic radius.

`NO_EXIT_OBSERVED` means the trajectory never crossed the chosen radius in
the sampled time window `[0,1e-5 xi]`. It is a VALID RIGHT-CENSORED observation,
not a failed original ODE integration and not evidence of never exiting later.

## Surgical repair

- Only `CROSSED_AFTER_START` with a genuine root has a numerical exit time.
- `NO_EXIT_OBSERVED` has a blank `exit_delta_xi`, status
  `NO_EXIT_OBSERVED`, and `support_observed_horizon=1e-5`.
  The end of the observation window is NEVER mislabelled as a crossing.
- `OUTSIDE_AT_START` and unrecognized labels still abort the run.
- Five-trajectory family comparison time is now half the MINIMUM support
  horizon, where the horizon is the measured crossing if one occurs, or the
  end of the observation window for a right-censored trajectory.
  If none exits, the common time is half the observation window.
- The local common segment is checked at an additional dense 81-point grid.
  This is a numerical guard, NOT interval-arithmetic certification.
- Both per-trajectory CSV and per-family CSV store actual exits versus
  censored counts. The proof JSON includes totals for all 60 trajectories.
- Seven new regression tests cover censored, crossed and mixed cohorts,
  a fully censored family, out-of-support initial values, invalid times.

The Q550 ODE, SHA-pinned historical inputs, kappa0, calibration radius,
perturbations, candidate surfaces, integration tolerances and fit/holdout
protocol are unchanged. This hotfix must be laid OVER the original v18.38
bundle and v18.38.1 hotfix; no full reinstallation or orbit replay is needed.
No new original Q550 integration was run in this construction environment.

## On the original server

```bash
cd /root/elab1/hysteresis
unzip -o q550_v18_38_2_support_censor_hotfix.zip
cd q550_kick203_coupled_level_normal_scaling_v18_38_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_38_server_retry2.log
```
