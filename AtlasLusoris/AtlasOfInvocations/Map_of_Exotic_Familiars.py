"""
Map of Exotic Familiars — a familiar nobody else at the table has.

The eight published forms in ``Map_of_Familiars`` are fixed creatures out of
the Monster Manual.  This is the other route: the spirit is *built*, from a
creature type and a pool of traits, so what answers the summons is a slime, or
a living toy, or a drake the size of a dog, and it belongs to that character.

The shape is deliberately the one everybody already knows from monster-collecting
games.  A **type** decides the damage, the look, and which traits are even
possible; the traits are the moveset.  Nothing in the pool escalates damage,
because that is where familiars break: every trait buys a *sense*, a *movement
mode*, or a *trick*.  A familiar that flies, sees the invisible and carries
messages is a delight at any level and a threat at none.

Budget is the caster's Proficiency Bonus, and tiers gate what is reachable, so
a level 1 familiar gets two small talents and a level 17 one gets six, some of
them strange.  The numbers come from the 2023 playtest Pact Familiar, which is
the only version of these rules that scales with its caster:

	AC      10 + spellcasting modifier
	HP      5 + Warlock level, in d4 Hit Dice
	strike  2 + half Warlock level, damage by type

Naming follows the type and the look, so the sheet says what it is and what it
resembles: *Undead Familiar (ghost-like)*, *Ooze Familiar (slime-like)*.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(
	frozen=True,
	)
class Trait:
	"""One talent a summoned familiar might have."""

	name: str
	text: str
	# Types that may have it.  Empty means any type may.
	types: tuple[str, ...] = field(
		default_factory=tuple,
		)
	tier: int = 1

	def allowed(
			self,
			kind: str,
			) -> bool:
		return not self.types or kind in self.types


@dataclass(
	frozen=True,
	)
class Familiar_Type:
	"""A type: what it is made of, what it looks like, what it does on a hit."""

	name: str
	damage: str
	looks: tuple[str, ...]
	affinity: tuple[str, ...] = field(
		default_factory=tuple,
		)


TYPES = {
	record.name: record
	for record in (
		Familiar_Type(
			name="Aberration",
			damage="Acid",
			looks=(
				"a flumph",
				"a knot of tentacles",
				"a single floating eye",
				"a mouth that hums",
				),
			affinity=(
				"Great Old One",
				"Aberrant",
				"Aberration",
				"Hermeticist",
				),
			),
		Familiar_Type(
			name="Celestial",
			damage="Radiant",
			looks=(
				"an owl too clean for the weather",
				"a raven with no shadow",
				"a small winged thing that hums plainchant",
				"a hare that will not be looked at directly",
				),
			affinity=(
				"Celestial",
				"Aasimar",
				"Acolyte",
				"Inquisitor",
				),
			),
		Familiar_Type(
			name="Construct",
			damage="Force",
			looks=(
				"a living toy",
				"a clockwork bird missing one wing",
				"a doll somebody loved to pieces",
				"a hand, walking",
				),
			affinity=(
				"Construct",
				"Artificer",
				"Crafter",
				"Hermeticist",
				),
			),
		Familiar_Type(
			name="Dragon",
			damage="Fire",
			looks=(
				"a drake the size of a dog",
				"a winged serpent",
				"a dragonet with an inflated opinion",
				"a lizard that reads over your shoulder",
				),
			affinity=(
				"Dragon",
				"Draconic",
				"Kobold",
				"Sorcerer",
				),
			),
		Familiar_Type(
			name="Elemental",
			damage="Thunder",
			looks=(
				"an ember that will not go out",
				"a dust devil the size of a cat",
				"a puddle that follows",
				"a draught with opinions",
				),
			affinity=(
				"Elemental",
				"Genasi",
				"Storm",
				),
			),
		Familiar_Type(
			name="Fey",
			damage="Psychic",
			looks=(
				"a pixie",
				"a fox with one tail too many",
				"a moth the colour of a rumour",
				"a child's drawing of a bird",
				),
			affinity=(
				"Fey",
				"Elf",
				"Destined",
				"Naturalist",
				"Wildkeeper",
				),
			),
		Familiar_Type(
			name="Fiend",
			damage="Poison",
			looks=(
				"an imp",
				"a goat-eyed cat",
				"a toad wearing a very small ring",
				"a rat that keeps accounts",
				),
			affinity=(
				"Fiend",
				"Tiefling",
				"Infernal",
				"Servant",
				),
			),
		Familiar_Type(
			name="Monstrosity",
			damage="Piercing",
			looks=(
				"an owlbear cub",
				"a chimera the size of a loaf",
				"something with the wrong number of joints",
				"a crab wearing a bird's skull",
				),
			affinity=(
				"Monstrosity",
				"Beast",
				"Hunter",
				"Survivalist",
				),
			),
		Familiar_Type(
			name="Ooze",
			damage="Acid",
			looks=(
				"a slime",
				"a bucket of something that likes you",
				"a stain that arrives before you do",
				"a jar you did not pack",
				),
			affinity=(
				"Ooze",
				"Alchemist",
				"Hermeticist",
				),
			),
		Familiar_Type(
			name="Undead",
			damage="Necrotic",
			looks=(
				"a ghost",
				"a skull with a candle in it",
				"a shadow that is not yours",
				"a doll that was buried with somebody",
				),
			affinity=(
				"Undead",
				"Necromancy",
				"Spirit Medium",
				"Exorcist",
				"Survivor",
				),
			),
		)
	}


# The moveset.  Senses, movement and tricks only: nothing here raises damage,
# which is the one axis that turns a familiar into a second character.
TRAITS = (
	Trait(
		name="Keen Senses",
		text="Darkvision 60 feet and Advantage on Perception checks relying on sight.",
		),
	Trait(
		name="Nose for It",
		text="Advantage on Perception and Survival checks that rely on smell.",
		),
	Trait(
		name="Small Places",
		text="It can move through a space as narrow as one inch without squeezing.",
		),
	Trait(
		name="Courier",
		text="It can carry and deliver a written message, and will not be talked out of it.",
		),
	Trait(
		name="Mimic",
		text="It can reproduce any sound or voice it has heard, badly enough to be funny and well enough to work once.",
		),
	Trait(
		name="Deliver Spell",
		text="When you cast a spell with a range of touch, the familiar can deliver it with its own touch while within 120 feet of you.",
		tier=2,
		),
	Trait(
		name="Climber",
		text="Climb Speed equal to its Speed, including across ceilings.",
		types=(
			"Aberration",
			"Construct",
			"Fiend",
			"Monstrosity",
			"Ooze",
			),
		),
	Trait(
		name="Flight",
		text="Fly Speed 40 feet.",
		types=(
			"Celestial",
			"Dragon",
			"Elemental",
			"Fey",
			"Fiend",
			"Undead",
			),
		),
	Trait(
		name="Swimmer",
		text="Swim Speed equal to its Speed, and it can breathe underwater.",
		types=(
			"Aberration",
			"Elemental",
			"Monstrosity",
			"Ooze",
			),
		),
	Trait(
		name="Burrower",
		text="Burrow Speed 15 feet through earth and loose stone.",
		types=(
			"Aberration",
			"Construct",
			"Monstrosity",
			"Ooze",
			),
		),
	Trait(
		name="Incorporeal Step",
		text="Once per Short Rest it can pass through a solid object no thicker than five feet, taking 1d10 Force damage if it ends its move inside one.",
		types=(
			"Fey",
			"Undead",
			),
		tier=2,
		),
	Trait(
		name="Seep",
		text="It can pass through any opening that would admit water, carrying nothing.",
		types=(
			"Elemental",
			"Ooze",
			),
		tier=2,
		),
	Trait(
		name="Sees the Unseen",
		text="It perceives Invisible creatures and objects within 30 feet.",
		types=(
			"Aberration",
			"Celestial",
			"Fey",
			"Undead",
			),
		tier=2,
		),
	Trait(
		name="Tremorsense",
		text="Tremorsense 30 feet.",
		types=(
			"Aberration",
			"Construct",
			"Monstrosity",
			"Ooze",
			),
		tier=2,
		),
	Trait(
		name="Reads the Room",
		text="It knows whether a creature it can see is lying, though not what the truth is.",
		types=(
			"Aberration",
			"Celestial",
			"Fey",
			"Fiend",
			),
		tier=2,
		),
	Trait(
		name="Stubborn Little Thing",
		text="Advantage on saving throws against being Charmed or Frightened, and it cannot be turned against you.",
		tier=2,
		),
	Trait(
		name="Extradimensional Escape",
		text="When it would drop to 0 Hit Points it instead drops to 1 and vanishes for 1 hour, or until you call it back as a Magic action. Recharges on a Long Rest.",
		tier=2,
		),
	Trait(
		name="Bearer",
		text="It is Small rather than Tiny and can carry a rider of its own size or smaller at its Speed.",
		types=(
			"Construct",
			"Dragon",
			"Elemental",
			"Monstrosity",
			),
		tier=3,
		),
	Trait(
		name="Borrowed Eyes",
		text="You can see and hear through it at any distance while you are on the same plane.",
		tier=3,
		),
	Trait(
		name="Second Shape",
		text="As a Bonus Action it takes another look from its type's list, keeping its statistics.",
		tier=3,
		),
	Trait(
		name="Ward",
		text="Once per Long Rest, when you would take damage while it is within 5 feet, it takes the damage instead.",
		tier=3,
		),
	Trait(
		name="Knows the Way",
		text="It always knows the direction and rough distance to a place it has been.",
		tier=3,
		),
	Trait(
		name="Unsleeping",
		text="It does not sleep, eat or breathe, and keeps watch without complaint.",
		types=(
			"Construct",
			"Elemental",
			"Undead",
			),
		),
	)


@dataclass(
	frozen=True,
	)
class Summoned_Familiar:
	"""One built familiar, ready for the sheet."""

	kind: Familiar_Type
	look: str
	traits: tuple[Trait, ...]
	armour_class: int
	hit_points: int
	hit_dice: str
	strike: str

	def title(
			self,
			) -> str:
		return f"{self.kind.name} Familiar ({self.look})"

	def block(
			self,
			) -> str:
		rows = [
			self.title(),
			f"AC {self.armour_class} · HP {self.hit_points} ({self.hit_dice}) · Speed 30 ft.",
			f"Strike. Melee spell attack, reach 5 ft., {self.strike} {self.kind.damage} damage.",
			]
		rows.extend(
			f"{trait.name}. {trait.text}"
			for trait in self.traits
			)

		return "\n".join(
			rows
			)


def _tier_for(
		level: int,
		) -> int:
	"""How strange a familiar may get at this level."""
	if level >= 11:
		return 3

	return 2 if level >= 5 else 1


def summon_familiar(
		char,
		level: int | None = None,
		kind: str | None = None,
		*,
		dice,
		) -> Summoned_Familiar:
	"""
	Build one exotic familiar for this caster.

	Type is drawn by Familial Preference, so what answers follows from what the
	caster is.  Traits are drawn from the pool its type allows, as many as the
	caster's Proficiency Bonus, and only up to the tier their level has earned.
	"""
	from AtlasLusoris.AtlasOfInvocations.Map_of_Familiars import (
		AFFINITY_WEIGHT,
		_caster_marks,
		)

	level = int(
		level
		or getattr(
			char,
			"level",
			1,
			)
		or 1
		)
	bonus = (
		level - 1
		) // 4 + 2

	if kind is None:
		marks = _caster_marks(
			char
			)
		names = list(
			TYPES
			)
		weights = [
			AFFINITY_WEIGHT
			if any(
				word.lower() in marks
				for word in TYPES[name].affinity
				)
			else 1
			for name in names
			]
		kind = char.Pick(
			names,
			weights,
			dice=dice,
			)

	record = TYPES[
		kind
		]
	ceiling = _tier_for(
		level
		)
	pool = [
		trait
		for trait in TRAITS
		if trait.allowed(
			record.name
			)
		and trait.tier <= ceiling
		]
	chosen: list[Trait] = []

	while pool and len(
		chosen
		) < bonus:
		trait = char.Pick(
			pool,
			dice=dice,
			)
		chosen.append(
			trait
			)
		pool.remove(
			trait
			)

	casting = int(
		getattr(
			char,
			"spell_attack_modifier",
			0,
			) or 3
		)

	return Summoned_Familiar(
		kind=record,
		look=char.Pick(
			list(
				record.looks
				),
			dice=dice,
			),
		traits=tuple(
			sorted(
				chosen,
				key=lambda trait: (
					trait.tier,
					trait.name,
					),
				)
			),
		armour_class=10 + casting,
		hit_points=5 + level,
		hit_dice=f"{level}d4",
		strike=f"{2 + level // 2}",
		)


__all__ = (
	"Familiar_Type",
	"Summoned_Familiar",
	"TRAITS",
	"TYPES",
	"Trait",
	"summon_familiar",
	)
