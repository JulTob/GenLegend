"""
Ledger_of_Armors — the PHB 2024 armor table, built with ``Make_Armour``.

One record per armor and the Shield. ``str_requirement``/``stealth_disadvantage``
are recorded but not yet enforced — a later quest applies the Speed penalty and
Stealth check disadvantage; Quest 1 only needs the data to exist and be queryable.
"""

from __future__ import annotations

from AtlasInventarium.Grimoire_of_Items import Make_Armour, Make_Shield, Item


# ---------------------------------------------------------------------------
# Light Armor — full Dexterity applies
# ---------------------------------------------------------------------------

Padded = Make_Armour(
		name="Padded",
		base_ac=11,
		kind="Light",
		value=5,
		weight=8,
		stealth_disadvantage=True,
		description="Quilted layers of cloth and batting.",
		)

Leather = Make_Armour(
		name="Leather",
		base_ac=11,
		kind="Light",
		value=10,
		weight=10,
		description="The breastplate and shoulder protectors are made of "
			"leather that has been stiffened by being boiled in oil.",
		)

Studded_Leather = Make_Armour(
		name="Studded Leather",
		base_ac=12,
		kind="Light",
		value=45,
		weight=13,
		description="Leather reinforced with close-set rivets or spikes.",
		)


# ---------------------------------------------------------------------------
# Medium Armor — Dexterity capped at +2
# ---------------------------------------------------------------------------

Hide = Make_Armour(
		name="Hide",
		base_ac=12,
		kind="Medium",
		value=10,
		weight=12,
		description="A crude armor made from thick furs and pelts.",
		)

Chain_Shirt = Make_Armour(
		name="Chain Shirt",
		base_ac=13,
		kind="Medium",
		value=50,
		weight=20,
		description="A shirt of interlocking metal rings worn under clothing.",
		)

Scale_Mail = Make_Armour(
		name="Scale Mail",
		base_ac=14,
		kind="Medium",
		value=50,
		weight=45,
		stealth_disadvantage=True,
		description="A coat of leather covered with overlapping pieces of metal.",
		)

Breastplate = Make_Armour(
		name="Breastplate",
		base_ac=14,
		kind="Medium",
		value=400,
		weight=20,
		description="A fitted metal chest piece worn with supple leather.",
		)

Half_Plate = Make_Armour(
		name="Half Plate",
		base_ac=15,
		kind="Medium",
		value=750,
		weight=40,
		stealth_disadvantage=True,
		description="Shaped metal plates cover most of the wearer's body.",
		)


# ---------------------------------------------------------------------------
# Heavy Armor — Dexterity does not apply
# ---------------------------------------------------------------------------

Ring_Mail = Make_Armour(
		name="Ring Mail",
		base_ac=14,
		kind="Heavy",
		value=30,
		weight=40,
		stealth_disadvantage=True,
		description="Leather armor with heavy rings sewn into it.",
		)

Chain_Mail = Make_Armour(
		name="Chain Mail",
		base_ac=16,
		kind="Heavy",
		value=75,
		weight=55,
		str_requirement=13,
		stealth_disadvantage=True,
		description="Interlocking metal rings, worn over a padded coat.",
		)

Splint = Make_Armour(
		name="Splint",
		base_ac=17,
		kind="Heavy",
		value=200,
		weight=60,
		str_requirement=15,
		stealth_disadvantage=True,
		description="Narrow vertical strips of metal riveted to a backing of leather.",
		)

Plate = Make_Armour(
		name="Plate",
		base_ac=18,
		kind="Heavy",
		value=1500,
		weight=65,
		str_requirement=15,
		stealth_disadvantage=True,
		description="Shaped, interlocking metal plates covering the entire body.",
		)


Shield = Make_Shield(
		name="Shield",
		bonus=2,
		value=10,
		weight=6,
		# {material} is filled per hero by Map_of_Materials.personalise, so the
		# catalogue entry stays generic while the one a Character carries says
		# what it is actually made of.
		description="A {material} shield strapped to one arm.",
		)


LIGHT_ARMOR: tuple[Item, ...] = (
		Padded, Leather, Studded_Leather,
		)
MEDIUM_ARMOR: tuple[Item, ...] = (
		Hide, Chain_Shirt, Scale_Mail, Breastplate, Half_Plate,
		)
HEAVY_ARMOR: tuple[Item, ...] = (
		Ring_Mail, Chain_Mail, Splint, Plate,
		)

ARMORS: tuple[Item, ...] = LIGHT_ARMOR + MEDIUM_ARMOR + HEAVY_ARMOR

ARMORS_BY_NAME: dict[str, Item] = {
		armor.name: armor
		for armor in ARMORS
		}


__all__ = (
		"ARMORS",
		"ARMORS_BY_NAME",
		"HEAVY_ARMOR",
		"LIGHT_ARMOR",
		"MEDIUM_ARMOR",
		"Shield",
		)


def _self_test():
	from AtlasInventarium.Grimoire_of_Items import Armour, Shield as ShieldTag

	names = [armor.name for armor in ARMORS]
	assert len(names) == len(set(names)), (
			"duplicate armor names in the ledger"
			)
	assert len(ARMORS) == 3 + 5 + 4, len(ARMORS)

	for armor in ARMORS:
		assert armor in Armour, armor.name

	for armor in LIGHT_ARMOR:
		assert armor.dex_cap is None, armor.name
	for armor in MEDIUM_ARMOR:
		assert armor.dex_cap == 2, armor.name
	for armor in HEAVY_ARMOR:
		assert armor.dex_cap == 0, armor.name

	# AC climbs within each tier
	assert [armor.base_ac for armor in LIGHT_ARMOR] == sorted(
			armor.base_ac for armor in LIGHT_ARMOR
			)
	assert [armor.base_ac for armor in HEAVY_ARMOR] == sorted(
			armor.base_ac for armor in HEAVY_ARMOR
			)

	assert Shield in ShieldTag
	assert Shield.shield_bonus == 2

	assert Chain_Mail.str_requirement == 13
	assert Leather.str_requirement == 0

	print(
			f"OK — Ledger_of_Armors self-test ({len(ARMORS)} armors + Shield)"
			)


if __name__ == "__main__":
	_self_test()
