"""
Grimoire_of_Items — one generic Item, crafted into gear by Tags.

Thought pattern (read this before the code)
	1. An Item is almost nothing: a name, a price, a weight, a description.
	   Everything else is a Tag. There are no Armor/Weapon subclasses.
	2. Tags craft it. ``Wearable``/``Wieldable`` say where it can sit,
	   ``Armour``/``Weapon``/``Shield`` say what it does, ``Simple``/``Martial``
	   gate proficiency, ``Magical`` carries what it grants.
	3. ``Equipped`` is a Tag, not a slot pointer. So "is more than one armour
	   equipped?" is a question you can ASK — and answer by selling the worse
	   one and rebuilding (``reconcile``).
	4. Anything an artifact grants is summed at READ time (``armour_class``,
	   ``grant_total``). Natural defences are never overwritten, so removing or
	   selling the artifact simply removes its contribution.

Usage
	from AtlasInventarium.Grimoire_of_Items import (
			Build_Armour, Build_Weapon, equip, armour_class,
			)
	mail = Build_Armour(name="Chain Mail", base_ac=16, kind="Heavy", value=75)
	equip(char, mail)
	armour_class(char)          # derived — never stored
"""

from __future__ import annotations

import math

from TopKit import Imprint, Pre, Report, Tag


def copper(
		gold: float,
		) -> float:
	"""
	Round a purse DOWN to the copper piece (1/100 gold).

	Always down: a merchant does not round in the customer's favour, and
	floating-point crumbs must never invent a coin that is not there.

	The epsilon is doing real work. ``0.29 * 100`` is 28.999999999999996 in
	binary floating point, so a bare floor() would DESTROY a copper on
	perfectly ordinary amounts. Nudging by a millionth of a cent lands such
	values on the integer they were always meant to be, while a genuine
	fraction (12.999 gp) still floors down to 12.99.
	"""
	return math.floor(
			float(
					gold
					) * 100 + 1e-6
			) / 100


# ---------------------------------------------------------------------------
# The generic Item
# ---------------------------------------------------------------------------


class Item:
	"""A thing with a price. Tags supply every other meaning."""

	def __init__(
			item,
			name: str = "",
			value: float = 0,
			weight: float = 0,
			quantity: int = 1,
			description: str = "",
			):
		# A Club stays a Club. Crafting does not rename a thing — it earns it
		# a TITLE, exactly as a Character keeps their name and gains one.
		# `name` is identity (catalogue lookups match on it); `title` is what
		# this particular specimen came to be called.
		item.name = name
		item.title = ""
		item.value = value
		item.weight = weight
		item.quantity = quantity
		item.description = description
		# Which ability swings this, when it is not the ordinary Str/Dex rule.
		# Lives on the base Item so ``blurb`` can read it unconditionally.
		item.attack_with = ""
		# Filled by Tag Imprints; read by the derived-stat helpers.
		item.grants: dict[str, int] = {}

	@property
	def called(item) -> str:
		"""What to show a reader: the earned title, else the plain name."""
		return item.title or item.name

	@property
	def total_value(item) -> float:
		return item.value * item.quantity

	@property
	def total_weight(item) -> float:
		return item.weight * item.quantity

	def blurb(item) -> str:
		"""
		What this thing DOES, then what it is.

		Armour states its base and how much Dexterity it lets through — the
		same courtesy a weapon does with its damage — so a reader can see
		where a number came from instead of a bare total.
		"""
		parts: list[str] = []

		if item in Armour:
			line = f"AC {item.base_ac}"
			if item.dex_cap is None:
				line += " + Dex"
			elif item.dex_cap > 0:
				line += f" + Dex (max +{item.dex_cap})"
			parts.append(
					f"{line}, {item.armour_kind} armour"
					)
		elif item in Shield:
			parts.append(
					f"+{item.shield_bonus} AC"
					)
		elif item in Weapon:
			line = f"{item.damage} {item.damage_type}"
			if item.properties:
				line += ", " + ", ".join(
						item.properties
						)
			parts.append(
					line
					)
			# Which ability swings it. Said plainly, because a weapon that
			# quietly used a different score would be a trap on the sheet.
			if item.attack_with:
				parts.append(
						f"Attacks with {item.attack_with}"
						)
			if item.mastery:
				parts.append(
						f"Mastery: {item.mastery}"
						)

		if item.grants:
			parts.append(
					", ".join(
							f"{value:+} {key}"
							for key, value in sorted(
									item.grants.items()
									)
							)
					)

		if item.description:
			parts.append(
					item.description
					)

		return ". ".join(
				part.rstrip(".")
				for part in parts
				if part
				) + ("." if parts else "")

	def __str__(item) -> str:
		from AtlasVenustas import Entry
		return Entry(
				item.called,
				item.blurb(),
				)

	def __repr__(item) -> str:
		return (
			f"{item.called} "
			f"({item.value} gp, {item.weight} lb"
			f"{f', x{item.quantity}' if item.quantity != 1 else ''})"
			)


# ---------------------------------------------------------------------------
# Tag vocabulary — what an Item can BE
# ---------------------------------------------------------------------------


class Gear(Tag):
	"""Root of everything an adventurer can own."""

	NAME = "Gear"

	@Pre
	def Item_Only(
			target,
			):
		return isinstance(
				target,
				Item,
				)


class Wearable(Gear):
	"""Worn on the body — armour, cloaks, rings."""

	NAME = "Wearable"


class Wieldable(Gear):
	"""Held in a hand — weapons, shields, focuses."""

	NAME = "Wieldable"


class Armour(Wearable):
	"""Worn on the body — the "Wearing" slot. Carries BASE_AC and DEX_CAP."""

	NAME = "Armour"


class Headwear(Wearable):
	"""Hats, helms, circlets, crowns."""

	NAME = "Headwear"


class Footwear(Wearable):
	"""Boots, sandals, greaves."""

	NAME = "Footwear"


class Cloak(Wearable):
	"""Capes, cloaks, mantles."""

	NAME = "Cloak"


class Handwear(Wearable):
	"""Gauntlets, gloves, bracers, bracelets."""

	NAME = "Handwear"


class Jewelry(Wearable):
	"""Rings, amulets, brooches — several may be worn at once."""

	NAME = "Jewelry"


class Shield(Wieldable):
	"""Held defence — stacks with armour."""

	NAME = "Shield"


class Weapon(Wieldable):
	"""Deals damage. Carries damage and mastery through Build_Weapon."""

	NAME = "Weapon"


class Simple(Gear):
	NAME = "Simple"


class Martial(Gear):
	NAME = "Martial"


class Melee(Gear):
	NAME = "Melee"


class Ranged(Gear):
	NAME = "Ranged"


class Magical(Gear):
	"""Grants something beyond its mundane use — summed, never written."""

	NAME = "Magical"


class Consumable(Gear):
	"""
	Spent when used — potions, scrolls, ammunition, rations.

	Exempt from the one-of-a-kind rule: carrying four Potions of Healing is
	the point, not a duplication bug.
	"""

	NAME = "Consumable"


class Firearm(Weapon):
	"""DMG-optional gunpowder weapons — excluded from plain Martial proficiency."""

	NAME = "Firearm"


class Equipped(Gear):
	"""In use right now. Only what can be worn or wielded may be equipped."""

	NAME = "Equipped"

	@Pre
	def Wearable_Or_Wieldable(
			target,
			):
		return (
			target in Wearable
			or target in Wieldable
			)


class Carried(Gear):
	"""
	At hand — on the belt, the back, the bandolier. Not in use, but
	reachable. The three tiers (in use / at hand / in the bag) partition
	what a hero owns; ``equip`` and ``carry`` each strip the other.
	"""

	NAME = "Carried"


_ARMOUR_KINDS = (
		"Light",
		"Medium",
		"Heavy",
		)


# ---------------------------------------------------------------------------
# Builders — the single construction point per kind of gear
# ---------------------------------------------------------------------------


def Build_Item(
		*,
		name: str,
		value: float = 0,
		weight: float = 0,
		quantity: int = 1,
		description: str = "",
		grants: dict[str, int] | None = None,
		tags: tuple[type[Tag], ...] = (),
		) -> Item:
	"""Craft one Item and stamp the Tags that give it meaning."""
	if not name or not name.strip():
		raise ValueError(
				"Build_Item: name is required."
				)

	item = Item(
			name=name,
			value=value,
			weight=weight,
			quantity=quantity,
			description=description,
			)

	if grants:
		item.grants = dict(
				grants
				)
		Magical(
				item
				)

	for tag in tags:
		if item not in tag:
			tag(
					item
					)

	return item


def Build_Armour(
		*,
		name: str,
		base_ac: int,
		kind: str = "Light",
		value: float = 0,
		weight: float = 0,
		description: str = "",
		grants: dict[str, int] | None = None,
		str_requirement: int = 0,
		stealth_disadvantage: bool = False,
		) -> Item:
	"""Craft armour. ``kind`` is Light / Medium / Heavy and sets the DEX cap.

	``str_requirement``/``stealth_disadvantage`` are recorded on the record —
	a later quest enforces them (Speed penalty, Stealth checks); Quest 1 only
	needs the data to exist and be queryable.
	"""
	if kind not in _ARMOUR_KINDS:
		raise ValueError(
				f"Build_Armour: kind must be one of {_ARMOUR_KINDS}, got {kind!r}."
				)

	item = Build_Item(
			name=name,
			value=value,
			weight=weight,
			description=description,
			grants=grants,
			tags=(
					Armour,
					),
			)
	item.base_ac = base_ac
	item.armour_kind = kind
	item.str_requirement = str_requirement
	item.stealth_disadvantage = stealth_disadvantage
	# Light armour adds all of Dexterity, Medium caps it, Heavy ignores it.
	item.dex_cap = (
			None
			if kind == "Light"
			else (
				2
				if kind == "Medium"
				else 0
				)
			)
	return item


def Build_Shield(
		*,
		name: str = "Shield",
		bonus: int = 2,
		value: float = 10,
		weight: float = 6,
		description: str = "",
		grants: dict[str, int] | None = None,
		) -> Item:
	"""Craft a shield. Its bonus is a grant, so it is summed like any other."""
	item = Build_Item(
			name=name,
			value=value,
			weight=weight,
			description=description,
			grants=grants,
			tags=(
					Shield,
					),
			)
	item.shield_bonus = bonus
	return item


def Build_Worn(
		*,
		name: str,
		slot: type[Tag],
		value: float = 0,
		weight: float = 0,
		description: str = "",
		grants: dict[str, int] | None = None,
		) -> Item:
	"""
	Craft something worn in a non-armour slot: hat, boots, cape, gloves, ring.

	``slot`` is one of ``Headwear``/``Footwear``/``Cloak``/``Handwear``/
	``Jewelry``. Whatever it grants is summed live, never written onto the
	Character — take the cloak off and its bonus leaves with it.
	"""
	if slot not in (
			Headwear,
			Footwear,
			Cloak,
			Handwear,
			Jewelry,
			):
		raise ValueError(
				f"Build_Worn: {slot!r} is not a wearable slot."
				)

	return Build_Item(
			name=name,
			value=value,
			weight=weight,
			description=description,
			grants=grants,
			tags=(
					slot,
					),
			)


def Build_Consumable(
		*,
		name: str,
		value: float = 0,
		weight: float = 0,
		quantity: int = 1,
		description: str = "",
		) -> Item:
	"""Craft a potion, scroll, or other one-use good. Stacks freely."""
	return Build_Item(
			name=name,
			value=value,
			weight=weight,
			quantity=quantity,
			description=description,
			tags=(
					Consumable,
					),
			)


def Build_Weapon(
		*,
		name: str,
		damage: str,
		damage_type: str = "Bludgeoning",
		category: str = "Simple",
		reach: str = "Melee",
		mastery: str = "",
		properties: tuple[str, ...] = (),
		value: float = 0,
		weight: float = 0,
		description: str = "",
		grants: dict[str, int] | None = None,
		attack_with: str = "",
		) -> Item:
	"""Craft a weapon. ``category`` gates proficiency, ``mastery`` its property.

	``category="Firearm"`` tags ``Firearm`` instead of the plain ``Weapon`` —
	Firearm IS-A Weapon (Tag inheritance), so ``item in Weapon`` still holds,
	but a Martial-proficient character does not get firearms for free.

	``attack_with`` names the ability this weapon attacks with when it is
	NOT the usual Strength/Dexterity rule.
	"""
	tags: list[type[Tag]] = [
			Firearm
			if category == "Firearm"
			else Weapon,
			]
	tags.append(
			Simple
			if category == "Simple"
			else Martial
			)
	tags.append(
			Ranged
			if reach == "Ranged"
			else Melee
			)

	item = Build_Item(
			name=name,
			value=value,
			weight=weight,
			description=description,
			grants=grants,
			tags=tuple(
					tags
					),
			)
	item.damage = damage
	item.damage_type = damage_type
	item.category = category
	item.reach = reach
	item.mastery = mastery
	item.attack_with = attack_with
	item.properties = tuple(
			properties
			)
	return item


# ---------------------------------------------------------------------------
# Owning, equipping, selling
# ---------------------------------------------------------------------------


def gear_tags(
		item: Item,
		) -> tuple[type[Tag], ...]:
	"""Every Gear Tag this Item currently carries (Equipped excluded).

	Walks the Gear subtree rather than a hand-kept list, so a new Tag is
	picked up automatically.
	"""
	found: list[type[Tag]] = []
	frontier = [
			Gear,
			]

	while frontier:
		tag = frontier.pop()
		frontier.extend(
				tag.__subclasses__()
				)
		if tag is Equipped or tag is Gear:
			continue
		if item in tag and tag not in found:
			found.append(
					tag
					)

	return tuple(
			found
			)


def instantiate(
		prototype: Item,
		quantity: int | None = None,
		) -> Item:
	"""
	Mint an independent copy of a Ledger prototype.

	Ledger entries are shared module-level objects. ``Equipped`` is a Tag on
	the object itself, so handing the same prototype to two characters would
	let one character's sale un-equip the other's gear. Everything issued to
	a character therefore goes through here first. The copy starts unequipped.
	"""
	fresh = Item(
			name=prototype.name,
			value=prototype.value,
			weight=prototype.weight,
			quantity=(
				prototype.quantity
				if quantity is None
				else quantity
				),
			description=prototype.description,
			)

	for field, value in prototype.__dict__.items():
		if field in (
				"_TOPKIT_STATE",
					#-- TopKit's own state: each copy must start its own.
					#-- (TagKit 0.2.0a1 called it _TAGKIT_STATE; the old name
					#-- silently shared one state between all copies.)
				"name",
				"value",
				"weight",
				"quantity",
				"description",
				"grants",
				):
			continue
		setattr(
				fresh,
				field,
				value,
				)

	# A clone keeps the original's name AND any title it earned.
	fresh.name = prototype.name
	fresh.title = prototype.title

	fresh.grants = dict(
			prototype.grants
			)

	for tag in gear_tags(
			prototype
			):
		if fresh not in tag:
			tag(
					fresh
					)

	return fresh


def _belongings(
		char,
		) -> list[Item]:
	belongings = getattr(
			char,
			"belongings",
			None,
			)
	if belongings is None:
		belongings = []
		char.belongings = belongings
	return belongings


def owned(
		char,
		) -> list[Item]:
	"""Everything the character carries, equipped or not."""
	return list(
			_belongings(
					char
					)
			)


def equipped(
		char,
		tag: type[Tag] | None = None,
		) -> list[Item]:
	"""Items currently in use, optionally narrowed to a Tag (Armour, Weapon…)."""
	return [
			item
			for item in _belongings(
					char
					)
			if item in Equipped
			and (
				tag is None
				or item in tag
				)
			]


def carried(
		char,
		) -> list[Item]:
	"""Everything not currently in use — at hand and in the bag alike."""
	return [
			item
			for item in _belongings(
					char
					)
			if item not in Equipped
			]


def carrying(
		char,
		tag: type[Tag] | None = None,
		) -> list[Item]:
	"""At hand: on the belt or the back, one swap from being in use."""
	return [
			item
			for item in _belongings(
					char
					)
			if item in Carried
			and item not in Equipped
			and (
				tag is None
				or item in tag
				)
			]


def bagged(
		char,
		) -> list[Item]:
	"""The pack proper — owned, not in use, and not at hand either."""
	return [
			item
			for item in _belongings(
					char
					)
			if item not in Equipped
			and item not in Carried
			]


def acquire(
		char,
		item: Item,
		) -> Item:
	"""Take ownership without paying (loot, a gift, a starting kit)."""
	belongings = _belongings(
			char
			)
	if item not in belongings:
		belongings.append(
				item
				)
	return item


def buy(
		char,
		item: Item,
		) -> bool:
	"""Purchase into the bag. Returns False when it cannot be afforded."""
	purse = getattr(
			char,
			"purse",
			0,
			)
	if item.total_value > purse:
		return False

	char.purse = copper(
			purse - item.total_value
			)
	acquire(
			char,
			item,
			)
	return True


def issue(
		char,
		prototype: Item,
		quantity: int | None = None,
		) -> Item:
	"""Give the character a fresh copy of a Ledger prototype, free of charge."""
	return acquire(
			char,
			instantiate(
					prototype,
					quantity,
					),
			)


def purchase(
		char,
		prototype: Item,
		quantity: int | None = None,
		) -> Item | None:
	"""Buy a fresh copy of a Ledger prototype. Returns None if unaffordable."""
	item = instantiate(
			prototype,
			quantity,
			)
	if not buy(
			char,
			item,
			):
		return None
	return item


def sell(
		char,
		item: Item,
		) -> bool:
	"""Sell an owned item back into the purse and drop it from the ledger."""
	belongings = _belongings(
			char
			)
	if item not in belongings:
		return False

	belongings.remove(
			item
			)
	char.purse = copper(
			getattr(
					char,
					"purse",
					0,
					) + item.total_value
			)
	return True


def equip(
		char,
		item: Item,
		) -> Item:
	"""Put an owned item into use. Acquires it first when it is not owned."""
	acquire(
			char,
			item,
			)
	if item in Carried:
		del Carried[
				item
				]
	if item not in Equipped:
		Equipped(
				item
				)
	return item


def unequip(
		item: Item,
		) -> Item:
	"""Stop using an item. It stays owned, in the bag."""
	if item in Equipped:
		del Equipped[
				item
				]
	return item


def carry(
		char,
		item: Item,
		) -> Item:
	"""Sling an owned item within reach. Acquires it first when not owned."""
	acquire(
			char,
			item,
			)
	if item in Equipped:
		del Equipped[
				item
				]
	if item not in Carried:
		Carried(
				item
				)
	return item


def stow(
		item: Item,
		) -> Item:
	"""Put an at-hand item away into the pack. It stays owned."""
	if item in Carried:
		del Carried[
				item
				]
	return item


# ---------------------------------------------------------------------------
# Derived stats — read-time sums, so nothing overwrites natural defences
# ---------------------------------------------------------------------------


def grant_total(
		char,
		key: str,
		) -> int:
	"""Sum one kind of grant across everything currently equipped."""
	return sum(
			int(
					item.grants.get(
							key,
							0,
							)
					)
			for item in equipped(
					char
					)
			)


def worn_armour(
		char,
		) -> Item | None:
	"""The armour in use, if any."""
	worn = equipped(
			char,
			Armour,
			)
	return worn[0] if worn else None


def held_shield(
		char,
		) -> Item | None:
	shields = equipped(
			char,
			Shield,
			)
	return shields[0] if shields else None


def _modifier(
		score: int,
		) -> int:
	return (
		int(
				score
				) - 10
		) // 2


def armour_class(
		char,
		unarmoured: int | None = None,
		) -> int:
	"""
	Derive AC. Never stored, so artifacts and armour can come and go freely.

	``unarmoured`` is the character's own no-armour formula (Unarmored Defence
	or plain 10 + Dexterity); the best of it and the worn armour wins, then
	shields and magical grants are added.
	"""
	dexterity = _modifier(
			getattr(
					getattr(
							char,
							"AS",
							None,
							),
					"DEX",
					10,
					)
			)

	if unarmoured is None:
		unarmoured = 10 + dexterity

	armour = worn_armour(
			char
			)
	if armour is None:
		base = unarmoured
	else:
		cap = armour.dex_cap
		allowed = (
				dexterity
				if cap is None
				else min(
						dexterity,
						cap,
						)
				)
		base = max(
				armour.base_ac + allowed,
				unarmoured,
				)

	shield = held_shield(
			char
			)
	if shield is not None:
		base += shield.shield_bonus

	return base + grant_total(
			char,
			"AC",
			)


# ---------------------------------------------------------------------------
# Reconciliation — the question Tags let us ask, and the repair
# ---------------------------------------------------------------------------


# How many of each slot a body can use at once. Jewelry is the odd one:
# rings and an amulet coexist, so it is not a one-of-a-kind slot.
SLOTS: tuple[tuple[type[Tag], int], ...] = (
		(Armour, 1),
		(Shield, 1),
		(Headwear, 1),
		(Footwear, 1),
		(Cloak, 1),
		(Handwear, 1),
		(Jewelry, 3),
		)


# How many items a hero can keep within reach before mastery widens it.
CARRY_BASE = 2


def carry_capacity(
		char,
		) -> int:
	"""
	How many items this hero can keep within reach.

	Weapon Mastery is the one thing that widens it: the drills are
	meaningless if five of the six weapons are at the bottom of a pack.
	"""
	extra = 0
	try:
		from AtlasLusoris.Map_of_Weapon_Masteries import (
				mastery_count,
				)

		extra = int(
				mastery_count(
						char
						) or 0
				)
	except Exception:
		extra = 0

	return CARRY_BASE + max(
			0,
			extra,
			)


def _worth(
		item: Item,
		) -> tuple:
	"""
	How good a piece is, for deciding which one to keep in a full slot.

	Armour counts its class, a shield its bonus, and anything magical the
	weight of what it grants; price breaks the remaining ties.
	"""
	protection = getattr(
			item,
			"base_ac",
			0,
			) or getattr(
			item,
			"shield_bonus",
			0,
			)
	granted = sum(
			abs(
					int(
							value
							)
					)
			for value in item.grants.values()
			)
	return (
			protection,
			granted,
			item.value,
			)


def slot_of(
		item: Item,
		) -> type[Tag] | None:
	"""Which body slot this item occupies, if any."""
	for tag, _capacity in SLOTS:
		if item in tag:
			return tag
	return None


def reconcile(
		char,
		) -> list[Item]:
	"""
	Repair an impossible loadout and return what was sold.

	One body cannot wear two breastplates, two hats, or hold two shields.
	Keep the best piece per slot, sell the rest back into the purse. This is
	only expressible because "equipped" is a Tag we can QUERY rather than a
	slot pointer we would silently overwrite.
	"""
	sold: list[Item] = []

	for tag, capacity in SLOTS:
		in_use = equipped(
				char,
				tag,
				)
		if len(
				in_use
				) <= capacity:
			continue

		in_use.sort(
				key=_worth,
				reverse=True,
				)
		for loser in in_use[capacity:]:
			unequip(
					loser
					)
			sell(
					char,
					loser,
					)
			sold.append(
					loser
					)

	return sold


__all__ = (
		"Armour",
		"Build_Armour",
		"Build_Consumable",
		"Build_Item",
		"Build_Shield",
		"Build_Weapon",
		"Build_Worn",
		"Cloak",
		"Consumable",
		"Carried",
		"CARRY_BASE",
		"Equipped",
		"Firearm",
		"Footwear",
		"Gear",
		"Handwear",
		"Headwear",
		"Item",
		"Jewelry",
		"Magical",
		"Martial",
		"Melee",
		"Ranged",
		"SLOTS",
		"Shield",
		"Simple",
		"Wearable",
		"Weapon",
		"Wieldable",
		"acquire",
		"bagged",
		"buy",
		"carry",
		"carry_capacity",
		"carried",
		"carrying",
		"copper",
		"slot_of",
		"armour_class",
		"equip",
		"equipped",
		"gear_tags",
		"grant_total",
		"held_shield",
		"instantiate",
		"issue",
		"owned",
		"purchase",
		"reconcile",
		"sell",
		"stow",
		"unequip",
		"worn_armour",
		)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def _self_test():
	class Scores:
		DEX = 14
		CON = 16
		WIS = 12

	class Dummy:
		def __init__(self):
			self.AS = Scores()
			self.purse = 500

	# --- generic item, crafted by Tags ---------------------------------
	mail = Build_Armour(
			name="Chain Mail",
			base_ac=16,
			kind="Heavy",
			value=75,
			weight=55,
			description="Interlocking rings over a padded coat.",
			)
	assert mail in Armour and mail in Wearable and mail in Gear
	assert mail not in Weapon
	assert isinstance(
			mail,
			Item,
			)

	leather = Build_Armour(
			name="Leather Armour",
			base_ac=11,
			kind="Light",
			value=10,
			weight=10,
			)
	sword = Build_Weapon(
			name="Longsword",
			damage="1d8",
			damage_type="Slashing",
			category="Martial",
			mastery="Sap",
			value=15,
			weight=3,
			)
	assert sword in Weapon and sword in Martial and sword in Melee
	assert sword not in Simple

	char = Dummy()

	# --- unarmoured AC is the plain formula ----------------------------
	assert armour_class(char) == 12, armour_class(char)

	# --- heavy armour ignores Dexterity --------------------------------
	equip(
			char,
			mail,
			)
	assert armour_class(char) == 16, armour_class(char)

	# --- a shield stacks ------------------------------------------------
	shield = Build_Shield()
	equip(
			char,
			shield,
			)
	assert armour_class(char) == 18, armour_class(char)

	# --- artifacts GRANT, they do not overwrite -------------------------
	cloak = Build_Item(
			name="Cloak of Protection",
			value=200,
			weight=1,
			description="A traveller's cloak that turns a blow aside.",
			grants={
					"AC": 1,
					"saves": 1,
					},
			tags=(
					Wearable,
					),
			)
	equip(
			char,
			cloak,
			)
	assert cloak in Magical
	assert armour_class(char) == 19, armour_class(char)
	assert grant_total(
			char,
			"saves",
			) == 1

	# removing the artifact removes exactly its contribution
	unequip(
			cloak
			)
	assert armour_class(char) == 18, armour_class(char)
	equip(
			char,
			cloak,
			)

	# --- Unarmored Defence beats weak armour without being overwritten --
	monk = Dummy()
	equip(
			monk,
			leather,
			)
	# 10 + DEX(2) + WIS(1) = 13 beats Leather 11 + DEX(2) = 13 -> ties, so
	# raise the monk formula and confirm the natural defence wins.
	assert armour_class(
			monk,
			unarmoured=16,
			) == 16

	# --- two armours equipped: ask the question, repair the answer ------
	before = char.purse
	equip(
			char,
			leather,
			)
	assert len(
			equipped(
					char,
					Armour,
					)
			) == 2
	sold = reconcile(
			char
			)
	assert [
			item.name
			for item in sold
			] == [
			"Leather Armour",
			], sold
	assert len(
			equipped(
					char,
					Armour,
					)
			) == 1
	assert worn_armour(
			char
			).name == "Chain Mail"
	assert char.purse == before + leather.value
	assert leather not in owned(
			char
			)

	# --- bag vs equipped -------------------------------------------------
	rations = Build_Item(
			name="Rations",
			value=1,
			weight=2,
			quantity=5,
			description="Dry food for the road.",
			)
	acquire(
			char,
			rations,
			)
	assert rations in carried(
			char
			)
	assert rations not in equipped(
			char
			)

	# --- buying respects the purse ---------------------------------------
	broke = Dummy()
	broke.purse = 5
	assert buy(
			broke,
			Build_Armour(
					name="Plate",
					base_ac=18,
					kind="Heavy",
					value=1500,
					),
			) is False
	assert owned(
			broke
			) == []

	# --- copper() must never destroy a coin ------------------------------
	# Regression: a bare floor() turned 0.29 into 0.28, because 0.29 * 100
	# is 28.999999999999996 in binary floating point.
	losses = [
			cents / 100
			for cents in range(
					0,
					20000,
					)
			if copper(
					cents / 100
					) != cents / 100
			]
	assert not losses, f"copper() destroyed coins at {losses[:5]}"
	assert copper(12.999) == 12.99, "genuine fractions must still floor down"
	assert copper(0.299) == 0.29

	# --- Ledger prototypes must not alias between characters -------------
	# Regression: Equipped is a Tag on the object, so handing the SAME
	# prototype to two characters let one character's sale un-equip the
	# other's gear. Everything issued goes through instantiate().
	prototype = Build_Armour(
			name="Shared Mail",
			base_ac=16,
			kind="Heavy",
			value=75,
			weight=55,
			)
	alice = Dummy()
	bob = Dummy()
	alice_mail = issue(
			alice,
			prototype,
			)
	bob_mail = issue(
			bob,
			prototype,
			)

	assert alice_mail is not bob_mail
	assert alice_mail is not prototype
	# the copy really is armour, with its record intact
	assert alice_mail in Armour and alice_mail in Wearable
	assert alice_mail.base_ac == 16
	assert alice_mail.dex_cap == 0
	assert alice_mail.armour_kind == "Heavy"
	# a fresh copy starts unequipped
	assert alice_mail not in Equipped

	equip(
			alice,
			alice_mail,
			)
	equip(
			bob,
			bob_mail,
			)
	assert armour_class(
			bob
			) == 16

	unequip(
			alice_mail
			)
	sell(
			alice,
			alice_mail,
			)
	# Bob is untouched by Alice's sale
	assert bob_mail in Equipped, "prototype aliasing regressed"
	assert armour_class(
			bob
			) == 16
	assert bob_mail in owned(
			bob
			)
	assert alice_mail not in owned(
			alice
			)
	# and the prototype itself was never equipped or sold
	assert prototype not in Equipped
	assert prototype not in owned(
			alice
			)

	# --- issue/purchase quantities and purse behaviour -------------------
	stack = issue(
			bob,
			Build_Item(
					name="Arrows",
					value=0.05,
					weight=0.05,
					quantity=1,
					),
			quantity=20,
			)
	assert stack.quantity == 20

	rich = Dummy()
	rich.purse = 100
	bought = purchase(
			rich,
			prototype,
			)
	assert bought is not None and rich.purse == 25
	assert purchase(
			rich,
			prototype,
			) is None, "must refuse when unaffordable"
	assert rich.purse == 25, "a refused purchase must not touch the purse"

	print(
			"OK — Grimoire_of_Items self-test "
			"(generic Item, Tags craft it, grants derived, reconcile repairs, "
			"prototypes never alias)"
			)


if __name__ == "__main__":
	_self_test()
