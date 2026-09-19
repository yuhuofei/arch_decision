# OpenSpec Adapter

This adapter integrates OpenSpec change workflows with
`arch_decision` architecture governance.

## Responsibility

OpenSpec owns:

- change exploration
- change proposal
- change specifications
- change design
- change tasks
- implementation
- archive

`arch_decision` owns:

- architecture impact analysis
- architecture decisions
- technology selection
- architecture constraints
- architecture acceptance
- architecture verification

## Normal Change

```text
OpenSpec Explore
    |
    v
Architecture Impact Check
    |
    | NO IMPACT
    v
OpenSpec Propose
    |
    v
Review
    |
    v
Apply
    |
    v
Archive

