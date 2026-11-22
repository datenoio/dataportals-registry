# Archived one-shot scripts

These scripts ran a single discovery or country-fix pass. They are kept for history, not as part of the day-to-day CLI.

Do **not** add new one-shot country or Censys-compare scripts here. Use `scripts/builder.py`, `scripts/apidetect.py`, `scripts/promote_scheduled.py`, and `scripts/check_liveness.py` instead.

If a script is still needed, move it back to `scripts/` and add a test. The scripts find the repository root and import `constants` / `yaml_io` relative to `scripts/`, so they do not run from this folder.

Scripts that no doc, test or other script referenced were moved here in November 2026 (tech-debt phase 1). Their git history follows the move (`git log --follow`).
