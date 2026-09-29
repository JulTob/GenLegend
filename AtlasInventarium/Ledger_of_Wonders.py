"""
Ledger_of_Wonders — magic items, consumables, and classic adventuring wonders.

Every bonus here is a ``grants`` entry, so it is summed at read time and
disappears the moment the item is unequipped or sold. Nothing in this file
writes to a Character.

Where an item's effect is not yet mechanised (a Bag of Holding's capacity,
a Goggles' darkvision), it is carried as prose in ``description`` and left
OUT of ``grants`` — an unimplemented effect must not masquerade as a number
on the sheet.
"""

from __future__ import annotations

from AtlasInventarium.Grimoire_of_Items import (
		Make_Consumable,
		Make_Item,
		Make_Weapon,
		Make_Worn,
		Cloak,
		Footwear,
		Handwear,
		Headwear,
		Item,
		Jewelry,
		)


# ---------------------------------------------------------------------------
# Worn wonders — bonuses live in `grants`, summed live
# ---------------------------------------------------------------------------

Cloak_of_Protection = Make_Worn(
		name="Cloak of Protection",
		slot=Cloak,
		value=350,
		weight=1,
		grants={
				"AC": 1,
				"saves": 1,
				},
		description="A traveller's cloak that turns a blow aside and steadies "
			"the wearer against harm they never saw coming.",
		)

Ring_of_Protection = Make_Worn(
		name="Ring of Protection",
		slot=Jewelry,
		value=350,
		weight=0,
		grants={
				"AC": 1,
				"saves": 1,
				},
		description="A plain band that seems to tighten a moment before danger.",
		)

Bracers_of_Defense = Make_Worn(
		name="Bracers of Defense",
		slot=Handwear,
		value=600,
		weight=2,
		grants={
				"AC": 2,
				},
		description="Unarmoured arms turn aside steel as if plated. They do "
			"nothing for someone already wearing armour or holding a shield.",
		)

Boots_of_Striding = Make_Worn(
		name="Boots of Striding",
		slot=Footwear,
		value=250,
		weight=1,
		grants={
				"speed": 10,
				},
		description="Every step covers more ground than it has any right to.",
		)

Amulet_of_Health = Make_Worn(
		name="Amulet of Health",
		slot=Jewelry,
		value=800,
		weight=1,
		grants={
				"HP": 10,
				},
		description="The wearer's constitution steadies to a hardy baseline, "
			"whatever their natural frailty.",
		)

Circlet_of_Insight = Make_Worn(
		name="Circlet of Insight",
		slot=Headwear,
		value=400,
		weight=1,
		grants={
				"initiative": 2,
				},
		description="Thought arrives a half-second ahead of everyone else's.",
		)

Brooch_of_Shielding = Make_Worn(
		name="Brooch of Shielding",
		slot=Jewelry,
		value=300,
		weight=0,
		grants={
				"saves": 1,
				},
		description="A small silver pin that drinks the edge off hostile magic.",
		)

# --- classics whose effect is prose, not yet a number ----------------------

# Carried, not worn: a satchel occupies no body slot, so it must not
# compete with rings for one.
# Carries no mechanical bonus: encumbrance is not modelled, so there is no
# capacity for this to raise.
Bag_of_Holding = Make_Item(
		name="Bag of Holding",
		value=500,
		weight=15,
		description="The inside is far larger than the outside.",
		)

Goggles_of_Night = Make_Worn(
		name="Goggles of Night",
		slot=Headwear,
		value=250,
		weight=1,
		# Prose only: senses are not yet grantable, so this sets no
		# darkvision range on the Character.
		description="Darkvision to 60 feet, or a further 60 for eyes that "
			"already have it.",
		)

Gauntlets_of_Might = Make_Worn(
		name="Gauntlets of Might",
		slot=Handwear,
		value=700,
		weight=2,
		# Prose only: an item cannot yet override an ability score, so the
		# Character's Strength is untouched.
		description="The wearer's Strength settles at a giant's baseline.",
		)


# Wonders whose effect is prose rather than a grant, declared rather than
# detected. The self-test used to look for the phrase "not yet" inside the
# description, which forced an implementation note onto the player's sheet:
# "Vision is not yet modelled as a grant." Naming the set here keeps the same
# guarantee, keeps the reason in the code where it belongs, and additionally
# catches the opposite mistake, an item left in this tuple after somebody
# finally gives it grants.
PROSE_ONLY_WONDERS: tuple[Item, ...] = (
		Bag_of_Holding,
		Goggles_of_Night,
		Gauntlets_of_Might,
		)

WORN_WONDERS: tuple[Item, ...] = (
		Cloak_of_Protection, Ring_of_Protection, Bracers_of_Defense,
		Boots_of_Striding, Amulet_of_Health, Circlet_of_Insight,
		Brooch_of_Shielding, Goggles_of_Night, Gauntlets_of_Might,
		)

# Wonders that are carried rather than worn — no body slot, no competition.
CARRIED_WONDERS: tuple[Item, ...] = (
		Bag_of_Holding,
		)


# ---------------------------------------------------------------------------
# Consumables — these are MEANT to repeat; they stack freely
# ---------------------------------------------------------------------------

Potion_of_Healing = Make_Consumable(
		name="Potion of Healing",
		value=50,
		weight=0.5,
		description="Drink as a Bonus Action to regain 2d4 + 2 Hit Points.",
		)

Potion_of_Greater_Healing = Make_Consumable(
		name="Potion of Greater Healing",
		value=150,
		weight=0.5,
		description="Drink as a Bonus Action to regain 4d4 + 4 Hit Points.",
		)

Antitoxin = Make_Consumable(
		name="Antitoxin",
		value=50,
		weight=0,
		description="Advantage on saving throws against poison for 1 hour.",
		)

Oil_Flask = Make_Consumable(
		name="Oil Flask",
		value=0.1,
		weight=1,
		description="Thrown or poured, then lit. Burns for 2 rounds.",
		)

Scroll_of_Protection = Make_Consumable(
		name="Scroll of Protection",
		value=180,
		weight=0,
		description="Reading it wards a 5-foot radius against one kind of "
			"creature for 5 minutes.",
		)

Spell_Scroll = Make_Consumable(
		name="Spell Scroll",
		value=75,
		weight=0,
		description="A single spell, expended on casting. The spell it holds "
			"is chosen when the scroll is granted.",
		)

CONSUMABLES: tuple[Item, ...] = (
		Potion_of_Healing, Potion_of_Greater_Healing, Antitoxin, Oil_Flask,
		Scroll_of_Protection, Spell_Scroll,
		)


# ---------------------------------------------------------------------------
# Implements — weapons a caster can actually swing
# ---------------------------------------------------------------------------
#
# Julio (2026-08-05): "for magic users it would make sense to have some
# weapons that attack with int/wis/cha, to make them more usable… It should be
# clearly described in the description which one is using."
#
# The whole point of an implement is the ability it uses, so ``attack_with``
# is a FIELD, printed by ``Item.blurb`` on its own line. A caster reading
# their sheet sees "Attacks with Intelligence" beside the damage, not a
# sentence of prose they have to interpret.
#
# They are Simple weapons on purpose: an implement makes a caster usable in
# melee, it does not hand them martial training they never had.

Runeblade = Make_Weapon(
		name="Runeblade",
		damage="1d8",
		damage_type="Force",
		category="Simple",
		reach="Melee",
		properties=(
				"Versatile (1d10)",
				),
		value=400,
		weight=3,
		attack_with="Intelligence",
		description="A {material} blade cut with a scholar's notation. It "
			"answers to a mind that has read it, not to an arm.",
		grants={},
		)

Oath_Mace = Make_Weapon(
		name="Oath Mace",
		damage="1d6",
		damage_type="Radiant",
		category="Simple",
		reach="Melee",
		value=380,
		weight=4,
		attack_with="Wisdom",
		description="A head of {material} that strikes where its bearer's "
			"conviction points, and nowhere else.",
		grants={},
		)

Beguiler_Rapier = Make_Weapon(
		name="Beguiler's Rapier",
		damage="1d6",
		damage_type="Psychic",
		category="Simple",
		reach="Melee",
		properties=(
				"Finesse",
				),
		value=420,
		weight=2,
		attack_with="Charisma",
		description="A slender length of {material}. Its wielder wins the "
			"exchange by presence, and the blade merely arrives.",
		grants={},
		)

Warden_Staff = Make_Weapon(
		name="Warden's Staff",
		damage="1d8",
		damage_type="Bludgeoning",
		category="Simple",
		reach="Melee",
		properties=(
				"Versatile (1d10)",
				),
		value=360,
		weight=4,
		attack_with="Wisdom",
		description="A shaft of {material} grown, not cut. It moves with the "
			"instinct of the one holding it.",
		grants={},
		)

Hexbolt_Wand = Make_Weapon(
		name="Hexbolt Wand",
		damage="1d6",
		damage_type="Necrotic",
		category="Simple",
		reach="Ranged",
		properties=(
				"Range 60/180",
				),
		value=450,
		weight=1,
		attack_with="Charisma",
		description="A rod of {material} that spits a mote of cold light as "
			"far as its bearer can hold a grudge.",
		grants={},
		)

IMPLEMENTS: tuple[Item, ...] = (
		Runeblade, Oath_Mace, Beguiler_Rapier, Warden_Staff, Hexbolt_Wand,
		)

# Which ability each Guild would want an implement to use. A Guild absent
# here has no business with one — Fighters and Barbarians attack perfectly
# well with an arm.
IMPLEMENT_ABILITY: dict[str, str] = {
		"Wizard": "Intelligence",
		"Artificer": "Intelligence",
		"Cleric": "Wisdom",
		"Druid": "Wisdom",
		"Ranger": "Wisdom",
		"Monk": "Wisdom",
		"Bard": "Charisma",
		"Sorcerer": "Charisma",
		"Warlock": "Charisma",
		"Paladin": "Charisma",
		}


def implements_for(
		ability: str,
		) -> tuple[Item, ...]:
	"""Every implement that attacks with this ability."""
	return tuple(
			implement
			for implement in IMPLEMENTS
			if implement.attack_with == ability
			)


WONDERS: tuple[Item, ...] = WORN_WONDERS + CARRIED_WONDERS + CONSUMABLES

WONDERS_BY_NAME: dict[str, Item] = {
		wonder.name: wonder
		for wonder in WONDERS
		}


# Which wonders become plausible at which Hero level — the generator uses
# this so a level-1 character is not handed an Amulet of Health.
WONDER_TIERS: tuple[tuple[int, tuple[Item, ...]], ...] = (
		(
				1,
				(
						Potion_of_Healing,
						Oil_Flask,
						Antitoxin,
						),
				),
		(
				5,
				(
						Cloak_of_Protection,
						Ring_of_Protection,
						Boots_of_Striding,
						Brooch_of_Shielding,
						Goggles_of_Night,
						Potion_of_Greater_Healing,
						Spell_Scroll,
						),
				),
		(
				11,
				(
						Bracers_of_Defense,
						Circlet_of_Insight,
						Bag_of_Holding,
						Scroll_of_Protection,
						),
				),
		(
				17,
				(
						Amulet_of_Health,
						Gauntlets_of_Might,
						),
				),
		)


def wonders_up_to(
		level: int,
		) -> tuple[Item, ...]:
	"""Every wonder plausible for a Hero of this level."""
	found: list[Item] = []
	for minimum, wonders in WONDER_TIERS:
		if level >= minimum:
			found.extend(
					wonders
					)
	return tuple(
			found
			)


__all__ = (
		"CARRIED_WONDERS",
		"CONSUMABLES",
		"IMPLEMENTS",
		"IMPLEMENT_ABILITY",
		"WONDERS",
		"WONDERS_BY_NAME",
		"WONDER_TIERS",
		"WORN_WONDERS",
		"implements_for",
		"wonders_up_to",
		)


def _self_test():
	from AtlasInventarium.Grimoire_of_Items import (
			Consumable,
			Magical,
			Wearable,
			slot_of,
			)

	names = [wonder.name for wonder in WONDERS]
	assert len(names) == len(set(names)), "duplicate wonder names"

	# Anything that grants must be flagged Magical; anything that does not
	# must be honest about it rather than carrying an empty grants dict.
	for wonder in WORN_WONDERS:
		assert wonder in Wearable, wonder.name
		assert slot_of(wonder) is not None, wonder.name
		if wonder.grants:
			assert wonder in Magical, wonder.name
		else:
			assert wonder in PROSE_ONLY_WONDERS, (
					f"{wonder.name} grants nothing and is not declared in "
					"PROSE_ONLY_WONDERS"
					)

	# The other direction, so the declaration cannot go stale: once an item
	# really does grant something, it has to leave the tuple.
	for wonder in PROSE_ONLY_WONDERS:
		assert not wonder.grants, (
				f"{wonder.name} now grants {wonder.grants} and must be "
				"removed from PROSE_ONLY_WONDERS"
				)

	for consumable in CONSUMABLES:
		assert consumable in Consumable, consumable.name
		assert slot_of(consumable) is None, (
				f"{consumable.name} must not occupy a body slot"
				)

	# A satchel is carried, never worn — it must not compete for a ring slot.
	for carried_wonder in CARRIED_WONDERS:
		assert slot_of(carried_wonder) is None, (
				f"{carried_wonder.name} must not occupy a body slot"
				)
		assert carried_wonder not in Wearable, carried_wonder.name

	assert Cloak_of_Protection.grants == {
			"AC": 1,
			"saves": 1,
			}

	# Tier gating
	assert Potion_of_Healing in wonders_up_to(
			1
			)
	assert Cloak_of_Protection not in wonders_up_to(
			1
			)
	assert Cloak_of_Protection in wonders_up_to(
			5
			)
	assert Amulet_of_Health in wonders_up_to(
			20
			)
	assert len(
			wonders_up_to(
					20
					)
			) == len(
			WONDERS
			), "every wonder should be reachable by level 20"

	# --- implements: the ability must be stated, not implied ---------------
	from AtlasInventarium.ItemKit import Simple, Weapon

	abilities = set()
	for implement in IMPLEMENTS:
		assert implement in Weapon, implement.name
		assert implement in Simple, (
				f"{implement.name} must not smuggle martial training to a caster"
				)
		assert implement.attack_with, (
				f"{implement.name} is an implement with no ability"
				)
		# The reader must SEE which score swings it.
		assert f"Attacks with {implement.attack_with}" in implement.blurb(), (
				implement.blurb()
				)
		assert slot_of(implement) is None, (
				f"{implement.name} is wielded, not worn"
				)
		abilities.add(
				implement.attack_with
				)

	assert abilities == {
			"Intelligence",
			"Wisdom",
			"Charisma",
			}, abilities

	# Every Guild that wants an implement must have one to want.
	for guild, ability in IMPLEMENT_ABILITY.items():
		assert implements_for(
				ability
				), f"{guild} wants a {ability} implement and none exists"

	print(
			f"OK — Ledger_of_Wonders self-test ({len(WORN_WONDERS)} worn, "
			f"{len(CONSUMABLES)} consumables, {len(IMPLEMENTS)} implements, "
			f"4 tiers)"
			)


if __name__ == "__main__":
	_self_test()
