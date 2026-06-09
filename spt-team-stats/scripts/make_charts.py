#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Рисует PNG-графики из spt_data.json.
Usage: python3 make_charts.py spt_data.json <output_dir>
Требует matplotlib (pip install matplotlib --break-system-packages)."""
import sys, json, os, datetime as dt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.titlesize"] = 13
plt.rcParams["axes.titleweight"] = "bold"
BLUE="#2D6CDF"; GREEN="#2BA84A"; RED="#E2533B"; GREY="#9AA0A6"; ORANGE="#F2A33C"; PURPLE="#7E57C2"

def save(fig, path):
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)

def main(data, outdir):
    D = json.load(open(data, encoding="utf-8"))
    tn = D["params"].get("team_name", "команды")
    os.makedirs(outdir, exist_ok=True)
    p = lambda n: os.path.join(outdir, n)

    # 1. burndown
    bd = D["burndown"]
    weeks = [dt.date.fromisoformat(w) for w, _, _, _ in bd]
    openc = [c for _, c, _, _ in bd]; opened = [o for _, _, o, _ in bd]; closed = [c for _, _, _, c in bd]
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar(weeks, opened, width=4, color=GREEN, alpha=.55, label="Заведено за неделю")
    ax.bar(weeks, [-c for c in closed], width=4, color=RED, alpha=.55, label="Закрыто за неделю")
    ax.plot(weeks, openc, color=BLUE, lw=2.6, marker="o", ms=4, label="Открыто SPT (накопл.)")
    for x, y in zip(weeks, openc):
        ax.annotate(str(y), (x, y), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=7, color=BLUE)
    ax.axhline(0, color="#444", lw=.8)
    ax.set_title(f"Динамика открытых баг-SPT команды {tn} по неделям")
    ax.set_ylabel("кол-во SPT"); ax.legend(loc="upper right", fontsize=9, framealpha=.9)
    ax.grid(axis="y", alpha=.25); fig.autofmt_xdate(); save(fig, p("chart_burndown.png"))

    # 2. lifetime
    lf = D["lifetime"]; ml = D["month_life"]; months = sorted(ml)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw={"width_ratios": [1, 1.3]})
    a1.bar(["Свежие SPT\n(в периоде)", "Легаси\n(старый бэклог)"],
           [lf.get("fresh_median") or 0, lf.get("legacy_median") or 0], color=[GREEN, GREY], width=.6)
    a1.set_title("Медианное время жизни\nзакрытых SPT, дни"); a1.set_ylabel("дни")
    for i, v in enumerate([lf.get("fresh_median") or 0, lf.get("legacy_median") or 0]):
        a1.annotate(f"{v:.0f} дн", (i, v), textcoords="offset points", xytext=(0, 5), ha="center", fontweight="bold")
    a1.grid(axis="y", alpha=.25)
    med = [ml[m]["median"] for m in months]; ns = [ml[m]["n"] for m in months]
    a2.bar(months, med, color=BLUE, alpha=.8, width=.6); a2.plot(months, med, color=RED, lw=2, marker="o")
    for i, (v, n) in enumerate(zip(med, ns)):
        a2.annotate(f"{v:.0f}\n(n={n})", (i, v), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=8)
    a2.set_title("Медиана времени до закрытия\nпо месяцу закрытия, дни"); a2.set_ylabel("дни")
    a2.grid(axis="y", alpha=.25); save(fig, p("chart_lifetime.png"))

    # 3. priorities
    order = ["P0", "P1", "P2", "P3", "P4", "—"]
    pc = D["pri_closed"]; pi = D["pri_created"]
    order = [k for k in order if pi.get(k) or pc.get(k)]
    x = np.arange(len(order)); w = .38
    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.bar(x - w/2, [pi.get(k, 0) for k in order], w, label="Заведено в периоде", color=BLUE, alpha=.85)
    ax.bar(x + w/2, [pc.get(k, 0) for k in order], w, label="Закрыто в периоде", color=GREEN, alpha=.85)
    ax.set_xticks(x); ax.set_xticklabels(order); ax.set_title("SPT по приоритетам: заведено vs закрыто")
    ax.set_ylabel("кол-во"); ax.legend(); ax.grid(axis="y", alpha=.25)
    for i, k in enumerate(order):
        if pi.get(k): ax.annotate(str(pi[k]), (i - w/2, pi[k]), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=8)
        if pc.get(k): ax.annotate(str(pc[k]), (i + w/2, pc[k]), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=8)
    save(fig, p("chart_priority.png"))

    # 4. people (кто перевёл в Resolved)
    ppl = D["people"]; items = sorted(ppl.items(), key=lambda x: x[1])
    names = [k for k, v in items]; vals = [v for k, v in items]
    fig, ax = plt.subplots(figsize=(9, max(3.5, .5 * len(names) + 2)))
    bars = ax.barh(names, vals, color=PURPLE, alpha=.85)
    ax.set_title(f"Закрыто SPT по людям (перевод в Resolved), {tn}"); ax.set_xlabel("кол-во закрытых SPT")
    for b, v in zip(bars, vals):
        ax.annotate(str(v), (b.get_width(), b.get_y() + b.get_height()/2), textcoords="offset points",
                    xytext=(5, 0), va="center", fontweight="bold")
    ax.grid(axis="x", alpha=.25); save(fig, p("chart_people.png"))

    # 5. transferred
    tr = D["transferred"]; total = tr["closed"] + tr["open"]
    fig, (b1, b2) = plt.subplots(1, 2, figsize=(10, 4.3), gridspec_kw={"width_ratios": [1.5, 1]})
    bp = tr["by_pri"]; po = ["P0", "P1", "P2", "P3", "P4", "—"]
    cols = {"P0": "#8E1B0E", "P1": "#C0392B", "P2": ORANGE, "P3": "#F4C542", "P4": "#7FB069", "—": GREY}
    xs = [q for q in po if q in bp]
    b1.bar(xs, [bp[q] for q in xs], color=[cols[q] for q in xs])
    b1.set_title(f"Переданные в другие команды: {total} баг-SPT\nпо приоритетам"); b1.set_ylabel("кол-во")
    b1.grid(axis="y", alpha=.25)
    for i, q in enumerate(xs):
        b1.annotate(str(bp[q]), (i, bp[q]), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=9, fontweight="bold")
    if total:
        b2.pie([tr["closed"], tr["open"]], labels=[f"Закрыто\n({tr['closed']})", f"В работе\n({tr['open']})"],
               autopct="%1.0f%%", colors=[GREEN, GREY], startangle=90, textprops={"fontsize": 10})
    b2.set_title("Статус переданных"); save(fig, p("chart_transferred.png"))

    # 6. handoff
    ho = D.get("handoff", {})
    if ho:
        lbl = {"01": "Янв", "02": "Фев", "03": "Март", "04": "Апрель", "05": "Май",
               "06": "Июнь", "07": "Июль", "08": "Авг", "09": "Сен", "10": "Окт", "11": "Нояб", "12": "Дек"}
        ms = sorted(ho)
        med = [ho[m]["median"] for m in ms]; avg = [ho[m]["avg"] for m in ms]; ns = [ho[m]["n"] for m in ms]
        x = np.arange(len(ms)); w = .38
        fig, ax = plt.subplots(figsize=(9, 4.8))
        ax.bar(x - w/2, med, w, label="Медиана", color=BLUE)
        ax.bar(x + w/2, avg, w, label="Среднее", color=ORANGE, alpha=.85)
        ax.plot(x - w/2, med, color=RED, lw=2, marker="o")
        for i in range(len(ms)):
            ax.annotate(f"{med[i]:.1f}", (x[i]-w/2, med[i]), textcoords="offset points", xytext=(0, 4), ha="center", fontsize=8, fontweight="bold")
            ax.annotate(f"{avg[i]:.1f}", (x[i]+w/2, avg[i]), textcoords="offset points", xytext=(0, 4), ha="center", fontsize=8)
        ax.set_xticks(x); ax.set_xticklabels([f"{lbl.get(m[-2:], m)}\n(n={n})" for m, n in zip(ms, ns)])
        ax.set_title("Скорость передачи бага в другую команду по месяцу поступления")
        ax.set_ylabel("дни от поступления до передачи"); ax.legend(); ax.grid(axis="y", alpha=.25)
        save(fig, p("chart_handoff.png"))
    print("charts ->", outdir)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 make_charts.py spt_data.json <output_dir>"); sys.exit(1)
    main(sys.argv[1], sys.argv[2])
