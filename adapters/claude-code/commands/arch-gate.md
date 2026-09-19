# Architecture Gate

Determine whether implementation may proceed.

## Mandatory Reading

Read:

- `.sdd/CANONICAL.md`
- `.sdd/decision-trees/decision-protocol.md`
- current `decision.json`
- current `technology-selection.md`
- current verification artifacts

## Gate Conditions

Check:

1. Required architecture decisions exist.
2. No unresolved `BLOCKED` decision exists.
3. No unresolved `REQUIRE_CONFIRMATION` exists.
4. Required human confirmations are recorded.
5. Accepted decisions are internally consistent.
6. Technology selection is consistent with accepted constraints.
7. Complexity budget is satisfied or explicitly approved.
8. Required verification artifacts exist.
9. No architecture-changing requirement is unaccounted for.

## Output

Return exactly one:

`IMPLEMENTATION_ALLOWED`

or

`IMPLEMENTATION_BLOCKED`

If blocked, provide:

- blocking decision
- evidence
- required action

## Critical Rule

Do not resolve a blocking architecture decision inside this command.

The gate evaluates state.

It does not make new architecture decisions.
