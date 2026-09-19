# Spec Kit Adapter

This adapter integrates `arch_decision` with Spec Kit.

## Responsibility

`arch_decision` owns:

- architecture decisions
- technology selection
- architecture constraints
- decision status
- complexity budget
- architecture verification

Spec Kit owns:

- specification
- clarification
- implementation planning
- task generation
- implementation workflow
- convergence

## Critical Boundary

Spec Kit MUST consume accepted architecture decisions.

Spec Kit MUST NOT silently replace:

- language
- framework
- database
- infrastructure
- deployment architecture
- authentication architecture

If the accepted architecture cannot satisfy the specification, the agent
must create an architecture change request and return to `arch_decision`.

## Recommended Flow

```text
arch_decision
    |
    | ACCEPTED
    v
Spec Kit Specify
    |
    v
Clarify
    |
    v
Plan
    |
    v
Tasks
    |
    v
Implement
    |
    v
Converge
