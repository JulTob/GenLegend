# QST-0092 — Rogue Assassin crashes on a dead inventory call; the kits move to the Training Tag

- **Type:** bug
- **Priority:** 🔴 urgent *(a selectable Specialization crashed for every seed at level 3 and up)*
- **Status:** Working (fix landed; awaiting Julio's closing word)
- **Owner:** Claude (branch `questa/QST-0092-assassins-tools-on-the-tag`, 2026-09-06)
- **Route to:** Methods (Wizard) · Workshop (Artificer) · Contracts (Warlock)
- **Parent:** QST-0091.2 (Guild and Specialization as one declaration)
- **Sidequests:** —
- **Related:** QST-0046 (GearKit) · QST-0089 · QST-0088 · TrainingKit `apply` · Decree 0007

> Minted under `Documenta/` (Julio, 2026-09-06: "fix the crashes").

---

## 🔍 Diagnosis (what & where)

A wide sweep of the Player path on 2026-09-06 (every Guild at levels 1 to 20, every Species, every Background, every Specialization, three genders; 1,164 requests, each summoned, projected with `to_dict` and rendered with `build_character_sheet`) found one crash signature: **Rogue with the Assassin specialization at level 3 and above**, every seed.

`AtlasLusoris/Map_of_Classes/Training/Rogue.py` line 149, in the legacy Assassin's Tools block, built two `Grimoire_of_Objects.Object`s and called `character.equipment.buy_item(...)`. Since QST-0046 the Character's equipment is a GearKit `Loadout`, which has no `buy_item`. The TOP Training Tag `Assassins_Tools` in `AtlasOfTraining/Map_of_Rogue_Training.py` already carried the feature text, but nothing granted the kits there, so the legacy block was the only place the Assassin actually received them.

## 🧾 Evidence

- Wide sweep: `DONE 1161/1164 ok; 1 distinct signature: summon AttributeError Training/Rogue.py:149 in features: 'Loadout' object has no attribute 'buy_item'`, requests `{'guild': 'Rogue', 'specialization': 'Assassin', 'level': 3|10|20}`.
- `training_covers("Rogue", "Assassin's Tools")` → True: the TOP Tag owns the prose already.
- `Make_Training(apply=...)` exists and the Bard training map already threads `apply` through its helpers; the Rogue map's `_path` and `_assassin` did not.
- `GearKit.issue(char, prototype)` and `Ledger_of_Tools.TOOLS_BY_NAME` are the doors `_proficient_tools` already uses to put a tool in the bag.

## 🎯 Desired outcome

An Assassin builds at every level, carries a Disguise Kit and a Poisoner's Kit as real Items in the Loadout, is proficient with both, and the grant lives on the Training Tag that names it. The legacy block no longer touches gear.

## 🧭 Notes for the Agora / implementer

- Julio's choice, 2026-09-06: grant on the TOP Training Tag, delete the legacy gear block (over "fix the legacy line" and "text only").
- `apply` runs once per awaken (TrainingKit guards on the existing sheet line), after `Outfit_Player`, so the Loadout exists when the kits are issued.
- The legacy Feature text for Assassin's Tools is removed too: `filter_legacy_features` would have dropped it as a duplicate of the Tag's Entry; deleting it is one fewer thing to disagree.

---

## ✅ Resolution (filled when Solved)
- **Decided by:** Julio, 2026-09-06.
- **What changed:** `Map_of_Rogue_Training.py`: `_path` and `_assassin` accept `apply`; `_grant_assassins_tools` sets both tool proficiencies and issues both kits through `GearKit.issue` and `TOOLS_BY_NAME`; `Assassins_Tools` declares `apply=_grant_assassins_tools`. `Training/Rogue.py`: the Assassin's Tools block (Feature, `Object`s, `buy_item`) is gone, with a two-line note pointing at the Tag. Wide sweep after the fix: 1,164 of 1,164.
- **Practice/preference to remember:** a Specialization's grant belongs on its Training Tag through `apply`, never in a legacy ladder; the wide sweep (every level, every axis, render included) is the gate that finds a subclass that only crashes when chosen.

---

## 🏛️ Council

> Workshop Consul (Artificer): `Loadout` retired `buy_item` on purpose; the door is `issue`. A grant that bypasses the door is not a grant, it is a leak.
> Methods Consul (Wizard): The Tag already said the words. Now it does the thing. That is the whole direction of QST-0091.2, one feature early.
> Contracts Consul (Warlock): Proficiency and possession are two facts; both are set in one `apply`, so a sheet can never show one without the other.

**Weighting:** reach 1 × severity 3 = **3** · council leaning: `build`
