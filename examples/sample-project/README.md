# RepoLens sample project

Run from the repository root:

```bash
repolens scan examples/sample-project --lang en
repolens scan examples/sample-project --format json --out /tmp/sample-repolens.json
repolens query examples/sample-project --query greet
```

This fixture is intentionally tiny so contributors can understand expected symbol extraction before adding a language adapter.
