<div align="center">

# RepoLens

### See the shape of your codebase before asking AI to change it.

**Local-first · multilingual · deterministic · agent-ready**

[![CI](https://github.com/akrm77-tech/repolens/actions/workflows/ci.yml/badge.svg)](https://github.com/akrm77-tech/repolens/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB.svg)](https://www.python.org/)

[Quick start](#quick-start) · [Why RepoLens](#why-repolens) · [Roadmap](#roadmap) · [Contributing](#contributing)

</div>

RepoLens turns a source repository into a **reviewable structural map**: files, languages, symbols, imports, content hashes, and change drift. It runs locally, needs no API key, and exports Markdown for humans or JSON for CI and AI agents.

> RepoLens is not another hosted chat wrapper. Its trusted base layer is evidence from the repository itself. Optional AI adapters can come later; the core stays reproducible, inspectable, and private by default.

## The 30-second demo

```bash
# Install from source
python -m pip install -e .

# Generate an Arabic repository map
repolens scan ./your-repo --lang ar --out REPO_MAP.md

# Create a machine-readable baseline
repolens scan ./your-repo --format json --out .repolens.json

# Find a symbol or path
repolens query ./your-repo --query authentication

# Detect structural drift after a change
repolens diff ./your-repo --against .repolens.json
```

The first command works offline. No account, hosted model, telemetry, or source upload is required.

For a zero-risk first run, use the included [sample project](examples/sample-project):

```bash
repolens scan examples/sample-project --lang en
repolens query examples/sample-project --query greet
```

## Why RepoLens

Modern repositories are too complex for a plain file tree and too sensitive to send blindly to a hosted model. RepoLens occupies the useful middle: it creates a small, portable evidence layer that can be reviewed in a pull request, translated for a global team, or passed to an agent through a future MCP adapter.

| Need | RepoLens answer |
|---|---|
| Onboarding | A readable map of files, symbols, imports, and languages |
| Privacy | Local-first scanning with no network call in the core |
| Localization | Markdown labels in English, Arabic, Spanish, French, or Chinese |
| CI and agents | Versioned JSON snapshots with hashes and stable paths |
| Change awareness | Added, removed, and changed file detection |
| Fast feedback | Tested on `bot_tech`: 438 lines scanned in about 0.05 seconds |

## Example output

A JSON snapshot is intentionally compact and source-free:

```json
{
  "schema": "repolens/v1",
  "root": "/workspace/project",
  "files": [
    {
      "path": "src/main.py",
      "language": "Python",
      "sha256": "…",
      "lines": 418,
      "symbols": [
        {"name": "run_bot", "kind": "function", "line": 211}
      ],
      "imports": ["telegram", "sqlite3"]
    }
  ]
}
```

The snapshot stores metadata and hashes, not the contents of your source files. Review generated reports before publishing them because paths and symbol names may still reveal sensitive architecture.

## Quick start

### Install

```bash
git clone https://github.com/akrm77-tech/repolens.git
cd repolens
python -m pip install -e .
```

Requirements: Python 3.10 or newer. The alpha release has no runtime dependency outside the Python standard library.

### Scan a repository

```bash
repolens scan ./my-repo
repolens scan ./my-repo --format json --out .repolens.json
repolens scan ./my-repo --lang ar --out REPO_MAP.md
```

Supported report languages: English (`en`), Arabic (`ar`), Spanish (`es`), French (`fr`), and Chinese (`zh`). The scanner recognizes Python, JavaScript, TypeScript, Rust, Go, Java, Kotlin, C, C++, C#, Ruby, PHP, Swift, Scala, Shell, and SQL by extension.

### Query and diff

```bash
repolens query ./my-repo --query auth
repolens diff ./my-repo --against .repolens.json
```

The diff command reports three intentionally simple categories: `added`, `removed`, and `changed`. That makes it suitable for a first CI policy without pretending to understand every semantic code change.

## How it works

```text
source tree
    │
    ▼
safe local scanner ──► language + symbols + imports + hashes
    │
    ├──────────────► localized Markdown for humans
    ├──────────────► JSON snapshot for CI and agents
    └──────────────► drift diff for pull requests
```

The scanner skips common dependency, cache, build, VCS, and undecodable files. It never executes the target repository. Symbol extraction is intentionally conservative in 0.1; Tree-sitter adapters are planned for language-accurate parsing.

## What makes this different

Aider is an excellent terminal coding assistant with a repository map. Litho / deepwiki-rs focuses on AI-generated C4 documentation. repo-map generates LLM-authored file notes. RepoLens is deliberately narrower: **an offline, multilingual, evidence-first snapshot that can become shared infrastructure for all of them**.

That distinction matters. The project does not promise perfect architecture understanding or automatic documentation truth. It provides a deterministic base that other tools can cite and compare.

## Roadmap

- [x] Offline scanner with language detection, symbols, imports, and hashes
- [x] JSON schema and localized Markdown renderer
- [x] Query and snapshot drift commands
- [x] Tests, security policy, CI, and Apache-2.0 license
- [ ] YAML and configuration-file adapters
- [ ] Tree-sitter adapters for precise syntax extraction
- [ ] GitHub Action that comments on repository drift
- [ ] Read-only MCP server with path and line citations
- [ ] Git history and pull-request impact analysis
- [ ] Optional Ollama / llama.cpp adapter with an explicit privacy switch
- [ ] Benchmark suite across multilingual repositories
- [ ] Web UI for signed, shareable reports

## Project status

RepoLens is an early usable alpha. Regex extraction can miss advanced syntax and inferred imports or symbols are not a security boundary. The project is looking for feedback from maintainers of Python, TypeScript, Go, Rust, and Java repositories.

## Contributing

The highest-value contributions are language fixtures, parser precision, localized labels, CI integrations, and real-world bug reports. Before opening a pull request:

```bash
python -m pip install -e '.[dev]'
pytest
python -m compileall -q src
ruff check src tests
ruff format --check src tests
mypy src tests
```

Please keep the core dependency-light, offline by default, and free of telemetry. See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Launch and community

Read the [launch plan](docs/launch-plan.md) for the release sequence, demo assets, success metrics, and distribution strategy. If RepoLens is useful to you, the most valuable first action is not a star: run it on a real repository and open an issue with one concrete false positive or missing language construct.

## العربية

RepoLens أداة محلية لفهم بنية المستودعات البرمجية دون إرسال الكود إلى خدمة خارجية. تنشئ خريطة Markdown أو Snapshot بصيغة JSON، وتدعم إخراجًا بالعربية والإنجليزية والإسبانية والفرنسية والصينية، مع اكتشاف التغييرات بين نسختين من المشروع.

## License

Apache-2.0. See [LICENSE](LICENSE).
