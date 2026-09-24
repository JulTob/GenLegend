"""
Ledger_of_Weapons — the PHB 2024 weapon table, built with ``Make_Weapon``.

One record per weapon; nothing here decides who owns one — that is a
loadout policy's job (``GearKit`` / ``Outfit``). This Ledger only answers
"what does a Longsword look like": its damage, its properties, its mastery.

Musket and Pistol are DMG-optional gunpowder weapons, tagged ``Firearm``
(a Weapon subtype) rather than plain ``Weapon`` — Martial proficiency does
not grant them for free (the audit's exact complaint about the old
catalogue: a Ranger with no firearm training could still "master" one).
"""

from __future__ import annotations

from AtlasInventarium.Grimoire_of_Items import Make_Weapon, Item


# ---------------------------------------------------------------------------
# Simple Melee
# ---------------------------------------------------------------------------

Club = Make_Weapon(
		name="Club",
		damage="1d4",
		damage_type="Bludgeoning",
		category="Simple",
		reach="Melee",
		mastery="Slow",
		properties=("Light",),
		value=0.1,
		weight=2,
		)

Dagger = Make_Weapon(
		name="Dagger",
		damage="1d4",
		damage_type="Piercing",
		category="Simple",
		reach="Melee",
		mastery="Nick",
		properties=("Finesse", "Light", "Thrown (20/60)"),
		value=2,
		weight=1,
		)

Greatclub = Make_Weapon(
		name="Greatclub",
		damage="1d8",
		damage_type="Bludgeoning",
		category="Simple",
		reach="Melee",
		mastery="Push",
		properties=("Two-Handed",),
		value=0.2,
		weight=10,
		)

Handaxe = Make_Weapon(
		name="Handaxe",
		damage="1d6",
		damage_type="Slashing",
		category="Simple",
		reach="Melee",
		mastery="Vex",
		properties=("Light", "Thrown (20/60)"),
		value=5,
		weight=2,
		)

Javelin = Make_Weapon(
		name="Javelin",
		damage="1d6",
		damage_type="Piercing",
		category="Simple",
		reach="Melee",
		mastery="Slow",
		properties=("Thrown (30/120)",),
		value=0.5,
		weight=2,
		)

Light_Hammer = Make_Weapon(
		name="Light Hammer",
		damage="1d4",
		damage_type="Bludgeoning",
		category="Simple",
		reach="Melee",
		mastery="Nick",
		properties=("Light", "Thrown (20/60)"),
		value=2,
		weight=2,
		)

Mace = Make_Weapon(
		name="Mace",
		damage="1d6",
		damage_type="Bludgeoning",
		category="Simple",
		reach="Melee",
		mastery="Sap",
		value=5,
		weight=4,
		)

Quarterstaff = Make_Weapon(
		name="Quarterstaff",
		damage="1d6",
		damage_type="Bludgeoning",
		category="Simple",
		reach="Melee",
		mastery="Topple",
		properties=("Versatile (1d8)",),
		value=0.2,
		weight=4,
		)

Sickle = Make_Weapon(
		name="Sickle",
		damage="1d4",
		damage_type="Slashing",
		category="Simple",
		reach="Melee",
		mastery="Nick",
		properties=("Light",),
		value=1,
		weight=2,
		)

Spear = Make_Weapon(
		name="Spear",
		damage="1d6",
		damage_type="Piercing",
		category="Simple",
		reach="Melee",
		mastery="Sap",
		properties=("Thrown (20/60)", "Versatile (1d8)"),
		value=1,
		weight=3,
		)


# ---------------------------------------------------------------------------
# Simple Ranged
# ---------------------------------------------------------------------------

Dart = Make_Weapon(
		name="Dart",
		damage="1d4",
		damage_type="Piercing",
		category="Simple",
		reach="Ranged",
		mastery="Vex",
		properties=("Finesse", "Thrown (20/60)"),
		value=0.05,
		weight=0.25,
		)

Light_Crossbow = Make_Weapon(
		name="Light Crossbow",
		damage="1d8",
		damage_type="Piercing",
		category="Simple",
		reach="Ranged",
		mastery="Slow",
		properties=("Ammunition (80/320)", "Loading", "Two-Handed"),
		value=25,
		weight=5,
		)

Shortbow = Make_Weapon(
		name="Shortbow",
		damage="1d6",
		damage_type="Piercing",
		category="Simple",
		reach="Ranged",
		mastery="Vex",
		properties=("Ammunition (80/320)", "Two-Handed"),
		value=25,
		weight=2,
		)

Sling = Make_Weapon(
		name="Sling",
		damage="1d4",
		damage_type="Bludgeoning",
		category="Simple",
		reach="Ranged",
		mastery="Slow",
		properties=("Ammunition (30/120)",),
		value=1,
		weight=0,
		)


# ---------------------------------------------------------------------------
# Martial Melee
# ---------------------------------------------------------------------------

Battleaxe = Make_Weapon(
		name="Battleaxe",
		damage="1d8",
		damage_type="Slashing",
		category="Martial",
		reach="Melee",
		mastery="Topple",
		properties=("Versatile (1d10)",),
		value=10,
		weight=4,
		)

Flail = Make_Weapon(
		name="Flail",
		damage="1d8",
		damage_type="Bludgeoning",
		category="Martial",
		reach="Melee",
		mastery="Sap",
		value=10,
		weight=2,
		)

Glaive = Make_Weapon(
		name="Glaive",
		damage="1d10",
		damage_type="Slashing",
		category="Martial",
		reach="Melee",
		mastery="Graze",
		properties=("Heavy", "Reach", "Two-Handed"),
		value=20,
		weight=6,
		)

Greataxe = Make_Weapon(
		name="Greataxe",
		damage="1d12",
		damage_type="Slashing",
		category="Martial",
		reach="Melee",
		mastery="Cleave",
		properties=("Heavy", "Two-Handed"),
		value=30,
		weight=7,
		)

Greatsword = Make_Weapon(
		name="Greatsword",
		damage="2d6",
		damage_type="Slashing",
		category="Martial",
		reach="Melee",
		mastery="Graze",
		properties=("Heavy", "Two-Handed"),
		value=50,
		weight=6,
		)

Halberd = Make_Weapon(
		name="Halberd",
		damage="1d10",
		damage_type="Slashing",
		category="Martial",
		reach="Melee",
		mastery="Cleave",
		properties=("Heavy", "Reach", "Two-Handed"),
		value=20,
		weight=6,
		)

Lance = Make_Weapon(
		name="Lance",
		damage="1d10",
		damage_type="Piercing",
		category="Martial",
		reach="Melee",
		mastery="Topple",
		properties=("Reach", "Special (one-handed while mounted)"),
		value=10,
		weight=6,
		)

Longsword = Make_Weapon(
		name="Longsword",
		damage="1d8",
		damage_type="Slashing",
		category="Martial",
		reach="Melee",
		mastery="Sap",
		properties=("Versatile (1d10)",),
		value=15,
		weight=3,
		)

Maul = Make_Weapon(
		name="Maul",
		damage="2d6",
		damage_type="Bludgeoning",
		category="Martial",
		reach="Melee",
		mastery="Topple",
		properties=("Heavy", "Two-Handed"),
		value=10,
		weight=10,
		)

Morningstar = Make_Weapon(
		name="Morningstar",
		damage="1d8",
		damage_type="Piercing",
		category="Martial",
		reach="Melee",
		mastery="Sap",
		value=15,
		weight=4,
		)

Pike = Make_Weapon(
		name="Pike",
		damage="1d10",
		damage_type="Piercing",
		category="Martial",
		reach="Melee",
		mastery="Push",
		properties=("Heavy", "Reach", "Two-Handed"),
		value=5,
		weight=18,
		)

Rapier = Make_Weapon(
		name="Rapier",
		damage="1d8",
		damage_type="Piercing",
		category="Martial",
		reach="Melee",
		mastery="Vex",
		properties=("Finesse",),
		value=25,
		weight=2,
		)

Scimitar = Make_Weapon(
		name="Scimitar",
		damage="1d6",
		damage_type="Slashing",
		category="Martial",
		reach="Melee",
		mastery="Nick",
		properties=("Finesse", "Light"),
		value=25,
		weight=3,
		)

Shortsword = Make_Weapon(
		name="Shortsword",
		damage="1d6",
		damage_type="Piercing",
		category="Martial",
		reach="Melee",
		mastery="Vex",
		properties=("Finesse", "Light"),
		value=25,
		weight=2,
		)

Trident = Make_Weapon(
		name="Trident",
		damage="1d8",
		damage_type="Piercing",
		category="Martial",
		reach="Melee",
		mastery="Topple",
		properties=("Thrown (20/60)", "Versatile (1d10)"),
		value=5,
		weight=4,
		)

War_Pick = Make_Weapon(
		name="War Pick",
		damage="1d8",
		damage_type="Piercing",
		category="Martial",
		reach="Melee",
		mastery="Sap",
		value=5,
		weight=2,
		)

Warhammer = Make_Weapon(
		name="Warhammer",
		damage="1d8",
		damage_type="Bludgeoning",
		category="Martial",
		reach="Melee",
		mastery="Push",
		properties=("Versatile (1d10)",),
		value=15,
		weight=2,
		)

Whip = Make_Weapon(
		name="Whip",
		damage="1d4",
		damage_type="Slashing",
		category="Martial",
		reach="Melee",
		mastery="Slow",
		properties=("Finesse", "Reach"),
		value=2,
		weight=3,
		)


# ---------------------------------------------------------------------------
# Martial Ranged
# ---------------------------------------------------------------------------

Blowgun = Make_Weapon(
		name="Blowgun",
		damage="1",
		damage_type="Piercing",
		category="Martial",
		reach="Ranged",
		mastery="Vex",
		properties=("Ammunition (25/100)", "Loading"),
		value=10,
		weight=1,
		)

Hand_Crossbow = Make_Weapon(
		name="Hand Crossbow",
		damage="1d6",
		damage_type="Piercing",
		category="Martial",
		reach="Ranged",
		mastery="Vex",
		properties=("Ammunition (30/120)", "Light", "Loading"),
		value=75,
		weight=3,
		)

Heavy_Crossbow = Make_Weapon(
		name="Heavy Crossbow",
		damage="1d10",
		damage_type="Piercing",
		category="Martial",
		reach="Ranged",
		mastery="Push",
		properties=("Ammunition (100/400)", "Heavy", "Loading", "Two-Handed"),
		value=50,
		weight=18,
		)

Longbow = Make_Weapon(
		name="Longbow",
		damage="1d8",
		damage_type="Piercing",
		category="Martial",
		reach="Ranged",
		mastery="Slow",
		properties=("Ammunition (150/600)", "Heavy", "Two-Handed"),
		value=50,
		weight=2,
		)


# ---------------------------------------------------------------------------
# Firearms (DMG-optional — tagged Firearm, not granted by plain Martial)
# ---------------------------------------------------------------------------

Musket = Make_Weapon(
		name="Musket",
		damage="1d12",
		damage_type="Piercing",
		category="Firearm",
		reach="Ranged",
		mastery="Slow",
		properties=("Ammunition (40/120)", "Loading", "Two-Handed"),
		value=500,
		weight=10,
		description="A DMG-optional firearm — Martial proficiency alone does not grant it.",
		)

Pistol = Make_Weapon(
		name="Pistol",
		damage="1d10",
		damage_type="Piercing",
		category="Firearm",
		reach="Ranged",
		mastery="Vex",
		properties=("Ammunition (30/90)", "Loading"),
		value=250,
		weight=3,
		description="A DMG-optional firearm — Martial proficiency alone does not grant it.",
		)


SIMPLE_MELEE: tuple[Item, ...] = (
		Club, Dagger, Greatclub, Handaxe, Javelin, Light_Hammer, Mace,
		Quarterstaff, Sickle, Spear,
		)
SIMPLE_RANGED: tuple[Item, ...] = (
		Dart, Light_Crossbow, Shortbow, Sling,
		)
MARTIAL_MELEE: tuple[Item, ...] = (
		Battleaxe, Flail, Glaive, Greataxe, Greatsword, Halberd, Lance,
		Longsword, Maul, Morningstar, Pike, Rapier, Scimitar, Shortsword,
		Trident, War_Pick, Warhammer, Whip,
		)
MARTIAL_RANGED: tuple[Item, ...] = (
		Blowgun, Hand_Crossbow, Heavy_Crossbow, Longbow,
		)
FIREARMS: tuple[Item, ...] = (
		Musket, Pistol,
		)

WEAPONS: tuple[Item, ...] = (
		SIMPLE_MELEE + SIMPLE_RANGED + MARTIAL_MELEE + MARTIAL_RANGED + FIREARMS
		)

WEAPONS_BY_NAME: dict[str, Item] = {
		weapon.name: weapon
		for weapon in WEAPONS
		}


__all__ = (
		"FIREARMS",
		"MARTIAL_MELEE",
		"MARTIAL_RANGED",
		"SIMPLE_MELEE",
		"SIMPLE_RANGED",
		"WEAPONS",
		"WEAPONS_BY_NAME",
		)


def _self_test():
	from AtlasInventarium.Grimoire_of_Items import Firearm, Martial, Melee, Ranged, Simple, Weapon

	names = [weapon.name for weapon in WEAPONS]
	assert len(names) == len(set(names)), (
			"duplicate weapon names in the ledger"
			)
	assert len(WEAPONS) == 10 + 4 + 18 + 4 + 2, len(WEAPONS)

	for weapon in WEAPONS:
		assert weapon in Weapon, weapon.name
		assert weapon.mastery, f"{weapon.name} has no mastery property"
		assert (weapon in Simple) != (weapon in Martial), (
				f"{weapon.name} must be exactly one of Simple/Martial"
				)
		assert (weapon in Melee) != (weapon in Ranged), (
				f"{weapon.name} must be exactly one of Melee/Ranged"
				)

	for weapon in FIREARMS:
		assert weapon in Firearm, weapon.name
		assert weapon in Martial, "firearms still gate on Martial category"

	for weapon in SIMPLE_MELEE + SIMPLE_RANGED:
		assert weapon not in Firearm

	assert Longsword in Martial and Longsword in Melee
	assert Shortbow in Simple and Shortbow in Ranged
	assert "Finesse" in Dagger.properties

	print(
			f"OK — Ledger_of_Weapons self-test ({len(WEAPONS)} weapons, "
			f"{len(FIREARMS)} firearms tagged separately)"
			)


if __name__ == "__main__":
	_self_test()
