"""Epic Boon feats — 2024 PHB catalogue."""
#-- Recovered from the pre-wipe bytecode mirror (QST-0134).  The file left by
#-- the 2026-08-29 accident said "Declarations are verbatim" and was not: all
#-- twelve Boons were the bare word None.  They import without error, so
#-- nothing complained -- but nothing registered either, and FeatKit's own
#-- self-test has been failing on `assert len(all_epic_boons()) >= 12` ever
#-- since.  A Character of level 19 or above could not be granted a Boon.
#--
#-- Every name and every rule sentence below is the original's, read out of
#-- .recovery-vault/_prewipe-pyc-mirror/ and printed by machine, not retyped.
#--
#-- Two mirrored copies survive and differ in exactly one string: Boon of
#-- Energy Resistance.  The copy used here opens, as all eleven others do,
#-- with "Increase one ability score by 1, to a maximum of 30."  The other
#-- copy had lost that sentence and gained a stray "<br><b>Resistances.</b>",
#-- a markup style no file in AtlasOfFeats uses -- a half-finished edit caught
#-- by the wipe.  If that edit was deliberate, this is the line to change.
#--
#-- Does this module own a domain axis (QST-0134)?  No.  It is a catalogue:
#-- twelve entries handed to FeatKit.Make_Epic_Boon, which mints the Tag and
#-- owns the Rank_Reached gate.  A Map adds content, never structure.

from __future__ import annotations

from AtlasLusoris.FeatKit import Make_Epic_Boon


BoonOfCombatProwess = Make_Epic_Boon(
		name="Boon of Combat Prowess",
		description=(
				"Increase one ability score by 1, to a maximum of 30. Once per turn when you miss with an attack roll, you can hit instead."
				),
		)

BoonOfDimensionalTravel = Make_Epic_Boon(
		name="Boon of Dimensional Travel",
		description=(
				"Increase one ability score by 1, to a maximum of 30. Immediately after you take the Attack action or the Magic action, you can teleport up to 30 feet to an unoccupied space you can see."
				),
		)

BoonOfEnergyResistance = Make_Epic_Boon(
		name="Boon of Energy Resistance",
		description=(
				"Increase one ability score by 1, to a maximum of 30. You gain Resistance to two damage types of your choice from Acid, Cold, Fire, Lightning, Necrotic, Poison, Psychic, Radiant, and Thunder. You can change the types when you finish a Long Rest."
				),
		)

BoonOfFate = Make_Epic_Boon(
		name="Boon of Fate",
		description=(
				"Increase one ability score by 1, to a maximum of 30. When you or a creature within 60 feet of you succeeds or fails a D20 Test, you can roll 2d4 and apply the total as a bonus or penalty to the roll. Once you use this Boon, you can't use it again until you finish a Short or Long Rest."
				),
		)

BoonOfFortitude = Make_Epic_Boon(
		name="Boon of Fortitude",
		description=(
				"Increase one ability score by 1, to a maximum of 30. Your Hit Point maximum increases by 40. Whenever you regain Hit Points, you can regain extra Hit Points equal to your Constitution modifier (minimum of 1). You can gain this extra healing only once per turn."
				),
		)

BoonOfIrresistibleOffense = Make_Epic_Boon(
		name="Boon of Irresistible Offense",
		description=(
				"Increase your Strength or Dexterity by 1, to a maximum of 30. The Bludgeoning, Piercing, and Slashing damage you deal ignores Resistance. When you roll a 20 on an attack roll, the target takes extra damage of the attack's type equal to the ability score you increased with this Boon."
				),
		)

BoonOfRecovery = Make_Epic_Boon(
		name="Boon of Recovery",
		description=(
				"Increase one ability score by 1, to a maximum of 30. You have a pool of ten d10s. As a Bonus Action, you can expend dice from the pool and regain Hit Points equal to the total. You also regain all expended dice when you finish a Long Rest. If you are reduced to 0 Hit Points but not killed outright, you can drop to 1 Hit Point instead and regain Hit Points equal to half your Hit Point maximum (once per Long Rest)."
				),
		)

BoonOfSkill = Make_Epic_Boon(
		name="Boon of Skill",
		description=(
				"Increase one ability score by 1, to a maximum of 30. You gain proficiency in all skills. Choose one skill in which you have proficiency; you gain Expertise in it."
				),
		)

BoonOfSpeed = Make_Epic_Boon(
		name="Boon of Speed",
		description=(
				"Increase one ability score by 1, to a maximum of 30. Your Speed increases by 30 feet. As a Bonus Action, you can take the Disengage action, which also ends the Grappled condition on you."
				),
		)

BoonOfSpellRecall = Make_Epic_Boon(
		name="Boon of Spell Recall",
		description=(
				"Increase your Intelligence, Wisdom, or Charisma by 1, to a maximum of 30. Whenever you cast a spell with a spell slot of levels 1–4, roll a d4. If you roll the slot's level, the spell is cast without expending the slot."
				),
		)

BoonOfTheNightSpirit = Make_Epic_Boon(
		name="Boon of the Night Spirit",
		description=(
				"Increase one ability score by 1, to a maximum of 30. While you are in Dim Light or Darkness, you have Resistance to all damage except Force, Psychic, and Radiant, and you can take a Bonus Action to become Invisible. The Invisibility ends early after you take an action, Bonus Action, or Reaction."
				),
		)

BoonOfTruesight = Make_Epic_Boon(
		name="Boon of Truesight",
		description=(
				"Increase one ability score by 1, to a maximum of 30. You have Truesight with a range of 60 feet."
				),
		)


def _self_test() -> None:
	"""Every Boon in this Map reaches the register FeatKit draws from."""
	from AtlasLusoris.FeatKit import all_epic_boons

	declared = (
			BoonOfCombatProwess,
			BoonOfDimensionalTravel,
			BoonOfEnergyResistance,
			BoonOfFate,
			BoonOfFortitude,
			BoonOfIrresistibleOffense,
			BoonOfRecovery,
			BoonOfSkill,
			BoonOfSpeed,
			BoonOfSpellRecall,
			BoonOfTheNightSpirit,
			BoonOfTruesight,
			)

	assert len(declared) == 12, \
			f"The 2024 catalogue holds twelve Boons, not {len(declared)}."

	for boon in declared:
		assert boon is not None, "A Boon that is None is the bug this file had."
		assert boon.NAME.startswith("Boon of"), \
				f"{boon.NAME!r} is not named as a Boon."
		assert boon.SOURCE == "Epic Boon", \
				f"{boon.NAME} is filed under {boon.SOURCE!r}, not as a Boon."

	registered = all_epic_boons()
	for boon in declared:
		assert boon in registered, \
				f"{boon.NAME} was built but never registered with FeatKit."

	#-- The whole point of the catalogue: FeatKit can find twelve of them.
	assert len(registered) >= 12, \
			f"FeatKit sees only {len(registered)} Epic Boons."

	#-- Every Boon raises an ability score; that opening sentence is the shape
	#-- the 2024 catalogue gives them, and the sheet prints it.
	names = [boon.NAME for boon in declared]
	assert len(set(names)) == len(names), f"Two Boons share a name: {names}"

	print(
			f"OK — Map_of_Epic_Boons self-test ({len(declared)} Boons)"
			)


if __name__ == "__main__":
	_self_test()
