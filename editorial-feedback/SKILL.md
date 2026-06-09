---
name: editorial-feedback
description: Analyze provided text and return actionable, prioritized editorial feedback on completeness, consistency, clarity, accuracy, robustness, accessibility, and alignment with purpose. Use when the user asks for editorial review, critique, publishing readiness feedback, or improvement suggestions for text; do not rewrite the full text unless explicitly requested.
---

# Editorial Feedback

## Purpose

Use this skill to analyze provided text and return actionable, prioritized editorial feedback. Help the author improve completeness, consistency, clarity, accuracy, robustness, accessibility, and alignment with purpose.

## When to use

Use this skill when the user provides text and asks for:

- Editorial review
- Critique
- Improvement suggestions
- Feedback on structure, clarity, accuracy, or completeness
- Prioritized recommendations before publishing, sending, or presenting text

Do not rewrite the full text unless the user explicitly asks for a rewritten version.

## Core rule

Return the analysis in the same language as the input text.

If the language of the input text cannot be determined, ask one clarifying question before proceeding.

## Evaluation criteria

Analyze the text explicitly against each criterion below.

### 1. Completeness

Check for:

- Missing information
- Unstated assumptions
- Unanswered questions
- Logical or contextual gaps
- Missing audience, goal, scope, examples, constraints, or next steps

### 2. Consistency

Check for:

- Internal contradictions
- Mismatched tone
- Inconsistent terminology
- Conflicting claims
- Claims that conflict with obvious reality or common knowledge

### 3. Clarity

Check for:

- Ambiguous wording
- Vague claims
- Awkward phrasing
- Unclear references
- Overloaded sentences
- Unclear structure or sequence

Suggest clearer alternatives where useful.

### 4. Accuracy

Check for:

- Factual claims that may be incorrect
- Numerical claims that need validation
- Outdated claims
- Unverifiable statements
- Claims requiring source support

Mark which claims require verification and suggest how to verify them.

### 5. Robustness

Check for:

- Missing alternative scenarios
- Edge cases
- Failure modes
- Objections the reader may raise
- Worst-case scenarios
- Dependencies or risks not addressed

### 6. Accessibility

Check readability for the intended audience:

- Jargon level
- Sentence length
- Structure
- Cognitive load
- Assumed background knowledge
- Whether the text is understandable for its target reader

Recommend adjustments for the target audience.

### 7. Purpose

Check whether each section, paragraph, or sentence contributes to the text's goal.

Identify:

- Redundant content
- Irrelevant details
- Weakly justified sections
- Missing connection to the main purpose
- Places where the author should cut, move, or strengthen content

## Output format

Return only the analysis and recommendations. Do not include unrelated commentary.

Use this structure:

```markdown
# Executive summary

[2-4 sentences. Give the overall assessment and the top 3 priorities to fix.]

# Detailed findings

## Completeness

### Issue 1: [short issue title]

**Excerpt:** "[exact quote]"
**Location:** [line, paragraph, section, or "not specified"]
**Problem:** [concise explanation]
**Severity:** Critical / Major / Minor
**Recommendation:** [concrete recommendation]

**Suggested replacement:**
> [replacement text, if relevant]

**Rationale:** [one-line explanation]

## Consistency

[Same issue structure.]

## Clarity

[Same issue structure.]

## Accuracy

[Same issue structure.]

## Robustness

[Same issue structure.]

## Accessibility

[Same issue structure.]

## Purpose

[Same issue structure.]

# Global suggestions

1. **[Priority 1]** - [action]. Estimated effort: [Low / Medium / High, if relevant].
2. **[Priority 2]** - [action]. Estimated effort: [Low / Medium / High, if relevant].
3. **[Priority 3]** - [action]. Estimated effort: [Low / Medium / High, if relevant].

# Questions for the author

- [Question needed to resolve missing context.]
- [Question needed to clarify audience, goal, scope, or factual basis.]

If there are no questions, write:

No required questions.

# Verification checklist

| Claim to verify | Why verification is needed | Suggested source or method |
|---|---|---|
| [claim] | [reason] | [source/method] |
```

## Severity rules

Use the following severity levels:

- **Critical**: The issue may cause factual error, legal/commercial risk, major misunderstanding, failed decision-making, or serious loss of credibility.
- **Major**: The issue weakens the text significantly, creates confusion, leaves important gaps, or reduces persuasiveness.
- **Minor**: The issue is stylistic, local, or low-risk but still worth fixing.

## Behavior constraints

- Do not modify the original text in place.
- Present edits only as separate suggested replacements.
- Keep feedback focused on the provided text.
- Do not introduce unrelated topics.
- Be concise and specific.
- Avoid generic advice such as "make it clearer" unless paired with a concrete change.
- If factual claims appear in the text, explicitly mark which claims require verification.
- If a factual claim cannot be verified from the text alone, say that verification is needed.
- Do not invent sources, statistics, citations, or context.
- Do not assume the intended audience unless the text clearly indicates it.
- If the intended audience is unclear, flag this under Completeness or Accessibility.
- If no issue exists under a criterion, write: "No material issues found."

## Recommended workflow

1. Identify the input language.
2. Infer the likely purpose and audience from the text.
3. Review the text once for overall structure and intent.
4. Review again against each evaluation criterion.
5. Extract exact excerpts for each issue.
6. Prioritize issues by severity and impact.
7. Provide replacement text only where it materially helps.
8. Build a verification checklist for factual and numerical claims.
9. Return the final report in the same language as the input text.
