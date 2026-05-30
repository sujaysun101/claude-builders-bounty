#!/usr/bin/env python3
"""Generate a structured CHANGELOG.md from git history since the last tag.

Dependency-free: only requires Python 3 and git.
"""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class Entry:
    subject: str


def sh(cmd: list[str]) -> str:
    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    return out.decode("utf-8", errors="replace").strip()


def try_last_tag() -> str | None:
    try:
        return sh(["git", "describe", "--tags", "--abbrev=0"]) or None
    except subprocess.CalledProcessError:
        return None


def subjects_since(tag: str | None) -> list[str]:
    rev = "HEAD" if not tag else f"{tag}..HEAD"
    out = sh(["git", "log", "--no-merges", "--pretty=format:%s", rev])
    if not out:
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]


def bucket(subject: str) -> str:
    lower = subject.lower()
    if lower.startswith(("feat", "add")):
        return "Added"
    if lower.startswith("fix"):
        return "Fixed"
    if lower.startswith(("remove", "delete")):
        return "Removed"
    return "Changed"


def render(subjects: list[str], tag: str | None) -> str:
    today = dt.date.today().isoformat()
    since_line = "(all commits)" if not tag else f"since tag {tag}"

    buckets: dict[str, list[str]] = {"Added": [], "Fixed": [], "Changed": [], "Removed": []}
    for s in subjects:
        buckets[bucket(s)].append(s)

    def section(name: str) -> str:
        lines = [f"### {name}"]
        if not buckets[name]:
            lines.append("- (none)")
        else:
            lines.extend([f"- {s}" for s in buckets[name]])
        return "\n".join(lines)

    parts = [
        "# Changelog",
        "",
        f"## [Unreleased] - {today}",
        "",
        f"_Generated from git history {since_line}._",
        "",
        section("Added"),
        "",
        section("Fixed"),
        "",
        section("Changed"),
        "",
        section("Removed"),
        "",
    ]
    return "\n".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="CHANGELOG.md")
    args = ap.parse_args()

    sh(["git", "rev-parse", "--is-inside-work-tree"])

    tag = try_last_tag()
    subjects = subjects_since(tag)
    text = render(subjects, tag)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

