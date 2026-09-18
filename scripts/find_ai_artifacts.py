#!/usr/bin/env python3
"""
Scan extracted document text for common leaked AI-tool artifacts:
broken citation tags from AI search/browsing tools, and assistant-voice
phrases that indicate raw AI output was pasted in without editing.

Usage:
    python3 find_ai_artifacts.py <path-to-extracted-text.txt>

Extend PATTERNS for your own domain as you find new leak signatures.
"""
import re
import sys

PATTERNS = [
    r"<Cite\b",                          # broken citation-tool tags
    r"turn\d+search\d+",                 # AI browsing-tool internal refs
    r"\bas an AI\b",
    r"\bas a language model\b",
    r"\bI don't have access to\b",
    r"\bI do not have access to\b",
    r"\bI cannot verify\b",
    r"\bI can provide\b.{0,40}\bif you\b",
    r"\bplease share\b",
    r"\bplease provide\b.{0,40}\b(image|graph|chart|document|file)\b",
    r"\bI'm unable to\b",
    r"\bI am unable to\b",
    r"\bfeel free to\b",
    r"\bupload the\b",
    r"\battach the\b",
    r"\blet me know if\b",
]

def scan(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    lines = text.splitlines()
    hits = []
    compiled = [re.compile(p, re.IGNORECASE) for p in PATTERNS]
    for i, line in enumerate(lines, start=1):
        for pat, rx in zip(PATTERNS, compiled):
            if rx.search(line):
                hits.append((i, pat, line.strip()[:200]))
    return hits

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 find_ai_artifacts.py <path-to-extracted-text.txt>")
        sys.exit(1)
    hits = scan(sys.argv[1])
    if not hits:
        print("No known AI-artifact patterns found. (This does not prove the document is clean —")
        print("it only means these specific signatures weren't present. Extend PATTERNS as needed.)")
        sys.exit(0)
    print(f"Found {len(hits)} potential AI-artifact match(es):\n")
    for line_no, pattern, snippet in hits:
        print(f"  line {line_no}  [{pattern}]")
        print(f"    {snippet}\n")
    print("Treat each of these as a reason to independently verify related content")
    print("(e.g., if a citation tag leaked, verify every citation in that section).")

if __name__ == "__main__":
    main()
