# RepoLens

**Local-first, multilingual repository intelligence for humans and AI agents.**

RepoLens turns a source repository into a deterministic, reviewable map: files, languages, symbols, imports, hashes, and architecture drift. It works offline by default, emits Markdown or JSON, and is designed to become an MCP provider and CI check without forcing source code through a hosted model.

> RepoLens is not another chat wrapper. Its trusted base layer is structural evidence from the repository itself. Optional AI adapters can be added later, but the core output remains reproducible and inspectable.

## Why this project

AI coding tools and documentation generators are growing quickly, but teams still need a small, vendor-neutral source of truth for onboarding, code review, localization, and change impact. RepoLens focuses on the gap between a static tree and a full AI wiki: useful immediately, private by default, and easy to diff in pull requests.

## Install

```bash
python -m pip install -e .
repolens scan . --lang en
```

No API key is required.

## Usage

```bash
# Human-readable map in Arabic
repolens scan ./my-repo --lang ar --out REPO_MAP.md

# Machine-readable snapshot for CI or agents
repolens scan ./my-repo --format json --out .repolens.json

# Search paths and symbols
repolens query ./my-repo --query auth

# Compare current code with a previous snapshot
repolens diff ./my-repo --against .repolens.json
```

Supported output languages: English (`en`), Arabic (`ar`), Spanish (`es`), French (`fr`), and Chinese (`zh`). The scanner currently recognizes Python, JavaScript, TypeScript, Rust, Go, Java, Kotlin, C/C++, C#, Ruby, PHP, Swift, Scala, Shell, and SQL by extension.

## Design

```text
source tree -> safe scanner -> structural index -> JSON snapshot
                                      |-> localized Markdown
                                      |-> query API
                                      |-> architecture drift diff
                                      |-> future MCP / CI adapters
```

The first release intentionally avoids network access, code execution, and model calls. Hidden directories, dependency folders, lockfiles, undecodable files, and common build artifacts are skipped. Hashes are used for change detection; source contents are never copied into the snapshot.

## Roadmap

- [x] Offline scanner with language detection, symbols, imports, hashes
- [x] JSON schema version and localized Markdown renderer
- [x] Query and snapshot diff commands
- [x] Unit tests and GitHub Actions CI
- [ ] Tree-sitter adapters for richer language-accurate syntax
- [ ] MCP server with `scan`, `query`, and `explain_change` tools
- [ ] Git history and pull-request impact analysis
- [ ] Optional local LLM adapter (Ollama/llama.cpp) with evidence citations
- [ ] Web UI and signed, shareable repository reports
- [ ] Benchmark suite across multilingual repositories

## Project status

This is an early, usable alpha. Regex extraction is deliberately conservative; it is not a compiler and may miss advanced syntax. Do not treat inferred imports or symbols as a security boundary. Review generated reports before publishing them.

## Development

```bash
python -m pip install -e . pytest
pytest
python -m compileall -q src
```

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). RepoLens is Apache-2.0 licensed; contributions that improve language coverage, localization, test fixtures, and CI integrations are especially welcome.
