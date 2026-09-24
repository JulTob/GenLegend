"""Gender Tags used by naming, titles, and narrative identity."""

from TopKit import Action
from TopKit import Flag
from TopKit import Imprint
from TopKit import Pre
from TopKit import Tag
from TopKit import Underlay

from AtlasActorLudi.CharactersKit import Character


@Flag
class Gender(Tag):
	"""Root Tag for naming and title gender context."""

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
		"""Render Gender from current Tag membership."""
		if specification.strip().casefold() == "gender":
			return Find_Gender( target )

		return prior( specification )


@Flag
class Male(Gender):
	"""Masculine naming and title context."""

	PRONOUN = "He"
	TOKENS = (
		"He",
		"Male",
		"He/Him",
		"Masculine",
		"Him",
		)

	@Imprint
	def Set_Gender(
			target,
			gender=None,
			):
		target.gender = gender or Male.PRONOUN


@Flag
class Female(Gender):
	"""Feminine naming and title context."""

	PRONOUN = "She"
	TOKENS = (
		"She",
		"Female",
		"She/Her",
		"Feminine",
		"Her",
		)

	@Imprint
	def Set_Gender(
			target,
			gender=None,
			):
		target.gender = gender or Female.PRONOUN


@Flag
class Agender(Gender):
	"""Neutral or setting-specific naming and title context."""

	PRONOUN = "They"
	TOKENS = (
		"They",
		"Agender",
		"They/Them",
		"Fluid",
		"Other",
		"Them",
		)

	@Imprint
	def Set_Gender(
			target,
			gender=None,
			):
		target.gender = gender or Agender.PRONOUN


GENDER_TAGS = {
	token.casefold(): tag
	for tag in (
		Male,
		Female,
		Agender,
		)
	for token in tag.TOKENS
	}


def Current_Gender(
		target,
		) -> type[Gender] | None:
	"""Return the one Gender Shape currently carried by a Character."""
	carried = tuple(
		tag
		for tag in (
			Male,
			Female,
			Agender,
			)
		if target in tag
		)

	if len( carried ) > 1:
		raise ValueError(
			"A Character carries conflicting Gender Shapes: "
			+ ", ".join(
				tag.__name__
				for tag in carried
				)
			+ "."
			)

	return (
		carried[ 0 ]
		if carried
		else None
		)


def Find_Gender(
		target,
		) -> str:
	"""Find the narrative Gender label from current Tag membership."""
	tag = Current_Gender( target )

	if tag is None:
		return ""

	return tag.__name__.replace(
		"_",
		" ",
		)


def Gender_Reveal(
		target,
		gender=None,
		):
	"""Apply one Gender Shape while preserving the current naming token."""
	dice_bag = target.Dice_Bag(
		"identity.gender",
		version="1",
		namespace="GenLegendActor",
		)
	selected_gender = (
		gender
		or getattr(
			target,
			"gender",
			None,
			)
		or target.Pick(
			(
				"They",
				"He",
				"She",
				),
			dice=dice_bag,
			)
		)
	gender_tag = GENDER_TAGS.get(
		str(
			selected_gender
			).strip().casefold(),
		Agender,
		)
	current_tag = Current_Gender( target )

	if (
		current_tag is not None
		and current_tag is not gender_tag
		):
		raise ValueError(
			"A Character cannot carry two Gender Shapes: "
			f"{current_tag.__name__!r} and "
			f"{gender_tag.__name__!r}."
			)

	gender_tag(
		target,
		gender=selected_gender,
		)

	return gender_tag


def _self_test():
	character = Character(
		seed=11,
		)

	tag = Gender_Reveal(
		character,
		"She",
		)

	assert tag is Female
	assert character.gender == "She"
	assert character in Female
	assert character in Gender
	assert "Female" in character
	assert Current_Gender( character ) is Female
	assert Find_Gender( character ) == "Female"
	assert f"{character:Gender}" == "Female"

	print( "OK — GendersKit self-test" )


__all__ = (
	"Agender",
	"Current_Gender",
	"Female",
	"Find_Gender",
	"GENDER_TAGS",
	"Gender",
	"Gender_Reveal",
	"Male",
	)


if __name__ == "__main__":
	_self_test()
