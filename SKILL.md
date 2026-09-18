---
name: academic-integrity-grader
description: "Grades or reviews an academic report (thesis chapter, dissertation, OJT/SIP/capstone/internship report) against the ACTUAL official rubric for its institution or course — never a generic invented one — and treats data fabrication, leaked AI-tool artifacts, or other integrity red flags as gating conditions rather than folding them into an averaged score. Produces a direct, human-voiced, chapter-by-chapter corrections document instead of a structured AI-report. MANDATORY TRIGGERS: 'grade this report', 'assess this thesis/dissertation', 'review this against [university/institution] rubric', 'is this ready to submit', 'check this for academic integrity issues', 'mark this report'. STRONG TRIGGERS: 'give me a brutal/honest assessment of this paper', 'does this pass or fail', 'what grade would this get', 'stress-test this before I submit it'. Do NOT trigger for casual writing feedback, creative writing critique, or homework with no formal rubric — this skill is for formal academic submissions being graded against a real marking scheme."
---

# Academic Integrity Grader

Most AI grading help fails in one of two directions: it either rubber-stamps anything reasonably well-written, or it nitpicks grammar and citation style while missing the one thing that actually disqualifies the work. This skill is built around a different idea: **verify the real rubric, read the whole thing before judging any of it, and treat integrity red flags as a gate, not a line item.**

It was built from a real case: a project report that read well on the surface — clear objectives, a solid theoretical framework, real and verifiable citations — but whose data-analysis chapters admitted, in the document's own words, that the findings were "simulated for demonstration," while the table of contents and annexures described the same material as "actual responses collected." Averaging that into a weighted score would have quietly implied partial credit for invented data. Gating it — scoring what's real, and marking the rest as not gradable rather than poorly gradable — was the only honest way to report it.

## Core principles

1. **Confirm the rubric with the user, then verify it. Never invent one.** Ask which rubric to grade against if it isn't already clear. If the user names an institution, course, or marking scheme, find the real official document (syllabus PDF, department handbook, published rubric) and cite it. If a search can't turn up an authoritative version, say so explicitly and ask the user to provide the rubric directly, rather than fabricating criteria that merely sound plausible.
2. **Read the entire source before forming any judgment.** Extract the full text — every paragraph, every table — rather than sampling chapters. A document can look strong for 40 pages and then contradict itself on page 41 in a way that changes the whole assessment.
3. **Integrity red flags gate the score; they don't average into it.** Fabricated data presented as real, leaked AI-generation artifacts, internal factual contradictions, or plagiarism indicators are not "a weak section." Score the sections that rest on genuine work normally. Mark the compromised ones as NOT GRADABLE / NOT CERTIFIED, separately, and say so in plain language in the final verdict.
4. **One leaked artifact means check everything, not just that one thing.** If you find a broken AI-tool citation tag, an assistant's reply pasted into the text, or any other sign that content wasn't authored end-to-end, that's a reason to independently verify every citation and every factual claim you can check — not just note the one you tripped over. This is cheap (a handful of targeted searches) and it's the difference between "a citation is real" and "a citation looks real."
5. **Exclude what you can't see. Don't guess it.** If you're grading from a document alone, mark viva-voce, live presentation, and mentor/supervisor feedback components as explicitly excluded rather than estimating a number for them.
6. **Write the final feedback like a person, not like an AI system report.** No "council," "advisor," "multi-agent," or "peer review" framing in the deliverable itself — even if you used an internal stress-testing step to sanity-check your own judgment, fold the substance of that reasoning into your own voice. First person, direct, addressed to the person who wrote the report. (This matters more than it sounds: a corrections report that reads like unedited AI output undermines its own credibility, especially when part of what it's flagging is unedited AI output in the *original* document.)
7. **When asked for a blunt final verdict, give one.** State the actual numeric passing threshold, show the math, and name the single disqualifying issue directly. "Borderline" is a cop-out if the rubric's own passing rule makes the answer clear.

## Workflow

**1. Locate and verify the rubric.**
Confirm with the user which rubric to grade against before doing anything else — don't assume. If they name an institution/course but don't attach the rubric itself, search for the actual official marking scheme (universities and institutions often publish these in syllabus PDFs or course handbooks): find the primary source, extract it directly (see tooling note below), and quote the real marks breakdown rather than summarizing from memory or guessing. If a live web search can't turn up an authoritative version, say so explicitly and ask the user to supply the rubric document directly rather than proceeding on a guess. If a companion structural template exists (e.g., a sample report showing expected chapter structure), pull that too — structural deviations are worth flagging.

**2. Extract the full source document.**
Don't rely on a generic "read a PDF/DOCX" tool that requires retries or rerouting — use a library that handles the actual file format directly and extracts paragraphs and tables in document order (see `scripts/` for a Python approach). Read the whole thing before scoring anything.

**3. Draft an independent score against every assessable rubric item**, with a quote or specific section reference backing each score — not just a number. If you can't point to the exact place in the document that justifies a score, don't give it yet.

**4. Scan for integrity red flags.** Run `scripts/find_ai_artifacts.py` (or equivalent) against the extracted text for common leaked-AI-tool patterns, and read the front matter (table of contents, executive summary, annexures) against the body for internal contradictions — data described as "actual" in one place and "simulated"/"illustrative"/"for demonstration" in another is the single most common and most serious version of this.

**5. If anything from step 4 fires, verify every citation and every checkable factual claim**, not just the one that triggered the search. Web search the actual titles/DOIs/authors against real publication databases.

**6. Score what's real. Gate what isn't.** Build a scoring table where genuinely-assessable sections get normal marks, and any section resting on fabricated/contradictory data is marked NOT GRADABLE with a one-line reason, kept separate from the numeric subtotal.

**7. Optional — stress-test your own draft** before finalizing, especially for a high-stakes verdict. A multi-perspective self-critique pass (see the `llm-council` skill, if available, for a structured way to do this) is good for catching your own softening bias — it's easy to read a well-written report and unconsciously grade the prose instead of the substance.

**8. Write the corrections document in a human voice.** Structure suggestion:
   - A short, direct opening note (what's good, what's not, why the rest of this matters)
   - The rubric you used and its real source
   - The handful of critical, non-rubric issues that matter more than any line item (with quotes)
   - The marks table (gated, not averaged)
   - Chapter-by-chapter corrections: quote the problem, state the fix, in plain sentences — not clipped "Issue:/Fix:" fragments
   - A direct bottom line
   - What you checked this against (rubric source, verified citations)

**9. If asked for a final pass/fail verdict**, do the arithmetic against the rubric's actual passing rule (e.g., minimum percentage, separate pass/fail heads) and say which side of the line it falls on, plainly.

## Tooling notes

- For `.docx` sources: use `python-docx` directly (`pip install python-docx`). Iterate `document.element.body` children in order (paragraphs and tables interleaved) rather than `document.paragraphs` alone, so table content isn't read out of sequence. Never route a Word document through a PDF-oriented reader tool — wrong tool for the format, and it tends to fail and get silently retried on a different tool, wasting time/cost for no benefit.
- For `.pdf` sources: `pypdf` (or `pdfplumber`/`pdftotext` if available) extracts text directly and reliably — again, avoid flaky all-purpose "read any document" tools that require rerouting.
- To build the corrections document itself as a `.docx`: also `python-docx` — headings, tables, and styled paragraphs are straightforward to generate, and it keeps the whole pipeline in one library.
- `scripts/find_ai_artifacts.py` is a small, extensible grep-style scanner for common leaked-AI-tool patterns (broken citation tags, assistant-voice phrases like "please share a clearer image," "as an AI," etc.). Extend its pattern list for your domain.

## Worked example (generalized)

A business-school internship report scored well on first read: clear objectives, a real and verifiable literature review, a solid theoretical framework. But its findings chapter stated outright that the analysis used "simulated data for demonstration," while the table of contents and annexures both described the same material as "actual responses collected." That is a direct self-contradiction about the authenticity of the report's core deliverable, and the institution's own guidelines required primary data collection.

The right move was not to average this into a single score — a few points off "data analysis," a few off "overall quality." It was to score the sections that were genuinely done (the theoretical framework, the literature review — the latter independently verified citation-by-citation once one AI-tool artifact turned up in that chapter) and mark the data-analysis chapters as not gradable in current form, stating plainly what would need to happen (real data collection) before the report could be assessed as intended. When asked for a blunt final verdict, the honest answer — worked out from the institution's own numeric passing threshold — was a clear fail, not a hedge.

## When NOT to use this

- Casual writing feedback, blog drafts, or work with no formal grading rubric — this skill is calibrated for high-stakes, rubric-based academic submissions.
- Creative writing, where "gating" and rubric literalism aren't the right frame.
- Anything the user explicitly wants gentle, encouraging feedback on rather than an exam-conditions assessment — ask first if it's unclear which mode they want.
