"""
Grimoire_of_Crafts — affixes that personalise an Item for its Hero.

Thought pattern (read this before the code)
	1. A Craft is a PROPERTY, not an item. "of Defense" is the +1 AC; the
	   Chain Mail is just the thing it is stamped on. Borrowing the shape of
	   modern CRPG affixes: bring the properties across, never the items.
	2. A Craft is a Tag on the Item, so "is this blade warded?" is a question
	   you ask (``blade in Of_Warding``) rather than a flag you maintain.
	3. What a Craft grants is merged into ``item.grants``, which the derived
	   readers already sum at read time. A crafted item therefore needs NO
	   new plumbing: equip it and the bonus appears, sell it and it leaves.
	4. Crafts are gated on the HERO — their level, and the Tags they carry.
	   A Barbarian's fury-craft cannot end up on a Wizard's robe, and a
	   tier-3 craft cannot end up on a level-2 character.
	5. A Craft is declared by pinning it. ``Declared_Craft`` validates what
	   the property grants and where it may land, those answers live on the
	   Tag as Reports, and its Field, ``Declared_Craft[:]``, is the
	   catalogue. Nothing keeps a list beside the declarations.

Usage
	from AtlasInventarium.Grimoire_of_Crafts import forge, crafts_for
	forge(mail, Of_Defense, hero=char)     # -> "Chain Mail of Defense"
	crafts_for(char)                        # every affix this Hero qualifies for
	Declared_Craft[:]                       # every declared affix, in order
"""

from __future__ import annotations

from collections.abc import Callable

from TopKit import Pin, Pre, Record, Tag

from AtlasInventarium.Grimoire_of_Items import (
		Armour,
		Cloak,
		Footwear,
		Gear,
		Handwear,
		Headwear,
		Item,
		Jewelry,
		Magical,
		Shield,
		Weapon,
		)


class Craft(Gear):
	"""Root of every forgeable property."""

	NAME = "Craft"

	@Pre
	def Item_Only(
			target,
			):
		return isinstance(
				target,
				Item,
				)


# Tier -> the Hero level at which the property becomes forgeable.
TIERS: dict[int, int] = {
		1: 1,
		2: 5,
		3: 11,
		4: 17,
		}


def _resolve_tier(
		target,
		tier,
		) -> int:
	"""The tier a declaration asked for, refused when ``TIERS`` has no such row."""
	if (
			isinstance(
					tier,
					bool,
					)
			or tier not in TIERS
			):
		raise ValueError(
				f"Craft {target.NAME!r}: tier must be one of {sorted(TIERS)}, "
				f"got {tier!r}."
				)
	return tier


def _tag_tuple(
		target,
		tags,
		role: str,
		) -> tuple[type[Tag], ...]:
	"""A tuple of Tag classes, refused when anything else is offered."""
	resolved = tuple(
			tags or ()
			)
	for tag in resolved:
		if (
				not isinstance(
						tag,
						type,
						)
				or not issubclass(
						tag,
						Tag,
						)
				):
			raise ValueError(
					f"Craft {target.NAME!r}: {role} must hold Tags, got {tag!r}."
					)
	return resolved


@Pin
class Declared_Craft(Tag):
	"""
	Root Pin for every property the forge knows.

	A Craft is declared by applying this Pin to the Craft Tag. The keyword
	inputs are validated here and land on the Tag as Reports (``GRANTS``,
	``TIER``, ``MIN_LEVEL``, ``AFFIX``, ``APPLIES_TO``, ``REQUIRES``,
	``FORBIDS``), and ``Declared_Craft[:]`` is the catalogue, in declaration
	order. A declaration this Pin refuses never joins the Field.
	"""

	@Pre
	def Craft_Tag_Only(
			target,
			):
		return (
				isinstance(
						target,
						type,
						)
				and issubclass(
						target,
						Craft,
						)
				and target is not Craft
				)

	@Record
	def GRANTS(
			target,
			*,
			grants=None,
			) -> dict[str, int]:
		if not grants:
			raise ValueError(
					f"Craft {target.NAME!r} must grant something."
					)
		return dict(
				grants
				)

	@Record
	def TIER(
			target,
			*,
			tier=1,
			) -> int:
		return _resolve_tier(
				target,
				tier,
				)

	@Record
	def MIN_LEVEL(
			target,
			*,
			tier=1,
			) -> int:
		return TIERS[
				_resolve_tier(
						target,
						tier,
						)
				]

	@Record
	def AFFIX(
			target,
			*,
			affix="suffix",
			) -> str:
		if affix not in (
				"prefix",
				"suffix",
				):
			raise ValueError(
					f"Craft {target.NAME!r}: affix must be 'prefix' or 'suffix', "
					f"got {affix!r}."
					)
		return affix

	@Record
	def APPLIES_TO(
			target,
			*,
			applies_to=(),
			) -> tuple[type[Tag], ...]:
		return _tag_tuple(
				target,
				applies_to,
				"applies_to",
				)

	@Record
	def REQUIRES(
			target,
			*,
			requires=(),
			) -> tuple[type[Tag], ...]:
		return _tag_tuple(
				target,
				requires,
				"requires",
				)

	@Record
	def FORBIDS(
			target,
			*,
			forbids=(),
			) -> tuple[type[Tag], ...]:
		return _tag_tuple(
				target,
				forbids,
				"forbids",
				)


def _class_name(
		name: str,
		) -> str:
	return "".join(
			part.capitalize()
			for part in name.replace(
					"-",
					" ",
					).replace(
					"'",
					"",
					).split()
			)


def Make_Craft(
		*,
		name: str,
		grants: dict[str, int],
		tier: int = 1,
		affix: str = "suffix",
		applies_to: tuple[type[Tag], ...] = (),
		requires: tuple[type[Tag], ...] = (),
		forbids: tuple[type[Tag], ...] = (),
		description: str = "",
		) -> type[Craft]:
	"""
	Declare one forgeable property.

	``applies_to``  — the Item Tags that can carry it (a blade-craft belongs
	                  on a Weapon, not on boots). Empty means anything.
	``requires``    — Hero Tags the wearer must have. This is how a Guild's
	                  identity reaches its gear.
	``forbids``     — Hero Tags that rule it out.
	``tier``        — 1/2/3/4, resolved against ``TIERS`` for a level gate.

	The Tag is built with only its identity and its prose; everything the
	forge gates on is handed to ``Declared_Craft``, which validates it and
	lands it on the Tag as Reports. A declaration the Pin refuses raises here
	and never joins the catalogue.
	"""
	if not name or not name.strip():
		raise ValueError(
				"Make_Craft: name is required."
				)

	namespace = {
			"NAME": name,
			"DESCRIPTION": description,
			"__module__": __name__,
			}

	craft = type(
			_class_name(
					name
					),
			(
					Craft,
					),
			namespace,
			)
	Declared_Craft(
			craft,
			grants=grants,
			tier=tier,
			affix=affix,
			applies_to=applies_to,
			requires=requires,
			forbids=forbids,
			)
	return craft


# ---------------------------------------------------------------------------
# Eligibility
# ---------------------------------------------------------------------------


def suits_item(
		item: Item,
		craft: type[Craft],
		) -> bool:
	"""Can this property live on this kind of thing?"""
	applies = craft.APPLIES_TO
	if not applies:
		return True
	return any(
			item in tag
			for tag in applies
			)


def suits_hero(
		hero,
		craft: type[Craft],
		) -> bool:
	"""Is the Hero deep enough, and of the right kind, for this property?"""
	if hero is None:
		return True

	level = int(
			getattr(
					hero,
					"level",
					1,
					) or 1
			)
	if level < craft.MIN_LEVEL:
		return False

	for tag in craft.REQUIRES:
		if hero not in tag:
			return False
	for tag in craft.FORBIDS:
		if hero in tag:
			return False

	return True


def crafts_for(
		hero,
		item: Item | None = None,
		) -> tuple[type[Craft], ...]:
	"""Every property this Hero qualifies for, optionally for one Item."""
	return tuple(
			craft
			for craft in Declared_Craft[:]
			if suits_hero(
					hero,
					craft,
					)
			and (
				item is None
				or suits_item(
						item,
						craft,
						)
				)
			)


# ---------------------------------------------------------------------------
# Forging
# ---------------------------------------------------------------------------


def craft_name(
		base: str,
		craft: type[Craft],
		) -> str:
	if craft.AFFIX == "prefix":
		return f"{craft.NAME} {base}"
	return f"{base} {craft.NAME}"


def forge(
		item: Item,
		craft: type[Craft],
		hero=None,
		) -> Item:
	"""
	Stamp a property onto an Item, merging what it grants.

	The Tag is purely semantic — the grant merge happens HERE, deliberately,
	exactly once. (An Imprint would re-run when the item is cloned for
	another owner and silently double the bonus.)

	Raises when the property does not suit the item or the Hero: a refusal
	is a bug worth seeing, not something to swallow.
	"""
	if not suits_item(
			item,
			craft,
			):
		raise ValueError(
				f"forge: {craft.NAME!r} does not belong on {item.name!r}."
				)
	if not suits_hero(
			hero,
			craft,
			):
		raise ValueError(
				f"forge: {craft.NAME!r} is beyond this hero "
				f"(needs level {craft.MIN_LEVEL})."
				)
	if item in craft:
		return item

	craft(
			item
			)
	if item not in Magical:
		Magical(
				item
				)

	for key, value in craft.GRANTS.items():
		item.grants[key] = item.grants.get(
				key,
				0,
				) + value

	# A crafted Club is still a Club — it has simply earned a title. `name`
	# is never touched, so catalogue lookups keep recognising it.
	item.title = craft_name(
			item.title or item.name,
			craft,
			)
	# Crafted goods are worth more than their plain kin.
	item.value = round(
			item.value + 100 * craft.TIER,
			2,
			)
	return item


def crafts_on(
		item: Item,
		) -> tuple[type[Craft], ...]:
	"""Which properties this Item carries."""
	return tuple(
			craft
			for craft in Declared_Craft[:]
			if item in craft
			)


# ---------------------------------------------------------------------------
# The starting catalogue — properties, not items
# ---------------------------------------------------------------------------

_ARMOUR_LIKE = (
		Armour,
		Shield,
		Cloak,
		Headwear,
		Footwear,
		Handwear,
		Jewelry,
		)


Of_Defense = Make_Craft(
		name="of Defense",
		grants={
				"AC": 1,
				},
		tier=1,
		applies_to=_ARMOUR_LIKE,
		description="The piece turns a blow that should have landed.",
		)

Of_Warding = Make_Craft(
		name="of Warding",
		grants={
				"saves": 1,
				},
		tier=1,
		applies_to=_ARMOUR_LIKE,
		description="Ill fortune slides off the wearer.",
		)

Of_Precision = Make_Craft(
		name="of Precision",
		grants={
				"attack": 1,
				},
		tier=1,
		applies_to=(
				Weapon,
				),
		description="The weapon finds the gap by itself.",
		)

Of_Wounding = Make_Craft(
		name="of Wounding",
		grants={
				"damage": 1,
				},
		tier=1,
		applies_to=(
				Weapon,
				),
		description="Its edge bites deeper than the wound suggests.",
		)

Of_the_Bear = Make_Craft(
		name="of the Bear",
		grants={
				"HP": 5,
				},
		tier=2,
		applies_to=_ARMOUR_LIKE,
		description="The wearer endures well past the point of sense.",
		)

Of_Swiftness = Make_Craft(
		name="of Swiftness",
		grants={
				"speed": 5,
				},
		tier=2,
		applies_to=(
				Footwear,
				Cloak,
				),
		description="The ground gives a little more with every stride.",
		)

Of_Vigilance = Make_Craft(
		name="of Vigilance",
		grants={
				"initiative": 2,
				},
		tier=2,
		applies_to=_ARMOUR_LIKE,
		description="The wearer is already moving when the ambush starts.",
		)

Of_the_Aegis = Make_Craft(
		name="of the Aegis",
		grants={
				"AC": 2,
				},
		tier=3,
		applies_to=_ARMOUR_LIKE,
		description="A hush of force gathers wherever a strike would fall.",
		)

Of_Ruin = Make_Craft(
		name="of Ruin",
		grants={
				"attack": 2,
				"damage": 2,
				},
		tier=3,
		applies_to=(
				Weapon,
				),
		description="What it strikes tends not to be repaired.",
		)

Of_the_Paragon = Make_Craft(
		name="of the Paragon",
		grants={
				"AC": 3,
				"saves": 2,
				},
		tier=4,
		applies_to=_ARMOUR_LIKE,
		description="Legends accrete to whoever carries this.",
		)


#-- A snapshot of the Field, read once at import. Read ``Declared_Craft[:]``
#-- for a live view after later declarations.
CRAFTS: tuple[type[Craft], ...] = tuple(
		Declared_Craft[:]
		)

CRAFTS_BY_NAME: dict[str, type[Craft]] = {
		craft.NAME: craft
		for craft in CRAFTS
		}


__all__ = (
		"CRAFTS",
		"CRAFTS_BY_NAME",
		"Make_Craft",
		"Craft",
		"Declared_Craft",
		"TIERS",
		"craft_name",
		"crafts_for",
		"crafts_on",
		"forge",
		"suits_hero",
		"suits_item",
		)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def _self_test():
	from AtlasInventarium.Grimoire_of_Items import (
			Make_Armour,
			Make_Weapon,
			Make_Worn,
			armour_class,
			equip,
			grant_total,
			instantiate,
			unequip,
			)
	from TopKit import TagCompositionError

	class Scores:
		DEX = 14

	class Hero:
		def __init__(
				self,
				level,
				):
			self.AS = Scores()
			self.purse = 1000
			self.level = level

	# --- the catalogue is the Pin's Field, in declaration order ----------
	catalogue = (
			Of_Defense,
			Of_Warding,
			Of_Precision,
			Of_Wounding,
			Of_the_Bear,
			Of_Swiftness,
			Of_Vigilance,
			Of_the_Aegis,
			Of_Ruin,
			Of_the_Paragon,
			)
	assert tuple(
			Declared_Craft[:]
			) == catalogue, "the Field must hold every declared Craft, in order"
	assert all(
			craft in Declared_Craft
			for craft in catalogue
			)
	assert CRAFTS == catalogue
	assert CRAFTS_BY_NAME == {
			craft.NAME: craft
			for craft in catalogue
			}

	# --- what a declaration asked for lands on the Tag as Reports --------
	assert Of_Defense.GRANTS == {
			"AC": 1,
			}
	assert Of_Defense.TIER == 1
	assert Of_Defense.MIN_LEVEL == 1
	assert Of_Defense.AFFIX == "suffix"
	assert Of_Defense.APPLIES_TO == _ARMOUR_LIKE
	assert Of_Defense.REQUIRES == ()
	assert Of_Defense.FORBIDS == ()
	assert Of_Ruin.GRANTS == {
			"attack": 2,
			"damage": 2,
			}
	assert Of_Ruin.APPLIES_TO == (
			Weapon,
			)
	assert Of_the_Paragon.TIER == 4
	assert Of_the_Paragon.MIN_LEVEL == TIERS[4] == 17
	assert Of_Defense.DESCRIPTION, "the prose stays on the Tag itself"

	# --- a refused declaration never joins the Field ---------------------
	for refused in (
			dict(
					name="of Nothing",
					grants={},
					),
			dict(
					name="of the Fifth Tier",
					grants={
							"AC": 1,
							},
					tier=5,
					),
			dict(
					name="of Sideways",
					grants={
							"AC": 1,
							},
					affix="infix",
					),
			dict(
					name="of Boots",
					grants={
							"AC": 1,
							},
					applies_to=(
							"Boots",
							),
					),
			):
		try:
			Make_Craft(
					**refused
					)
			raise AssertionError(
					f"the Pin must refuse {refused['name']!r}"
					)
		except TagCompositionError:
			pass
	assert tuple(
			Declared_Craft[:]
			) == catalogue, "a refused Craft must not join the Field"

	# --- a craft is a property, summed live ------------------------------
	novice = Hero(
			1
			)
	mail = Make_Armour(
			name="Chain Mail",
			base_ac=16,
			kind="Heavy",
			value=75,
			)
	equip(
			novice,
			mail,
			)
	assert armour_class(
			novice
			) == 16

	forge(
			mail,
			Of_Defense,
			hero=novice,
			)
	# The thing keeps its name and earns a title — identity is never rewritten.
	assert mail.name == "Chain Mail", mail.name
	assert mail.title == "Chain Mail of Defense", mail.title
	assert mail.called == "Chain Mail of Defense"
	assert mail in Of_Defense and mail in Craft and mail in Magical
	assert armour_class(
			novice
			) == 17, "the craft must raise AC with no new plumbing"

	# --- crafts stack, and each is queryable -----------------------------
	forge(
			mail,
			Of_Warding,
			hero=novice,
			)
	assert mail.name == "Chain Mail", "name is identity; it never accretes"
	assert mail.title == "Chain Mail of Defense of Warding", mail.title
	assert grant_total(
			novice,
			"saves",
			) == 1
	assert {
			craft.NAME
			for craft in crafts_on(
					mail
					)
			} == {
			"of Defense",
			"of Warding",
			}

	# --- forging twice is a no-op, not a double bonus --------------------
	forge(
			mail,
			Of_Defense,
			hero=novice,
			)
	assert armour_class(
			novice
			) == 17, "re-forging must not stack with itself"

	# --- taking it off removes exactly the craft's contribution ----------
	unequip(
			mail
			)
	assert armour_class(
			novice
			) == 12, "10 + DEX once the crafted mail is off"

	# --- level gates -----------------------------------------------------
	try:
		forge(
				Make_Armour(
						name="Plate",
						base_ac=18,
						kind="Heavy",
						),
				Of_the_Paragon,
				hero=novice,
				)
		raise AssertionError(
				"a level-1 hero must not receive a tier-4 craft"
				)
	except ValueError:
		pass

	veteran = Hero(
			17
			)
	assert Of_the_Paragon in crafts_for(
			veteran
			)
	assert Of_the_Paragon not in crafts_for(
			novice
			)
	assert Of_Defense in crafts_for(
			novice
			)

	# --- item-kind gates -------------------------------------------------
	boots = Make_Worn(
			name="Boots",
			slot=Footwear,
			value=5,
			)
	try:
		forge(
				boots,
				Of_Precision,
				hero=veteran,
				)
		raise AssertionError(
				"a weapon-craft must not land on boots"
				)
	except ValueError:
		pass

	forge(
			boots,
			Of_Swiftness,
			hero=veteran,
			)
	assert boots.name == "Boots"
	assert boots.title == "Boots of Swiftness"

	blade = Make_Weapon(
			name="Longsword",
			damage="1d8",
			category="Martial",
			value=15,
			)
	forge(
			blade,
			Of_Ruin,
			hero=veteran,
			)
	assert blade.grants == {
			"attack": 2,
			"damage": 2,
			}

	# --- a crafted item clones correctly for another owner ---------------
	copy = instantiate(
			blade
			)
	assert copy is not blade
	assert copy.name == blade.name
	assert copy.title == blade.title, "an earned title must survive cloning"
	assert copy in Of_Ruin, "the craft must survive cloning"
	assert copy.grants == blade.grants, "grants must not double on clone"

	# --- crafts_for narrows by item too ----------------------------------
	for craft in crafts_for(
			veteran,
			blade,
			):
		assert suits_item(
				blade,
				craft,
				)

	# --- the accessors read the Field and answer as the list did ---------
	assert crafts_for(
			novice
			) == (
			Of_Defense,
			Of_Warding,
			Of_Precision,
			Of_Wounding,
			)
	assert crafts_for(
			veteran
			) == catalogue
	assert crafts_for(
			veteran,
			blade,
			) == (
			Of_Precision,
			Of_Wounding,
			Of_Ruin,
			)
	assert crafts_on(
			mail
			) == (
			Of_Defense,
			Of_Warding,
			)
	assert crafts_on(
			blade
			) == (
			Of_Ruin,
			)

	print(
			f"OK — Grimoire_of_Crafts self-test ({len(Declared_Craft[:])} crafts; "
			"properties stamped as Tags, granted live, gated by level and hero)"
			)


if __name__ == "__main__":
	_self_test()
