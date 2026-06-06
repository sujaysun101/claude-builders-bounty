# n8n Weekly GitHub Dev Summary

This submission adds an importable n8n workflow that gathers a repository's weekly GitHub activity, asks Claude Sonnet 4 to write a narrative summary, and sends the summary to Discord, Slack, or email.

## Files

- `workflows/weekly-dev-summary.json`: importable n8n workflow export.
- `scripts/validate_n8n_workflow.py`: local validator for the workflow structure.

## Five-step setup

1. Import `workflows/weekly-dev-summary.json` into n8n.
2. Create two HTTP Header Auth credentials:
   - `GitHub token header`: header name `Authorization`, value `Bearer <github-token>`.
   - `Anthropic API key header`: header name `x-api-key`, value `<anthropic-api-key>`.
3. Set environment variables for the n8n process:
   - `GITHUB_REPO=owner/repo`
   - `SUMMARY_LANGUAGE=EN` or `SUMMARY_LANGUAGE=FR`
   - `DELIVERY_MODE=discord`, `DELIVERY_MODE=slack`, or `DELIVERY_MODE=email`
   - `DISCORD_WEBHOOK_URL`, `SLACK_WEBHOOK_URL`, or `EMAIL_FROM` and `EMAIL_TO`
4. Execute the workflow manually once and verify the destination receives the summary.
5. Activate the workflow; the schedule trigger runs every Friday at 5pm using cron `0 17 * * 5`.

## What the workflow does

The workflow builds a seven-day reporting window, fetches commits, closed issues, and merged pull requests from the GitHub API, then sends the normalized activity data to `claude-sonnet-4-20250514` through the Anthropic Messages API. The prompt asks Claude to avoid inventing facts and to produce a concise engineering narrative in English or French.

Delivery is selected with `DELIVERY_MODE`. Discord is the default fallback because it requires only a webhook URL and keeps the workflow easy to test.

## Validation

Run the local validator from the repository root:

```bash
python scripts/validate_n8n_workflow.py
```

The validator checks that the workflow is valid JSON, import-shaped, scheduled weekly, calls GitHub for commits/issues/merged PRs, uses `claude-sonnet-4-20250514`, exposes EN/FR and destination configuration, and includes Discord, Slack, and email delivery nodes.

## Live n8n execution evidence

The workflow still needs to be imported into a real n8n instance and executed once with real credentials before claiming the bounty. Add the successful execution screenshot under `docs/n8n-weekly-dev-summary/` before opening or updating a PR for issue #5.
