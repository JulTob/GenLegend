"""
Open_Hand_Kit — the Warrior of the Open Hand: its Tag and its lessons.

Thought pattern
	1. The Warrior is a Tag: ``OpenHand``, a Specialization of the Monk.
	2. Each lesson names its Warrior by that Tag (``path=OpenHand``), a
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


OpenHand = Make_Specialization(
	guild=Monk,
	name="Open Hand",
	module=__name__,
	)


def _open_hand(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		flag: bool = False,
		):
	"""One Open Hand lesson: it awakens only for this Warrior."""
	return Make_Training(
			name=name,
			guild_name=GUILD,
			min_level=min_level,
			description=description,
			chips=chips,
			path=OpenHand,
			flag=flag,
			)


# ---------------------------------------------------------------------------
# Open_Hand: the lessons
# ---------------------------------------------------------------------------


Open_Hand_Technique = _open_hand(
		name="Open Hand Technique",
		min_level=3,
		description=(
			"Whenever you hit a creature with an attack granted by your "
			"Flurry of Blows, you can impose one of the following "
			"effects on that target:"
			"\n\n"
			"\n- **Addle.** The target can't make Opportunity "
			"Attacks until the start of its next turn."
			"\n- **Push.** Strength save or be pushed up to 15 feet "
			"away from you."
			"\n- **Topple.** Dexterity save or have the Prone "
			"condition."
			"\n\n"
			),
		)

Wholeness_of_Body = _open_hand(
		name="Wholeness of Body",
		min_level=6,
		description=(
			"As a *Bonus Action*, roll your Martial Arts die and "
			"regain Hit Points equal to the roll plus your Wisdom "
			"modifier (minimum 1).\n\nYou can use this feature a "
			"number of times equal to your Wisdom modifier (minimum "
			"once). "
			"All uses restore on a Long Rest."
			),
		)

Fleet_Step = _open_hand(
		name="Fleet Step",
		min_level=11,
		description=(
			"When you take a Bonus Action other than Step of the Wind, "
			"you can also use **Step of the Wind** immediately after "
			"that Bonus Action."
			),
		)

Quivering_Palm = _open_hand(
		name="Quivering Palm",
		min_level=17,
		description=(
			"When you hit a creature with an Unarmed Strike, you can "
			"expend **4 Focus Points** to start imperceptible "
			"vibrations in the target's body, lasting a number of days "
			"equal to your Monk level.\n\nThe vibrations are harmless "
			"until you end them. When you take the Attack action, you "
			"can forgo one attack to end the vibrations. To end them, "
			"you and the target must be on the same plane. When you end "
			"them, the target makes a Constitution save, taking "
			"**10d12 Force damage** on a failed save or half on "
			"success.\n\nYou can have only one creature under this "
			"effect at a time. You can end vibrations harmlessly with "
			"no action."
			),
		)
