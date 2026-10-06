"""
Shadow_Kit — the Warrior of Shadow: its Tag and its lessons.

Thought pattern
	1. The Warrior is a Tag: ``Shadow``, a Specialization of the Monk.
	2. Each lesson names its Warrior by that Tag (``path=Shadow``), a
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


Shadow = Make_Specialization(
	guild=Monk,
	name="Shadow",
	module=__name__,
	)


def _shadow(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		flag: bool = False,
		):
	"""One Shadow lesson: it awakens only for this Warrior."""
	return Make_Training(
			name=name,
			guild_name=GUILD,
			min_level=min_level,
			description=description,
			chips=chips,
			path=Shadow,
			flag=flag,
			)


# ---------------------------------------------------------------------------
# Shadow: the lessons
# ---------------------------------------------------------------------------


Shadow_Arts = _shadow(
		name="Shadow Arts",
		flag=True,
		min_level=3,
		description=(
			"You can use your discipline to create illusions and "
			"harness shadows.\n\n**Darkness.** Expend 1 Focus Point "
			"to cast *Darkness* without components. You can see "
			"within the spell's area. While active, you can move the "
			"Darkness to a space within 60 feet at the start of each of "
			"your turns.\n\n**Darkvision.** You gain Darkvision 60 "
			"feet (or +60 feet if you already have it)."
			"\n\n**Shadowy Figments.** You know the *Minor "
			"Illusion* cantrip. Wisdom is your spellcasting ability "
			"for it."
			),
		)

Shadow_Step = _shadow(
		name="Shadow Step",
		min_level=6,
		description=(
			"While entirely within Dim Light or Darkness, you can use a "
			"*Bonus Action* to **teleport up to 60 feet** to an "
			"unoccupied space you can see that is also in Dim Light or "
			"Darkness. You then have Advantage on the next melee attack "
			"you make before the end of the current turn."
			),
		)

Improved_Shadow_Step = _shadow(
		name="Improved Shadow Step",
		min_level=11,
		description=(
			"When you use your Shadow Step, you can expend 1 Focus "
			"Point to remove the requirement that you must start and "
			"end in Dim Light or Darkness for that use. As part of this "
			"Bonus Action, you can make an Unarmed Strike immediately "
			"after you teleport."
			),
		)

Cloak_of_Shadows = _shadow(
		name="Cloak of Shadows",
		min_level=17,
		description=(
			"As a *Magic action* while entirely within Dim Light "
			"or Darkness, expend **3 Focus Points** to shroud "
			"yourself with shadows for 1 minute (or until "
			"Incapacitated, or until you end your turn in Bright "
			"Light). While shrouded:"
			"\n\n\n- **Invisibility.** You have the Invisible "
			"condition."
			"\n- **Partially Incorporeal.** You can move through "
			"occupied spaces as Difficult Terrain. If you end your turn "
			"in such a space, you are shunted to the last unoccupied "
			"space you were in."
			"\n- **Shadow Flurry.** You can use Flurry of Blows "
			"without expending Focus Points.\n\n"
			),
		)
