# RepoLens launch plan

This plan is designed to maximize the chance of useful adoption without making an impossible promise about star counts. Stars are an awareness signal; repeat usage, external contributors, and real repository scans are stronger evidence that the project is working.

## Positioning

Lead with one memorable sentence:

> **See the shape of your codebase before asking AI to change it.**

The wedge is not “another AI documentation generator.” RepoLens is a local, multilingual, evidence-first snapshot that works without a model and can later feed CI systems and agents. Every launch asset should demonstrate that distinction in under one minute.

## Release sequence

### Phase 1 — Make the repository trustworthy

Before public launch, keep the README above the fold focused on the command, output, privacy model, and a real benchmark. Keep the Apache-2.0 license, security policy, contribution guide, CI workflow, and a small set of deterministic fixtures. Add issue templates for parser bugs, language requests, and feature proposals.

**Definition of done:** a new contributor can clone the repository, install it, scan a fixture, run the tests, and understand the alpha limitations in less than ten minutes.

### Phase 2 — Ship the five-minute proof

Publish a short terminal recording or animated GIF showing this exact path:

1. Scan a mixed Python/TypeScript repository.
2. Open the localized `REPO_MAP.md`.
3. Save a JSON baseline.
4. Change one file.
5. Run `repolens diff` and show the changed path.

Use a real open-source fixture or the project repository itself. Do not use synthetic claims, fake performance numbers, or a dashboard full of vanity metrics.

### Phase 3 — Earn the first external users

Invite five to ten maintainers who own different language stacks. Ask each person to run one command and report one missing symbol, unsupported file type, or confusing output. Convert every useful report into a fixture and regression test. This creates a credible language-coverage story and gives contributors a reason to return.

The first meaningful milestone is five unrelated repositories using RepoLens, not a particular number of stars.

### Phase 4 — Turn usage into a GitHub workflow

Implement a small GitHub Action that stores a baseline artifact and comments on added, removed, and changed files in pull requests. Keep it read-only and allow a repository-level opt-out. Publish a copy-paste workflow so the value is visible without installing Python locally.

Suggested future workflow:

```yaml
name: Repository drift
on: [pull_request]
jobs:
  repolens:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pipx run repolens scan . --format json --out .repolens.json
      - run: pipx run repolens diff . --against .repolens-baseline.json
```

This is a roadmap example, not a claim that an official Action already exists.

### Phase 5 — Become an agent primitive

Add a read-only MCP server only after the structural JSON contract is stable. The first tools should be `scan_repository`, `query_repository`, and `diff_repository`. Responses should cite repository-relative paths and line numbers. An optional local-model adapter should remain behind an explicit privacy switch and never replace the deterministic evidence layer.

## Launch assets

Create these assets in order of leverage:

- A README hero section with the one-line promise and copy-paste command.
- A short terminal GIF showing scan → map → diff.
- A small multilingual fixture repository with expected JSON output.
- A GitHub Action example once the Action is implemented.
- Three before/after onboarding stories: a bot, a web app, and a systems project.
- A release post that explains what RepoLens does not do as clearly as what it does.

Use consistent names, screenshots, and commands across GitHub, social posts, Reddit, Hacker News, and developer communities. Do not mass-post identical promotional text; tailor the technical problem to each community.

## Distribution playbook

On launch day, publish the GitHub release and README first. Then share the terminal demo with a concrete question: “Which language construct should RepoLens support next?” This produces better discussion than asking people to star the repository.

During the following week, publish one technical note per real improvement: parser fixture, privacy decision, CI prototype, or benchmark. Respond to every actionable issue quickly. Thank users publicly in release notes only with their permission.

After the first external users appear, submit to appropriate open-source directories and GitHub topic pages. A community post should contain the problem, one command, one real output, the limitations, and a direct invitation to test—not an inflated claim about disruption.

## Metrics

Track the following in a simple weekly log:

- Successful installs and completed scans.
- Number of unrelated repositories scanned.
- Repeat usage within 30 days.
- GitHub Action runs after the Action ships.
- External contributors and merged language fixtures.
- Open issue response time.
- False-positive rate on the benchmark fixtures.
- Stars and forks as secondary awareness signals.

A realistic sequence is: five external repositories, three useful bug reports, one outside contributor, and one repeat user before optimizing for broad promotion. No metric guarantees future growth.

## Risks and guardrails

The category is competitive, so do not clone a hosted documentation wiki. Regex extraction can miss syntax, so label results as structural hints and add Tree-sitter adapters through tested fixtures. Reports can reveal sensitive architecture, so keep the core offline, exclude common secret-bearing files, and warn before publishing output. Avoid telemetry and avoid sending source code to a model by default.

## Definition of a successful launch

The launch is successful when an unfamiliar developer can understand the value from the README, install the tool without an account, scan a real repository in seconds, inspect a useful artifact, and report a concrete improvement. Stars may follow that behavior, but they cannot be promised or manufactured.
