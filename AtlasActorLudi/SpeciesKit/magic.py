from AtlasVenustas import Chip
"""Shared mechanics for magic contributed by a Species Heritage."""


ABILITY_LABELS = {
	"INT": "Intelligence",
	"WIS": "Wisdom",
	"CHA": "Charisma",
	}


def Align_Lineage_Ability(
		target,
		options,
		) -> str | None:
	"""
	Cast the Heritage's spells with whatever the Character already casts with.

	The rules make this a free choice: an Elven Lineage is cast with
	"Intelligence, Wisdom, or Charisma", chosen by the player.  No player picks
	their second-best score, so neither does this.  A Covenantor who answers to
	Wisdom casts the lineage with Wisdom too, instead of carrying two
	spellcasting abilities and the confusion that comes with them.

	The Heritage is chosen before the Guild exists, so the draw made back then
	stands as the fallback: it is what a Character with no spellcasting class
	keeps, and it is still seed-stable.  This only overrides it when the
	Character turns out to cast with one of the offered abilities.
	"""
	from AtlasLusoris.GuildKit import casting_ability

	legal = tuple(
		options
		or ()
		)
	answers = casting_ability(
		target
		)

	if answers and answers in legal:
		target.species_spellcasting_ability = answers

	return getattr(
		target,
		"species_spellcasting_ability",
		None,
		)


def Resolve_Species_Spells(
		target,
		spell_progression,
		):
	"""Add the Species spells unlocked at the Character's current level."""
	from AtlasMagia import Lodge_of_Spells

	known_spells = getattr(
		target,
		"known_spells",
		None,
		)

	if known_spells is None:
		known_spells = []
		target.known_spells = known_spells

	known_names = {
		getattr(
			spell,
			"name",
			None,
			)
		for spell in known_spells
		}
	unlocked = []

	for required_level, provider_key in spell_progression:
		if target.level < required_level:
			continue

		spell = getattr(
			Lodge_of_Spells,
			provider_key,
			)
		unlocked.append( spell )

		if spell.name not in known_names:
			known_spells.append( spell )
			known_names.add(
				spell.name
				)

	target.species_spells = tuple(
		spell.name
		for spell in unlocked
		)

	return tuple( unlocked )


def Species_Spellcasting_Chips(
		target,
		):
	"""Project the chosen ability and current derived spell values."""
	ability = getattr(
		target,
		"species_spellcasting_ability",
		None,
		)
	ability_label = ABILITY_LABELS.get(
		ability,
		ability,
		)
	chips = [
		Chip(
			"🪄",
			"Spellcasting Ability",
			ability_label,
			),
		]
	scores = getattr(
		target,
		"AS",
		None,
		)

	if (
		scores is None
		or ability is None
		):
		return tuple( chips )

	score = int(
		getattr(
			scores,
			ability,
			10,
			)
		)
	modifier = (
		score
		- 10
		) // 2
	proficiency = int(
		getattr(
			target,
			"proficiency_bonus",
			2,
			)
		)
	save_dc = (
		8
		+ proficiency
		+ modifier
		)
	attack = (
		proficiency
		+ modifier
		)
	target.species_spell_save_dc = save_dc
	target.species_spell_attack_bonus = attack
	# No "Species Spell Attack" chip: it is only ever proficiency + the
	# spellcasting ability's modifier, which the Attack Rolls table already
	# lists for that ability.  Save DC has no such table anywhere on the
	# sheet, so it stays the one chip worth its space.
	chips.append(
		Chip(
			"🔮",
			"Species Spell Save DC",
			save_dc,
			),
		)

	return tuple( chips )


def Spell_Progression(
		spell_progression,
		) -> str:
	"""Describe a Species spell progression using public spell names."""
	from AtlasMagia import Lodge_of_Spells

	return ", ".join(
		(
			f"{getattr(Lodge_of_Spells, provider_key).name} "
			f"at level {level}"
			)
		for level, provider_key in spell_progression
		)
