# North Star

## Win Condition

The student can independently design, write, plan, and apply production Terraform for
AWS from scratch, with state intact after every operation, no runaway costs, and every
change traceable through plan output and version control.

**Derivation:**
- "Independently design and write" — a student who only follows tutorials cannot
  adapt when the environment changes; the win condition requires ownership, not copying.
- "State stays intact" — Terraform's only persistent artifact is the state file; losing
  or corrupting it means reimporting or rebuilding everything by hand. Safety here is
  binary: intact or incident.
- "No runaway cost" — IaC mistakes can provision large resources at scale without a
  human approving each one. Understanding cost impact before `apply` is a production
  safety requirement, not a bonus.
- "Changes are auditable" — plan output and VCS history are the paper trail a team
  uses for change management, incident review, and compliance. If changes are not
  auditable, the IaC is not safe for a shared codebase.

## Tie-Break Rule

When interview ROI and depth of understanding diverge, **interview wins**.

**Derivation:**
- The student's primary goal is to pass a senior DevOps/SRE interview. Deep
  understanding of Terraform internals (provider plugin protocol, go-getter internals,
  state schema versioning) is valuable but has diminishing returns for that goal.
- When session time is limited and two paths compete, the engine routes to the path
  that most directly improves interview performance.
- "Depth of understanding" is not sacrificed arbitrarily — it is ranked second only
  when it conflicts with interview ROI, not routinely.
