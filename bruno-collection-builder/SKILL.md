---
name: "bruno-collection-builder"
description: "Create and update Bruno API collections from endpoint lists, OpenAPI specs, cURL commands, or existing Bruno folders. Use when Codex needs to scaffold a Bruno collection, add requests or folders, define environments, auth, docs, scripts, or tests in Bruno YAML or .bru format."
---

# Purpose

Use this skill to create or modify Bruno API collections directly on disk.

# Inputs

- Target directory for the collection
- Source material such as an OpenAPI document, cURL commands, endpoint notes, or an existing Bruno collection
- Preferred Bruno format if specified: OpenCollection YAML (`.yml`) or legacy Bru (`.bru`)
- Environment, auth, variable, and test requirements

# Workflow

1. Inspect the target path before editing. Detect `opencollection.yml` for YAML collections and `bruno.json` for legacy Bru collections. Preserve the existing format and folder layout.
2. If the collection is new and the user did not specify a format, default to YAML. Use `.bru` only when the user requests it or compatibility with an older Bruno workflow matters.
3. Normalize the source material into a concrete plan: collection name, folder map, environments, shared auth, request list, URLs, params, bodies, and assertions. Do not start writing files until each request has a stable name, method, and path.
4. If you are creating a new collection, run `scripts/scaffold_collection.py` to create the root files and optional environment stubs.
5. Read `references/format-guide.md` before authoring or editing root files, folder metadata, or environment files.
6. Read `references/request-templates.md` when adding requests. Keep shared headers and auth at the highest sensible scope and use `inherit` below that.
7. Prefer variables such as `{{baseUrl}}`, `{{token}}`, or `{{clientId}}` over hard-coded environment values. Put secrets in environment files or placeholders, not inline in committed requests.
8. If the input is OpenAPI, Postman, Insomnia, or WSDL and a mechanical import is faster than hand-authoring, read `references/converters.md` and decide whether to use Bruno's official converter tooling.
9. Validate the result statically: correct root filename, matching file extensions, folder metadata present, reasonable `seq` ordering within siblings, and no invented auth or request details. If Bruno CLI or app automation is already available, use it for an extra sanity check.

# Output Contract

- Create or update a runnable Bruno collection on disk.
- Preserve or explicitly state the chosen file format.
- Leave obvious placeholders only where the source material is incomplete.
- Report any assumptions, missing endpoints, or secret values that still need user input.

# Guardrails

- Avoid unsupported claims.
- Do not mix YAML and `.bru` in a new collection unless the user asks for a mixed tree or the existing collection already mixes formats.
- Do not invent endpoints, auth flows, payload schemas, or tests that are not supported by the provided source material.
- Do not hard-code secrets into request files.
- Do not rename or reorder an existing collection gratuitously; preserve the current layout unless the user asked for a restructure.

# References

- Read `references/format-guide.md` for collection layout, root files, and environment syntax.
- Read `references/request-templates.md` for minimal folder, request, and environment templates in both formats.
- Read `references/converters.md` when starting from OpenAPI, Postman, Insomnia, or WSDL inputs.
- Use `scripts/scaffold_collection.py` to create a new collection skeleton before filling request files by hand.
