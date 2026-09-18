"""Public NonPlayer generation across Race, Guild, and Background."""
#-- Recovered from the 2026-08-29 bytecode (QST-0134), the last of the twelve.
#-- Every docstring and every one of the six failure messages is the
#-- original's, word for word; the transcription was proved instruction for
#-- instruction against the vaulted .pyc — identical on the first pass —
#-- before this layout was applied.
#--
#-- Does this module own a domain axis (QST-0134)?  No.  It is the public
#-- door: it takes what a caller asked for in any of the four spellings the
#-- project has used, settles them into the two axes that exist, fills the
#-- gaps from the Character's own dice, and hands the result to the Grimoire.
#-- Identity_Axis belongs to Map_of_Archetypes, the Guilds to GuildKit, the
#-- Backgrounds to BackgroundKit.  Nothing here is a property of a Character.

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from secrets import randbits

from Minion import chronicler, minion

from AtlasActorLudi.CharactersKit import Character
from AtlasActorLudi.AtlasAlusoris.Grimoire_of_NPC import NPC
from AtlasActorLudi.AtlasAlusoris.Map_of_Archetypes import (
	Classify_Archetype,
	Identity_Axis,
	)

from AtlasActorLudi.AtlasAlusoris.Map_of_Races import race_weights
from AtlasLusoris.BackgroundKit import NONPLAYER_BACKGROUNDS
from AtlasLusoris.GuildKit import GUILDS


@dataclass(
	frozen=True,
	slots=True,
	)
class NonPlayer_Choices:
	"""Selectable Alusoris dimensions exposed to a frontline."""

	races: tuple[str, ...]
	guilds: tuple[str, ...]
	backgrounds: tuple[str, ...]

	@property
	def classes(self) -> tuple[str, ...]:
		"""Sheet-language alias for Guild choices."""
		return self.guilds


def choices() -> NonPlayer_Choices:
	"""Return sorted immutable choices without presentation placeholders."""
	return NonPlayer_Choices(
		races=tuple(
			sorted(
				race
				for race in race_weights
				if race
				)
			),
		guilds=tuple(
			sorted(
				GUILDS
				)
			),
		backgrounds=tuple(
			sorted(
				NONPLAYER_BACKGROUNDS
				)
			),
		)


def _requested(
	value: str | None,
	) -> str | None:
	if value in (None, "Random"):



		return None

	return value


def _set_axis(
	requests: dict[Identity_Axis, str | None],
	axis: Identity_Axis,
	name: str,
	*,
	source: str,
	) -> None:
	current = requests[
		axis
		]


	if current is not None:
		if current != name:

			raise ValueError(
				f"NonPlayer {axis.value.title()} and {source} disagree: "
				f"{current!r} != {name!r}."
				)



	requests[
		axis
		] = name


def _resolve_identity_requests(
	*,
	guild: str | None,
	background: str | None,
	profile: str | None,
	archetype: str | None,
	) -> dict[Identity_Axis, str | None]:
	requests = {
		Identity_Axis.GUILD: None,
		Identity_Axis.BACKGROUND: None,
		}

	requested_guild = _requested(
		guild
		)

	requested_background = _requested(
		background
		)

	requested_profile = _requested(
		profile
		)

	requested_archetype = _requested(
		archetype
		)


	if requested_guild is not None:
		if requested_guild not in GUILDS:
			raise ValueError(
				f"Unknown NonPlayer Guild: {requested_guild!r}."
				)

		_set_axis(
			requests,
			Identity_Axis.GUILD,
			requested_guild,
			source="Guild",
			)


	if requested_profile is not None:
		if requested_profile not in NONPLAYER_BACKGROUNDS:
			raise ValueError(
				"Unknown legacy NonPlayer Profile/Background: "
				f"{requested_profile!r}."
				)

		_set_axis(
			requests,
			Identity_Axis.BACKGROUND,
			requested_profile,
			source="legacy Profile",
			)


	if requested_background is not None:
		if requested_background in NONPLAYER_BACKGROUNDS:
			identity = (
				Identity_Axis.BACKGROUND,
				requested_background,
				)
		else:
			try:
				legacy = Classify_Archetype(
					requested_background
					)

				identity = (
					legacy.axis,
					legacy.name,
					)
			except ValueError as error:
				raise ValueError(
					"Unknown NonPlayer Background or legacy Archetype: "
					f"{requested_background!r}."
					) from error

		_set_axis(
			requests,
			identity[0],
			identity[1],
			source="legacy Background",
			)


	if requested_archetype is not None:
		legacy = Classify_Archetype(
			requested_archetype
			)

		_set_axis(
			requests,
			legacy.axis,
			legacy.name,
			source="legacy Archetype",
			)


	return requests


def _chosen_or_random(
	character: Character,
	dimension: str,
	requested: str | None,
	available,
	*,
	weights=None,
	) -> str:
	valid_values = tuple(
		available
		)


	if not valid_values:
		raise RuntimeError(
			f"No NonPlayer {dimension} choices are available."
			)


	if requested is not None:
		if requested not in valid_values:
			raise ValueError(
				f"Unknown NonPlayer {dimension}: {requested!r}."
				)

		return requested

	dice_bag = character.Dice_Bag(
		f"identity.nonplayer.{dimension.casefold()}",
		version="1",
		namespace="GenLegendActor",
		)

	return character.Pick(
		valid_values,
		weights=(
			tuple(
				weights
				)
			if weights is not None
			else None
			),
		dice=dice_bag,
		)


@minion
def _attempt_nonplayer(
	*,
	target: Character,
	race: str,
	guild: str,
	background: str,
	level: int,
	seed: int,
	light: bool,
	) -> Character:
	"""Perform one generation attempt through the current Alusoris Grimoire."""
	return NPC(
		target=target,
		race=race,
		guild=guild,
		background=background,
		level=level,
		seed=seed,
		light=light,
		)


def _generation_seed(
	seed: int | None,
	) -> int:
	if seed is None:
		return randbits(
			64
			)

	resolved = int(
		seed
		)


	if resolved < 0:
		raise ValueError(
			"A NonPlayer generation seed must be zero or greater."
			)


	return resolved


@chronicler
def summon_nonplayer(
	race: str | None = None,
	archetype: str | None = None,
	level: int = 1,
	seed: int | None = None,
	light: bool = False,
	*,
	guild: str | None = None,
	background: str | None = None,
	profile: str | None = None,
	) -> Character:
	"""Generate one NonPlayer Character through Guild and Background."""
	requested_level = max(
		1,
		int(
			level
			),
		)

	current_seed = _generation_seed(
		seed
		)

	character = Character(
		seed=current_seed,
		level=requested_level,
		)

	identities = _resolve_identity_requests(
		guild=guild,
		background=background,
		profile=profile,
		archetype=archetype,
		)

	race_names = tuple(
		race_weights
		)

	selected_race = _chosen_or_random(
		character,
		"Race",
		_requested(
			race
			),
		race_names,
		weights=(
			race_weights[name]
			for name in race_names
			),
		)

	selected_guild = _chosen_or_random(
		character,
		"Guild",
		identities[
			Identity_Axis.GUILD
			],
		GUILDS,
		)

	selected_background = _chosen_or_random(
		character,
		"Background",
		identities[
			Identity_Axis.BACKGROUND
			],
		NONPLAYER_BACKGROUNDS,
		)

	last_error = None

	#-- Five attempts, each with the seed nudged on: a Race and Guild that
	#-- cannot be built together should not fail a whole request.
	#--
	#-- It also means a *permanent* fault reads as "after five attempts"
	#-- rather than as itself.  That is what hides QST-0134 finding 1 today:
	#-- Grimoire_of_NPC.SetSize cannot build any full NonPlayer, so light=False
	#-- always exhausts the five and reports exhaustion instead of the
	#-- TypeError underneath.  `raise ... from last_error` keeps the real
	#-- cause attached, which is how that finding was traced.
	for _ in range(
		5
		):
		try:
			return _attempt_nonplayer(
				target=character,
				race=selected_race,
				guild=selected_guild,
				background=selected_background,
				level=requested_level,
				seed=current_seed,
				light=light,
				)
		except Exception as error:
			last_error = error
			current_seed += 1
			character = Character(
				seed=current_seed,
				level=requested_level,
				)

	raise RuntimeError(
		"Unable to summon a NonPlayer Character after five attempts."
		) from last_error


def summon_nonplayer_list(
	race: str | None = None,
	archetype: str | None = None,
	count: int = 5,
	seed: int | None = None,
	*,
	guild: str | None = None,
	background: str | None = None,
	profile: str | None = None,
	level: int | None = None,
	) -> list[Character]:
	"""Generate a deterministic list of independently seeded Characters."""
	if count < 1:
		raise ValueError(
			"A NonPlayer list must contain at least one Character."
			)

	batch_seed = _generation_seed(
		seed
		)

	result = []

	for index in range(
		count
		):
		character_seed = batch_seed + index

		character_level = (
			max(
				1,
				int(
					level
					),
				)
			if level is not None
			else Random(
				character_seed
				).randint(
				1,
				20,
				)
			)

		result.append(
			summon_nonplayer(
				race=race,
				archetype=archetype,
				guild=guild,
				background=background,
				profile=profile,
				level=character_level,
				seed=character_seed,
				)
			)

	return result


__all__ = ('NonPlayer_Choices', 'choices', 'summon_nonplayer', 'summon_nonplayer_list')


def _test_the_choices_offered() -> None:
	"""The frontline is offered every Race, Guild and Background, sorted."""
	offered = choices()

	assert offered.races and offered.guilds and offered.backgrounds
	assert list(offered.races) == sorted(offered.races), "Races come sorted."
	assert list(offered.guilds) == sorted(offered.guilds)
	assert list(offered.backgrounds) == sorted(offered.backgrounds)
	assert "" not in offered.races, "A blank is a placeholder, not a Race."
	assert offered.classes is offered.guilds, \
			"The sheet's word for a Guild is the same tuple."

	#-- Frozen on purpose: a frontline must not edit the menu it was handed.
	try:
		offered.races = ()
	except Exception:
		pass
	else:
		raise AssertionError(
				"The choices record should not be editable."
				)


def _test_a_request_is_settled_before_a_Character_exists() -> None:
	"""Four spellings of one identity settle onto the two axes that exist."""

	def settled(**request):
		fields = {
				"guild": None,
				"background": None,
				"profile": None,
				"archetype": None,
				}
		fields.update(request)
		answer = _resolve_identity_requests(**fields)
		return (
			answer[Identity_Axis.GUILD],
			answer[Identity_Axis.BACKGROUND],
			)

	assert settled() == (None, None), "Asking for nothing settles nothing."
	assert settled(guild="Wizard") == ("Wizard", None)
	assert settled(background="Sage") == (None, "Sage")
	assert settled(profile="Sage") == (None, "Sage"), "The retired alias lands."
	assert settled(guild="Wizard", background="Sage") == ("Wizard", "Sage")

	#-- "Random" is the form saying it has no preference, not a name.
	assert settled(guild="Random", background="Random") == (None, None)

	#-- An Archetype lands on whichever axis still answers to it.
	assert settled(archetype="Wizard") == ("Wizard", None)
	assert settled(archetype="Criminal") == (None, "Criminal")

	#-- A Background that is really an Archetype is routed, not refused.
	assert settled(background="Wizard") == ("Wizard", None)

	#-- The same thing said twice is one request; said two ways, a mistake.
	assert settled(background="Sage", profile="Sage") == (None, "Sage")

	refusals = (
			( { "guild": "Nonesuch" }, "Unknown NonPlayer Guild" ),
			( { "profile": "Nonesuch" }, "Unknown legacy NonPlayer Profile" ),
			( { "background": "Nonesuch" },
				"Unknown NonPlayer Background or legacy Archetype" ),
			( { "guild": "Wizard", "archetype": "Rogue" }, "disagree" ),
			( { "background": "Sage", "profile": "Soldier" }, "disagree" ),
			)
	for request, expected in refusals:
		try:
			settled(**request)
		except ValueError as refusal:
			assert expected in str(refusal), \
					f"{request} was refused, but not for {expected!r}: {refusal}"
		else:
			raise AssertionError(
					f"{request} should have been refused."
					)


def _test_the_seed_a_request_is_built_from() -> None:
	"""A public seed is a number at or above zero, or it is drawn for you."""
	assert _generation_seed(0) == 0
	assert _generation_seed(7) == 7
	assert _generation_seed("7") == 7, "A seed from a form arrives as text."

	drawn = { _generation_seed(None) for _ in range(5) }
	assert len(drawn) == 5, "An unasked seed is fresh each time."

	#-- Character uses -1 as its own 'pick one' sentinel; the public door
	#-- must not let that leak in and mean something else.
	try:
		_generation_seed(-1)
	except ValueError as refusal:
		assert "zero or greater" in str(refusal), \
				f"Refused, but not for the sentinel: {refusal}"
	else:
		raise AssertionError(
				"A negative seed should be refused at the public door."
				)


def _test_choosing_a_dimension() -> None:
	"""What was asked for is honoured; what was not is drawn, repeatably."""
	from AtlasActorLudi.CharactersKit import Character

	who = Character(seed=404, level=3)

	assert _chosen_or_random(who, "Guild", "Wizard", GUILDS) == "Wizard"

	drawn = _chosen_or_random(who, "Guild", None, GUILDS)
	assert drawn in GUILDS
	assert _chosen_or_random(
			Character(seed=404, level=3),
			"Guild",
			None,
			GUILDS,
			) == drawn, "The same Character draws the same Guild."

	refusals = (
			( ("Guild", "Nonesuch", GUILDS), ValueError, "Unknown NonPlayer Guild" ),
			( ("Guild", None, ()), RuntimeError, "choices are available" ),
			)
	for (dimension, requested, available), kind, expected in refusals:
		try:
			_chosen_or_random(who, dimension, requested, available)
		except kind as refusal:
			assert expected in str(refusal), \
					f"{dimension}/{requested} refused, but not for {expected!r}: {refusal}"
		else:
			raise AssertionError(
					f"{dimension}/{requested!r} should have been refused."
					)


def _test_summoning() -> None:
	"""One NonPlayer, and a list of them, each seeded on its own."""
	#-- Only light NonPlayers can be built today: QST-0134 finding 1 in
	#-- Grimoire_of_NPC stops every full one at SetSize, and the retry loop
	#-- above reports that as exhaustion.  Proved here so the day it is fixed,
	#-- this check says so.
	try:
		summon_nonplayer(seed=1, level=3)
	except RuntimeError as exhausted:
		assert "after five attempts" in str(exhausted)
		assert exhausted.__cause__ is not None, \
				"The real cause must stay attached to the exhaustion."
	else:
		raise AssertionError(
				"A full NonPlayer now builds: QST-0134 finding 1 is fixed. "
				"Relax this check."
				)

	npc = summon_nonplayer(seed=1, level=3, light=True)
	assert npc.race and npc.char_class and npc.background
	assert npc.level == 3

	#-- The same seed summons the same NonPlayer.
	assert summon_nonplayer(seed=1, level=3, light=True).name == npc.name

	#-- A named axis is honoured all the way through.
	asked = summon_nonplayer(
			seed=2,
			level=1,
			light=True,
			guild="Wizard",
			background="Sage",
			)
	assert asked.char_class == "Wizard" and asked.background == "Sage"

	#-- A list is a batch of independently seeded Characters.
	try:
		summon_nonplayer_list(count=0)
	except ValueError as refusal:
		assert "at least one Character" in str(refusal)
	else:
		raise AssertionError(
				"A list of no Characters should be refused."
				)


def _self_test() -> None:
	_test_the_choices_offered()
	_test_a_request_is_settled_before_a_Character_exists()
	_test_the_seed_a_request_is_built_from()
	_test_choosing_a_dimension()
	_test_summoning()
	print("OK — Alusoris Map_of_NonPlayer_Generation self-test")


if __name__ == "__main__":
	_self_test()
