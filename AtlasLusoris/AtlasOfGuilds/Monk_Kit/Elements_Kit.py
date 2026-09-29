"""
Elements_Kit — the Warrior of the Elements: its Tag and its lessons.

Thought pattern
	1. The Warrior is a Tag: ``Elements``, a Specialization of the Monk.
	2. Each lesson names its Warrior by that Tag (``path=Elements``), a
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


Elements = Make_Specialization(
	guild=Monk,
	name="Elements",
	module=__name__,
	)


def _elements(
		*,
		name: str,
		min_level: int,
		description,
		chips=(),
		flag: bool = False,
		):
	"""One Elements lesson: it awakens only for this Warrior."""
	return Make_Training(
			name=name,
			guild_name=GUILD,
			min_level=min_level,
			description=description,
			chips=chips,
			path=Elements,
			flag=flag,
			)


# ---------------------------------------------------------------------------
# Elements: the lessons
# ---------------------------------------------------------------------------


Elemental_Attunement = _elements(
		name="Elemental Attunement",
		min_level=3,
		description=(
			"At the start of your turn, you can expend 1 Focus Point to "
			"imbue yourself with elemental energy for 10 minutes or "
			"until Incapacitated. While active:"
			"\n\n\n- **Reach.** Your Unarmed Strike reach is 10 feet "
			"greater than normal, as elemental energy extends from "
			"you."
			"\n- **Elemental Strikes.** When you hit with an Unarmed "
			"Strike, you can deal Acid, Cold, Fire, Lightning, or "
			"Thunder damage instead. You can also force a Strength "
			"save; on a failed save, move the target up to 10 feet "
			"toward or away from you."
			"\n\n"
			),
		)

Manipulate_Elements = _elements(
		name="Manipulate Elements",
		flag=True,
		min_level=3,
		description=(
			"You know the *Elementalism* cantrip. Wisdom is your "
			"spellcasting ability for it."
			),
		)

Elemental_Burst = _elements(
		name="Elemental Burst",
		min_level=6,
		description=(
			"As a *Magic action*, expend **2 Focus Points** to "
			"cause elemental energy to burst in a **20-foot-radius "
			"Sphere** centered on a point within 120 feet. Choose "
			"Acid, Cold, Fire, Lightning, or Thunder damage.\n\nEach "
			"creature in the Sphere makes a Dexterity save. On a failed "
			"save, a creature takes damage equal to **three rolls of "
			"your Martial Arts die**. On a success, half damage."
			),
		)

Stride_of_the_Elements = _elements(
		name="Stride of the Elements",
		min_level=11,
		description=(
			"While your Elemental Attunement is active, you have a "
			"**Fly Speed and Swim Speed** equal to your Speed."
			),
		)

Elemental_Epitome = _elements(
		name="Elemental Epitome",
		min_level=17,
		description=(
			"While your Elemental Attunement is active, you gain the "
			"following additional benefits:\n\n**Damage Resistance.** "
			"Resistance to one of the following damage types of your "
			"choice: Acid, Cold, Fire, Lightning, or Thunder. You can "
			"change this choice at the start of each of your turns."
			"\n\n**Destructive Stride.** When you use Step of the "
			"Wind, your Speed increases by 20 feet until the end of the "
			"turn. Any creature of your choice takes damage equal to "
			"one roll of your Martial Arts die when you enter a space "
			"within 5 feet of it (once per turn). Damage type is your "
			"choice of Acid, Cold, Fire, Lightning, or Thunder."
			"\n\n**Empowered Strikes.** Once on each of your turns, "
			"you can deal extra damage equal to one Martial Arts die "
			"roll when you hit with an Unarmed Strike. Same damage type "
			"as the strike."
			),
		)
