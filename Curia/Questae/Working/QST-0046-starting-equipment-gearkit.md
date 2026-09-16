# QST-0046 — Starting equipment: retire the legacy Inventory for a TOP gear layer

- **Type:** refactor
- **Priority:** 🟠 high
- **Status:** Working
- **Owner:** Agent (Julio's direction)
- **Route to:** Architecture Consul (Druid), Contracts Consul (Warlock), Balance Consul (Fighter)
- **Parent:** —
- **Sidequests:** QST-0046.1 (split the Ledgers by axis) · QST-0046.2 (gear naming & materials)
- **Related:** `Canon/TagKit-Doctrine.md` · `Canon/Single-Source-of-Truth.md` · QST-0045

---

## 🔍 Diagnosis (what & where)

`AtlasInventarium/Grimoire_of_Objects.py` was pre-TOP legacy: string-matched `if/elif`
tables, choices from global `random`, mechanics described but never instantiated, and
several parallel implementations of the same fact. A seven-agent audit (2026-07-29)
found, among others:

- the budget rolled **twice** per character, the second roll overwriting the purse;
- `value` and `weight` **transposed** on every Armor and Weapon (`super().__init__`
  argument order);
- shield `+2 AC` applied unconditionally on each of two `set_Armor` passes (**+4**), and
  a ranged weapon then displacing the shield while its bonus stayed in the AC;
- `Melee_Martial` / `Ranged_Martial` were **verbatim copies of the Simple lists** — no
  character could own a martial weapon;
- Weapon Mastery sampled the full 37-weapon catalogue with no reference to what the
  character owned or was trained for;
- Unarmored Defence existed **three times** (description-only Tags, a dead feat that
  would crash, and a live skill-flag hack), with no reconciliation;
- magic items were description-only: a Cloak of Protection changed nothing.

## 🧾 Evidence

Audit report and per-file line references are in the working notes; reproduced
symptoms included `Purse: 38.70000000000002 gp` on the sheet, `Clothes … AC 15` with no
indication where 15 came from, and a level-20 Paladin whose Cloak of Protection sat
inert in the bag.

## 🎯 Desired outcome

Gear follows the project's own shape: **records → Kit → Tags**, one construction point,
seeded per-character streams, forks resolved rather than described, and every mechanic
actually instantiated on the character.

## 🧭 Notes for the Agora / implementer

Julio's design (2026-07-30), which supersedes the first plan: **one generic `Item`**
(name, price, weight, description) with Tags supplying all meaning; `Equipped` as a
**Tag, not a slot pointer**, so "two armours are worn" is a question you can ask and
repair; and **everything an artifact grants summed at read time** so natural defences
are never overwritten.

Do NOT reintroduce a parallel production line: the legacy `Grimoire_of_Objects` is to
disappear, not to be maintained alongside.

---

## 📌 Landed so far (2026-07-31)

- `Grimoire_of_Items` — generic `Item`; Tags (`Armour`, `Weapon`, `Shield`, `Wearable`,
  slot tags, `Simple`/`Martial`, `Melee`/`Ranged`, `Firearm`, `Consumable`, `Magical`);
  `Equipped` as a Tag; `reconcile()` repairing over-capacity slots by selling the worse
  piece; `copper()` flooring; prototypes cloned via `instantiate()` so Ledger entries
  never alias between characters.
- Ledgers — Weapons (38 + 2 firearms), Armors (12 + Shield), Gear (25 tools, 30 items,
  all 7 packs), Wonders (magic items + consumables, tiered by level).
- `Grimoire_of_Crafts` — affixes as Tags (`of Defense` = `grants={"AC": 1}`), gated by
  item kind, hero Tags, and tier→level.
- `GearKit` — `Outfit_Player`, proficiency read off Guild Tags, derived AC, `Loadout`
  view for the sheet.
- Weapon Mastery bridge — masteries planned first as `Mastery_Of_…` Tags, balanced half
  reach / half close (Thrown counts as reach), then the loadout **buys those weapons**.
- Invariant sweep lives in `GearKit.__main__` (project keeps tests in module mains).

## 🚧 Remaining

- ~~Delete `Grimoire_of_Objects` (now unreachable from the player path, still imported).~~ Done 2026-09-16 on Julio's go: the module, its two dead imports and `Codex_of_Progression.apply_class_proficiencies` (never called; it would crash on the GearKit `Loadout`) are gone. Measured first: 13 Guilds at levels 1 and 5 made zero calls into the module, and 52 generated characters fingerprint identically before and after.
- NPCs stay on their own path **by Julio's explicit decision** — they should carry less,
  favour characteristic weapons, and use lootables. Not this quest.
- `str_requirement` / `stealth_disadvantage` recorded but not enforced.
- Background `EQUIPMENT` Report still unread (thematic per-background kits).
- `WEAPON_MASTERIES` dict still parallel to the weapon Ledger (verified identical, but
  duplication remains).

---

## ✅ Resolution (filled when Solved)
- **Decided by:** —
- **What changed:** —
- **Moved to Solved:** —

---

## ⚗️ Reward (separate dialog — do not fill during implementation)

- **Reward file:** *(pending distillation dialog)*
- **Distilled:** *(pending)*

---

## 🏛️ Council

> Architecture Consul (Druid): The legacy layer collapsed three independent axes —
> what a thing IS, who may use it, and what it grants — into one procedural function.
> Splitting them into records, Tags, and a Kit is the only version of this that grows.
> Contracts Consul (Warlock): The load-bearing choice is that grants are summed at read
> time. It makes "remove the cloak" free and makes AC impossible to desync. Keep it;
> resist any temptation to cache the number.
> Balance Consul (Fighter): A hero who drills six masteries and carries none of those
> weapons has six lines of text about nothing. Buying the drilled weapons is right even
> though it is expensive. No objection.

**Weighting:** reach 3 × severity 3 = **9** · council leaning: `build`
