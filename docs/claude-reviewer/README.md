# Claude PR Reviewer

`claude-review` is a dependency-free CLI that turns a GitHub pull request diff
into a structured Markdown review comment.

It satisfies bounty #4 by accepting a PR URL, analyzing the diff, and returning:

- a 2-sentence summary of the change;
- identified risks;
- improvement suggestions;
- a Low / Medium / High confidence score.

## Install

```bash
git clone https://github.com/claude-builders-bounty/claude-builders-bounty.git
cd claude-builders-bounty
```

## Usage

```bash
python claude-review --pr https://github.com/owner/repo/pull/123
```

For offline testing, pass a saved diff:

```bash
python claude-review --diff-file ./sample.diff
```

The tool first fetches `https://github.com/owner/repo/pull/123.diff`. If that
fails and the GitHub CLI is installed, it falls back to `gh pr diff`.

## Test

```bash
python -m unittest
```

## GitHub Action

An optional workflow example is available at
`docs/claude-reviewer/github-action.yml`. Copy it into
`.github/workflows/claude-review.yml` in a repository that also contains this
reviewer, or adapt the checkout step to install the reviewer from your fork.
The workflow uses a hidden `claude-review:bot` marker and updates its previous
comment on subsequent pushes, so it does not spam a PR thread on every commit.

## Notes

The analyzer is intentionally conservative and deterministic. It flags common
review risks such as possible secrets, dynamic code execution, raw HTML writes,
disabled TLS verification, broad error handling, large diffs, and application
changes without obvious test updates.

## Claude Code Agent

This repo also includes `.claude/agents/pr-reviewer.md`, so Claude Code users can
run the reviewer as a focused PR review agent backed by the CLI.
