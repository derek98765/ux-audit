"""Embed local audit screenshots in the issue cards of a draft HTML report."""

import argparse
import base64
from collections import Counter
from html import escape
import json
from pathlib import Path
import re
import sys

MARKER = re.compile(r"<!-- issue-screenshots:([\w-]+) -->")
IMAGE_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}


def screenshot_figure(screenshot, audit_directory):
    relative_path = Path(screenshot["path"])
    path = (audit_directory / relative_path).resolve()
    if relative_path.is_absolute() or audit_directory not in path.parents:
        raise ValueError("image path must be relative to the audit JSON directory")
    mime = IMAGE_TYPES.get(path.suffix.lower())
    if not mime:
        raise ValueError("expected a PNG, JPEG or WebP image")
    image = base64.b64encode(path.read_bytes()).decode("ascii")
    alt = escape(screenshot["alt"])
    caption = escape(screenshot["caption"])
    return (
        '<figure class="issue-screenshot">'
        f'<img alt="{alt}" src="data:{mime};base64,{image}" />'
        f"<figcaption>{caption}</figcaption></figure>"
    )


def issue_evidence(finding, audit_directory):
    elements = []
    for screenshot in finding.get("screenshots", []):
        try:
            elements.append(screenshot_figure(screenshot, audit_directory))
        except (OSError, ValueError, KeyError) as error:
            print(f'{finding["id"]}: {screenshot.get("path", "(no path)")}: {error}', file=sys.stderr)
            elements.append('<p class="issue-screenshot-note">A saved screenshot could not be loaded.</p>')
    if note := finding.get("screenshot_note"):
        elements.append(f'<p class="issue-screenshot-note">{escape(note)}</p>')
    return "\n".join(elements)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit", type=Path)
    parser.add_argument("html", type=Path)
    args = parser.parse_args()

    audit = json.loads(args.audit.read_text(encoding="utf-8"))
    draft = args.html.read_text(encoding="utf-8")
    findings = audit["findings"]
    if Counter(MARKER.findall(draft)) != Counter(finding["id"] for finding in findings):
        parser.error("the draft must contain exactly one screenshot marker per finding")
    by_id = {finding["id"]: finding for finding in findings}
    if len(by_id) != len(findings):
        parser.error("finding IDs must be unique")

    audit_directory = args.audit.resolve().parent
    report = MARKER.sub(lambda match: issue_evidence(by_id[match[1]], audit_directory), draft)
    args.html.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
