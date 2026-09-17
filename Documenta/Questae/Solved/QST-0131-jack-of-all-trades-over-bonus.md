# QST-0131 — Jack of All Trades adds half PB to skills that already add PB

- **Type:** bug
- **Priority:** 🔴 urgent — *every Bard of level 2 or more printed a wrong skill modifier*
- **Status:** Solved
- **Owner:** Claude (Julio's go, 2026-09-16)
- **Route to:** Lorekeeper · Contracts (Warlock) · Testing (Rogue)
- **Parent:** —
- **Sidequests:** —
- **Related:** QST-0047 (the lasting shape: a derived modifier, not a stored flag) · QST-0116.4 (Backgrounds write the ledger after the sheet is built)

---

## 🔍 Diagnosis (what & where)

`AtlasActorLudi/Grimoire_of_Skills.py`, `Skill.calculate_modifier`. The 2024 rule (quoted by `Map_of_Bard_Training.Jack_of_All_Trades`): add half the Proficiency Bonus to an ability check that **does not already** use it. The code added PB for any trained skill, then added half PB again to every skill below Expertise that carried `jack=True`.

The flag goes stale by construction: `Grimoire_of_Characters.set_Skills` flags every untrained skill at Bard level 2, and `Apply_Background_Training` (and Origin Feats, Species features) train some of those skills afterwards. A trained skill kept the flag and printed ability + PB + PB//2.

## 🧾 Evidence

Found by comparing the deleted `Grimoire_of_Training.py` (whose branch structure was right) with the live class. Unit: ability 10, PB 3, level 1, `jack=True` → +4 (rule: +3). Generation (`summon_player`, Bards at levels 2/3/5, seeds 1–30): **90 of 90** characters had a trained skill still flagged (1 skill: 42, 2 skills: 39, 3 skills: 9); the late trainer was the Background in 129 cases, an Origin Feat in 6, a Species feature in 6. Seed 42, level 3, Farmer: Nature +4, Animal Handling +4. The sheet reads `calculate_modifier()` (`app/components/shared.py:447`), so the wrong number reached the player.

## 🎯 Desired outcome

Half PB only on untrained skills, whatever order training arrives in.

## 🧭 Notes for the Agora / implementer

The one-line fix guards on `proficiency_level == 0`. The lasting answer (QST-0047) is a derived modifier that asks "does this check already add PB?" at read time, so no flag can go stale.

---

## ✅ Resolution
- **Decided by:** Julio, 2026-09-16 (chat: "Let's do those 1..4").
- **What changed:** `Skill.calculate_modifier` adds half PB only when `proficiency_level == 0`. Verified: unit table, seed 42 L3 Bard prints +3, smoke and replay rites green.
- **Practice/preference to remember:** a rule that depends on *now* must be derived at read time, never stored on the object at one instant.

---

## 🏛️ Council

> Lorekeeper (Elf Sage): The rule is one sentence, "does not already use", and the code answered a different question, "was untrained when the Bard turned two". The fix restores the sentence.
> Contracts Consul (Warlock): A stored flag is a promise about the past. Guard it on the present until QST-0047 removes it.

**Weighting:** reach ⟨3⟩ × severity ⟨3⟩ = **9** · council leaning: `build`
