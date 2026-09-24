"""
Ledger_of_Gear — adventuring gear, valuables, and the seven equipment packs.

Built with ``Make_Item``.  Tools are in ``Ledger_of_Tools``.

Data source: the 2024 equipment tables (dnd2024.wikidot.com/equipment:tool
and :adventuring-gear), transcribed 2026-07-31. Prices and weights are game
FACTS and are reproduced as such; every description here is our own wording.

Costs are held in gold: 1 SP = 0.1 GP, 1 CP = 0.01 GP.
"""

from __future__ import annotations

from AtlasInventarium.Grimoire_of_Items import Make_Item, Item


# Tools live in ``Ledger_of_Tools``, their one copy (QST-0116).  This file
# carried a second, hand-kept list of every tool that nothing imported.


# ---------------------------------------------------------------------------
# Adventuring Gear
# ---------------------------------------------------------------------------

def _gear(
		name: str,
		value: float,
		weight: float,
		description: str = "",
		) -> Item:
	return Make_Item(
			name=name,
			value=value,
			weight=weight,
			description=description,
			)


Backpack = _gear("Backpack", 2, 5, "Holds a cubic foot or 30 pounds of gear.")
Ball_Bearings = _gear("Ball Bearings", 1, 2, "Spilled across the ground to send pursuers sprawling.")
Bedroll = _gear("Bedroll", 1, 7)
Bell = _gear("Bell", 1, 0)
Blanket = _gear("Blanket", 0.5, 3)
Book = _gear("Book", 25, 5)
Bullseye_Lantern = _gear("Bullseye Lantern", 10, 2, "Casts a cone of bright light.")
Caltrops = _gear("Caltrops", 1, 2, "A bag of spikes strewn to slow a charge.")
Candle = _gear("Candle", 0.01, 0)
Case_Map_or_Scroll = _gear("Map or Scroll Case", 1, 1)
Chest = _gear("Chest", 5, 25)
Clothes_Fine = _gear("Fine Clothes", 15, 6)
Costume = _gear("Costume", 5, 4)
Crowbar = _gear("Crowbar", 2, 5, "Grants Advantage on Strength checks where leverage helps.")
Holy_Water = _gear("Holy Water", 25, 1, "A flask of blessed water, thrown as an improvised weapon.")
Hooded_Lantern = _gear("Hooded Lantern", 5, 2, "Its shutter dims the light without dousing it.")
Ink = _gear("Ink", 10, 0, "A one-ounce bottle.")
Ink_Pen = _gear("Ink Pen", 0.02, 0)
Lamp = _gear("Lamp", 0.5, 1, "Burns oil, shedding light in a 15-foot radius.")
Mirror = _gear("Mirror", 5, 0.5, "A polished steel hand mirror.")
Oil = _gear("Oil", 0.1, 1, "A flask of oil — fuel for a lamp, or thrown and lit.")
Paper = _gear("Paper", 0.2, 0, "One sheet.")
Parchment = _gear("Parchment", 0.1, 0, "One sheet.")
Perfume = _gear("Perfume", 5, 0)
Rations = _gear("Rations", 0.5, 2, "Dry food sufficient for one day.")
Robe = _gear("Robe", 1, 4)
Rope = _gear("Rope", 1, 5, "Fifty feet of it.")
Tinderbox = _gear("Tinderbox", 0.5, 1, "Flint, fire steel, and tinder for striking a spark.")
Torch = _gear("Torch", 0.01, 1, "Burns for 1 hour, shedding bright light in a 20-foot radius.")
Waterskin = _gear("Waterskin", 0.2, 5, "Holds 4 pints; the weight given is when full.")

ADVENTURING_GEAR: tuple[Item, ...] = (
		Backpack, Ball_Bearings, Bedroll, Bell, Blanket, Book, Bullseye_Lantern,
		Caltrops, Candle, Case_Map_or_Scroll, Chest, Clothes_Fine, Costume,
		Crowbar, Holy_Water, Hooded_Lantern, Ink, Ink_Pen, Lamp, Mirror, Oil,
		Paper, Parchment, Perfume, Rations, Robe, Rope, Tinderbox, Torch,
		Waterskin,
		)

ADVENTURING_GEAR_BY_NAME: dict[str, Item] = {
		item.name: item
		for item in ADVENTURING_GEAR
		}


# ---------------------------------------------------------------------------
# Valuables — wealth a hero wears instead of hauling
# ---------------------------------------------------------------------------
#
# Julio (2026-08-05): "for jewels it should be multi, instead of carrying a
# lot of money." Coin is heavy, conspicuous and easy to lose; anyone with
# means converts the surplus into something they can wear, and the Jewelry
# slot already holds three. These grant NOTHING — their whole worth is their
# resale value, which is exactly the point.
#
# Prices follow the 2024 gemstone and art-object bands (10 / 25 / 50 / 100 /
# 250 / 750 gp), so selling one back is never a surprise.

def _jewel(
		name: str,
		value: float,
		description: str = "",
		) -> Item:
	from AtlasInventarium.ItemKit import Make_Worn, Jewelry
	return Make_Worn(
			name=name,
			slot=Jewelry,
			value=value,
			weight=0,
			description=description,
			)


Copper_Band = _jewel(
		"Copper Band",
		10,
		"A twist of {material}, worn smooth. Worth a night's lodging.",
		)
Amber_Pendant = _jewel(
		"Amber Pendant",
		25,
		"A drop of {material} on a cord, with something small caught inside.",
		)
Signet_Ring = _jewel(
		"Signet Ring",
		50,
		"A {material} ring cut with a mark. It opens doors coin cannot.",
		)
Jade_Torc = _jewel(
		"Jade Torc",
		100,
		"A heavy collar of {material}. Wealth worn where everyone can see it.",
		)
Pearl_Chain = _jewel(
		"Pearl Chain",
		250,
		"Matched pearls on {material}. A merchant's fortune, worn at the throat.",
		)
Ruby_Circlet = _jewel(
		"Ruby Circlet",
		750,
		"A band of {material} set with a stone the colour of a slow fire.",
		)

VALUABLES: tuple[Item, ...] = (
		Copper_Band, Amber_Pendant, Signet_Ring,
		Jade_Torc, Pearl_Chain, Ruby_Circlet,
		)

VALUABLES_BY_NAME: dict[str, Item] = {
		item.name: item
		for item in VALUABLES
		}


# ---------------------------------------------------------------------------
# Packs — contents and prices as printed; weights are summed from the parts
# ---------------------------------------------------------------------------

_PACK_CONTENTS: dict[str, tuple[tuple[str, int], ...]] = {
		"Burglar's Pack": (
				("Backpack", 1), ("Ball Bearings", 1), ("Bell", 1),
				("Candle", 10), ("Crowbar", 1), ("Hooded Lantern", 1),
				("Oil", 7), ("Rations", 5), ("Rope", 1), ("Tinderbox", 1),
				("Waterskin", 1),
				),
		"Diplomat's Pack": (
				("Chest", 1), ("Fine Clothes", 1), ("Ink", 1), ("Ink Pen", 5),
				("Lamp", 1), ("Map or Scroll Case", 2), ("Oil", 4),
				("Paper", 5), ("Parchment", 5), ("Perfume", 1),
				("Tinderbox", 1),
				),
		"Dungeoneer's Pack": (
				("Backpack", 1), ("Caltrops", 1), ("Crowbar", 1), ("Oil", 2),
				("Rations", 10), ("Rope", 1), ("Tinderbox", 1), ("Torch", 10),
				("Waterskin", 1),
				),
		"Entertainer's Pack": (
				("Backpack", 1), ("Bedroll", 1), ("Bell", 1),
				("Bullseye Lantern", 1), ("Costume", 3), ("Mirror", 1),
				("Oil", 8), ("Rations", 9), ("Tinderbox", 1), ("Waterskin", 1),
				),
		"Explorer's Pack": (
				("Backpack", 1), ("Bedroll", 1), ("Oil", 2), ("Rations", 10),
				("Rope", 1), ("Tinderbox", 1), ("Torch", 10), ("Waterskin", 1),
				),
		"Priest's Pack": (
				("Backpack", 1), ("Blanket", 1), ("Holy Water", 1), ("Lamp", 1),
				("Rations", 7), ("Robe", 1), ("Tinderbox", 1),
				),
		"Scholar's Pack": (
				("Backpack", 1), ("Book", 1), ("Ink", 1), ("Ink Pen", 1),
				("Lamp", 1), ("Oil", 10), ("Parchment", 10), ("Tinderbox", 1),
				),
		}

_PACK_PRICES: dict[str, float] = {
		"Burglar's Pack": 16,
		"Diplomat's Pack": 39,
		"Dungeoneer's Pack": 12,
		"Entertainer's Pack": 40,
		"Explorer's Pack": 10,
		"Priest's Pack": 33,
		"Scholar's Pack": 40,
		}


def Make_Pack(
		name: str,
		contents: tuple[tuple[str, int], ...],
		value: float,
		) -> Item:
	"""
	Craft a pack as one purchasable Item that remembers what is inside it.

	``item.contents`` is ``((item_name, quantity), …)`` — a loadout policy
	resolves the names against ``ADVENTURING_GEAR_BY_NAME`` when it opens the
	pack into the bag.
	"""
	weight = sum(
			ADVENTURING_GEAR_BY_NAME[item_name].weight * quantity
			for item_name, quantity in contents
			)
	pack = Make_Item(
			name=name,
			value=value,
			weight=weight,
			description="A pack of standard adventuring gear.",
			)
	pack.contents = contents
	return pack


PACKS: tuple[Item, ...] = tuple(
		Make_Pack(
				name,
				_PACK_CONTENTS[name],
				_PACK_PRICES[name],
				)
		for name in sorted(
				_PACK_CONTENTS
				)
		)

PACKS_BY_NAME: dict[str, Item] = {
		pack.name: pack
		for pack in PACKS
		}

Explorers_Pack = PACKS_BY_NAME["Explorer's Pack"]


__all__ = (
		"ADVENTURING_GEAR",
		"ADVENTURING_GEAR_BY_NAME",
		"Make_Pack",
		"Explorers_Pack",
		"PACKS",
		"PACKS_BY_NAME",
		"VALUABLES",
		"VALUABLES_BY_NAME",
		)


def _self_test():
	gear_names = [item.name for item in ADVENTURING_GEAR]
	assert len(gear_names) == len(set(gear_names))

	assert len(PACKS) == 7, f"expected all seven packs, got {len(PACKS)}"

	for pack in PACKS:
		assert pack.contents, f"{pack.name} is empty"
		for item_name, quantity in pack.contents:
			assert item_name in ADVENTURING_GEAR_BY_NAME, (
					f"{pack.name} references unknown item {item_name!r}"
					)
			assert quantity > 0
		# A pack must never cost MORE than buying its parts loose.
		loose = sum(
				ADVENTURING_GEAR_BY_NAME[item_name].value * quantity
				for item_name, quantity in pack.contents
				)
		assert pack.value <= loose + 1e-6, (
				f"{pack.name} costs {pack.value} but its parts total {loose}"
				)

	# Valuables are wealth, not power: they must grant nothing at all, or
	# "carry your money as jewels" would quietly become a stat boost.
	from AtlasInventarium.ItemKit import Jewelry, Wearable

	values = [jewel.value for jewel in VALUABLES]
	assert values == sorted(
			values
			), "valuables must read cheapest-first, so a purse can be spent down"
	for jewel in VALUABLES:
		assert jewel in Jewelry and jewel in Wearable, jewel.name
		assert not jewel.grants, (
				f"{jewel.name} grants {jewel.grants} — valuables are wealth, "
				f"not equipment"
				)
		assert jewel.weight == 0, f"{jewel.name} should be lighter than coin"

	print(
			f"OK — Ledger_of_Gear self-test "
			f"({len(ADVENTURING_GEAR)} gear items, {len(PACKS)} packs, "
			f"{len(VALUABLES)} valuables)"
			)


if __name__ == "__main__":
	_self_test()
