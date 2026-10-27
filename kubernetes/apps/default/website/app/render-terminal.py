#!/usr/bin/env python3
"""Render the plain-text homepage with ANSI colors and OSC 8 hyperlinks."""

from pathlib import Path
import re

ESC = "\x1b"
RESET = f"{ESC}[0m"
LINK_END = f"{ESC}]8;;{ESC}\\"
LINK = re.compile(r"https://[^\s]+|lucas\.summers\.dev@gmail\.com")
SECTIONS = {"hello.", "experience", "selected projects", "find me online"}
ENTRIES = {
    "Consulting Intern · Icertis",
    "Software Engineering Intern · BMC Software",
    "Engineering Intern · West Biofuels",
    "Homelab",
    "ML Model Reporting Toolkit",
    "2048 AI Strategy Playground",
}


def color(text: str, code: str) -> str:
    return f"{ESC}[{code}m{text}{RESET}"


def hyperlink(match: re.Match[str]) -> str:
    label = match.group()
    target = f"mailto:{label}" if "@" in label else label
    return f"{ESC}]8;;{target}{ESC}\\{color(label, '4;34')}{LINK_END}"


def render(line: str) -> str:
    if line == "lucas summers":
        return color(line, "1;36")
    if line in SECTIONS:
        return color(line, "1;34")
    if line in ENTRIES:
        return color(line, "1;36")
    if line.startswith(("Jun –", "Summers ")) or re.fullmatch(r"[-=]+", line):
        return color(line, "2")
    if line.startswith("plain text"):
        return color("plain text · no tracking · ", "2") + LINK.sub(hyperlink, line.split(" · ", 2)[2])
    return LINK.sub(hyperlink, line)


if __name__ == "__main__":
    directory = Path(__file__).parent
    source = (directory / "terminal.txt").read_text(encoding="utf-8")
    (directory / "terminal.ansi").write_text(
        "\n".join(render(line) for line in source.splitlines()) + "\n",
        encoding="utf-8",
    )
