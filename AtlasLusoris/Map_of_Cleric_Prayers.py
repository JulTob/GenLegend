"""
Cleric prayers — short faith-lines for Domain voice.

The Guild's theme is **faith**: not necessarily a named god, but what the
Character puts their trust in.  A Domain is a take on that faith.  A prayer is
one sentence that names the take.

Assembly
	1. start from ``DEFAULT_PRAYERS`` (every Cleric);
	2. add ``DOMAIN_PRAYERS`` for the Domain they carry;
	3. add ``SPECIES_PRAYERS`` / ``SPECIES_DOMAIN_PRAYERS`` for their people;
	4. add ``CULTURE_PRAYERS`` and, if the Domain is known,
	   ``CULTURE_DOMAIN_PRAYERS`` (same network as gear titles);
	5. ``Pick`` one line from the assembled ledger.

Rendering: the Guild paragraph is shared; each Domain ``extends`` it with
its own mouth, and seats the drawn prayer in a sentence that is not the
same twice.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Ledgers
# ---------------------------------------------------------------------------


DEFAULT_PRAYERS = (
	"Something answers when you call. You may not understand it, but you can trust it.",
	"Faith is a door you keep opening, even when you don't know what's on the other side.",
	"Faith is a window you keep opening. Even dark clouds can let the light in.",
	"Heavens do not shout. They shine.",
	"A vow is mightier than a bow. It weights less, and carries further.",
	"You are the miracle.",
	"You can be the miracle. Just try.",
	"If you can’t be a good example, then you’ll just have to serve as a horrible warning.",
	)


DOMAIN_PRAYERS = {
	"Life": (
		"Life finds a way.",
		"While I breathe, I hope.",
		"Sufficient unto the day.",
		"What is bent may still drink the rain.",
		),
	"Light": (
		"A candle loses nothing by lighting another.",
		"Even a little is enough to walk by.",
		"The dark is patient. So is the dawn.",
		"What you warm, you keep.",
		"Looking for the light around us, we find it on our own.",
		"In a world of darkness, we find our own light.",
		"In a cold world, we set the fires.",
		"The night hides a world, but reveals a universe.",
		),
	"Trickery": (
		"By indirections, find the way.",
		"Not every closed door is locked.",
		"A smile can be a key.",
		"The watched road is the emptiest.",
		"Normal is an illusion. What is normal for the spider is chaos for the fly.",
		),
	"War": (
		"If you would have peace, keep watch.",
		"The drawn blade has already chosen.",
		"No one returns the same.",
		"Stand where you said you would.",
		"Never interrupt an enemy making a mistake.",
		"A long dispute means that both parties are wrong.",
		"The person who masters himself through self-control and discipline is ultimately undefeatable.",
		
		),
	"Grave": (
		"From dust we come, to dust we return.",
		"If you can't rest in peace, rest in power.",
		"Two coins for the ferryman. One word for the grave.",
		"Life's pains end in the grave.",
        "Our actions may echo in eternity.",
		"Different in life, all men are equal in death.",
		),
	"Knowledge": (
		"Know thyself.",
		"I know that I know nothing.",
		"Ask, and the asking changes you.",
		"What is written outlives the hand.",
		"Knowledge is a mirror, not a book.",
		"You have to study a lot to know very little.",
		"The wise man knows he knows nothing.",
		"When senses fail us, reason must step in.",
		"The believer is happy; the doubter is wise.",
		"Mortals and books share their enemies: Fire, water, time, and their own contents.",

		),
	}


SPECIES_PRAYERS = {
	"Human": (
		"Ask the gods, but trust yourself.",
		),
	"Tiefling": (
		"Ash remembers the flame.",
		),
	"Goliath": (
		"The winds are fast, but they do not hurry.",
		"Each snowflake is small, but it is part of the avalanche.",
		),
	"Dwarf": (
		"Metal shapes in the forge. People in the challenge.",
		"A saint is a sinner trying to be better.",
		"Forgetting is hard, but harder is forgiving.",
		),
	"Dragonborn": (
		"Clan. Honor. Duty.",
		"Your word is your bond.",
		),
	"Elf": (
		"Dreams are made to be lived.",
		"May the dream guide your way.",
		),
	"Aasimar": (
		"Greatness is a gift. Greatness is a burden.",
		),
	"Halfling": (
		"Rush not. Small feet. Small steps. Long journeys.",
		"One can simply walk anywhere.",
		"The world is a big place. It is also a great place.",
		"Every day is a new story.",
		"The world is not inside your books."
		),
	"Gnome": (
		"Wonder and Wander.",
		"Care not for what you cannot change.",
		"Care not for what you cannot change. Change what you can.",
		"Care not for what you cannot carry."

		),
	"Orc": (
		"The storm is coming.",
		"The storm guides the winds.",
		"The wind rider must master the storm.",
		"The wind rider must follow the storm.",
		),
	}


# Species × Domain — a hint of the people in the Domain's mouth, not a lecture.
SPECIES_DOMAIN_PRAYERS = {
	(
		"Tiefling",
		"Grave",
		): (
		"I show the door. I do not pass.",
		"For the last two coins, I will guide.",
		),
	(
		"Tiefling",
		"Life",
		): (
		"You can rise from the ashes.",
		),
	(
		"Tiefling",
		"War",
		): (
		"War is never a choice, but a necessity.",
		"War is doesn't ask. You still have to answer.",
		"Defend. Protect. Forgive.",
		),
	(
		"Goliath",
		"War",
		): (
		"Stand your ground. Understand your enemy.",
		),
	(
		"Goliath",
		"Light",
		): (
		"The darkest night holds the brightest stars.",
		),
	(
		"Dwarf",
		"Life",
		): (
		"The real gold is in your soul.",
		"The real gold is in your faith.",
		"Gold held is not living. Gold earned is gold spent.",
		"Gold, like life, must be shared and passed on.",
		"The metals you carry in your soul are your real fortune.",
		),
	(
		"Dwarf",
		"Knowledge",
		): (
		"The stones remember.",
		"He who reads much and walks much, sees much and knows much.",  # Cervantes
		),
	(
		"Dragonborn",
		"War",
		): (
		"Life is a long battle..",  
		),
	(
		"Dragonborn",
		"Light",
		): (
		"Fire spreads. We gather around it.",  
		),
	(
		"Aasimar",
		"Light",
		): (
		"Let there be light.",
		),
	(
		"Elf",
		"Light",
		): (
		"Light, love, and music will endure.", 
		),
	(
		"Elf",
		"Knowledge",
		): (
		"We live in one another's shadow.",  # Irish: Ar scáth a chéile
		),
	(
		"Halfling",
		"Life",
		): (
		"Haste has no blessing.",  # Swahili
		),
	(
		"Gnome",
		"Knowledge",
		): (
		"You were not made to live as brutes, but to follow virtue and knowledge.",  # Dante
		),
	(
		"Gnome",
		"Life",
		): (
		"One sees clearly only with the heart.",  # Saint-Exupéry
		),
	(
		"Dwarf",
		"War",
		): (
		"There is no shortcut without work.",  # No hay atajo sin trabajo
		),
	(
		"Dwarf",
		"Grave",
		): (
		"Let nothing disturb you. Let nothing frighten you.",  # Teresa of Ávila
		"They shall be dust, but dust with love.",  # Quevedo
		),
	}


# Only lines that still sound like faith whichever Domain is showing.
CULTURE_PRAYERS = {
	"china": (
		"Do not do to others what you would not have done to you.",
		),
	"persia": (
		"This too shall pass.",
		),
	"germany": (
		"Mortals propose, Gods dispose.",
		),
	"india": (
		"Truth alone triumphs.",
		),
	"maghreb": (
		"Help yourself, and Heavens will help you.",
		),
	"switzerland": (
		"Help yourself, and Heavens will help you.",
		),
	}


# (culture, Domain). Empty pairs are omitted on purpose.
CULTURE_DOMAIN_PRAYERS = {
	("greece", "Knowledge"): (
		"Nothing in excess.",
		),
	("greece", "War"): (
		"We learn by suffering.",
		),
	("rome", "Life"): (
		"While I breathe, I hope.",
		),
	("rome", "Knowledge"): (
		"Make haste slowly.",
		),
	("japan", "Life"): (
		"Fall seven times, stand up eight.",
		),
	("japan", "Knowledge"): (
		"Sit and listen. Listen and learn.",
		),
	("aztec", "Grave"): (
		"Not forever on earth: only a little while here.",
		),
	("aztec", "Light"): (
		"Flower and song: that is our offering.",
		),
	("korea", "Life"): (
		"At the end of hardship, joy comes.",
		),
	("iberia", "Life"): (
		"Traveller, there is no road; you make the road by walking.",
		),
	("andalus", "Grave"): (
		"This world is a bridge. We all must cross.",
		),
	("norse", "Grave"): (
		"Cattle die, kinsmen die, you yourself will die; one thing never dies: the judgment on each life.",
		),
	("rus", "Knowledge"): (
		"Gods are not in strength, but in truth.",
		),
	("mongol", "Light"): (
		"The Eternal Light is watching.",
		),
	("celt", "Life"): (
		"There is no strength without coming together.",
		),
	("levante", "Life"): (
		"Patience is the key to relief.",
		),
	("africa", "Life"): (
		"Haste has no blessing.",
		),
	("egypt", "Grave"): (
		"What endures the grave weights on the living.",
		),
	("carthage", "Life"): (
		"Perhaps someday even this will be a joy to remember.",
		),
	("italy", "Light"): (
		"Love is what moves the sun and the other stars.",
		),
	("india", "Knowledge"): (
		"You have a right to the work, never to its fruits.",
		),
	("oceania", "Life"): (
		"We are all in the same canoe.",
		),
	("ninja", "Life"): (
		"Spring comes and the grass grows by itself.",
		),
	("grimdark", "Grave"): (
		"Though Heavens slay me, Heavens I trust.",
		),
	("arthuriana", "War"): (
		"Do what you must, come what may.",
		),
	("fairytale_fae", "Trickery"): (
		"Nature has no name.",
		),
	("china", "Life"): (
		"The highest good is like water. It flows where it is needed.",
		),
	}


# ---------------------------------------------------------------------------
# Resolution
# ---------------------------------------------------------------------------


def _domain_of(
		character,
		domain: str | None,
		) -> str | None:
	if domain:
		return domain

	for attr in (
			"specialization",
			"subclass",
			"domain",
			"path",
			):
		value = getattr(
			character,
			attr,
			None,
			)
		if isinstance(
				value,
				str,
				) and value:
			# "Life Domain" → "Life"
			return value.removesuffix(
				" Domain"
				)

	return None


# Legacy race labels sometimes surface where Species should.
_RACE_TO_SPECIES = {
	"Fiend": "Tiefling",
	"Giant": "Goliath",
	"Dragon": "Dragonborn",
	}


def _species_of(
		character,
		) -> str | None:
	species = getattr(
		character,
		"species",
		None,
		)
	if isinstance(
			species,
			str,
			) and species:
		return species

	race = getattr(
		character,
		"race",
		None,
		)
	if isinstance(
			race,
			str,
			) and race:
		return _RACE_TO_SPECIES.get(
			race,
			race,
			)

	return None


def _cultures_of(
		character,
		) -> tuple[str, ...]:
	try:
		from AtlasInventarium.Map_of_Gear_Titles import (
				cultures_of,
				)
	except Exception:
		return ()

	try:
		found = cultures_of(
			character
			)
	except Exception:
		return ()

	if not found:
		return ()

	return tuple(
		found
		)


def prayer_ledger(
		character,
		domain: str | None = None,
		) -> tuple[str, ...]:
	"""
	Assemble the prayer pool for this Character.

	Order is stable; duplicates are dropped while preserving first sighting.
	"""
	resolved_domain = _domain_of(
		character,
		domain,
		)
	species = _species_of(
		character
		)

	pool: list[str] = []
	seen: set[str] = set()

	def _extend(
			lines,
			):
		for line in lines:
			if not line:
				continue
			if line in seen:
				continue
			seen.add(
				line
				)
			pool.append(
				line
				)

	_extend(
		DEFAULT_PRAYERS
		)

	if resolved_domain in DOMAIN_PRAYERS:
		_extend(
			DOMAIN_PRAYERS[
				resolved_domain
				]
			)

	if species in SPECIES_PRAYERS:
		_extend(
			SPECIES_PRAYERS[
				species
				]
			)

	if species and resolved_domain:
		_extend(
			SPECIES_DOMAIN_PRAYERS.get(
				(
					species,
					resolved_domain,
					),
				(),
				)
			)

	for culture in _cultures_of(
			character
			):
		_extend(
			CULTURE_PRAYERS.get(
				culture,
				(),
				)
			)
		if resolved_domain:
			_extend(
				CULTURE_DOMAIN_PRAYERS.get(
					(
						culture,
						resolved_domain,
						),
					(),
					)
				)

	return tuple(
		pool
		)


def prayer_purpose(
		domain: str | None,
		) -> str:
	"""
	The Dice Bag purpose of a Domain's prayer: the Domain Tag's class name.

	The Domain is a Cleric Specialization; its Tag offers the prayer, so
	the purpose is that Tag's class name (``Life.prayer``, ``War.prayer``),
	never the display name.  A prayer with no Domain has no Tag to name
	it and is refused.
	"""
	from AtlasLusoris.GuildKit import Specialization_Tag

	if not domain:
		raise ValueError(
			"A prayer is drawn for a Cleric Domain; none was given or carried."
			)

	domain_tag = Specialization_Tag(
		"Cleric",
		domain,
		)

	return f"{domain_tag.__name__}.prayer"


def pick_prayer(
		character,
		domain: str | None = None,
		) -> str:
	"""Draw one prayer from the assembled ledger (seeded, deterministic)."""
	ledger = prayer_ledger(
		character,
		domain=domain,
		)

	if not ledger:
		return DEFAULT_PRAYERS[
			0
			]

	resolved_domain = _domain_of(
		character,
		domain,
		)
	dice = character.Dice_Bag(
		prayer_purpose(
			resolved_domain
			),
		)

	return character.Pick(
		ledger,
		dice=dice,
		)


# ---------------------------------------------------------------------------
# Guild and Domain voice
# ---------------------------------------------------------------------------
# Core fantasy: Being Watched (over) — keeping, not surveillance.
# Sell the class through that fantasy (what a Cleric *is*), not mood alone.
# Biblical / Jedi cadence: parallel clauses, open molds, invitation.
# The register comes from parallelism, parataxis and concrete images,
# never from archaic vocabulary (no thee, no shall) — that reads costume.
# The identity of the watcher stays a guess, so the mold stays open.
# Domain trickles doctrine into behavior; prayer seats at the end.


CLERIC_DESCRIPTION = (
	"There is something watching over you, and it has been with you "
	"always. Maybe a god. Maybe your ancestors. Maybe the universe "
	"itself, turning its face toward you. Whatever it is, you have "
	"been carried farther than you know.\n\n"
	"You can feel it. Maybe you don't see it, and you may not be able "
	"to explain why, but still you do believe. You believe there is a plan for you, and you are meant for something. What it is, you are not sure. You only hope you will be enough. Still, in the hour you falter, a hand "
	"is there to hold you. It was held out before you reached for it. Of that, you are certain.\n\n"
	"You have defied the odds, and contemplated miracles long enough "
	"you started doing your own."
	)


DOMAIN_OPENINGS = {
	"Life": (
		"Falling is not the end, while there is still breath to return "
		"to. Until you can stand again.\n\n"
		"You do not count whether you earned the rising. You learn to "
		"stay. To restore. To heal — the way you were shown."
		),
	"Light": (
		"The next step appears when you need it. Light always shows the way."
		),
	"Trickery": (
		"On the wrong nights, the count still comes out right. You learn the narrow way, the timely word, the door that should have been locked."
		),
	"War": (
		"You learn to stand when lying down would be easier. The bar does not move."
		),
	"Grave": (
		"What should rest, you let rest. What broke the order, you "
		"return.\n\n"
		"You keep the line — and sometimes, quietly, you bend it back."
		),
	"Knowledge": (
		"Answers are not given to stay in your hand. You work the "
		"lesson until it is yours.\n\n"
		"You teach yourself on behalf of what taught you first."
		),
	}


DOMAIN_FRAMES = {
	"Life": (
		'In a low hour, a line came back to you: '
		'"{prayer}"'
		),
	"Light": (
		'A sentence stayed with you at the crossing: '
		'"{prayer}"'
		),
	"Trickery": (
		'It sounded like a joke. The world has treated it as true ever '
		'since: "{prayer}"'
		),
	"War": (
		'Before the first stand, a line became the bar: '
		'"{prayer}"'
		),
	"Grave": (
		'You heard it where endings are kept in order: '
		'"{prayer}"'
		),
	"Knowledge": (
		'You were taught one sentence, and it stayed: '
		'"{prayer}"'
		),
	}


def voice_of_domain(
		domain: str,
		):
	"""
	One Domain layer: its own mouth, then the drawn prayer in its frame.
	"""
	opening = DOMAIN_OPENINGS.get(
		domain,
		"",
		)
	frame = DOMAIN_FRAMES.get(
		domain,
		'You once heard "{prayer}" You feel that it is true.',
		)

	def voice(
			character,
			) -> str:
		prayer = pick_prayer(
			character,
			domain=domain,
			)
		seated = frame.format(
			prayer=prayer,
			)
		if not opening:
			return seated
		return (
			f"{opening}\n\n"
			f"{seated}"
			)

	return voice


def bind_cleric_voice(
		guild,
		domains,
		) -> None:
	"""
	Seat Guild and Domain prose on Tags that were built without it.

	Does not re-declare Specializations. It replaces the empty ``Describe``
	layers the vaulted kit left behind.
	"""
	from AtlasLusoris.GuildKit import Describe_Layer

	guild.DESCRIPTION = CLERIC_DESCRIPTION
	guild.Describe = Describe_Layer(
		CLERIC_DESCRIPTION,
		extend=True,
		heading=None,
		)

	for domain_tag in domains:
		name = domain_tag.NAME
		voice = voice_of_domain(
			name
			)
		domain_tag.DESCRIPTION = voice
		domain_tag.Describe = Describe_Layer(
			voice,
			extend=True,
			heading=f"{name} Domain",
			)


__all__ = (
	"DEFAULT_PRAYERS",
	"DOMAIN_PRAYERS",
	"SPECIES_PRAYERS",
	"SPECIES_DOMAIN_PRAYERS",
	"CULTURE_PRAYERS",
	"CULTURE_DOMAIN_PRAYERS",
	"CLERIC_DESCRIPTION",
	"prayer_ledger",
	"prayer_purpose",
	"pick_prayer",
	"voice_of_domain",
	"bind_cleric_voice",
	)


if __name__ == "__main__":
	#-- Self-test (QST-0144.6, ruling 8).  A Domain's prayer is drawn from
	#-- one bag named by the Domain Tag's class name, with the default key,
	#-- from the ledger assembled for that Character and Domain.
	import random as stdlib_random
	from AtlasActorLudi.CharactersKit import Character

	assert prayer_purpose( "Life" ) == "Life.prayer"
	assert prayer_purpose( "War" ) == "War.prayer"
	for missing in ( None, "" ):
		try:
			prayer_purpose(
					missing
					)
		except ValueError as error:
			assert "Cleric Domain" in str( error )
		else:
			raise AssertionError(
					"prayer_purpose named a bag for no Domain."
					)
	try:
		prayer_purpose(
				"Nonesuch"
				)
	except KeyError as error:
		assert "has no Specialization" in str( error )
	else:
		raise AssertionError(
				"prayer_purpose named a bag for a Domain nobody declared."
				)

	opened = []
		#-- (purpose, version, namespace) of every bag opened
	drawn = {}
		#-- purpose -> [pool] of every draw from those bags

	class Probe_Dice(
			stdlib_random.Random
			):
		purpose = "?"

		def choice(
				dice,
				population,
				):
			drawn.setdefault( dice.purpose, [] ).append(
					list( population )
					)
			return super().choice(
					population
					)

	original_dice_bag = Character.Dice_Bag

	def recording_dice_bag(
			char,
			purpose,
			*,
			version="1",
			namespace="GenLegend",
			):
		bag = original_dice_bag(
				char,
				purpose,
				version=version,
				namespace=namespace,
				)
		opened.append(
				( purpose, version, namespace )
				)
		probe = Probe_Dice()
		probe.setstate(
				bag.getstate()
				)
		probe.purpose = purpose
		return probe

	char = Character(
			seed=1
			)
	Character.Dice_Bag = recording_dice_bag
	try:
		for domain in ( "Life", "Light", "Trickery", "War" ):
			opened.clear()
			drawn.clear()
			prayer = pick_prayer(
					char,
					domain=domain,
					)
			assert opened == [
					( f"{domain}.prayer", "1", "GenLegend" ),
					], opened
			[ pool ] = drawn[ f"{domain}.prayer" ]
			assert pool == list(
					prayer_ledger(
							char,
							domain=domain,
							)
					), domain
			assert prayer in pool
		#-- The voice seated on a Domain Tag draws the same bag.
		opened.clear()
		text = voice_of_domain(
				"Life"
				)(
				char
				)
		assert opened == [
				( "Life.prayer", "1", "GenLegend" ),
				], opened
		assert text
	finally:
		Character.Dice_Bag = original_dice_bag

	print(
			"OK: a Domain's prayer comes from one <Domain>.prayer bag, from "
			"the ledger assembled for the Character."
			)
