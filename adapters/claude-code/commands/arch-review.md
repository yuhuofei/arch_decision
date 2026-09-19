# Architecture — Review

Review the current architecture decisions.

## Objective

Identify unresolved, contradictory, stale, or unsupported decisions.

## Mandatory Reading

Read:

- `.sdd/CANONICAL.md`
- `.sdd/decision-trees/decision-protocol.md`
- current `decision.json`
- current `technology-selection.md`
- relevant project discovery

## Review

Check:

1. Constraint consistency
2. Evidence completeness
3. Alternative coverage
4. Decision status correctness
5. Complexity budget
6. Cost semantics
7. Version semantics
8. Review triggers
9. Decision history
10. Architecture/spec consistency

## Important

This is a review operation.

Do not silently rewrite decisions.

If a decision needs to change, report:

`ARCHITECTURE_CHANGE_REQUIRED`

and explain why.

## Output

Produce:

- findings
- severity
- evidence
- affected decision
- canonical rule reference
- recommended next action

Do not implement code.
