"""
Mercy_Kit — the Warrior of Mercy: its Tag and its lessons.

Thought pattern
	1. The Warrior is a Tag: ``Mercy``, a Specialization of the Monk.
	2. Each lesson names its Warrior by that Tag (``path=Mercy``), a
	   precondition: the lesson awakens only on a Character who already is
	   this Warrior. Never by text, so a typo is an import error, not a
	   silent mismatch.
	3. Adding a Warrior touches only its own Kit and ``Monk_Kit/__init__``.
"""

from __future__ import annotations

from AtlasLusoris.GuildKit import Make_Specialization
from AtlasLusoris.GuildKit import Monk
from AtlasLusoris.TrainingKit import Make_Training

from AtlasLusoris.AtlasOfGuilds.Monk_Kit.Core_Kit import GUILD
from AtlasLusoris.AtlasOfGuilds.Monk_Kit.Core_Kit import Monk_Level


Mercy = Make_Specialization(
	guild=Monk,
	name="Mercy",
	module=__name__,
	)


def _mercy(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		flag: bool = False,
		):
	"""One Mercy lesson: it awakens only for this Warrior."""
	return Make_Training(
			name=name,
			guild_name=GUILD,
			min_level=min_level,
			description=description,
			chips=chips,
			path=Mercy,
			flag=flag,
			)


# ---------------------------------------------------------------------------
# Mercy: the lessons
# ---------------------------------------------------------------------------


def _hand_of_harm_entry(
		char,
		) -> str:
	level = Monk_Level(char)
	poison_note = (
		"\n\nYou can also give that creature the Poisoned "
		"condition until the end of your next turn."
		if level >= 6
		else ""
		)
	return (
		"Once per turn when you hit a creature with an Unarmed "
		"Strike and deal damage, you can expend 1 Focus Point to "
		"deal extra **Necrotic damage** equal to one roll of "
		"your Martial Arts die plus your Wisdom modifier."
		f"{poison_note}"
		)


def _hand_of_healing_entry(
		char,
		) -> str:
	level = Monk_Level(char)
	cure_note = (
		"\n\nWhen you use Hand of Healing, you can also end "
		"one of the following conditions on the creature you heal "
		"(Blinded, Deafened, Paralyzed, Poisoned, or Stunned)."
		if level >= 6
		else ""
		)
	return (
		"As a *Magic action*, expend 1 Focus Point to touch a "
		"creature and restore Hit Points equal to one roll of your "
		"Martial Arts die plus your Wisdom modifier.\n\nWhen you "
		"use your Flurry of Blows, you can replace one Unarmed "
		"Strike with a use of this feature without expending a "
		"Focus Point for the healing."
		f"{cure_note}"
		)


Implements_of_Mercy = _mercy(
		name="Implements of Mercy",
		flag=True,
		min_level=3,
		description=(
			"You gain proficiency in Insight, Medicine, and Herbalism "
			"Kit. You also gain a special mask. It is a symbol of your "
			"tradition's philosophy."
			),
		)

Hand_of_Harm = _mercy(
		name="Hand of Harm",
		min_level=3,
		description=_hand_of_harm_entry,
		)

Hand_of_Healing = _mercy(
		name="Hand of Healing",
		min_level=3,
		description=_hand_of_healing_entry,
		)

Physicians_Touch = _mercy(
		name="Physician's Touch",
		min_level=6,
		description=(
			"Your Hand of Harm and Hand of Healing gain additional "
			"effects (see those entries). At level 6 and above, Hand of "
			"Harm can apply Poisoned, and Hand of Healing can cure a "
			"condition from the list."
			),
		)

Flurry_of_Healing_and_Harm = _mercy(
		name="Flurry of Healing and Harm",
		min_level=11,
		description=(
			"When you use Flurry of Blows, you can replace each of the "
			"Unarmed Strikes with a use of Hand of Healing **without "
			"expending Focus Points** for the healing."
			"\n\nIn addition, when you make an Unarmed Strike with "
			"Flurry of Blows and deal damage, you can use Hand of Harm "
			"with that strike "
			"**without expending a Focus Point**. You can still use "
			"Hand of Harm only once per turn.\n\nYou can use these "
			"benefits a total number of times equal to your Wisdom "
			"modifier (minimum once). All uses restore on a Long Rest."
			),
		)

Hand_of_Ultimate_Mercy = _mercy(
		name="Hand of Ultimate Mercy",
		min_level=17,
		description=(
			"Your mastery of life energy opens the door to the "
			"ultimate mercy. As a *Magic action*, touch the "
			"corpse of a creature that died within the past 24 hours "
			"and expend 5 Focus Points. The creature returns to life "
			"with Hit Points equal to **4d10 plus your Wisdom "
			"modifier**. Conditions removed on revival: Blinded, Deafened, "
			"Paralyzed, Poisoned, and Stunned.\n\nOnce you use this "
			"feature, you can't use it again until you finish a Long "
			"Rest."
			),
		)
