#!/usr/bin/env python3
"""Player sweep: summon, project, render; group every crash by signature.

Quick (default): every Guild at levels 1 and 5, three seeds, summon only (about 30 s).
Wide (--wide): every level 1..20, every Species, Background and Specialization,
three genders, each summoned, projected and rendered (about nine minutes).

Covers what the 78-cell gate does not: every level 1..20, every Species,
every Background, every Specialization, three genders. Each request runs
the same three steps the Shiny page runs: summon_player -> to_dict ->
build_character_sheet. A failure at any step is a user-visible crash.

Usage: make sweep-player [WIDE=1]   or   python scripts/sweep_player.py [--wide] [out.jsonl]
"""
from __future__ import annotations

import contextlib
import io
import json
import sys
import time
import traceback
from collections import Counter, defaultdict
from pathlib import Path

# `python scripts/sweep_player.py` puts scripts/ on the import path, not the
# project root, so the Atlas packages are invisible and the documented
# `make sweep-player` dies on the first import. Every other rite in this
# folder seats the root itself; this one never did.
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

WIDE = "--wide" in sys.argv[1:]
args = [a for a in sys.argv[1:] if a != "--wide"]
OUT = args[0] if args else None
quiet = lambda: (contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()))

with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    from AtlasActorLudi.Map_of_Character_Generation import choices, summon_player
    from AtlasLusoris.GuildKit import Specialization_Choices
    from app.components import build_character_sheet

ch = choices()
GUILDS = list(ch.guilds)
SPECIES = list(ch.species)
BACKGROUNDS = list(ch.backgrounds)
GENDERS = ["He", "She", "They"]


def innermost_repo_frame(tb: str) -> str:
    frames = [l.strip() for l in tb.splitlines() if l.strip().startswith('File "') and "/.venv/" not in l]
    if not frames:
        return "?"
    f = frames[-1]
    # File "/x/y/AtlasFoo/Bar.py", line 12, in baz
    try:
        path = f.split('"')[1]
        rest = f.split('"')[2]
        short = "/".join(path.split("/")[-2:])
        return short + rest.replace(", line ", ":").replace(", in ", " in ")
    except Exception:
        return f[:120]


def run(request: dict) -> dict:
    rec = {"request": request, "stage": "ok"}
    if not WIDE:
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                summon_player(**request)
            return rec
        except Exception as e:
            tb = traceback.format_exc()
            return {**rec, "stage": "summon", "type": type(e).__name__, "msg": str(e)[:160], "where": innermost_repo_frame(tb)}
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            character = summon_player(**request)
    except Exception as e:
        tb = traceback.format_exc()
        return {**rec, "stage": "summon", "type": type(e).__name__, "msg": str(e)[:160], "where": innermost_repo_frame(tb)}
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            data = character.to_dict()
    except Exception as e:
        tb = traceback.format_exc()
        return {**rec, "stage": "to_dict", "type": type(e).__name__, "msg": str(e)[:160], "where": innermost_repo_frame(tb)}
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            html = str(build_character_sheet(data))
        if len(html) < 500:
            return {**rec, "stage": "render", "type": "EmptySheet", "msg": f"sheet html only {len(html)} chars", "where": "app/components/character_sheet.py"}
    except Exception as e:
        tb = traceback.format_exc()
        return {**rec, "stage": "render", "type": type(e).__name__, "msg": str(e)[:160], "where": innermost_repo_frame(tb)}
    return rec


requests: list[dict] = []
# 1. every Guild, every level (quick: levels 1 and 5), three seeds
for g in GUILDS:
    for level in (range(1, 21) if WIDE else (1, 5)):
        for seed in (1, 2, 3):
            requests.append({"guild": g, "level": level, "seed": seed})
if not WIDE:
    pass  # the quick matrix stops here
# 2. every Species x every Guild at level 3, gender rotating
for i, s in enumerate(SPECIES if WIDE else []):
    for j, g in enumerate(GUILDS):
        requests.append({"species": s, "guild": g, "level": 3, "seed": 1, "gender": GENDERS[(i + j) % 3]})
# 3. every Background with a rotating Guild, levels 1 and 4
for i, b in enumerate(BACKGROUNDS if WIDE else []):
    for level in (1, 4):
        requests.append({"background": b, "guild": GUILDS[i % len(GUILDS)], "level": level, "seed": 2})
# 4. every Specialization at levels 3, 10, 20
for g in (GUILDS if WIDE else []):
    for spec in Specialization_Choices(g):
        for level in (3, 10, 20):
            requests.append({"guild": g, "specialization": spec, "level": level, "seed": 1})

print(f"requests: {len(requests)}", flush=True)
t0 = time.time()
sig_count: Counter = Counter()
sig_example: dict = {}
sig_requests: defaultdict = defaultdict(list)
ok = 0
import contextlib as _cl
with (open(OUT, "w") if OUT else _cl.nullcontext()) as out:
    for n, req in enumerate(requests, 1):
        rec = run(req)
        if out: out.write(json.dumps(rec) + "\n")
        if rec["stage"] == "ok":
            ok += 1
        else:
            sig = (rec["stage"], rec["type"], rec["where"], rec["msg"][:60])
            sig_count[sig] += 1
            sig_example.setdefault(sig, req)
            sig_requests[sig].append(req)
        if n % 100 == 0:
            print(f"  {n}/{len(requests)} ok={ok} fails={n-ok} {time.time()-t0:.0f}s", flush=True)

print(f"\nDONE {ok}/{len(requests)} ok in {time.time()-t0:.0f}s; {len(sig_count)} distinct signatures\n")
for sig, count in sig_count.most_common():
    stage, typ, where, msg = sig
    print(f"[{count:4d}] {stage:8s} {typ:24s} {where}")
    print(f"        {sig_example[sig]}")
    print(f"        {msg}")
    reqs = sig_requests[sig]
    guilds = sorted({r.get('guild') for r in reqs if r.get('guild')})
    levels = sorted({r.get('level') for r in reqs})
    print(f"        guilds={guilds} levels={levels[:12]}{'...' if len(levels)>12 else ''}")

sys.exit(1 if sig_count else 0)
