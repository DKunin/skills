# Bruno Collection Format Guide

## Format Selection

- Preserve the format that already exists in the target collection.
- Detect YAML collections by `opencollection.yml`.
- Detect legacy Bru collections by `bruno.json`. `collection.bru` is common in newer Bru collections but older collections may omit it.
- Default new collections to YAML unless the user explicitly asks for `.bru` or an older Bruno workflow requires it.
- Avoid mixing `.yml` and `.bru` in a brand new collection. Mixed trees are acceptable only when you are editing an existing migration-in-progress collection.

## YAML Collection Layout

Use this layout for OpenCollection YAML:

```text
my-collection/
|- opencollection.yml
|- environments/
|  `- development.yml
|- users/
|  |- folder.yml
|  |- get-users.yml
|  `- create-user.yml
`- healthcheck.yml
```

Minimal `opencollection.yml`:

```yaml
opencollection: "1.0.0"
info:
  name: "Example API"

extensions:
  bruno:
    ignore:
      - node_modules
      - .git
```

Notes:

- Use `.yml`, not `.yaml`, to match Bruno's examples and fixtures.
- Folder metadata lives in `folder.yml`.
- Requests are individual `.yml` files beside `folder.yml`.
- Environment files live under `environments/`.

## Bru Collection Layout

Use this layout for legacy Bru collections:

```text
my-collection/
|- bruno.json
|- collection.bru
|- environments/
|  `- development.bru
|- users/
|  |- folder.bru
|  |- get-users.bru
|  `- create-user.bru
`- healthcheck.bru
```

Minimal `bruno.json`:

```json
{
  "version": "1",
  "name": "Example API",
  "type": "collection",
  "ignore": [
    "node_modules",
    ".git"
  ]
}
```

Minimal `collection.bru`:

```bru
docs {
  # Example API
}
```

Notes:

- `collection.bru` is the collection-level file for shared docs, headers, auth, vars, scripts, and tests.
- Older collections may have only `bruno.json`; preserve that shape if you are editing in place.
- Folder metadata lives in `folder.bru`.

## Environment Files

YAML environment files use a top-level `name` and `variables` array:

```yaml
name: "Development"
variables:
  - name: baseUrl
    value: "https://api.dev.example.com"
  - name: token
    value: "CHANGEME"
```

Bru environment files use a `vars` block:

```bru
vars {
  baseUrl: https://api.dev.example.com
  token: CHANGEME
}
```

Use environment files for hostnames, credentials, and other deployment-specific values. Do not hard-code secrets in request files.

## Folder And Request Rules

- Keep one request per file.
- Use a stable display name inside the file and a filesystem-safe filename outside it.
- Preserve existing `seq` values when editing an established collection.
- For new siblings, use increasing `seq` values in the order the user will expect in Bruno.
- Put shared auth and headers at the highest sensible scope, then use `inherit` at lower levels.
- Prefer `{{baseUrl}}` and similar variables over literal hosts.

## Safe Editing Order

1. Confirm the collection format and root file.
2. Confirm the folder tree and request names.
3. Add or update environment files.
4. Add folder metadata files.
5. Add request files.
6. Recheck extensions, filenames, and `seq` ordering before returning.
