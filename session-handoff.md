# Session Handoff

## Current Active Feature

F002 — 评分引擎与JSON Schema

## Last Completed

Project scaffolding and documentation generated.

## Next Step

Run tests locally, then integrate real ERNIE API call in `src/mapes/judges/ernie_judge.py`.

## Known Constraints

- OCR is optional for MVP.
- Text-only pipeline must remain stable.
- Dify workflow should call the same logical modules: OCR → context builder → judge → scorer → report.
