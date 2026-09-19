# Architecture Change Request

## Purpose

An Architecture Change Request is created when an external workflow
discovers that the currently accepted architecture may no longer satisfy
the current requirements.

## Trigger Conditions

Create this request when a change requires:

- new infrastructure
- different database
- different backend/frontend framework
- different deployment topology
- different service boundary
- different authentication architecture
- different data ownership
- significant complexity increase
- a previously rejected technology
- an architectural assumption that is no longer valid

## Required Fields

### Change

Describe the requested change.

### Current Architecture

Reference the current accepted architecture decision.

### New Requirement

Describe the requirement causing the conflict.

### Conflict

Explain why the current architecture may not satisfy the requirement.

### Evidence

Provide repository or requirement evidence.

### Impact

Describe affected:

- architecture
- technology
- infrastructure
- cost
- complexity
- security
- operations

### Required Decision

State what architecture decision must be revisited.

## Rule

This document requests a decision.

It does not make the decision.

The final decision must be recorded through the canonical `arch_decision` workflow.
