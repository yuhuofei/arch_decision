# Architecture — New Project

You are starting a new project architecture workflow.

## Objective

Run the canonical `arch_decision` new-project workflow.

## Mandatory Reading

Before reasoning, read:

- `AGENTS.md`
- `.sdd/CANONICAL.md`
- `.sdd/LAYOUT.md`
- `.sdd/CONVENTIONS.md`
- `.sdd/decision-trees/decision-protocol.md`
- `.sdd/workflows/new-project.md`

Then identify the relevant:

- decision trees
- knowledge domains
- templates
- schemas

## Workflow

Execute the canonical workflow:

1. Discovery
2. Draft Spec
3. Constraint Extraction
4. Constraint Classification
5. Candidate Generation
6. Candidate Elimination
7. Scoring only when permitted
8. Complexity Budget
9. Decision Status
10. Human Confirmation when required
11. Final Accepted Architecture
12. Verification

## Restrictions

Do not write business implementation code.

Do not skip unresolved `REQUIRE_CONFIRMATION`.

Do not convert a preference into a hard constraint unless the canonical
rules explicitly allow it.

Do not treat default technology choices as final conclusions.

Do not create an ADR unless the canonical workflow determines that it is
needed.

## Required Artifacts

At the appropriate point, produce or update:

- `specs/<project>/project-discovery.md`
- `specs/<project>/technology-selection.md`
- `specs/<project>/decision.json`

Create other artifacts only when required by the canonical workflow.

## Completion

Stop when:

- architecture is accepted, or
- a human confirmation is required, or
- the workflow is blocked.

Report the exact decision status and the next required action.
