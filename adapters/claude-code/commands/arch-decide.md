# Architecture — Decision

Execute the canonical architecture and technology selection workflow.

## Mandatory Reading

Read:

- `.sdd/CANONICAL.md`
- `.sdd/decision-trees/decision-protocol.md`
- relevant decision trees
- relevant knowledge domains
- current project discovery
- current decision artifacts

## Objective

Determine the simplest architecture and technology choices that satisfy
the accepted requirements and constraints.

## Decision Process

Follow the canonical sequence:

1. Establish requirements
2. Identify constraints
3. Classify constraints
4. Generate reasonable candidates
5. Eliminate candidates using hard constraints
6. Apply direct decision rules
7. Score only when permitted
8. Check complexity budget
9. Determine decision status
10. Record evidence and alternatives
11. Request human confirmation when required

## Important

Do not:

- use popularity as a decision rule
- treat defaults as conclusions
- promote preferences to hard constraints
- add infrastructure without justification
- silently change accepted decisions

## Output

Update:

- `technology-selection.md`
- `decision.json`

Record:

- evidence
- constraints
- alternatives
- rejected candidates
- scores when applicable
- deferred decisions
- review triggers
- decision history

## Completion

Stop at:

- ACCEPTED
- REQUIRE_CONFIRMATION
- BLOCKED

according to canonical decision semantics.
