# QST-0050 — 🔴 RECOVERY BOARD: feat / background losses after the crisis

- **Type:** chore/cleanup (recovery)
- **Priority:** 🟠 high — *the lane itself is restored and verified; the sidequests are what remain*
- **Status:** Open — **board; the restoration described here is DONE, the sidequests are not**
- **Owner:** Claude (restoration below, complete) — *sidequests .1–.4 unclaimed*
- **Route to:** any recovery agent, Cleric (Repair), Rogue (Testing), Julio
- **Parent:** —
- **Sidequests:** QST-0050.1 · QST-0050.2 · QST-0050.3 · QST-0050.4 · QST-0050.5 · QST-0050.6
- **Related:** QST-0049 (the same crisis, spell lane) · `$S/RECOVERY-COORD.md` (live agent board) · the reflog `reset` + `fdf3b08` crisis commit

---

## 🔍 Diagnosis (what & where)

The same crisis that froze the spell work (QST-0049) also passed through the **feat / background** lane. The pre-crisis session had fixed a real bug there: the Crafter and Musician Origin Feats crashed character generation, because `FeaturesKit.Reserved_Background_Training` reserved a Background's whole **Tool menu** against what is only ever a **single** grant. That emptied the Feat's pool and made the **Artisan, Crafter and Entertainer Backgrounds 100% unbuildable** — it merely *read* as a ~7% random crash, because that is how often those Backgrounds came up in a draw.

The fix was two files. **One survived the crisis, the other did not:**

| Piece | State after crisis | Recovery source |
|---|---|---|
| `FeaturesKit.py` — reservation fix, `allow_short`, `at_most`, relaxed training Postconditions, 3 self-tests | ✅ survived intact | — |
| `BackgroundKit.py` — `_still_open()` + `_grant_tool` picking around the Feat, + 2 imports | ❌ **destroyed** by a restore from an older copy (file mtime 18:35, after the work) | re-applied by hand 2026-08-30, verbatim from session context |
| `Map_of_Official_Origin_Feats.py` — duplicate `_grant_training` | ❌ **stale copy re-inserted**, shadowing the live one | stale copy deleted 2026-08-30 |

**Why the second file mattered.** The two halves are one behaviour and neither works alone. `FeaturesKit` stops over-reserving; `BackgroundKit._still_open` has the Background choose its Tool from what the Character has not learnt, which it can do because it runs *after* the Feat. Drop the first and the crash returns; drop the second and Artisan grants a Tool the Feat already granted, so the Character gets three distinct Tools instead of four.

**Why the third file mattered.** The 2026-08-29 restore left **two** definitions of `_grant_training` in `Map_of_Official_Origin_Feats.py`. The later one was the pre-ledger version (`(char, options) -> str`, writing straight to the mutable sheet). Being later, it shadowed the live ledger-based one, so all four callers — every one of which passes `background_tag=` and reads a `Training_Batch` back — died with `TypeError: _grant_training() got an unexpected keyword argument 'background_tag'`.

## 🧾 Evidence

Before restoration, over 120 seeds (`summon_player(guild="Barbarian", level=12, seed=…)`):

```
Counter({'TagImprintError: Imprint Crafter.awaken failed': 5,
         'TagImprintError: Imprint Musician.awaken failed': 4, ...})
Artisan generated OK: 0 | Entertainer OK: 0
```

Instrumented at the failure, the Character held **zero** Artisan's Tools; the pool was emptied entirely by `exclude`:

```
FEATURE: Crafter
  candidates: 17   exclude: 19 (all 17 tools + the Background's 2 Skills)   trained: 0
```

After restoration, same 120 seeds: `Counter()` — no failures. Artisan **60/60**, Entertainer **60/60**, **0** Tool collisions, and a representative sheet shows four distinct Tools (Background took Cobbler's; Crafter took Mason's, Painter's, Weaver's).

`_test_feat_awakening_survives_bulk_generation` (312 Characters, all 13 Guilds, levels 1/4/8/12/16/20): **0 feat-awakening failures**.

## 🎯 Desired outcome

Two things, and only the second is still open:

1. ✅ The feat/background lane restored and defended so it cannot be silently lost a third time. **Done.**
2. ⬜ The generator healthy end to end. It is not: **238/312** Characters generate. The remaining ~24% fail for reasons in *other* Atlases, split into QST-0050.1 through .3. QST-0050.4 covers a fourth, test-only casualty.

## 🧭 Notes for the Agora / implementer

- **Do not restore `FeaturesKit.py` or `BackgroundKit.py` from `.recovery-vault` bytecode.** Those copies predate this fix. This is exactly how `BackgroundKit` was lost the first time.
- **Every edit carries a greppable banner.** Before touching any of the three files:
  ```
  grep -rn "RECOVERY NOTE 2026-08-30" --include="*.py" .
  ```
  Eight banners, each stating what the code is for, what breaks if reverted, and which file it is paired with.
- **Annotated copies live outside the repo** at `~/DnD-session-work-backup/`, so a blunt `git checkout` cannot reach them.
- **`grep -c 'def _grant_training(' AtlasLusoris/AtlasOfFeatures/Map_of_Official_Origin_Feats.py` must print `1`.** If a later restore reintroduces a second, keep the ledger-based one.
- **A Precondition was considered and rejected** for the short-pool case. `_take_first_that_applies` (FeatKit) only guards *General* feats; an Origin feat arrives through Tag inheritance in `Build_Background` and through `Grant_Origin_Feat`, neither of which catches `TagPreconditionError`. A refusing `@Pre` would trade one crash for another, and since a Background's Origin feat is not optional (Artisan *is* Crafter) it would have deleted three Backgrounds outright. Short grants (`allow_short`) are the answer instead: the Feature exists, and its Entry names only the training it actually gave.
- **The bulk self-test has two assertions and they mean different things.** `feature_failures == 0` is this lane's contract. `generated >= 300` is a coarse health check on the rest of the generator and currently fails at 238/312 for the reasons in the sidequests. Do not loosen the first to quiet the second.

---

## ✅ Resolution (filled when Solved)
- **Decided by:** —
- **What changed:** restoration complete (see Diagnosis table); board stays Open until QST-0050.1–.4 close.
- **Practice/preference to remember:** a fix that spans two files needs the pairing written **into both files**, not only into a ticket. The half with no comment is the half that gets restored away.

---

## 🏛️ Council
*Not yet held — minted during the live recovery scramble. Route to Cleric (Repair) and Rogue (Testing) if the sidequests need arbitration.*

**Weighting:** reach ⟨3⟩ × severity ⟨3⟩ = **9** · council leaning: `build`
