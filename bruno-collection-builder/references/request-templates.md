# Bruno Request Templates

Use these as starting points, then tailor params, bodies, headers, and tests to the actual API.

## YAML Templates

### Folder

```yaml
info:
  name: "Users"
  seq: 1
```

### GET Request

```yaml
info:
  name: "Get Users"
  type: http
  seq: 1

http:
  method: GET
  url: "{{baseUrl}}/users"
  auth: inherit
  params:
    - name: page
      value: "1"
      type: query

runtime:
  scripts:
    - type: tests
      code: |-
        test("returns 200", function() {
          expect(res.status).to.equal(200);
        });
```

### POST JSON Request

```yaml
info:
  name: "Create User"
  type: http
  seq: 2

http:
  method: POST
  url: "{{baseUrl}}/users"
  auth: inherit
  headers:
    - name: Content-Type
      value: application/json
  body:
    type: json
    data: |-
      {
        "name": "Jane Example",
        "email": "jane@example.com"
      }

runtime:
  scripts:
    - type: tests
      code: |-
        test("returns 201", function() {
          expect(res.status).to.equal(201);
        });
```

### Environment

```yaml
name: "Development"
variables:
  - name: baseUrl
    value: "https://api.dev.example.com"
  - name: token
    value: "CHANGEME"
```

## Bru Templates

### Folder

```bru
meta {
  name: Users
  seq: 1
}
```

### GET Request

```bru
meta {
  name: Get Users
  type: http
  seq: 1
}

get {
  url: {{baseUrl}}/users
  body: none
  auth: inherit
}

tests {
  test("returns 200", function() {
    expect(res.status).to.equal(200);
  });
}
```

### POST JSON Request

```bru
meta {
  name: Create User
  type: http
  seq: 2
}

post {
  url: {{baseUrl}}/users
  body: json
  auth: inherit
}

headers {
  Content-Type: application/json
}

body:json {
  {
    "name": "Jane Example",
    "email": "jane@example.com"
  }
}

tests {
  test("returns 201", function() {
    expect(res.status).to.equal(201);
  });
}
```

### Environment

```bru
vars {
  baseUrl: https://api.dev.example.com
  token: CHANGEME
}
```

## Editing Checklist

- Match the surrounding format and extension exactly.
- Keep auth at the collection or folder level when it is shared broadly.
- Use `inherit` if a parent already owns auth.
- Prefer placeholders like `CHANGEME` or `{{token}}` over inline secrets.
- Keep request tests small and directly tied to the source material.
