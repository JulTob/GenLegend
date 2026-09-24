"""Public Species application routes."""

from AtlasActorLudi.SpeciesKit.bases import Current_Creature_Type
from AtlasActorLudi.SpeciesKit.catalog import Current_Heritage
from AtlasActorLudi.SpeciesKit.catalog import Current_Species
from AtlasActorLudi.SpeciesKit.catalog import Heritages_By_Species
from AtlasActorLudi.SpeciesKit.catalog import Playable_Species
from AtlasActorLudi.SpeciesKit.catalog import Resolve_Heritage
from AtlasActorLudi.SpeciesKit.catalog import Resolve_Species
from AtlasActorLudi.SpeciesKit.catalog import Species_For_Heritage


def _random_species(
	character,
	):
	available = Playable_Species()
	dice_bag = character.Dice_Bag(
		"identity.species",
		version="2024",
		namespace="GenLegendActor",
		)

	return character.Pick(
		available,
		weights=tuple(
			tag.WEIGHT
			for tag in available
			),
		dice=dice_bag,
		)


def _random_heritage(
	character,
	species,
	available,
	size=None,
	):
	dice_bag = character.Dice_Bag(
		f"identity.species.{species.__name__}.heritage",
		version="2024",
		namespace="GenLegendActor",
		)

	def imprint(
		tag,
		):
		if character not in tag:
			if size is None:
				tag(
					character,
					)
			else:
				tag(
					character,
					size=size,
					)

	return character.Accept(
		available,
		dice=dice_bag,
		imprint=imprint,
		)


def Apply_Species(
	character,
	species=None,
	*,
	heritage=None,
	size=None,
	):
	"""Apply one concrete Species Shape and its resolved grants."""
	requested_heritage = (
		None
		if (
			heritage is None
			or (
				isinstance(
					heritage,
					str,
					)
				and heritage.strip().casefold() == "random"
				)
			)
		else Resolve_Heritage(heritage)
		)
	is_random = (
		species is None
		or (
			isinstance(
				species,
				str,
				)
			and species.strip().casefold() == "random"
			)
		)
	selected = (
		(
			Species_For_Heritage(
				requested_heritage,
				)
			if requested_heritage is not None
			else _random_species(character)
			)
		if is_random
		else Resolve_Species(species)
		)
	current = Current_Species(character)

	if (
		current is not None
		and current is not selected
		):
		raise ValueError(
			"A Character cannot carry two Species: "
			f"{current.__name__!r} and {selected.__name__!r}."
			)

	current_heritage = Current_Heritage(character)
	available_heritages = Heritages_By_Species().get(
		selected,
		(),
		)

	if available_heritages:
		if (
			requested_heritage is not None
			and requested_heritage not in available_heritages
			):
			owner = Species_For_Heritage(
				requested_heritage,
				)
			raise ValueError(
				f"Heritage {requested_heritage.__name__!r} requires Species "
				f"{owner.__name__!r}, not {selected.__name__!r}."
				)

		#-- Explicit ``is not None``: a Heritage is a Tag, and TopKit's
		#-- ``bool( Tag )`` asks whether it has members yet, so ``or``
		#-- would skip a requested Heritage nobody carries so far.
		if requested_heritage is not None:
			selected_heritage = requested_heritage
		elif current_heritage is not None:
			selected_heritage = current_heritage
		else:
			selected_heritage = _random_heritage(
				character,
				selected,
				available_heritages,
				size=size,
				)
		shape = selected_heritage
	elif requested_heritage is not None:
		owner = Species_For_Heritage(
			requested_heritage,
			)
		raise ValueError(
			f"Heritage {requested_heritage.__name__!r} requires Species "
			f"{owner.__name__!r}, not {selected.__name__!r}."
			)
	else:
		selected_heritage = None
		shape = selected

	if (
		current_heritage is not None
		and current_heritage is not selected_heritage
		):
		raise ValueError(
			"A Character cannot carry two Heritages: "
			f"{current_heritage.__name__!r} and "
			f"{selected_heritage.__name__!r}."
			)

	if character not in shape:
		shape(character,
			size=size,
			)

	character.species = selected.__name__.replace(
		"_",
		" ",
		)

	if selected_heritage is not None:
		character.heritage = (
			selected_heritage
			.__name__
			.replace(
				"_",
				" ",
				)
			)

	creature_type = Current_Creature_Type(character)

	if creature_type is not None:
		character.creature_type = creature_type.__name__

	return selected
