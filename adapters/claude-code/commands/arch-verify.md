# Architecture — Verification

Verify that the implemented system conforms to accepted architecture
decisions.

## Mandatory Reading

Read:

- `.sdd/CANONICAL.md`
- `.sdd/TRACEABILITY.md`
- current `decision.json`
- current `technology-selection.md`
- `verification.md`
- relevant source code
- relevant tests

## Verify

Check:

1. Accepted architecture
2. Selected technologies
3. Infrastructure
4. Dependencies
5. Runtime topology
6. Data stores
7. External integrations
8. Security boundaries
9. Complexity budget
10. Requirement traceability
11. Test evidence
12. Architecture drift

## Output

Report:

- PASS
- FAIL
- REVIEW_REQUIRED

For every failure provide:

- decision
- expected state
- actual state
- evidence
- affected files
- recommended action

Do not silently update architecture decisions.

If implementation intentionally differs from accepted architecture,
report:

`ARCHITECTURE_DRIFT`

and require a new architecture decision.
