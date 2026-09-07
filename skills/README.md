# AutoBridge Skills — Mandatory Bootstrap & Update Governance

This directory is the cloud source of truth for AutoBridge Research and Writing execution rules.

## Effective skills

- Research / topic selection / evidence collection: `skills/autobridge-research/SKILL.md`
- Writing / localization / content repair: `skills/autobridge-writing/SKILL.md`
- Permanent reviewed lessons: `/LESSONS_LEARNED.md`
- Batch-specific independent review findings: latest `reviews/**/review_handoff*.json`

## Mandatory startup rule for every AI

Before ANY AutoBridge Research or Writing task, the AI MUST:

1. `git pull` the latest `main`.
2. Read this `skills/README.md`.
3. Read the relevant current `SKILL.md` in full.
4. Read `/LESSONS_LEARNED.md` in full.
5. Read the latest applicable Review handoff.
6. Read the current batch Fact Sheet / Source Log / Manifest / Research Handoff as applicable.
7. Record the skill path and Git commit SHA used for the task.

An AI must never rely on an old chat copy of a Skill when the GitHub version is available.

---

# Permanent Skill Update Rule

Project-owner directive: **all confirmed Research/collection and Writing/content problems must remain synchronized into the two GitHub Skills.**

Whenever the project owner or independent Review AI confirms a new systemic issue, rule, failure pattern, quality gate, source rule, language rule, parameter rule, image rule, workflow-leak rule, SEO-content rule, or handoff rule, the responsible AI MUST perform a `SKILL_IMPACT_CHECK`.

## SKILL_IMPACT_CHECK

For every confirmed new rule/finding, classify:

- `RESEARCH_SKILL_IMPACT = YES/NO`
- `WRITING_SKILL_IMPACT = YES/NO`
- `LESSONS_LEARNED_IMPACT = YES/NO`

If `RESEARCH_SKILL_IMPACT=YES`, update:

`skills/autobridge-research/SKILL.md`

If `WRITING_SKILL_IMPACT=YES`, update:

`skills/autobridge-writing/SKILL.md`

If the issue is a reusable reviewed error pattern, also update `/LESSONS_LEARNED.md` after independent Review/project-owner confirmation.

A rule that affects both stages must be reflected in both Skills, with stage-specific wording.

## Same-round propagation

Skill maintenance is part of the SAME task round. Do not defer confirmed rules to “next batch”, “later”, “next time touched”, or chat memory.

A task that discovers and confirms a systemic issue is not fully closed until the applicable Skill update has been committed to GitHub, unless the actor lacks permission to edit Skills. In that case it MUST return:

`SKILL_UPDATE_REQUIRED=true`

with the exact proposed rule and target Skill path.

## No self-promotion of unconfirmed findings

Research AI and Writing AI may propose:

`NEW_LESSON_CANDIDATE`

or:

`SKILL_UPDATE_CANDIDATE`

But they must not convert an unconfirmed hypothesis into a permanent Skill rule by themselves.

Permanent updates require confirmation from either:

- the project owner; or
- the independent Review AI acting within its review responsibility.

## Version discipline

Whenever either Skill is substantively changed:

1. Increase its front-matter `version` (for example `1.0` → `1.1`).
2. Keep the canonical path unchanged (`.../SKILL.md`).
3. Commit the Skill update to GitHub.
4. Record the commit SHA in the task handoff.
5. Future AIs must use the latest `main` version, never a cached chat copy.

## Completion gate

Research completion must include:

- `RESEARCH_SKILL_VERSION_USED`
- `RESEARCH_SKILL_COMMIT_SHA_USED`
- `SKILL_IMPACT_CHECK_DONE=true`
- `SKILL_UPDATE_REQUIRED=true/false`

Writing completion must include:

- `WRITING_SKILL_VERSION_USED`
- `WRITING_SKILL_COMMIT_SHA_USED`
- `SKILL_IMPACT_CHECK_DONE=true`
- `SKILL_UPDATE_REQUIRED=true/false`

If a confirmed rule required a Skill update but the Skill was not updated or explicitly handed off for update, the stage must not claim clean completion.

---

# Responsibility boundaries

Research Skill owner: topic selection, evidence, fact boundaries, source logs, research handoff.

Writing Skill owner: article writing, controlled research patch, localization, content QA, content handoff.

Independent Review AI: confirms/rejects new systemic content rules and issues `REVIEW_PASS / REVISION_REQUIRED / NEEDS_RESEARCH / REJECT` for fixed content versions.

Codex: technical version/hash/preflight/publish gate only after review eligibility and explicit owner authorization.

Neither Research nor Writing AI may grant `REVIEW_PASS`, `PUBLISH_APPROVED=true`, or `HUMAN_REVIEWED=true`.

---

# Short bootstrap instruction for any replacement AI

Use this exact instruction when onboarding a new Research or Writing AI:

> Sync `xysjou/AutoBridge-Content-Pipeline` from GitHub. Read `skills/README.md` first, then read the relevant current `SKILL.md`, `LESSONS_LEARNED.md`, the latest applicable Review handoff, and the current batch evidence files. GitHub is the source of truth; do not rely on older chat copies. Apply `SKILL_IMPACT_CHECK` to every confirmed new issue and keep the applicable Skill synchronized before closing the task.
