# academic-integrity-grader

A [Claude Code](https://claude.com/claude-code) skill for grading academic reports — thesis chapters, dissertations, OJT/SIP/capstone/internship reports — against their **actual** official rubric, with data-fabrication and leaked-AI-artifact detection treated as a gate on the score rather than something averaged into it.

## Why this exists

Ask a general-purpose assistant to "grade my report" and you tend to get one of two failure modes: it's too generous and rubber-stamps anything well-written, or it nitpicks grammar and citation formatting while missing the one issue that actually disqualifies the submission. Neither is useful when the stakes are real.

This skill encodes a stricter process:

- Find and use the **real** marking scheme for the named institution/course — never a generic invented rubric.
- Read the **entire** source document before scoring anything.
- Treat integrity red flags — fabricated data presented as real, leaked AI-tool artifacts, internal contradictions — as **gating conditions**. A section built on invented data doesn't get a low score, it gets marked not gradable, separately from the numeric total.
- Once one red flag turns up, **verify everything checkable** (every citation, not a sample) rather than assuming the rest is fine.
- Deliver the result in a **direct, human voice** — not as a structured AI-report full of process labels.
- Give an **unambiguous pass/fail** when asked for one, worked out from the rubric's actual passing rule.

## Install

Copy this folder into your Claude Code skills directory:

```bash
# project-scoped (this repo only)
cp -r academic-integrity-grader /path/to/your/project/.claude/skills/

# or user-scoped (all projects)
cp -r academic-integrity-grader ~/.claude/skills/
```

Claude Code will pick it up automatically — it triggers on phrases like "grade this report," "assess this thesis against [rubric]," "is this ready to submit," or "does this pass or fail."

## Usage

```
grade this OJT report against the SPPU marking scheme: ~/Downloads/report.docx
```

```
review this dissertation chapter for submission readiness and give me a brutal honest verdict
```

The skill will look up the real rubric, read the full document, score what's genuine, gate what isn't, and produce a chapter-by-chapter corrections document.

## What's in here

- `SKILL.md` — the skill definition Claude Code loads.
- `scripts/find_ai_artifacts.py` — a small, extensible scanner for common leaked-AI-tool text patterns (broken citation tags, assistant-voice phrases like "please share a clearer image"). Extend the `PATTERNS` list for your own domain.

## A note on the case this was built from

This skill was generalized from a real grading session where a report's own table of contents and annexures described its findings as "actual responses collected," while the findings chapter itself said the data was "simulated for demonstration." That contradiction — not prose quality — was what actually mattered, and it's the kind of thing a rubric-line-item average will bury. No identifying details from that case are included here.

## License

MIT — see `LICENSE`.
