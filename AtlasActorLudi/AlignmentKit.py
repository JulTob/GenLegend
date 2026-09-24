"""
AlignmentKit

Alignment is a two-axis Geometry:

	Morality: Evil → Neutral → Good
	Order:    Lawful → Neutral → Chaotic

Neutral is the unmarked starting point. A Character carries only the axis
Tags that add meaning; Alignment derives the familiar format view from
their membership.

Evil, in this context, means antisocial behaviours. Their goals align only with personal benefit.
Good, in this context, means prosocial behaviours. Their goals sacrifice personal needs in favor of the collective, or the greater good, or the benefit of others.

Lawful, in this context, means inclined towards organizations and structures.
Chaotic, in this context, means inclined towards individualism and personal responsibility.

These tags influence further decisions, like titles, story beats, and motivation.
"""

from __future__ import annotations

from TopKit import Action
from TopKit import Pre
from TopKit import Tag
from TopKit import Underlay

from AtlasActorLudi.CharactersKit import Character


def Find_Alignment(
		target,
		):
	"""Compose the display value from current axis membership."""
	if target in Good:
		morality = "Good"
	elif target in Evil:
		morality = "Evil"
	else:
		morality = "Neutral"

	if target in Lawful:
		order = "Lawful"
	elif target in Chaotic:
		order = "Chaotic"
	else:
		order = "Neutral"

	if order == "Neutral":
		return f"True {morality}"
	if morality == "Neutral":
		return f"True {order}"
	return f"{order} {morality}"


class Alignment(Tag):
	"""Semantic context for a Character's moral and order axes."""

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
		"""Render the Alignment view and delegate every other format."""
		if specification.strip().casefold() == "alignment":
			return Find_Alignment(
					target,
					)
		return prior(
				specification,
				)


class Morality(Alignment):
	pass


class Good(Morality):

	@Pre
	def Not_Evil(
			target,
			):
		return target not in Evil


class Evil(Morality):

	@Pre
	def Not_Good(
			target,
			):
		return target not in Good


class Order(Alignment):
	pass


class Lawful(Order):

	@Pre
	def Not_Chaotic(
			target,
			):
		return target not in Chaotic


class Chaotic(Order):

	@Pre
	def Not_Lawful(
			target,
			):
		return target not in Lawful


_MORALITY_WORDS = {
		"good": Good,
		"evil": Evil,
		}
_ORDER_WORDS = {
		"lawful": Lawful,
		"chaotic": Chaotic,
		}
_ALIGNMENT_WORDS = frozenset(
		{
				"chaotic",
				"evil",
				"good",
				"lawful",
				"neutral",
				}
		)
_ALIGNMENT_CONFLICTS = {
		Good: Evil,
		Evil: Good,
		Lawful: Chaotic,
		Chaotic: Lawful,
		}


def _alignment_words(
		requested,
		):
	token = str(
			requested,
			).strip().replace(
			"_",
			" ",
			)
	words = tuple(
			"lawful" if word == "legal" else word
			for word in token.casefold().split()
			)
	if words and words[0] == "true":
		words = (
				"neutral",
				*words[1:],
				)
	if (
		not words
		or len(words) > 2
		or any(
				word not in _ALIGNMENT_WORDS
				for word in words
				)
		):
		raise ValueError(
				f"Unknown Alignment: {requested!r}."
				)
	return words


def _alignment_tags(
		requested,
		):
	words = _alignment_words(
			requested,
			)
	morality = tuple(
			_MORALITY_WORDS[word]
			for word in words
			if word in _MORALITY_WORDS
			)
	order = tuple(
			_ORDER_WORDS[word]
			for word in words
			if word in _ORDER_WORDS
			)
	if len(morality) > 1 or len(order) > 1:
		raise ValueError(
				f"Conflicting Alignment axes: {requested!r}."
				)
	return morality + order


def _random_alignment_tags(
		character,
		):
	dice_bag = character.Dice_Bag(
			"identity.alignment",
			version="2",
			namespace="GenLegendActor",
			)
	return tuple(
			tag
			for tag in (
					character.Pick(
							(
									None,
									Good,
									Evil,
									),
							dice=dice_bag,
							),
					character.Pick(
							(
									None,
									Lawful,
									Chaotic,
									),
							dice=dice_bag,
							),
					)
			if tag is not None
			)


def New_Alignment(
		character,
		alignment=None,
		):
	"""Apply independent Morality and Order Shapes; absence means Neutral."""
	is_random = alignment is None or (
			isinstance(
					alignment,
					str,
					)
			and alignment.strip().casefold() == "random"
			)
	selected_tags = (
			_random_alignment_tags(
					character,
					)
			if is_random
			else _alignment_tags(
					alignment,
					)
			)
	for requested_tag in selected_tags:
		existing_tag = _ALIGNMENT_CONFLICTS[
				requested_tag
				]
		if character in existing_tag:
			raise ValueError(
					"Alignment cannot replace an active axis Shape: "
					f"{existing_tag.__name__!r} with "
					f"{requested_tag.__name__!r}."
					)
	if character not in Alignment:
		Alignment(
				character,
				)
	for tag in selected_tags:
		if character not in tag:
			tag(
					character,
					)
	character.alignment = f"{character:Alignment}"
	return (
			Alignment,
			*selected_tags,
			)


def _test_independent_axes(
		):
	character = Character(
			seed=17,
			)
	New_Alignment(
			character,
			"Lawful Good",
			)
	assert character in Alignment
	assert character in Morality
	assert character in Good
	assert character in Order
	assert character in Lawful
	assert character not in Evil
	assert character not in Chaotic
	assert f"{character:Alignment}" == "Lawful Good"


def _test_neutral_is_absence(
		):
	character = Character(
			seed=18,
			)
	New_Alignment(
			character,
			"True Neutral",
			)
	assert character in Alignment
	assert character not in Good
	assert character not in Evil
	assert character not in Lawful
	assert character not in Chaotic
	assert f"{character:Alignment}" == "True Neutral"


def _test_membership_is_source(
		):
	character = Character(
			seed=19,
			)
	Alignment(
			character,
			)
	character.alignment = "stale compatibility record"
	Good(
			character,
			)
	Chaotic(
			character,
			)
	assert character in Good
	assert character in Chaotic
	assert f"{character:Alignment}" == "Chaotic Good"
	assert Find_Alignment(
			character,
			) == "Chaotic Good"


def _test_axis_conflicts(
		):
	from TopKit import TagPreconditionError
	character = Character(
			seed=20,
			)
	Evil(
			character,
			)
	try:
		Good(
				character,
				)
		raise AssertionError(
				"Good must reject a Character already carrying Evil."
				)
	except TagPreconditionError:
		pass
	assert character in Evil
	assert character not in Good


def _test_alignment_inputs(
		):
	lawful = Character(
			seed=21,
			)
	chaotic = Character(
			seed=22,
			)
	New_Alignment(
			lawful,
			"True Legal",
			)
	New_Alignment(
			chaotic,
			"True Chaotic",
			)
	assert lawful in Lawful
	assert lawful not in Good
	assert lawful not in Evil
	assert f"{lawful:Alignment}" == "True Lawful"
	assert chaotic in Chaotic
	assert chaotic not in Good
	assert chaotic not in Evil
	assert f"{chaotic:Alignment}" == "True Chaotic"


def _test_character_dice_bag(
		):
	first = Character(
			seed=23,
			)
	second = Character(
			seed=23,
			)
	first_dice_state = first.dices.getstate()
	second_dice_state = second.dices.getstate()
	New_Alignment(
			first,
			)
	New_Alignment(
			second,
			)
	assert f"{first:Alignment}" == f"{second:Alignment}"
	assert first.dices.getstate() == first_dice_state
	assert second.dices.getstate() == second_dice_state


def _self_test(
		):
	_test_independent_axes()
	_test_neutral_is_absence()
	_test_membership_is_source()
	_test_axis_conflicts()
	_test_alignment_inputs()
	_test_character_dice_bag()
	print(
			"OK — AlignmentKit self-test"
			)


__all__ = (
		"Alignment",
		"Chaotic",
		"Evil",
		"Find_Alignment",
		"Good",
		"Lawful",
		"Morality",
		"New_Alignment",
		"Order",
		)


if __name__ == "__main__":
	_self_test()
