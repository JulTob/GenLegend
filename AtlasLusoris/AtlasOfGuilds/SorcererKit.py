"""
SorcererKit

The Sorcerer Guild owns its 2024 progression, declared as data on its Tags
the way FighterKit declares the Fighter's.  Nothing here narrates a level in
an if-ladder.

	Sorcerer                 FEATURES, CHOICES, RESOURCES, SLOT_CREATION
	each Sorcerous Origin    FEATURES, and ALWAYS_PREPARED when it has spells;
	                         the Clockwork Origin also MANIFESTATIONS

The lessons themselves are Training Tags in
``AtlasOfTraining/Map_of_Sorcerer_Training.py``, which read these Reports
back whenever an entry quotes a number.  Metamagic options are Tags of their
own, in ``MetamagicKit``.

Choices the generator makes for a Sorcerer, and where each one lands:

	Metamagic options     Tag memberships     settled after the Origin commits
	Elemental Affinity    a Record            drawn by the level 6 lesson
	Manifestation of Order  a Record          drawn by the level 3 lesson

The first is a Tagging, and TagKit refuses to Tag a Target mid-application,
so it rides the Origin's ``after`` rite instead of a Training's ``apply``.
The other two only write Records, so they stay with the lesson that names
them, as the Bard's and the Barbarian's choices do.

The class and Origin descriptions are not written yet.  The fantasy is being
settled with Julio first; the prose lands on these Tags once it is.
"""

from __future__ import annotations

from dataclasses import dataclass

from TagKit import Report

from AtlasLusoris.Compass_of_Progression import (
	Always_Prepared,
	Choice_Progression,
	Feature_Grant,
	Resource_Progression,
	)
from AtlasLusoris.GuildKit import Build_Specialization
from AtlasLusoris.GuildKit import Sorcerer
from AtlasLusoris.MetamagicKit import (
	METAMAGIC,
	Apply_Metamagic,
	)
from AtlasMagia.Lodge_of_Spells import (
	Aid,
	Alarm,
	AlterSelf,
	ArcaneEye,
	ArmsOfHadar,
	CalmEmotions,
	CharmMonster,
	ChromaticOrb,
	Command,
	DetectThoughts,
	DispelMagic,
	DissonantWhispers,
	DragonsBreath,
	EvardsBlackTentacles,
	Fear,
	Fly,
	FreedomofMovement,
	GreaterRestoration,
	HungerHadar,
	LegendLore,
	LesserRestoration,
	MindSliver,
	ProtectionfromEnergy,
	ProtectionfromEvilandGood,
	RarysTelepathicBond,
	Sending,
	SummonAberration,
	SummonConstruct,
	SummonDragon,
	Telekinesis,
	WallofForce,
	)


GUILD = "Sorcerer"


# ---------------------------------------------------------------------------
# Declaration types owned by the Sorcerer
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Slot_Creation:
	"""One row of the Creating Spell Slots table."""

	slot_level: int
	cost: int
	sorcerer_level: int

	def __post_init__(self) -> None:
		if not 1 <= self.slot_level <= 5:
			raise ValueError(
				"Slot_Creation slot_level must be between 1 and 5, "
				f"not {self.slot_level!r}."
				)
		if self.cost < 1 or self.sorcerer_level < 1:
			raise ValueError(
				"Slot_Creation cost and sorcerer_level must be positive."
				)


# ---------------------------------------------------------------------------
# The core Sorcerer progression (PHB 2024)
# ---------------------------------------------------------------------------


SORCERER_FEATURES = (
	Feature_Grant(1, "Spellcasting"),
	Feature_Grant(1, "Innate Sorcery"),
	Feature_Grant(2, "Font of Magic"),
	Feature_Grant(2, "Metamagic"),
	Feature_Grant(5, "Sorcerous Restoration"),
	Feature_Grant(7, "Sorcery Incarnate"),
	Feature_Grant(20, "Arcane Apotheosis"),
	)

METAMAGIC_CHOICE = Choice_Progression(
	name="Metamagic",
	gains=(
			(2, 2),
			(10, 2),
			(17, 2),
			),
	options=tuple(
			METAMAGIC
			),
	)

SORCERER_CHOICES = (
	METAMAGIC_CHOICE,
	Choice_Progression(
			name="General Feat",
			gains=tuple(
					(level, 1)
					for level in (4, 8, 12, 16)
					),
			),
	Choice_Progression(
			name="Epic Boon",
			gains=(
					(19, 1),
					),
			),
	)

SORCERER_RESOURCES = (
	Resource_Progression(
			name="Sorcery Points",
			values=tuple(
					(level, str(level))
					for level in range(2, 21)
					),
			),
	Resource_Progression(
			name="Innate Sorcery",
			values=(
					(1, "2"),
					),
			),
	)

SLOT_CREATION = (
	Slot_Creation(1, 2, 2),
	Slot_Creation(2, 3, 3),
	Slot_Creation(3, 5, 5),
	Slot_Creation(4, 6, 7),
	Slot_Creation(5, 7, 9),
	)

Sorcerer.FEATURES = Report(SORCERER_FEATURES)
Sorcerer.CHOICES = Report(SORCERER_CHOICES)
Sorcerer.RESOURCES = Report(SORCERER_RESOURCES)
Sorcerer.SLOT_CREATION = Report(SLOT_CREATION)


# ---------------------------------------------------------------------------
# Reading the declarations for one Character
# ---------------------------------------------------------------------------


def _rank(
		char,
		) -> int:
	from AtlasLusoris.TrainingKit import level_in_guild
	return level_in_guild(
		char,
		GUILD,
		)


def _resource(
		name: str,
		char,
		) -> int:
	resource = next(
		resource
		for resource in SORCERER_RESOURCES
		if resource.name == name
		)
	value = resource.at(
		_rank(
			char
			)
		)
	return int(
		value or 0
		)


def Find_Sorcery_Points(
		char,
		) -> int:
	"""Sorcery Points at this Sorcerer level: none before level 2."""
	return _resource(
		"Sorcery Points",
		char,
		)


def Find_Innate_Sorcery_Uses(
		char,
		) -> int:
	"""Uses of Innate Sorcery between Long Rests."""
	return _resource(
		"Innate Sorcery",
		char,
		)


def Find_Metamagic_Count(
		char,
		) -> int:
	"""How many Metamagic options a Sorcerer of this level knows."""
	return METAMAGIC_CHOICE.total_at(
		_rank(
			char
			)
		)


def Find_Creatable_Slots(
		char,
		) -> tuple[Slot_Creation, ...]:
	"""The rows of the Creating Spell Slots table this Sorcerer has reached."""
	level = _rank(
		char
		)
	return tuple(
		row
		for row in SLOT_CREATION
		if row.sorcerer_level <= level
		)


def Find_Origin(
		char,
		):
	"""The Sorcerous Origin Shape this Character carries, or None."""
	from AtlasLusoris.GuildKit import specializations_on
	for tag in specializations_on(
			char
			):
		if tag in SPECIALIZATIONS:
			return tag
	return None


def Find_Always_Prepared(
		char,
		) -> tuple:
	"""
	Every Origin spell this Sorcerer keeps prepared at their level.

	Read from the Origin's ALWAYS_PREPARED Report, so the lesson that names
	them and the Spellcasting section that lists them cannot disagree.
	"""
	origin = Find_Origin(
		char
		)
	ladder = getattr(
		origin,
		"ALWAYS_PREPARED",
		None,
		)
	if ladder is None:
		return ()
	return ladder.at(
		_rank(
			char
			)
		)


# ---------------------------------------------------------------------------
# Choices that land as Records
# ---------------------------------------------------------------------------


def Resolve_Elemental_Affinity(
		char,
		) -> str:
	"""
	The damage type this Draconic Sorcerer's magic answers to, drawn once.

	Drawn from the five types the dragons breathe, as the Dragonborn's own
	Draconic Ancestors table lists them, but never one the Character already
	resists.  Elemental Affinity grants that Resistance, and a Dragonborn
	whose Sorcery repeated their ancestry would be granted what they already
	had.  The same holds for a Dwarf's Poison and a Tiefling's legacy.  Only
	if every type is already resisted, with nothing left to waste, is any
	type allowed.

	Drawn from its own named Dice Bag, level-free, so the element never
	changes between levels and never moves the Dragonborn's own draw.
	"""
	standing = getattr(
		char,
		"elemental_affinity",
		None,
		)
	if standing:
		return standing

	from AtlasActorLudi.SpeciesKit.Dragonborn.Map_of_Ancestors import (
		DRACONIC_ANCESTORS,
		)

	draconic_types = sorted(
		set(
			DRACONIC_ANCESTORS.values()
			)
		)
	resisted = set(
		getattr(
			char,
			"damage_resistances",
			(),
			) or ()
		)
	unresisted = [
		damage
		for damage in draconic_types
		if damage not in resisted
		]
	pool = unresisted or draconic_types

	dice = char.Dice_Bag(
		"sorcerer.draconic.affinity",
		version="1",
		namespace="GenLegendSorcerer",
		)
	affinity = char.Pick(
		pool,
		dice=dice,
		)
	char.elemental_affinity = affinity
	return affinity


def Resolve_Manifestation_Of_Order(
		char,
		) -> str:
	"""How this Clockwork Sorcerer's link to order shows, drawn once."""
	standing = getattr(
		char,
		"manifestation_of_order",
		None,
		)
	if standing:
		return standing
	dice = char.Dice_Bag(
		"sorcerer.clockwork.manifestation",
		version="1",
		namespace="GenLegendSorcerer",
		)
	manifestation = char.Pick(
		list(
			MANIFESTATIONS_OF_ORDER
			),
		dice=dice,
		)
	char.manifestation_of_order = manifestation
	return manifestation


# ---------------------------------------------------------------------------
# Choices that land as Tags
# ---------------------------------------------------------------------------


def Settle_Sorcerer_Choices(
		char,
		) -> None:
	"""
	Carry the Metamagic options this Sorcerer has learned.

	Runs as every Origin's ``after`` rite, once the Origin has committed and
	no Tag is mid-application.  Every Sorcerer carries an Origin from their
	first level (the Origin's lessons wait for level 3 on their own), so this
	reaches every Sorcerer.  Below level 2 the count is zero and nothing is
	applied.
	"""
	Apply_Metamagic(
		char,
		Find_Metamagic_Count(
			char
			),
		)


# ---------------------------------------------------------------------------
# Aberrant Sorcery
# ---------------------------------------------------------------------------


ABERRANT_FEATURES = (
	Feature_Grant(3, "Psionic Spells"),
	Feature_Grant(3, "Telepathic Speech"),
	Feature_Grant(6, "Psionic Sorcery"),
	Feature_Grant(6, "Psychic Defenses"),
	Feature_Grant(14, "Revelation in Flesh"),
	Feature_Grant(18, "Warping Implosion"),
	)

ABERRANT_SPELLS = Always_Prepared(
	gains=(
			(3, (ArmsOfHadar, CalmEmotions, DetectThoughts, DissonantWhispers, MindSliver)),
			(5, (HungerHadar, Sending)),
			(7, (EvardsBlackTentacles, SummonAberration)),
			(9, (RarysTelepathicBond, Telekinesis)),
			),
	)

AberrantSorcery = Build_Specialization(
	guild=Sorcerer,
	name="Aberrant Sorcery",
	module=__name__,
	reports={
			"FEATURES": ABERRANT_FEATURES,
			"ALWAYS_PREPARED": ABERRANT_SPELLS,
			},
	after=Settle_Sorcerer_Choices,
	)


# ---------------------------------------------------------------------------
# Clockwork Sorcery
# ---------------------------------------------------------------------------


CLOCKWORK_FEATURES = (
	Feature_Grant(3, "Clockwork Spells"),
	Feature_Grant(3, "Restore Balance"),
	Feature_Grant(6, "Bastion of Law"),
	Feature_Grant(14, "Trance of Order"),
	Feature_Grant(18, "Clockwork Cavalcade"),
	)

CLOCKWORK_SPELLS = Always_Prepared(
	gains=(
			(3, (Aid, Alarm, LesserRestoration, ProtectionfromEvilandGood)),
			(5, (DispelMagic, ProtectionfromEnergy)),
			(7, (FreedomofMovement, SummonConstruct)),
			(9, (GreaterRestoration, WallofForce)),
			),
	)

# The rulebook offers six ways the link to order can show while this Sorcerer
# casts.  One is drawn per Character and printed with Clockwork Spells.  Each
# is written to finish the sentence "While you cast your Sorcerer spells, …",
# so the lesson prints it as authored and never reformats it.
MANIFESTATIONS_OF_ORDER = (
	"spectral cogwheels turn in the air behind you.",
	"the hands of a clock sweep across your eyes.",
	"your skin takes on a sheen of polished brass.",
	"equations and bright geometric figures drift across your body.",
	"your Spellcasting Focus becomes, for a moment, a Tiny clockwork mechanism.",
	"you, and whoever your magic touches, hear gears ticking or a clock striking.",
	)

ClockworkSorcery = Build_Specialization(
	guild=Sorcerer,
	name="Clockwork Sorcery",
	module=__name__,
	reports={
			"FEATURES": CLOCKWORK_FEATURES,
			"ALWAYS_PREPARED": CLOCKWORK_SPELLS,
			"MANIFESTATIONS": MANIFESTATIONS_OF_ORDER,
			},
	after=Settle_Sorcerer_Choices,
	)


# ---------------------------------------------------------------------------
# Draconic Sorcery
# ---------------------------------------------------------------------------


DRACONIC_FEATURES = (
	Feature_Grant(3, "Draconic Resilience"),
	Feature_Grant(3, "Draconic Spells"),
	Feature_Grant(6, "Elemental Affinity"),
	Feature_Grant(14, "Dragon Wings"),
	Feature_Grant(18, "Dragon Companion"),
	)

DRACONIC_SPELLS = Always_Prepared(
	gains=(
			(3, (AlterSelf, ChromaticOrb, Command, DragonsBreath)),
			(5, (Fear, Fly)),
			(7, (ArcaneEye, CharmMonster)),
			(9, (LegendLore, SummonDragon)),
			),
	)

DraconicSorcery = Build_Specialization(
	guild=Sorcerer,
	name="Draconic Sorcery",
	module=__name__,
	reports={
			"FEATURES": DRACONIC_FEATURES,
			"ALWAYS_PREPARED": DRACONIC_SPELLS,
			},
	after=Settle_Sorcerer_Choices,
	)


# ---------------------------------------------------------------------------
# Wild Magic Sorcery
# ---------------------------------------------------------------------------


WILD_MAGIC_FEATURES = (
	Feature_Grant(3, "Wild Magic Surge"),
	Feature_Grant(3, "Tides of Chaos"),
	Feature_Grant(6, "Bend Luck"),
	Feature_Grant(14, "Controlled Chaos"),
	Feature_Grant(18, "Tamed Surge"),
	)

WildMagicSorcery = Build_Specialization(
	guild=Sorcerer,
	name="Wild Magic Sorcery",
	module=__name__,
	reports={
			"FEATURES": WILD_MAGIC_FEATURES,
			},
	after=Settle_Sorcerer_Choices,
	)


SPECIALIZATIONS = (
	AberrantSorcery,
	ClockworkSorcery,
	DraconicSorcery,
	WildMagicSorcery,
	)


# ---------------------------------------------------------------------------
# Focused self-test
# ---------------------------------------------------------------------------


def _self_test() -> None:
	assert METAMAGIC_CHOICE.total_at(1) == 0
	assert METAMAGIC_CHOICE.total_at(2) == 2
	assert METAMAGIC_CHOICE.total_at(10) == 4
	assert METAMAGIC_CHOICE.total_at(20) == 6
	assert SORCERER_RESOURCES[0].at(1) is None
	assert SORCERER_RESOURCES[0].at(20) == "20"
	assert [
		row.cost
		for row in SLOT_CREATION
		] == [
		2,
		3,
		5,
		6,
		7,
		]

	for origin, count in (
			(AberrantSorcery, 11),
			(ClockworkSorcery, 10),
			(DraconicSorcery, 10),
			):
		spells = origin.ALWAYS_PREPARED.at(
			20
			)
		assert len(
			spells
			) == count, origin.NAME
	assert DraconicSorcery.ALWAYS_PREPARED.at(
		4
		)[-1].name == "Dragon's Breath"
	assert DraconicSorcery.ALWAYS_PREPARED.at(
		9
		)[-1].name == "Summon Dragon"
	assert not hasattr(
		WildMagicSorcery,
		"ALWAYS_PREPARED",
		)
	assert len(
		ClockworkSorcery.MANIFESTATIONS
		) == 6
	assert {
		spec.NAME
		for spec in Sorcerer.SPECIALIZATIONS
		} == {
		spec.NAME
		for spec in SPECIALIZATIONS
		}
	print(
		"OK — SorcererKit self-test"
		)


if __name__ == "__main__":
	_self_test()
