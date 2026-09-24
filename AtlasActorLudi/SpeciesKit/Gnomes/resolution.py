"""Resolve Gnome rules onto a completed Character sheet."""

from AtlasActorLudi.SpeciesKit.magic import ABILITY_LABELS
from AtlasActorLudi.SpeciesKit.magic import Resolve_Species_Spells
from AtlasActorLudi.SpeciesKit.Gnomes.traits import Gnomish_Lineage
from AtlasActorLudi.SpeciesKit.magic import Align_Lineage_Ability
from AtlasActorLudi.SpeciesKit.magic import Species_Spellcasting_Chips
from AtlasActorLudi.SpeciesKit.presentation import Project_Species_Feature
from AtlasActorLudi.SpeciesKit.traits import Darkvision
from AtlasActorLudi.SpeciesKit.traits import Darkvision_Rules
from AtlasVenustas import Chip


def _forest_lineage(
		target,
		heritage,
		ability_label,
		):
	from AtlasMagia import Lodge_of_Spells

	free_spell = getattr(
		Lodge_of_Spells,
		heritage.FREE_CAST_SPELL,
		).name
	free_casts = (
		int(
			getattr(
				target,
				"proficiency_bonus",
				2,
				)
			)
		if heritage.FREE_CASTS == "PB"
		else int(
			heritage.FREE_CASTS
			)
		)
	target.species_spell_free_casts = {
		free_spell: free_casts,
		}
	Project_Species_Feature(
		target,
		"Forest Gnome Lineage",
		(
			"You were not supposed to go into the woods, but the Fey "
			"felt closer there, and you learnt to listen: to them "
			"when you found one, and to the birds and bees when you "
			"didn't, until both talked back. "
			f"<b>Spellcasting Ability.</b> {ability_label}. "
			"<br><b>Minor Illusion.</b> You know the Minor Illusion cantrip. "
			f"<br><b>{free_spell}.</b> You always have the spell prepared. "
			f"You can cast it without a spell slot {free_casts} times "
			"(equal to your Proficiency Bonus), regaining all uses on "
			"a Long Rest, and can also cast it with spell slots."
			),
		chips=(
			*Species_Spellcasting_Chips(
				target
				),
			Chip(
				"🐿️",
				f"{free_spell} Uses",
				free_casts,
				),
			),
		level=1,
		)


def _rock_lineage(
		target,
		heritage,
		ability_label,
		):
	target.rock_gnome_device_limit = heritage.DEVICE_LIMIT
	target.rock_gnome_device_armor_class = heritage.DEVICE_ARMOR_CLASS
	target.rock_gnome_device_hit_points = heritage.DEVICE_HIT_POINTS
	target.rock_gnome_device_duration_hours = heritage.DEVICE_DURATION_HOURS
	target.rock_gnome_device_casting_minutes = heritage.DEVICE_CASTING_MINUTES
	target.rock_gnome_device_activation = heritage.DEVICE_ACTIVATION
	target.rock_gnome_device_dismantle_action = (
		heritage.DEVICE_DISMANTLE_ACTION
		)
	target.rock_gnome_device_requires_touch = heritage.DEVICE_REQUIRES_TOUCH
	target.species_spell_free_casts = {}
	Project_Species_Feature(
		target,
		"Rock Gnome Lineage",
		(
			"You learned early that anything could be taken apart "
			"and improved, and somewhere along the way you learned "
			"to do it with a word instead of a screwdriver. "
			f"<b>Spellcasting Ability.</b> {ability_label}. "
			"<br><b>Cantrips.</b> You know Mending and Prestidigitation. "
			f"<br><b>Clockwork Device.</b> In {heritage.DEVICE_CASTING_MINUTES} "
			"minutes, you can use Prestidigitation to create a Tiny device "
			f"with AC {heritage.DEVICE_ARMOR_CLASS}, "
			f"{heritage.DEVICE_HIT_POINTS} Hit Point, and one chosen "
			"Prestidigitation effect. If that effect offers options, the "
			"device holds one chosen option. You or another creature can "
			f"activate it with a {heritage.DEVICE_ACTIVATION} while "
			"touching it. You can maintain no more than "
			f"{heritage.DEVICE_LIMIT} devices; each lasts "
			f"{heritage.DEVICE_DURATION_HOURS} hours or until you dismantle "
			f"it with a touch as a {heritage.DEVICE_DISMANTLE_ACTION} action."
			),
		chips=(
			*Species_Spellcasting_Chips(
				target
				),
			Chip(
				"⚙️",
				"Clockwork Devices",
				heritage.DEVICE_LIMIT,
				),
			),
		level=1,
		)


def Resolve_Gnome_Features(
		target,
		) -> None:
	"""Project Gnome Tags into readable Entries and mechanical Records."""
	from AtlasActorLudi.SpeciesKit.catalog import Current_Heritage
	from AtlasActorLudi.SpeciesKit.Gnomes import Forest_Gnome
	from AtlasActorLudi.SpeciesKit.Gnomes import Gnome
	from AtlasActorLudi.SpeciesKit.Gnomes import Rock_Gnome

	if target not in Gnome:
		return

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
			# The eyes are biology and stated as such.  The *reason* is left as
			# the gnome's own romantic guess ("said to be", "maybe"), which is
			# how a physical trait gets some myth without the book asserting
			# one.  See Documenta/Canon/Elves-and-the-Dreaming.md: the Fae are
			# made of dream, and that is never explained on the page.
			"*The Fae are said to be part of the Dream. Maybe Gnomes still "
			"carry some of it, because you have always felt the night "
			"welcomes you.*\n\n"
			+ Darkvision_Rules(
				darkvision_range
				)
			),
		level=1,
		)
	Project_Species_Feature(
		target,
		"Gnomish Cunning",
		(
			"Curiosity got your people through worse than a spell, "
			"and it still does. You have Advantage on Intelligence, "
			"Wisdom, and Charisma saving throws."
			),
		level=1,
		)
	heritage = Current_Heritage( target )

	if heritage is None:
		return

	Resolve_Species_Spells(
		target,
		heritage.SPELLS,
		)
	# Settled here rather than when the Heritage landed, because the Guild did
	# not exist yet and this follows whatever the Character casts with.
	ability = Align_Lineage_Ability(
		target,
		Gnomish_Lineage.SPELLCASTING_ABILITIES,
		)
	ability_label = ABILITY_LABELS.get(
		ability,
		ability,
		)

	if heritage is Forest_Gnome:
		_forest_lineage(
			target,
			heritage,
			ability_label,
			)
	elif heritage is Rock_Gnome:
		_rock_lineage(
			target,
			heritage,
			ability_label,
			)
