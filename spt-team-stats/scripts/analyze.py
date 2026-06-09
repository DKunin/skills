#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Считает агрегаты по issues.json -> spt_data.json. Сети не требует.
Usage: python3 analyze.py issues.json spt_data.json"""
import sys, json, datetime as dt, statistics as st
from collections import Counter, defaultdict

def d(s):
    return dt.date.fromisoformat(s) if s else None

def main(inp, outp):
    D = json.load(open(inp, encoding="utf-8"))
    P = D["params"]
    start = d(P["period_start"]); end = d(P["period_end"])
    ours = [(x["key"], d(x["created"]), d(x.get("resolved")), x.get("priority"),
             x.get("team"), x.get("summary", "")) for x in D.get("ours", [])]
    trans = [(x["key"], d(x["created"]), d(x.get("resolved")), x.get("priority"),
              x.get("team"), x.get("summary", "")) for x in D.get("transferred", [])]
    resolvers = D.get("resolvers", {})

    created_in = [x for x in ours if x[1] and x[1] >= start]
    backlog = [x for x in ours if x[1] and x[1] < start]
    closed_in = [x for x in ours if x[2] and start <= x[2] <= end]
    open_now = [x for x in ours if x[2] is None]
    open_at_start = [x for x in ours if x[1] and x[1] < start and (x[2] is None or x[2] >= start)]

    def pri(items): return dict(Counter((x[3] or "—") for x in items))

    # время жизни
    def days(a, b): return (b - a).days
    life = [(k, days(c, r), c, r) for k, c, r, p, t, s in closed_in]
    fresh = [l for k, l, c, r in life if c >= start]
    legacy = [l for k, l, c, r in life if c < start]
    month_life = defaultdict(list)
    for k, l, c, r in life:
        month_life[r.strftime("%Y-%m")].append(l)

    # недельный burndown
    mons = []
    cur = start - dt.timedelta(days=start.weekday())
    while cur <= end:
        mons.append(cur); cur += dt.timedelta(days=7)
    burndown = []
    for m in mons:
        wend = min(m + dt.timedelta(days=6), end)
        cnt = sum(1 for x in ours if x[1] and x[1] <= wend and (x[2] is None or x[2] > wend))
        op = sum(1 for x in ours if x[1] and m <= x[1] <= wend)
        cl = sum(1 for x in ours if x[2] and m <= x[2] <= wend)
        burndown.append((str(wend), cnt, op, cl))

    # скорость передачи
    ho_month = defaultdict(list)
    for h in D.get("handoff", []):
        a = dt.datetime.fromisoformat(h["arrival"]); t = dt.datetime.fromisoformat(h["transfer"])
        ho_month[a.strftime("%Y-%m")].append((t - a).total_seconds() / 86400.0)
    handoff = {m: {"n": len(v), "median": round(st.median(v), 2), "avg": round(st.mean(v), 2)}
               for m, v in ho_month.items()}

    tr_closed = [x for x in trans if x[2]]
    out = {
        "params": P,
        "totals": {"scope": len(ours), "created_in": len(created_in),
                   "backlog": len(backlog), "closed_in": len(closed_in),
                   "open_now": len(open_now), "open_at_start": len(open_at_start),
                   "transferred": len(trans), "peak_open": max((b[1] for b in burndown), default=0)},
        "created_by_team": dict(Counter(x[4] for x in created_in)),
        "pri_created": pri(created_in), "pri_closed": pri(closed_in), "pri_open": pri(open_now),
        "people": dict(Counter(resolvers.values())),
        "lifetime": {
            "all_median": round(st.median([l for _, l, _, _ in life]), 1) if life else None,
            "fresh_median": round(st.median(fresh), 1) if fresh else None,
            "fresh_avg": round(st.mean(fresh), 1) if fresh else None, "fresh_n": len(fresh),
            "legacy_median": round(st.median(legacy), 1) if legacy else None,
            "legacy_avg": round(st.mean(legacy), 1) if legacy else None, "legacy_n": len(legacy),
            "age_start_avg": round(st.mean([days(x[1], start) for x in open_at_start]), 0) if open_at_start else None,
            "age_now_avg": round(st.mean([days(x[1], end) for x in open_now]), 0) if open_now else None,
        },
        "month_life": {m: {"n": len(v), "median": round(st.median(v), 1)} for m, v in month_life.items()},
        "burndown": burndown,
        "transferred": {"by_team": dict(Counter(x[4] for x in trans)),
                        "by_pri": pri(trans), "closed": len(tr_closed),
                        "open": len(trans) - len(tr_closed)},
        "handoff": handoff,
        # списки для таблиц-приложений
        "open_list": [[k, p, t, c.isoformat(), s] for k, c, r, p, t, s in
                      sorted(open_now, key=lambda x: (x[3] or "Z", x[1] or dt.date.max))],
        "transferred_list": [[k, p, t, "закрыт" if r else "в работе", s] for k, c, r, p, t, s in
                             sorted(trans, key=lambda x: (x[3] or "Z", x[1] or dt.date.max))],
        "nonbug_list": [[x["key"], x.get("type", ""), x.get("status", ""), x.get("created", ""),
                         x.get("summary", "")] for x in sorted(D.get("nonbug", []),
                         key=lambda x: (x.get("type", ""), x.get("created", "")))],
    }
    json.dump(out, open(outp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # сводка + сверка
    T = out["totals"]
    print(f"Команда: {P['team_name']} | период {P['period_start']}..{P['period_end']}")
    print(f"Scope (Bug): {T['scope']} = заведено {T['created_in']} + бэклог {T['backlog']}")
    print(f"Закрыто {T['closed_in']} | открыто сейчас {T['open_now']} | "
          f"на старте {T['open_at_start']} (пик {T['peak_open']})")
    print(f"Передано: {T['transferred']} (закрыто {out['transferred']['closed']}, "
          f"открыто {out['transferred']['open']})")
    print("Приоритеты закрытых:", out["pri_closed"])
    print("По закрывшим (Resolved):", out["people"])
    assert T["closed_in"] + T["open_now"] == T["scope"], "closed+open != scope!"
    s_people = sum(out["people"].values())
    if s_people != T["closed_in"]:
        print(f"  ВНИМАНИЕ: сумма по людям ({s_people}) != закрыто ({T['closed_in']}) — "
              "проверь, что resolvers покрывают все закрытые баги.")
    print("Сверка scope OK. ->", outp)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 analyze.py issues.json spt_data.json"); sys.exit(1)
    main(sys.argv[1], sys.argv[2])
