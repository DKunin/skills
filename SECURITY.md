# Security Policy

## Reporting

Do not open a public issue for prompt injection payloads, secret exposure, unsafe automation, or any vulnerability that could be abused before remediation.

Report the issue to the repository maintainer through a private channel and include:

- A short summary
- Affected files or skills
- Reproduction steps
- Impact assessment
- Suggested mitigation, if known

## Scope

Treat the following as security-sensitive:

- Embedded credentials or tokens
- Unsafe shell commands in skill workflows or helper scripts
- Instructions that bypass normal safety or approval boundaries
- References that encourage exfiltration of local or private data

## Handling

- Prefer minimally scoped fixes.
- Remove sensitive material from test fixtures and examples.
- Add or update validation when the issue reveals a systemic gap.
