# arch_decision OpenSpec Integration

OpenSpec manages change workflows.

`arch_decision` manages architecture decisions.

## Explore

During Explore:

- inspect the current architecture
- inspect accepted technology decisions
- determine whether the change crosses an architecture boundary

Do not modify code.

## Propose

If there is no architecture impact:

continue normally.

If there is architecture impact:

create an architecture change request instead of silently selecting
another technology.

## Apply

Before Apply:

verify:

- OpenSpec proposal is accepted
- architecture gate passed
- required architecture decisions are accepted
- no blocking decision remains

## Archive

After successful implementation:

archive the change.

If the change modified architecture, ensure the new architecture decision
and decision history are recorded before archive.

## Rule

The existence of an OpenSpec design does not make an architecture decision
accepted.

Architecture acceptance comes from `arch_decision`.
