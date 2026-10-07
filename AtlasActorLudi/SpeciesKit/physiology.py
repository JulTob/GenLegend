"""Small shared Imprint helpers for concrete Species Shapes."""


def _selected_size(
	target,
	species,
	requested,
	) -> str | None:
	options = tuple(
		getattr(
			species,
			"SIZE_OPTIONS",
			(),
			)
		)

	if not options:
		return requested

	selected = (
		requested
		or getattr(
			target,
			"size",
			None,
			)
		)

	if selected is None:
		if len(options) == 1:
			selected = options[0]
		else:
			weights = getattr(
				species,
				"SIZE_WEIGHTS",
				None,
				)
			dice_bag = target.Dice_Bag( f"{species.__name__}.size" )
			selected = dice_bag.choices(
				options,
				weights=weights,
				k=1,
				)[
				0
				]

	if selected not in options:
		raise ValueError(
			f"{species.__name__} Size must be one of "
			f"{options!r}; received {selected!r}."
			)

	return selected


def Imprint_Species(
	target,
	species,
	size=None,
	) -> None:
	"""Imprint resolved physiology while membership remains transactional."""
	from AtlasActorLudi.SpeciesKit.bases import (
		CREATURE_TYPES,
		Current_Creature_Type,
		)
	from AtlasActorLudi.SpeciesKit.catalog import Current_Species

	current_species = Current_Species(target)

	if (
		current_species is not None
		and current_species is not species
		):
		raise ValueError(
			"A Character cannot carry two Species: "
			f"{current_species.__name__!r} and {species.__name__!r}."
			)

	expected_type = next(
		(
			creature_type
			for creature_type in CREATURE_TYPES
			if issubclass(
				species,
				creature_type,
				)
			),
		None,
		)
	current_type = Current_Creature_Type(target)

	if (
		expected_type is not None
		and current_type is not None
		and current_type is not expected_type
		):
		raise ValueError(
			f"{species.__name__} requires Creature Type "
			f"{expected_type.__name__!r}, not {current_type.__name__!r}."
			)

	target.species = species.__name__.replace(
		"_",
		" ",
		)

	selected_size = _selected_size(
		target,
		species,
		size,
		)

	if selected_size is not None:
		target.size = selected_size

	speed = getattr(
		species,
		"SPEED",
		None,
		)

	if speed is not None:
		target.speed = speed


def Imprint_Heritage(
	target,
	heritage,
	) -> None:
	"""Imprint one concrete Heritage while its Tagging remains atomic."""
	from AtlasActorLudi.SpeciesKit.catalog import Current_Heritage

	current = Current_Heritage(target)

	if (
		current is not None
		and current is not heritage
		):
		raise ValueError(
			"A Character cannot carry two Heritages: "
			f"{current.__name__!r} and {heritage.__name__!r}."
			)

	target.heritage = heritage.__name__.replace(
		"_",
		" ",
		)


def _test_dice_purpose() -> None:
	#-- Ruling 8 (QST-0144.6): a Size the Species leaves open comes from one
	#-- Dice Bag opened as "<Species>.size" with the default key, over the
	#-- Species' options with its weights; a single option opens no bag.
	from random import Random

	from AtlasActorLudi.CharactersKit import Character
	from AtlasActorLudi.SpeciesKit.Elves.base import Elf
	from AtlasActorLudi.SpeciesKit.Humans import Human

	opened = []
	drawn = []
	original_dice_bag = Character.Dice_Bag

	class Recording_Dice(
		Random
		):
		def choices(
			dice,
			population,
			weights=None,
			*,
			cum_weights=None,
			k=1,
			):
			drawn.append(
				(
					tuple(
						population
						),
					None
					if weights is None
					else tuple(
						weights
						),
					k,
					)
				)
			return Random.choices(
				dice,
				population,
				weights,
				cum_weights=cum_weights,
				k=k,
				)

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
		bag = original_dice_bag(
			char,
			purpose,
			**key,
			)
		probe = Recording_Dice()
		probe.setstate(
			bag.getstate()
			)
		return probe

	Character.Dice_Bag = recording_dice_bag
	try:
		character = Character(
			seed=7,
			)
		elf_size = _selected_size(
			character,
			Elf,
			None,
			)
		assert elf_size == "Medium"
		assert opened == [], opened
		human_size = _selected_size(
			character,
			Human,
			None,
			)
	finally:
		Character.Dice_Bag = original_dice_bag

	assert human_size in Human.SIZE_OPTIONS
	assert opened == [
		(
			"Human.size",
			{},
			),
		], opened
	assert drawn == [
		(
			Human.SIZE_OPTIONS,
			Human.SIZE_WEIGHTS,
			1,
			),
		], drawn


if __name__ == "__main__":
	_test_dice_purpose()
	print( "OK: SpeciesKit.physiology self-test" )
