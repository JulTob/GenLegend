"""Shared Species and Creature Type Geometry."""

from TopKit import Action
from TopKit import Pre
from TopKit import Tag
from TopKit import Underlay

from AtlasActorLudi.CharactersKit import Character


def _display_tag_name(
	tag,
	) -> str:
	return tag.__name__.replace(
		"_",
		" ",
		)


def Find_Species(
	target,
	) -> str:
	"""Find the narrative Species label from current Tag membership."""
	from AtlasActorLudi.SpeciesKit.catalog import Current_Species

	species = Current_Species(target)

	if species is None:
		return ""

	return _display_tag_name(species)


def Find_Heritage(
	target,
	) -> str:
	"""Find the narrative Heritage label from current Tag membership."""
	from AtlasActorLudi.SpeciesKit.catalog import Current_Heritage

	heritage = Current_Heritage(target)

	if heritage is None:
		return ""

	return _display_tag_name(heritage)


def Find_Subspecies(
	target,
	) -> str:
	"""Find the Heritage exposed through the older Subspecies vocabulary."""
	return Find_Heritage(target)


class Species(Tag):
	"""A Character's lineage and physical form."""

	@Pre
	def Character_Only(
		target,
		):
		return isinstance(
			target,
			Character,
			)

	@Action
	@Underlay
	def __format__(
		target,
		prior,
		specification,
		):
		"""Render the Species view and delegate every other format."""
		if specification.strip().casefold() == "species":
			return Find_Species(target)

		return prior(specification)


def No_Species_Yet(
	target,
	) -> bool:
	"""
	The gate every Species Shape declares: a Character has one Species.

	It sits on each Shape, not on ``Species``, because TopKit 0.2.0a3 does
	not re-run a Base's Preconditions when a second Shape of an active Base is
	applied (QST-0093.10).  Refusing at the gate keeps the conflict atomic.
	"""
	return target not in Species


class Heritage(Species):
	"""A more-specific lineage Shape beneath a Species."""

	@Action
	@Underlay
	def __format__(
		target,
		prior,
		specification,
		):
		"""Render the Heritage view and delegate every other format."""
		view = specification.strip().casefold()

		if view == "heritage":
			return Find_Heritage(target)

		if view == "subspecies":
			return Find_Subspecies(target)

		return prior(specification)


class Creature_Type(Tag):
	"""Canonical rules classification, independent from Species."""

	@Pre
	def Character_Only(
		target,
		):
		return isinstance(
			target,
			Character,
			)


class Humanoid(Creature_Type):
	"""A humanoid creature."""


class Fey(Creature_Type):
	"""A fey creature."""


class Elemental(Creature_Type):
	"""An elemental creature."""


class Celestial(Creature_Type):
	"""A celestial creature."""


class Undead(Creature_Type):
	"""An undead creature."""


class Vampire(Undead):
	"""An Undead creature with vampiric context."""


class Beast(Creature_Type):
	"""A beast."""


class Construct(Creature_Type):
	"""A constructed creature."""


class Dragon(Creature_Type):
	"""A dragon."""


class Fiend(Creature_Type):
	"""A fiend."""


class Aberration(Creature_Type):
	"""An aberration."""


class Giant(Creature_Type):
	"""A giant."""


class Monstrosity(Creature_Type):
	"""A monstrosity."""


class Ooze(Creature_Type):
	"""An ooze."""


class Plant(Creature_Type):
	"""A plant creature."""


CREATURE_TYPES = (
	Aberration,
	Beast,
	Celestial,
	Construct,
	Dragon,
	Elemental,
	Fey,
	Fiend,
	Giant,
	Humanoid,
	Monstrosity,
	Ooze,
	Plant,
	Undead,
	)

CREATURE_TYPE_TAGS = {
	tag.__name__: tag
	for tag in CREATURE_TYPES
	}


def Resolve_Creature_Type(
	requested,
	):
	"""Resolve a canonical Creature Type key or Tag."""
	if (
		isinstance(
			requested,
			type,
			)
		and issubclass(
			requested,
			Creature_Type,
			)
		):
		if requested is Vampire:
			return Undead

		if requested in CREATURE_TYPES:
			return requested

	key = str(requested).strip().replace(
		" ",
		"_",
		)

	for name, tag in CREATURE_TYPE_TAGS.items():
		if name.casefold() == key.casefold():
			return tag

	raise ValueError(
		f"Unknown Creature Type: {requested!r}."
		)


def Current_Creature_Type(
	target,
	):
	"""Return the one canonical Creature Type currently carried."""
	carried = tuple(
		tag
		for tag in CREATURE_TYPES
		if target in tag
		)

	if len(carried) > 1:
		raise ValueError(
			"A Character carries conflicting Creature Types: "
			+ ", ".join(
				tag.__name__
				for tag in carried
				)
			+ "."
			)

	return (
		carried[0]
		if carried
		else None
		)


def Apply_Creature_Type(
	target,
	requested,
	):
	"""Apply one canonical Creature Type and project its display key."""
	selected = Resolve_Creature_Type(requested)
	current = Current_Creature_Type(target)

	if (
		current is not None
		and current is not selected
		):
		raise ValueError(
			"A Character cannot carry two Creature Types: "
			f"{current.__name__!r} and {selected.__name__!r}."
			)

	if target not in selected:
		selected(target)

	target.creature_type = selected.__name__

	return selected


def No_Heritage_Yet(
	target,
	) -> bool:
	"""The gate every Heritage Shape declares: a Character has one Heritage."""
	return target not in Heritage
