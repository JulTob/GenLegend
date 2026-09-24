"""Fighting Style feats — 2024 PHB catalogue."""

from __future__ import annotations

from AtlasLusoris.FeatKit import Make_Fighting_Style


Archery = Make_Fighting_Style(
	name='Archery',
	description='You gain a +2 bonus to attack rolls you make with Ranged weapons.',
	)

BlindFighting = Make_Fighting_Style(
	name='Blind Fighting',
	description='You trained to fight without sight.',
	chips=(
			('Blindsight', '10 feet'),
			),
	)

Defense = Make_Fighting_Style(
	name='Defense',
	description="While you're wearing Light, Medium, or Heavy armor, you gain a +1 bonus to Armor Class.",
	)

Dueling = Make_Fighting_Style(
	name='Dueling',
	description="When you're holding a Melee weapon in one hand and no other weapons, you gain a +2 bonus to damage rolls with that weapon.",
	)

GreatWeaponFighting = Make_Fighting_Style(
	name='Great Weapon Fighting',
	description='When you roll damage for an attack you make with a Melee weapon that you are holding with two hands, you can treat any 1 or 2 on a damage die as a 3. The weapon must have the Two-Handed or Versatile property.',
	)

Interception = Make_Fighting_Style(
	name='Interception',
	description='When a creature you can see hits another creature within 5 feet of you with an attack roll, you can take a Reaction to reduce the damage by 1d10 plus your Proficiency Bonus. You must be holding a Shield or a Simple or Martial weapon.',
	)

Protection = Make_Fighting_Style(
	name='Protection',
	description='When a creature you can see attacks a target other than you within 5 feet of you, you can take a Reaction to impose Disadvantage on the triggering attack roll and all other attack rolls against that target until the start of your next turn if you remain within 5 feet and are holding a Shield.',
	)

ThrownWeaponFighting = Make_Fighting_Style(
	name='Thrown Weapon Fighting',
	description='When you hit with a ranged attack roll using a weapon that has the Thrown property, you gain a +2 bonus to the damage roll.',
	)

TwoWeaponFighting = Make_Fighting_Style(
	name='Two-Weapon Fighting',
	description="When you make an extra attack as a result of using a weapon that has the Light property, you can add your ability modifier to the damage of that attack if you aren't already adding it.",
	)

UnarmedFighting = Make_Fighting_Style(
	name='Unarmed Fighting',
	description="When you hit with your Unarmed Strike, you can deal Bludgeoning damage equal to 1d6 plus your Strength modifier instead of the normal damage. If you aren't holding any weapons or a Shield, the d6 becomes a d8. At the start of each of your turns, you can deal 1d4 Bludgeoning damage to one creature Grappled by you.",
	)

BlessedWarrior = Make_Fighting_Style(
	name='Blessed Warrior',
	description='You learn two cantrips of your choice from the Cleric spell list. They count as Paladin spells for you, and Charisma is your spellcasting ability for them.',
	guilds=('Paladin',),
	)

DruidicWarrior = Make_Fighting_Style(
	name='Druidic Warrior',
	description='You learn two cantrips of your choice from the Druid spell list. They count as Ranger spells for you, and Wisdom is your spellcasting ability for them.',
	guilds=('Ranger',),
	)
