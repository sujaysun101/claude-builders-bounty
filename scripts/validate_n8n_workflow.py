"""Validate the n8n weekly dev summary workflow export."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / "workflows" / "weekly-dev-summary.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    workflow = json.loads(WORKFLOW.read_text(encoding="utf-8"))
    names = {node.get("name", "") for node in workflow.get("nodes", [])}
    types = {node.get("type", "") for node in workflow.get("nodes", [])}
    blob = json.dumps(workflow, sort_keys=True)

    require(workflow.get("name") == "Weekly GitHub Dev Summary with Claude", "workflow name is wrong")
    require(len(workflow.get("nodes", [])) >= 10, "workflow should contain the full processing chain")
    require("n8n-nodes-base.scheduleTrigger" in types, "missing weekly schedule trigger")
    require("0 17 * * 5" in blob, "missing Friday 5pm cron expression")
    require("Fetch Commits" in names, "missing GitHub commits fetch")
    require("Fetch Closed Issues" in names, "missing GitHub closed issues fetch")
    require("Fetch Merged PRs" in names, "missing GitHub merged PRs fetch")
    require("api.github.com/repos" in blob, "missing GitHub repository API calls")
    require("api.github.com/search/issues" in blob, "missing merged pull request search")
    require("api.anthropic.com/v1/messages" in blob, "missing Anthropic Messages API call")
    require("claude-sonnet-4-20250514" in blob, "missing required Claude Sonnet 4 model")
    require("SUMMARY_LANGUAGE" in blob and "FR" in blob and "EN" in blob, "missing EN/FR language configuration")
    require("GITHUB_REPO" in blob, "missing configurable GitHub repo")
    require("DELIVERY_MODE" in blob and "DESTINATION_CHANNEL" in blob, "missing destination configuration")
    require("Send Discord Summary" in names, "missing Discord delivery")
    require("Send Slack Summary" in names, "missing Slack delivery")
    require("Send Email Summary" in names, "missing email delivery")
    require("Prepare Claude Prompt" in names, "missing prompt construction")

    print(f"validated {WORKFLOW.relative_to(ROOT)} with {len(workflow['nodes'])} nodes")


if __name__ == "__main__":
    main()
