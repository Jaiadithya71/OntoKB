# Explaining the ontoKB Ontology Upgrade Through JavaScript and TypeScript

## A useful analogy with an important distinction

The comparison is useful as an intuitive explanation, but it needs a small correction: **the most precise distinction between JavaScript and TypeScript is dynamic typing versus static typing, rather than simply weak typing versus strong typing.**

JavaScript has runtime types and permits implicit type conversion. TypeScript adds static type checking on top of JavaScript. However, TypeScript types are erased during compilation, so external inputs still require runtime validation.

## Applying the analogy to ontoKB and LOGOS

> Upgrading ontoKB to ontoKBv2 can be compared to moving from JavaScript to TypeScript: evolving from relatively flexible data representations to a system with explicit contracts for object types, properties, relationships and operations. LOGOS provides an architectural blueprint for this kind of enterprise ontology.

Two qualifications are essential:

- **ontoKB is not untyped.** It already has entity classifications and relationship constraints. What it lacks is a more complete set of property contracts, Actions, lifecycle rules and access controls.
- **An enterprise ontology goes beyond TypeScript-style type checking.** At runtime, it must control who can perform which operation on which object, under what conditions, how the operation changes state, and how the system records an audit trail. LOGOS contains foundations for these capabilities, but their complete enforcement still needs to be verified through testing.

## Recommended wording for project documentation

> ontoKBv2 aims to strengthen its contracts in a way analogous to moving from JavaScript to TypeScript, and then go further by enforcing those contracts at runtime through permissions, Actions, state transitions and audit records.
