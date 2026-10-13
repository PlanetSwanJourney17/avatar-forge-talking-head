# Contributing to avatar-forge-talking-head

Thanks for wanting to help forge talking heads. This repo is a service-oriented
Python desktop tool for generating AI avatars and lip-synced talking-head video
from a still image + an audio track.

## Ground rules

- **Python 3.11+** is the target runtime. We test on 3.11 and 3.12.
- Keep handlers thin. Business logic lives in `services/`, never in `handlers/`.
- Platform-specific code goes behind an adapter in `adapters/`. No `if sys.platform`
  branches scattered through services.
- Every new service gets a unit test under `tests/`.
- Type hints are required on all public functions. We run `mypy --strict` in CI.

## Dev setup

```bash
git clone https://github.com/avatar-forge/avatar-forge-talking-head
cd avatar-forge-talking-head
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -e ".[dev]"
python -m avatar_forge.cli doctor
```

## Layout

```
avatar_forge/
  bootstrap/     app startup, DI wiring, CLI entry
  handlers/      thin request/CLI handlers -> call services
  services/      business logic (lipsync, rig, render, voice)
  models/        dataclasses & pydantic schemas (no logic)
  adapters/      platform adapters (Windows audio, CUDA, ffmpeg)
  utils/         pure helpers
  config/        settings & defaults
```

## Submitting a change

1. Fork, branch off `main`, name the branch `feat/<short-name>`.
2. Run `ruff check . && mypy avatar_forge && pytest -q` before pushing.
3. Open a PR with a short description and a sample render if it changes output.
4. One reviewer approval required. CI must be green.

## Style

- `ruff` for lint + format. Line length 100.
- No wildcard imports. No mutable default args.
- Log via `logging.getLogger(__name__)`, never `print()` in library code.