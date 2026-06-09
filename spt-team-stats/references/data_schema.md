# Схема `issues.json`

Нормализованный вход для скриптов. Агент собирает его из Jira/Mattermost через
MCP. Даты — ISO (`YYYY-MM-DD`); `resolved` = `null`, если баг открыт.

```json
{
  "params": {
    "team_name": "Snowdrops",
    "team_tags": ["Snowdrops", "Profiles SNOW", "Passport Flippers"],
    "notify_channels": ["profiles", "#profiles-support"],
    "period_start": "2026-01-01",
    "period_end": "2026-06-04"
  },

  "ours": [
    {"key": "SPT-27611", "created": "2026-01-16", "resolved": "2026-03-27",
     "priority": "P2", "team": "Snowdrops",
     "summary": "Группы объявлений с Базовым +"}
  ],

  "nonbug": [
    {"key": "SPT-8142", "created": "2022-04-27", "resolved": null,
     "type": "Feature", "status": "In Progress",
     "summary": "Возможность удалить подписчиков"}
  ],

  "transferred": [
    {"key": "SPT-28640", "created": "2026-03-10", "resolved": "2026-04-14",
     "priority": "P1", "team": "Messenger Platform",
     "summary": "При подписке на продавца ошибка «Не удалось»"}
  ],

  "resolvers": {
    "SPT-27611": "Olga Kurillo",
    "SPT-27703": "Aleksandr Adamov"
  },

  "handoff": [
    {"key": "SPT-28640", "arrival": "2026-03-20T14:58", "transfer": "2026-04-13T13:07"}
  ]
}
```

Поля по разделам:

- **ours** — баги (`issuetype=Bug`) с текущим тегом команды ∈ team_tags, в
  скоупе периода (заведённые в периоде + бэклог, открытый на старте).
- **nonbug** — не-Bug задачи команды в том же скоупе (Feature, Performance
  degradation, …). В метрики не входят, идут в приложение.
- **transferred** — баги, пришедшие на команду (коммент нотификации) и сейчас
  на другой команде. `team` = принимающая команда.
- **resolvers** — `key → displayName` того, кто перевёл баг в Resolved (по
  changelog). Ключи должны покрывать все закрытые-в-периоде баги из `ours`.
- **handoff** — для переданных: время прихода на наш канал и время передачи
  дальше (полные ISO с временем). Необязательно, но даёт график скорости.
