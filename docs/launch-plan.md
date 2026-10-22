# Launch plan

## Release 0.1: prove the wedge

Publish a five-minute demo that scans a mixed-language repository, writes a localized `REPO_MAP.md`, and shows a pull-request diff after one file changes. Keep the demo repository small enough to clone quickly. The landing README should lead with the command and the generated artifact, not with AI claims.

## Release 0.2: become useful in CI

Add a GitHub Action that stores a baseline snapshot and comments on added, removed, or changed files. Add a stable JSON schema, exit codes for policy thresholds, and fixtures for Python, TypeScript, Go, Rust, and Java. Invite maintainers to report false positives and missing syntax patterns.

## Release 0.3: become an agent primitive

Ship a small MCP server with read-only tools: `scan_repository`, `query_repository`, and `diff_repository`. Every response should cite paths and line numbers from the structural index. Add an optional local-model adapter only after the deterministic layer has a benchmark and a clear privacy switch.

## Distribution channels

The highest-leverage launch assets are a terminal GIF, a copy-paste GitHub Action, language fixture badges, and before/after onboarding examples. Submit to relevant GitHub topic pages and communities only after the README, license, security policy, and issue templates are ready. Ask for concrete feedback rather than asking for stars.

## Metrics

Track successful installs, scans completed, CI action uses, unique contributors, issue response time, and repeat usage. Stars are a delayed awareness signal, not the product objective. A healthy early milestone is five unrelated repositories using the tool and filing actionable issues; a larger star count without usage is not proof of product-market fit.

## Risks and mitigations

Regex extraction can miss syntax, so label the output as structural hints and expand through tree-sitter adapters. Reports can expose sensitive architecture, so keep the core offline and warn before publishing snapshots. The category is competitive, so maintain the evidence-first, multilingual, CI/MCP wedge instead of cloning a hosted documentation wiki.
