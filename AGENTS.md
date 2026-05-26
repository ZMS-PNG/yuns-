# AGENTS.md — MAPES Coding Harness

## Startup Path

1. Read `prd/PRD.md` for product scope.
2. Read `docs/ARCHITECTURE.md` for system boundaries.
3. Read `feature_list.json` and pick exactly one `active` feature.
4. Run `./init.sh` before editing code.
5. Make the smallest change that advances the active feature.
6. Run verification before marking work done.
7. Update `progress.md` and `session-handoff.md` before stopping.

## Invariants

- Do not expand beyond the 3-day MVP unless the feature list is updated.
- Do not mark a feature done without runnable evidence.
- Keep judge output JSON-parseable and schema-compatible.
- Keep OCR optional; text-only flow must always work.
- Keep model providers behind interfaces; do not hard-code ERNIE into business logic.
- Do not put secrets in repository files. Use `.env` only.

## Definition of Done

A feature is done only when:

- Code or documentation is present in the expected path.
- `python -m pytest` passes.
- Demo input can produce a report JSON.
- `progress.md` records evidence.

## Verification Commands

```bash
./init.sh
python -m pytest
python -m mapes.cli --input data/cases/demo_cases.json --output artifacts/demo_report.json
```
