# Поля Jira (проект SPT) и JQL-шаблоны

## Кастомные поля

| Поле | ID | Тип / оператор | Пример значения |
|---|---|---|---|
| Avito.People Unit Teams (тег команды) | `customfield_22019` / `cf[22019]` | текст, только `~` | `Snowdrops`, `Profiles SNOW`, `Passport Flippers`, `Ahaha`, `Passport AvIDo` |
| Юнит | `customfield_12113` / `cf[12113]` | select, `=` | `AvitoID` |
| Priority for Bug | `customfield_12170` / `cf[12170]` | select | `P0`, `P1`, `P2`, `P3`, `P4` |

Примечания:
- `cf[22019]` НЕ поддерживает `=` и `WAS` (история по нему недоступна). Только `~`.
- У задачи может быть несколько исторических тегов команды (переименования) —
  обязательно перечисли все в `team_tags`.
- Поле «Команда» НЕ пишется в changelog, поэтому факт передачи по нему не
  отследить — используй метод с комментариями (см. methodology.md).

## Инструмент

`mcp__mcp-hub__call_tool` → `server="mcp-jira"`, `tool="jira_get_filter_result"`,
`arguments={"jql": "...", "fields": ["key","created", ...], "pageSize": 50, "page": 1}`.
Для истории: `tool="jira_get_issue"`, `arguments={"issueKey":"SPT-X","expandChangelog":true}`.
Комментарии: `tool="jira_get_comments"`, `arguments={"issueKey":"SPT-X"}`.

`pageSize` ≤ 50 — пагинируй при `totalCount` > 50. Большие ответы сохраняются в
файл (тогда Grep/Read по файлу).

## JQL-шаблоны

Обозначения: `<TAGS>` = `(cf[22019] ~ "Snowdrops" OR cf[22019] ~ "Profiles SNOW" OR ...)`,
`<S>`/`<E>` = period_start/end.

**Наши баги, заведённые в периоде:**
```
project = SPT AND issuetype = Bug AND <TAGS> AND created >= <S> AND created <= <E> ORDER BY created ASC
```

**Наш бэклог (открыт на старте):**
```
project = SPT AND issuetype = Bug AND <TAGS> AND created < <S> AND (resolutiondate >= <S> OR resolution is EMPTY) ORDER BY created ASC
```

**Не-Bug задачи команды в скоупе:**
```
project = SPT AND issuetype != Bug AND <TAGS> AND (created >= <S> OR resolutiondate >= <S> OR resolution is EMPTY) ORDER BY created ASC
```
(поля: + `issuetype`, `status`)

**Кандидаты в «переданные» (пришли на наш канал):**
```
project = SPT AND issuetype = Bug AND comment ~ "Нотификация отправлена <CHANNEL>" AND created >= <S> ORDER BY created ASC
```
Из результата переданные = те, у кого текущий `customfield_22019` НЕ входит в
team_tags. Поля: `key, created, resolutiondate, customfield_22019, customfield_12170`.

**Закрытые в периоде (для списка ключей под resolver-сбор):**
```
project = SPT AND issuetype = Bug AND <TAGS> AND resolutiondate >= <S> AND resolutiondate <= <E> ORDER BY resolutiondate ASC
```

**Summary пачкой по списку ключей:**
```
project = SPT AND key in (SPT-1, SPT-2, ...) ORDER BY key ASC
```
(поля: `key, summary`)
