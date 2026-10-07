"""Resolve Elf rule choices onto a completed Character sheet."""

from AtlasActorLudi.SpeciesKit.Elves.traits import Darkvision
from AtlasActorLudi.SpeciesKit.traits import Darkvision_Rules
from AtlasActorLudi.SpeciesKit.Elves.traits import Keen_Senses
from AtlasActorLudi.SpeciesKit.magic import ABILITY_LABELS
from AtlasActorLudi.SpeciesKit.magic import Resolve_Species_Spells
from AtlasActorLudi.SpeciesKit.Elves.traits import Elven_Lineage
from AtlasActorLudi.SpeciesKit.magic import Align_Lineage_Ability
from AtlasActorLudi.SpeciesKit.magic import Species_Spellcasting_Chips
from AtlasActorLudi.SpeciesKit.presentation import Project_Species_Feature


def _resolve_keen_senses(
	target,
	):
	skills = getattr(
		target,
		"skills",
		None,
		)

	if skills is None:
		return None

	selected = getattr(
		target,
		"keen_senses_skill",
		None,
		)

	if selected is None:
		available = tuple(
			name
			for name in Keen_Senses.SKILLS
			if getattr(
				getattr(
					skills,
					name,
					None,
					),
				"proficiency_level",
				0,
				) < 1
			)
		pool = (
			available
			or Keen_Senses.SKILLS
			)
		dice_bag = target.Dice_Bag( "Keen_Senses.choice" )
		selected = target.Pick(
			pool,
			dice=dice_bag,
			)
		target.keen_senses_skill = selected

	skill = getattr(
		skills,
		selected,
		None,
		)

	if (
		skill is not None
		and hasattr(
			skill,
			"set_proficiency",
			)
		):
		skill.set_proficiency()

	return selected


# One line per lineage, echoing what that Heritage's own description already
# established rather than restating it. Never a bloodline: elves drift as a
# people over centuries (Documenta/Canon/Elves-and-the-Dreaming.md), so these
# speak about what was taught or brought home, not what was passed down.
_LINEAGE_LINES = {
	"High_Elf": (
		"Your people traded with more than merchants, and not "
		"everything you brought home was cargo."
		),
	"Wood_Elf": (
		"The woods have always cared for your people. Now their "
		"whispers guide you, their paths open before you, and "
		"their shadows protect you."
		),
	"Dark_Elf": (
		"The dark taught your people how to survive it, and some "
		"of that lesson still answers when you call."
		),
	"Fae_Elf": (
		"The crossing into the Feywild left more on you than long "
		"ears."
		),
	"Shadow_Elf": (
		"Telling dream from thought took practice, and the "
		"practice became a kind of magic."
		),
	}


def _display_spellcasting_ability(
	target,
	) -> str:
	"""Find the highest eligible score when projecting the lineage Entry."""
	scores = getattr(
		target,
		"AS",
		None,
		)

	if scores is None:
		return getattr(
			target,
			"species_spellcasting_ability",
			"CHA",
			)

	return max(
		(
			"CHA",
			"INT",
			"WIS",
			),
		key=lambda ability: int(
			getattr(
				scores,
				ability,
				0,
				)
			),
		)


def _lineage_description(
	target,
	heritage,
	unlocked_spells,
	):
	ability = _display_spellcasting_ability(
		target,
		)
	ability_label = ABILITY_LABELS.get(
		ability,
		ability,
		)
	spell_list = "\n".join(
		f"- {spell.name}"
		for spell in unlocked_spells
		)
	has_leveled_spell = any(
		int(
			spell.level
			) > 0
		for spell in unlocked_spells
		)
	line = _LINEAGE_LINES.get(
		heritage.__name__,
		"",
		)
	description = (
		f"*{line}*\n\n"
		"**Spellcasting Ability.**\n\n"
		f"{ability_label}.\n\n"
		"**Lineage Spells.**\n\n"
		f"{spell_list}"
		).strip()

	if has_leveled_spell:
		description += (
			"\n\nYou always have these spells prepared. You can cast "
			"each of them once without a spell slot, regaining that "
			"use when you finish a Long Rest, and can also cast them "
			"with spell slots."
			)

	from AtlasActorLudi.SpeciesKit.Elves import High_Elf

	if heritage is High_Elf:
		description += (
			"\n\nAfter a Long Rest, Prestidigitation can be replaced "
			"with another Wizard cantrip."
			)

	return description


def Resolve_Elf_Features(
	target,
	) -> None:
	"""Project Elf Tags into readable Entries and mechanical ledgers."""
	from AtlasActorLudi.SpeciesKit.Elves.base import Elf
	from AtlasActorLudi.SpeciesKit.catalog import Current_Heritage

	if target not in Elf:
		return

	keen_sense = _resolve_keen_senses( target )
	darkvision_range = int(
		getattr(
			target,
			"darkvision",
			Darkvision.RANGE,
			)
		)
	Project_Species_Feature(
		target,
		"Darkvision",
		(
			"*Your elven eyes are sharp and your attention focused.*\n\n"
			+ Darkvision_Rules(
				darkvision_range
				)
			),
		level=1,
		)
	Project_Species_Feature(
		target,
		"Fey Ancestry",
		(
			"*The echoes of the Fae still linger in you, letting you see "
			"through trickery and deception.*\n\n"
			"You have Advantage on saving throws you make to avoid or "
			"end the Charmed condition."
			),
		level=1,
		)

	if keen_sense is not None:
		Project_Species_Feature(
			target,
			"Keen Senses",
			(
				"*Your focus and training can help you perceive your "
				"surroundings and understand your environment.*\n\n"
				f"You have proficiency in {keen_sense}."
				),
			level=1,
			)

	Project_Species_Feature(
		target,
		"Trance",
		(
			"*Elves are said to be made of the same essence as dream "
			"and nightmare. Perhaps there is more than mere poetry to "
			"it.*\n\n"
			"You don't need to sleep, and magic can't put you to sleep. "
			"You can finish a Long Rest in 4 hours by meditating."
			),
		level=1,
		)
	heritage = Current_Heritage( target )

	if heritage is None:
		return

	unlocked = Resolve_Species_Spells(
		target,
		heritage.SPELLS,
		)
	target.species_spell_free_casts = {
		spell.name: 1
		for spell in unlocked
		if int(
			spell.level
			) > 0
		}
	# Settled here rather than when the Heritage landed, because the Guild did
	# not exist yet and this follows whatever the Character casts with.
	Align_Lineage_Ability(
		target,
		Elven_Lineage.SPELLCASTING_ABILITIES,
		)
	Project_Species_Feature(
		target,
		f"{heritage.__name__.replace('_', ' ')} Lineage",
		_lineage_description(
			target,
			heritage,
			unlocked,
			),
		chips=Species_Spellcasting_Chips(
			target
			),
		level=1,
		)


def _test_dice_purpose() -> None:
	#-- Ruling 8 (QST-0144.6): the Keen Senses skill comes from one Dice Bag
	#-- opened as "Keen_Senses.choice" with the default key, over the skills
	#-- the Character is not yet proficient in, as before.
	from AtlasActorLudi.CharactersKit import Character
	from AtlasActorLudi.Grimoire_of_AbilityScores import AbilityScores
	from AtlasActorLudi.Grimoire_of_Skills import Char_Skills
	from AtlasActorLudi.Map_of_Scores import PB

	def character_with_skills(
		seed,
		):
		character = Character(
			seed=seed,
			)
		character.AS = AbilityScores(
			STR=10,
			DEX=12,
			CON=14,
			INT=16,
			WIS=15,
			CHA=13,
			character=character,
			)
		character.proficiency_bonus = PB( character.level )
		character.skills = Char_Skills(
			character,
			character.AS,
			character.proficiency_bonus,
			)
		return character

	opened = []
	drawn = []
	original_dice_bag = Character.Dice_Bag
	original_pick = Character.Pick

	def recording_dice_bag(
		char,
		purpose,
		**key,
		):
		opened.append(
			(
				purpose,
				key,
				)
			)
		return original_dice_bag(
			char,
			purpose,
			**key,
			)

	def recording_pick(
		char,
		ledger,
		weights=None,
		**options,
		):
		drawn.append(
			tuple(
				ledger
				)
			)
		return original_pick(
			char,
			ledger,
			weights,
			**options,
			)

	Character.Dice_Bag = recording_dice_bag
	Character.Pick = recording_pick
	try:
		untrained = character_with_skills( 7 )
		chosen = _resolve_keen_senses( untrained )
		perceptive = character_with_skills( 8 )
		perceptive.skills.Perception.set_proficiency()
		narrowed = _resolve_keen_senses( perceptive )
	finally:
		Character.Dice_Bag = original_dice_bag
		Character.Pick = original_pick

	assert opened == [
		(
			"Keen_Senses.choice",
			{},
			),
		(
			"Keen_Senses.choice",
			{},
			),
		], opened
	assert drawn == [
		Keen_Senses.SKILLS,
		(
			"Insight",
			"Survival",
			),
		], drawn
	assert chosen in Keen_Senses.SKILLS
	assert narrowed in (
		"Insight",
		"Survival",
		)
	assert getattr(
		untrained.skills,
		chosen,
		).proficiency_level >= 1


if __name__ == "__main__":
	_test_dice_purpose()
	print( "OK: SpeciesKit.Elves.resolution self-test" )
