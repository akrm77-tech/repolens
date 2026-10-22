# Contributing

1. Open an issue for a language adapter, output contract, or bug.
2. Keep the offline core dependency-light and deterministic.
3. Add a focused test for every parser or CLI behavior change.
4. Run `pytest` and `python -m compileall -q src` before opening a pull request.
5. Do not add telemetry, network calls, or secret-bearing fixtures without explicit design review.
