"""Resolve Tiefling rules onto a completed Character sheet."""

from AtlasActorLudi.SpeciesKit.magic import ABILITY_LABELS
from AtlasActorLudi.SpeciesKit.magic import Resolve_Species_Spells
from AtlasActorLudi.SpeciesKit.Tieflings.traits import Fiendish_Legacy
from AtlasActorLudi.SpeciesKit.magic import Align_Lineage_Ability
from AtlasActorLudi.SpeciesKit.magic import Species_Spellcasting_Chips
from AtlasActorLudi.SpeciesKit.presentation import Project_Species_Feature
from AtlasActorLudi.SpeciesKit.traits import Darkvision
from AtlasActorLudi.SpeciesKit.traits import Darkvision_Rules
from AtlasVenustas import Chip


def _project_darkvision(
	target,
	) -> None:
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
		Darkvision_Rules(
			darkvision_range
			),
		chips=(
			Chip(
				"👁️",
				"Darkvision",
				f"{darkvision_range} ft",
				),
			),
		level=1,
		)


def _project_otherworldly_presence(
	target,
	ability_label,
	) -> None:
	Project_Species_Feature(
		target,
		"Otherworldly Presence",
		(
			f"You know the Thaumaturgy cantrip. {ability_label} is your "
			"spellcasting ability for it."
			),
		level=1,
		)


def _legacy_free_cast_chips(
	free_casts,
	) -> tuple:
	return tuple(
		Chip(
			"✨",
			f"{spell_name} Free Cast",
			uses,
			)
		for spell_name, uses in free_casts.items()
		)


def _project_fiendish_legacy(
	target,
	heritage,
	legacy_spells,
	ability_label,
	) -> None:
	legacy_names = ", ".join(
		spell.name
		for spell in legacy_spells
		)
	free_casts = {
		spell.name: 1
		for spell in legacy_spells
		if int(
			spell.level
			) > 0
		}
	target.fiendish_legacy_spells = tuple(
		spell.name
		for spell in legacy_spells
		)
	target.fiendish_legacy_free_casts = free_casts
	target.species_spell_free_casts = dict(
		free_casts
		)
	description = (
		f"You have Resistance to {heritage.DAMAGE_RESISTANCE} damage. "
		f"You know the spells of your legacy at your level: {legacy_names}. "
		f"{ability_label} is your spellcasting ability for them."
		)
	if free_casts:
		description += (
			" You can cast each leveled spell among them once without a spell "
			"slot, and you regain the ability to do so when you finish a Long "
			"Rest. You can also cast it using any spell slots you have of the "
			"appropriate level."
			)
	Project_Species_Feature(
		target,
		f"Fiendish Legacy: {heritage.__name__}",
		description,
		chips=(
			Chip(
				"🛡️",
				"Damage Resistance",
				heritage.DAMAGE_RESISTANCE,
				),
			*Species_Spellcasting_Chips(
				target
				),
			*_legacy_free_cast_chips(
				free_casts
				),
			),
		level=1,
		)


def Resolve_Tiefling_Features(
	target,
	) -> None:
	"""Project gained Tiefling Tags, spells, and Records."""
	from AtlasMagia import Lodge_of_Spells

	from AtlasActorLudi.SpeciesKit.catalog import Current_Heritage
	from AtlasActorLudi.SpeciesKit.Tieflings import Otherworldly_Presence
	from AtlasActorLudi.SpeciesKit.Tieflings import Tiefling

	if target not in Tiefling:
		return

	heritage = Current_Heritage( target )

	if heritage is None:
		return

	unlocked = Resolve_Species_Spells(
		target,
		(
			*Otherworldly_Presence.SPELLS,
			*heritage.SPELLS,
			),
		)
	legacy_spell_names = {
		getattr(
			Lodge_of_Spells,
			provider_key,
			).name
		for required_level, provider_key in heritage.SPELLS
		if target.level >= required_level
		}
	legacy_spells = tuple(
		spell
		for spell in unlocked
		if spell.name in legacy_spell_names
		)
	# Settled here rather than when the Heritage landed, because the Guild did
	# not exist yet and this follows whatever the Character casts with.
	ability = Align_Lineage_Ability(
		target,
		Fiendish_Legacy.SPELLCASTING_ABILITIES,
		)
	ability_label = ABILITY_LABELS.get(
		ability,
		ability,
		)

	_project_darkvision( target )
	_project_otherworldly_presence(
		target,
		ability_label,
		)
	_project_fiendish_legacy(
		target,
		heritage,
		legacy_spells,
		ability_label,
		)
