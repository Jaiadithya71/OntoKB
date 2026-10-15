# Project Execution & Governance Rules

> [!IMPORTANT]
> The following rules are mandatory and unconditionally enforced for ALL AI agents, subagents, and automated workflows operating in this repository.

---

## 1. Strict Prohibition on Large Build Runs
* **Rule**: **NO big build runs without explicit permission from the user.**
* **Mandatory Pre-requisites**: Before running any major build, compiling large modules, running heavy multi-container Docker builds, downloading large foundation models, or executing intensive full-system build pipelines, the agent MUST first provide:
  1. **All relevant technical information** (what tools/compilers/dependencies are involved).
  2. **Estimated cost for building** (compute time, disk space, API inference cost, or cloud charges).
  3. **The entire plan of what will be built** (step-by-step plan, expected duration, and output artifacts).
* **Action**: Present this information and wait for the user's explicit approval before triggering the build.

---

## 2. Strict Prohibition on Automatic Git Push
* **Rule**: **NO automatic push to Git, unless explicitly asked by the user.**
* **Boundary**: Agents may stage (`git add`) and commit (`git commit`) locally if performing requested file modifications, but MUST NEVER execute `git push` (to `origin`, `upstream`, or any remote) proactively or automatically.
* **Action**: Only run `git push` when the user explicitly issues an instruction such as "push to git", "push to remote", or "git push".

---

## 3. Team Structure, Hours Allocation & Strategic Positioning
* **Team Members & Allocation (Option B: 80h per member, 240h total)**:
  * **Pooja**: Project Leader / Tech Lead (80 person-hours)
  * **Jaiadithya**: Core Developer (80 person-hours)
  * **Balachandra**: QA Engineer (80 person-hours)
  * **Total Team Effort**: 240 person-hours across a 9-week sprint (19 Oct 2026 – 18 Dec 2026).
* **Operational Model**:
  * We are developing **Alternative B (Decoupled Action-Centric Runtime & Epistemic Layer)** in parallel with Subteam 1 (Alternative A: Workbench Scaffolding) to evaluate practical enterprise usefulness.
  * **External Secrecy**: Never disclose pre-existing test verification or pre-built code in external proposals or presentations. Testing is presented as standard planned validation in Phase 4.
