# Product strategy

## Positioning

RepoLens is a local-first evidence layer for repository understanding. It deliberately sits between a plain file tree and a hosted AI wiki. The core promise is verifiable structure: every file, symbol, import, and change can be traced to the repository without a network call.

## Competitive gap

Aider already offers a strong terminal coding workflow and a repository map. Litho/deepwiki-rs focuses on AI-generated C4 documentation, external knowledge, and CI synchronization. repo-map generates LLM-authored notes with a SQLite cache. RepoLens should not compete by claiming a better generic chatbot or by copying a wiki UI. Its wedge is a small, private, multilingual structural snapshot that is useful in CI and can later feed many agents through MCP.

## Distribution loop

The shareable artifact is a localized `REPO_MAP.md` that a maintainer can commit beside a project. Pull requests can show a compact drift report. Contributors can use `repolens query` during onboarding. These artifacts create visible, repeatable utility without requiring a hosted account. A future benchmark should compare extraction precision and useful change-impact signals across repositories and languages rather than comparing prose quality alone.

## Honest growth assumptions

No repository can guarantee thousands of stars. Adoption depends on a sharp demo, maintainers who feel the pain, reliable language support, quick installation, and sustained issue response. The launch should therefore optimize for a memorable five-minute demo and reproducible evidence, not inflated claims or star-bait.
