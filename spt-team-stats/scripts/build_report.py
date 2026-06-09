#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Собирает Confluence storage-XHTML из spt_data.json.
Usage: python3 build_report.py spt_data.json report_body.xhtml [img_suffix]
img_suffix добавляется к именам картинок (для повторной публикации с новыми
именами вложений, т.к. Confluence не перезаписывает вложения)."""
import sys, json

def main(data, outp, suffix=""):
    D = json.load(open(data, encoding="utf-8"))
    P = D["params"]; T = D["totals"]; tn = P["team_name"]
    lf = D["lifetime"]; tr = D["transferred"]; ho = D.get("handoff", {})

    def link(k): return f'<a href="https://jr.avito.ru/browse/{k}">{k}</a>'
    def img(fn, w=900):
        fn = fn.replace(".png", f"{suffix}.png") if suffix else fn
        return f'<ac:image ac:width="{w}"><ri:attachment ri:filename="{fn}"/></ac:image>'
    def esc(s): return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    def panel(macro, title, body):
        return (f'<ac:structured-macro ac:name="{macro}"><ac:parameter ac:name="title">{title}'
                f'</ac:parameter><ac:rich-text-body>{body}</ac:rich-text-body></ac:structured-macro>')

    tags = ", ".join(P.get("team_tags", []))
    Pp = []
    # Оглавление: макрос Confluence TOC по заголовкам h2 (основные пункты).
    Pp.append('<h2>Оглавление</h2>')
    Pp.append('<ac:structured-macro ac:name="toc">'
              '<ac:parameter ac:name="minLevel">2</ac:parameter>'
              '<ac:parameter ac:name="maxLevel">2</ac:parameter>'
              '<ac:parameter ac:name="exclude">Оглавление</ac:parameter>'
              '</ac:structured-macro>')
    Pp.append(f'<p><em>Отчёт сформирован автоматически по данным Jira (проект SPT, '
              f'<strong>issuetype=Bug</strong>) за период {P["period_start"]} – {P["period_end"]}. '
              f'Команда: {esc(tn)} (теги: {esc(tags)}). Не-Bug задачи — см. Приложение В.</em></p>')

    Pp.append(panel("info", "Главный итог",
        f'<p>За период команда закрыла <strong>{T["closed_in"]}</strong> баг-SPT при '
        f'<strong>{T["created_in"]}</strong> заведённых, снизив открытый бэклог с '
        f'{T["open_at_start"]} (пик {T["peak_open"]}) до <strong>{T["open_now"]}</strong>. '
        f'Дополнительно <strong>{T["transferred"]}</strong> багов после анализа переданы в '
        f'другие команды.</p>'))

    Pp.append("<h2>1. Ключевые цифры</h2>")
    Pp.append("<table><tbody>"
        "<tr><th>Показатель</th><th>Значение</th></tr>"
        f'<tr><td>Баг-SPT в работе за период</td><td><strong>{T["scope"]}</strong> '
        f'({T["created_in"]} заведено + {T["backlog"]} бэклог)</td></tr>'
        f'<tr><td>Заведено в периоде</td><td><strong>{T["created_in"]}</strong> — '
        f'{", ".join(f"{k}: {v}" for k, v in D["created_by_team"].items())}</td></tr>'
        f'<tr><td>Закрыто / решено в периоде</td><td><strong>{T["closed_in"]}</strong></td></tr>'
        f'<tr><td>Открытых на старте</td><td>{T["open_at_start"]}</td></tr>'
        f'<tr><td>Пик открытых</td><td>{T["peak_open"]}</td></tr>'
        f'<tr><td>Открытых сейчас</td><td><strong>{T["open_now"]}</strong></td></tr>'
        f'<tr><td>Передано в другие команды</td><td><strong>{T["transferred"]}</strong> '
        f'(закрыто {tr["closed"]}, в работе {tr["open"]})</td></tr>'
        f'<tr><td>Медиана жизни «свежих» багов</td><td><strong>{lf.get("fresh_median")}</strong> дн'
        f' (среднее {lf.get("fresh_avg")})</td></tr>'
        "</tbody></table>")

    Pp.append("<h2>2. Динамика открытых баг-SPT по неделям</h2>")
    Pp.append(f'<p>Открытый бэклог: {T["open_at_start"]} на старте &rarr; {T["open_now"]} сейчас '
              f'(пик {T["peak_open"]}).</p>')
    Pp.append("<p>" + img("chart_burndown.png", 1000) + "</p>")

    Pp.append("<h2>3. Закрытые баги по приоритетам</h2>")
    pc = D["pri_closed"]; pi = D["pri_created"]
    keys = [k for k in ["P0", "P1", "P2", "P3", "P4", "—"] if pi.get(k) or pc.get(k)]
    Pp.append("<table><tbody><tr><th>Приоритет</th><th>Заведено</th><th>Закрыто</th></tr>"
        + "".join(f"<tr><td>{k}</td><td>{pi.get(k,0)}</td><td>{pc.get(k,0)}</td></tr>" for k in keys)
        + f'<tr><td><strong>Итого</strong></td><td><strong>{sum(pi.values())}</strong></td>'
        f'<td><strong>{sum(pc.values())}</strong></td></tr></tbody></table>')
    Pp.append("<p>" + img("chart_priority.png", 760) + "</p>")

    Pp.append("<h2>4. Время жизни багов</h2>")
    Pp.append("<table><tbody><tr><th>Категория</th><th>Медиана, дни</th><th>Среднее, дни</th><th>N</th></tr>"
        f'<tr><td>Свежие (заведены и закрыты в периоде)</td><td><strong>{lf.get("fresh_median")}</strong></td>'
        f'<td>{lf.get("fresh_avg")}</td><td>{lf.get("fresh_n")}</td></tr>'
        f'<tr><td>Легаси (старый бэклог)</td><td>{lf.get("legacy_median")}</td>'
        f'<td>{lf.get("legacy_avg")}</td><td>{lf.get("legacy_n")}</td></tr></tbody></table>')
    Pp.append("<p>" + img("chart_lifetime.png", 1000) + "</p>")
    if lf.get("age_start_avg") is not None and lf.get("age_now_avg") is not None:
        Pp.append(panel("note", "Зона внимания",
            f'<p>Средний возраст открытых багов: {lf["age_start_avg"]:.0f} дн на старте &rarr; '
            f'{lf["age_now_avg"]:.0f} дн сейчас. Если он растёт при снижении числа открытых — '
            f'в бэклоге задержались «долгожители», их стоит ревизовать на закрытие / Won’t Fix.</p>'))

    Pp.append("<h2>5. Кто закрывал баги (перевод в Resolved)</h2>")
    Pp.append('<p>«Закрывший» — тот, кто перевёл SPT в статус Resolved (по истории задачи), '
              'а не текущий assignee. Обычно это QA, верифицирующий фикс.</p>')
    ppl = D["people"]
    Pp.append("<table><tbody><tr><th>Закрыл (перевёл в Resolved)</th><th>Кол-во</th></tr>"
        + "".join(f"<tr><td>{esc(n)}</td><td>{c}</td></tr>" for n, c in sorted(ppl.items(), key=lambda x: -x[1]))
        + f'<tr><td><strong>Итого</strong></td><td><strong>{sum(ppl.values())}</strong></td></tr></tbody></table>')
    Pp.append("<p>" + img("chart_people.png", 820) + "</p>")

    Pp.append("<h2>6. Баги, переданные в другие команды</h2>")
    Pp.append(f'<p>Команда — точка входа профильных багов: бот уведомляет наш канал, мы анализируем '
              f'и маршрутизируем баг в ответственную команду. Передано <strong>{T["transferred"]}</strong> '
              f'багов в <strong>{len(tr["by_team"])}</strong> команд; закрыто {tr["closed"]}, в работе {tr["open"]}.</p>')
    pbt = tr["by_pri"]
    Pp.append("<table><tbody><tr><th>Приоритет</th><th>Передано</th></tr>"
        + "".join(f"<tr><td>{k}</td><td>{pbt.get(k,0)}</td></tr>" for k in ["P0", "P1", "P2", "P3", "P4", "—"] if k in pbt)
        + f'<tr><td><strong>Итого</strong></td><td><strong>{T["transferred"]}</strong></td></tr></tbody></table>')
    Pp.append("<p>" + img("chart_transferred.png", 820) + "</p>")

    if ho:
        Pp.append("<h2>7. Скорость передачи багов</h2>")
        Pp.append('<p>Время от поступления бага к нам до передачи в ответственную команду — '
                  'показатель скорости триажа.</p>')
        lblm = {"01": "Январь", "02": "Февраль", "03": "Март", "04": "Апрель", "05": "Май",
                "06": "Июнь", "07": "Июль", "08": "Август", "09": "Сентябрь", "10": "Октябрь", "11": "Ноябрь", "12": "Декабрь"}
        Pp.append("<table><tbody><tr><th>Месяц поступления</th><th>Медиана, дни</th><th>Среднее, дни</th><th>Кол-во</th></tr>"
            + "".join(f'<tr><td>{lblm.get(m[-2:], m)}</td><td>{ho[m]["median"]}</td>'
                      f'<td>{ho[m]["avg"]}</td><td>{ho[m]["n"]}</td></tr>' for m in sorted(ho))
            + "</tbody></table>")
        Pp.append("<p>" + img("chart_handoff.png", 820) + "</p>")

    Pp.append("<h2>8. Методология и оговорки</h2>")
    Pp.append("<ul>"
        "<li><strong>Источник:</strong> Jira, проект SPT, issuetype=Bug. Команда = поле «Avito.People "
        f"Unit Teams» (cf 22019) ∈ {{{esc(tags)}}}. Приоритет = cf 12170.</li>"
        "<li><strong>«Закрыто»</strong> = есть дата резолюции (resolutiondate) в периоде.</li>"
        "<li><strong>«Переданные»</strong> = баги, пришедшие на команду (бот-коммент «Нотификация "
        f'отправлена: {esc(", ".join(P.get("notify_channels", [])))}»), сейчас закреплённые за другой '
        "командой.</li>"
        "<li><strong>«Закрывший»</strong> = автор перехода статуса в Resolved (не assignee).</li>"
        "<li>Не-Bug задачи (Feature, Performance degradation) исключены — см. Приложение В.</li>"
        "</ul>")

    def table(title, header, rows):
        Pp.append(f"<h2>{title}</h2>")
        Pp.append("<table><tbody><tr>" + "".join(f"<th>{h}</th>" for h in header) + "</tr>"
                  + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
                  + "</tbody></table>")

    table(f"Приложение A. Открытые баги ({T['open_now']})",
          ["Задача", "Приоритет", "Описание", "Тег команды", "Заведена"],
          [[link(k), p or "—", esc(s), esc(t), c] for k, p, t, c, s in D["open_list"]])
    table(f"Приложение Б. Переданные баги ({T['transferred']})",
          ["Задача", "Приоритет", "Описание", "Принимающая команда", "Статус"],
          [[link(k), p or "—", esc(s), esc(t), stt] for k, p, t, stt, s in D["transferred_list"]])
    if D.get("nonbug_list"):
        table(f"Приложение В. Не-Bug задачи ({len(D['nonbug_list'])}, в статистику не входят)",
              ["Задача", "Тип", "Статус", "Заведена", "Описание"],
              [[link(k), esc(ty), esc(stt), c, esc(s)] for k, ty, stt, c, s in D["nonbug_list"]])

    html = "\n".join(Pp)
    open(outp, "w", encoding="utf-8").write(html)
    print("report ->", outp, len(html), "байт")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 build_report.py spt_data.json report_body.xhtml [img_suffix]"); sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
