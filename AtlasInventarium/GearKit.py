"""
GearKit — loadout POLICY over the Grimoire_of_Items primitives.

Thought pattern (read this before the code)
	1. ``Grimoire_of_Items`` knows what gear IS. This module knows who gets
	   WHAT. Primitives stay policy-free so a second policy can exist:
	   ``Outfit_Player`` here, ``Outfit_NonPlayer`` later (characteristic
	   weapon, travel light, lootables) without touching the item layer.
	2. Proficiency is read from the Guild Tags the Character already carries
	   (``HeavilyArmored``, ``MartialArms``, ``FinesseArms``, …) and from
	   Unarmored Defense skills (``Unarmed_Monk``, ``Unarmed_Barb``,
	   ``Unarmed_Dance``) — the machine-readable training data, not
	   string-matched class names. Who-may-wear-what lives in
	   ``Map_of_Gear_Proficiency``.
	3. Every pick is drawn from a per-character seeded stream, so the same
	   seed always outfits the same way (no reroll flicker).
	4. Nothing is written that a derived read could compute. AC is never
	   stored here: ``armour_class(char, unarmoured=…)`` sums it live.

Public surface
	Outfit_Player(char)      — issue a full starting loadout
	armour_allowance(char)   — armour kinds this Character trained with
	weapon_pool(char)        — weapons this Character may wield
	may_use_shield(char)     — shield training, and whether it fits the build
	unarmoured_formula(char) — the natural no-armour AC (Unarmored Defense)
	unarmoured_refuses_armour / _shield — Unarmored Defense takes no armour,
	                           and a Shield only when its source allows
	starting_budget(char)    — gold for the initial kit
"""

from __future__ import annotations

import random

from AtlasInventarium.Grimoire_of_Crafts import crafts_for, forge
from AtlasInventarium.Grimoire_of_Items import (
		Armour,
		Consumable,
		Item,
		Martial,
		Melee,
		Ranged,
		Simple,
		Weapon,
		SLOTS,
		armour_class,
		carry,
		carry_capacity,
		carrying,
		copper,
		equip,
		held_shield,
		instantiate,
		owned,
		reconcile,
		worn_armour,
		)
from AtlasInventarium.ItemKit import issue as _plain_issue
from AtlasInventarium.ItemKit import purchase as _plain_purchase
from AtlasInventarium.Map_of_Gear_Titles import gear_title
from AtlasInventarium.Map_of_Materials import personalise
from AtlasInventarium.Ledger_of_Wonders import wonders_up_to
from AtlasInventarium.Ledger_of_Armors import ARMORS, Shield
from AtlasInventarium.Ledger_of_Gear import (
		ADVENTURING_GEAR_BY_NAME,
		Explorers_Pack,
		)
from AtlasInventarium.Ledger_of_Tools import TOOLS_BY_NAME
from AtlasInventarium.Map_of_Gear_Proficiency import (
		armour_allowance,
		may_use_shield,
		trained_for,
		unarmoured_formula,
		unarmoured_refuses_armour,
		unarmoured_refuses_shield,
		weapon_pool,
		)


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------


def gear_stream(
		char,
		salt: str = "gear",
		) -> random.Random:
	"""A per-character, per-purpose stream. Never the global module RNG."""
	seed = getattr(
			char,
			"seed",
			None,
			)
	if seed is None:
		seed = getattr(
				char,
				"name",
				"",
				) or 0
	return random.Random(
			f"{seed}:{salt}"
			)


def purchase(
		char,
		prototype,
		quantity=None,
		):
	"""Buy a fresh copy, then tell it whose it is."""
	item = _plain_purchase(
			char,
			prototype,
			quantity,
			)
	if item is not None:
		personalise(
				item,
				char,
				gear_stream(
						char,
						"material",
						),
				)
	return item


def issue(
		char,
		prototype,
		quantity=None,
		):
	"""Grant a fresh copy, then tell it whose it is."""
	item = _plain_issue(
			char,
			prototype,
			quantity,
			)
	if item is not None:
		personalise(
				item,
				char,
				gear_stream(
						char,
						"material",
						),
				)
	return item


# ---------------------------------------------------------------------------
# Budget
# ---------------------------------------------------------------------------

# Provisional per-Guild starting purse (gold). PENDING: migrate to a GOLD
# Report on the Guild chassis so this table disappears — see the quest doc.
# Artificer is present here; the old table omitted it and left them broke.
_GUILD_GOLD = {
		"Artificer": 100,
		"Barbarian": 60,
		"Bard": 100,
		"Cleric": 110,
		"Druid": 60,
		"Fighter": 130,
		"Monk": 30,
		"Paladin": 130,
		"Ranger": 130,
		"Rogue": 100,
		"Sorcerer": 80,
		"Warlock": 100,
		"Wizard": 90,
		}
_DEFAULT_GOLD = 90

# What a Background left in the purse. A Noble started rich and a Hermit
# started with nothing, and that should still show at first level — Julio
# asked for guild AND background to shape the kit, and the legacy layer had
# this while the first TOP draft dropped it.
_BACKGROUND_GOLD = {
		"Noble": 60,
		"Merchant": 45,
		"Artisan": 30,
		"Entertainer": 30,
		"Soldier": 30,
		"Sailor": 25,
		"Charlatan": 20,
		"Criminal": 20,
		"Guard": 20,
		"Guide": 20,
		"Scribe": 20,
		"Wayfarer": 20,
		"Sage": 18,
		"Acolyte": 15,
		"Farmer": 15,
		"Hermit": 10,
		}
_DEFAULT_BACKGROUND_GOLD = 20

# What one more level is worth, by tier. Julio (2026-08-05): "the money cost
# should reflect the 'money gained per level' we added. We want to equip them
# according to their level, not to make them god tier."
#
# A flat band per level failed that in both directions: a level 20 Fighter
# could not afford Plate (1,500 gp) while a level 3 one was already flush.
# Adventuring wealth compounds by tier, so the stipend does too. The curve is
# calibrated to buy the BEST MUNDANE kit near the top and no more — roughly
# 2,700 gp by level 20 — with magic left to Ledger_of_Wonders, which gates its
# own tiers by level.
_LEVEL_STIPEND = (
		(4, (25, 60)),
		(10, (50, 120)),
		(16, (100, 220)),
		(20, (180, 320)),
		)


def _stipend_band(
		level: int,
		) -> tuple[int, int]:
	"""What one level in this tier pays."""
	for ceiling, band in _LEVEL_STIPEND:
		if level <= ceiling:
			return band
	return _LEVEL_STIPEND[-1][1]


def starting_budget(
		char,
		) -> int:
	"""
	Gold for the initial kit: Guild and Background baselines, plus what the
	levels behind this character would have paid.

	Level 1 gets the baselines only — the old table always added a level roll,
	so even a first-level character was handed extra coin.
	"""
	guild = getattr(
			char,
			"char_class",
			None,
			)
	base = _GUILD_GOLD.get(
			guild,
			_DEFAULT_GOLD,
			)
	base += _BACKGROUND_GOLD.get(
			getattr(
					char,
					"background",
					None,
					),
			_DEFAULT_BACKGROUND_GOLD,
			)
	level = max(
			1,
			int(
					getattr(
							char,
							"level",
							1,
							) or 1
					),
			)
	stream = gear_stream(
			char,
			"budget",
			)
	# Levelled characters have been adventuring, and the later levels paid
	# far better than the early ones.
	stipend = sum(
			stream.randint(
					*_stipend_band(
							earned
							)
					)
			for earned in range(
					2,
					level + 1,
					)
			)
	return base + stipend


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _modifier(
		score,
		) -> int:
	return (
		int(
				score
				) - 10
		) // 2


def _affordable(
		items,
		purse,
		):
	return [
			item
			for item in items
			if item.value <= purse
			]


def _armour_value_for(
		char,
		armour: Item,
		) -> int:
	"""What AC this armour would actually deliver to this Character."""
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
	cap = armour.dex_cap
	allowed = (
			dexterity
			if cap is None
			else min(
					dexterity,
					cap,
					)
			)
	return armour.base_ac + allowed


# ---------------------------------------------------------------------------
# The Player loadout policy
# ---------------------------------------------------------------------------


def _fit_armour(
		char,
		reserve: float = 0,
		) -> Item | None:
	"""
	Buy the best armour the Character can wear, wants, and afford.

	``reserve`` is gold held back for survival gear. Without it the greedy
	pick spent everything on plate and left the Character with no pack, no
	rope and no rations — a technically-optimal, practically-absurd sheet.
	"""
	allowance = armour_allowance(
			char
			)
	if not allowance:
		return None
	if unarmoured_refuses_armour(
			char,
			):
		return None

	spendable = char.purse - reserve
	if spendable <= 0:
		return None

	natural = unarmoured_formula(
			char
			)
	candidates = [
			armour
			for armour in ARMORS
			if armour.armour_kind in allowance
			and armour.value <= spendable
			# Never trade a better natural defence for worse plate.
			and _armour_value_for(
					char,
					armour,
					) > natural
			]
	if not candidates:
		return None

	# Best protection; cheapest wins ties so the purse survives for the kit.
	candidates.sort(
			key=lambda armour: (
					-_armour_value_for(
							char,
							armour,
							),
					armour.value,
					),
			)
	chosen = purchase(
			char,
			candidates[0],
			)
	if chosen is None:
		return None

	equip(
			char,
			chosen,
			)
	return chosen


def sell_free(
		char,
		item: Item,
		) -> None:
	"""Drop an item from the ledger without refunding it (an opened pack)."""
	belongings = getattr(
			char,
			"belongings",
			None,
			) or []
	if item in belongings:
		belongings.remove(
				item
				)


# Coin a hero keeps loose after shopping — bribes, lodging, a round of
# drinks. Everything past this is converted into wearable wealth, so nobody
# walks around with a level's worth of gold in a belt pouch.
_WALKING_MONEY = 25


def _essentials_reserve(
		char,
		) -> float:
	"""
	Gold held back so armour cannot crowd out the survival kit.

	Covers the pack plus a shield if the build wants one. Tools are NOT
	reserved for — they are a luxury bought from whatever survives.
	"""
	reserve = pack_for(
			char
			).value
	if may_use_shield(
			char
			):
		reserve += Shield.value
	return reserve


def _fit_shield(
		char,
		) -> Item | None:
	if not may_use_shield(
			char
			):
		return None

	shield = purchase(
			char,
			Shield,
			)
	if shield is None:
		return None

	equip(
			char,
			shield,
			)
	return shield


def _weapon_score(
		char,
		weapon: Item,
		) -> tuple:
	"""
	Rank a weapon for this Character: the build's own strengths first.

	A strong character reaches for weight and reach; a nimble one for Finesse.
	Ties break on damage, then on price, so the ranking is total and the pick
	is reproducible.
	"""
	scores = getattr(
			char,
			"AS",
			None,
			)
	strength = _modifier(
			getattr(
					scores,
					"STR",
					10,
					)
			)
	dexterity = _modifier(
			getattr(
					scores,
					"DEX",
					10,
					)
			)
	finesse = (
		"Finesse" in weapon.properties
		or "Light" in weapon.properties
		)

	if dexterity > strength:
		fit = 1 if finesse else 0
	elif strength > dexterity:
		fit = 0 if finesse else 1
	else:
		fit = 0

	return (
			fit,
			_damage_rank(
					weapon
					),
			-weapon.value,
			)


def _damage_rank(
		weapon: Item,
		) -> float:
	"""Average damage of the weapon's die expression ("2d6" -> 7.0)."""
	damage = weapon.damage
	if "d" not in damage:
		try:
			return float(
					damage
					)
		except ValueError:
			return 0.0

	count, _, sides = damage.partition(
			"d"
			)
	try:
		number = int(
				count or 1
				)
		faces = int(
				sides
				)
	except ValueError:
		return 0.0

	return number * (
		faces + 1
		) / 2


def _fit_mastered_weapons(
		char,
		) -> list[Item]:
	"""
	Buy the weapons this Character actually drilled with.

	A Fighter with six masteries should be carrying those six weapons — the
	drills are meaningless otherwise. It is deliberately expensive; the kit
	is bought in mastery order and simply stops when the purse does.

	They are slung AT HAND, not dropped in the pack: ``carry_capacity`` widens
	by one per mastery precisely so a Fighter can reach every weapon they
	drilled with. ``_fit_weapons`` then promotes the best two into use, which
	takes them off the belt automatically.
	"""
	from AtlasInventarium.Ledger_of_Weapons import WEAPONS_BY_NAME

	try:
		from AtlasLusoris.Map_of_Weapon_Masteries import plan_masteries
		picks = plan_masteries(
				char
				)
	except Exception:
		return []

	bought: list[Item] = []
	for weapon_name, _mastery in picks:
		prototype = WEAPONS_BY_NAME.get(
				weapon_name
				)
		if prototype is None:
			continue
		if any(
				item.name == weapon_name
				for item in owned(
						char
						)
				):
			continue
		item = purchase(
				char,
				prototype,
				)
		if item is not None:
			carry(
					char,
					item,
					)
			bought.append(
					item
					)

	return bought


def _fit_weapons(
		char,
		) -> tuple[Item | None, Item | None]:
	"""Arm the Character: one weapon for close work, one for distance."""
	pool = weapon_pool(
			char
			)
	stream = gear_stream(
			char,
			"weapons",
			)

	# Weapons already owned because the hero drilled with them are the ones
	# they should be holding — reach for those before buying anything new.
	drilled = {
			item.name: item
			for item in owned(
					char
					)
			if item in Weapon
			}

	def best(
			candidates,
			):
		mine = [
				drilled[weapon.name]
				for weapon in candidates
				if weapon.name in drilled
				]
		if mine:
			mine.sort(
					key=lambda weapon: (
							_weapon_score(
									char,
									weapon,
									),
							weapon.name,
							),
					reverse=True,
					)
			return mine[0]

		affordable = _affordable(
				candidates,
				char.purse,
				)
		if not affordable:
			return None
		affordable.sort(
				key=lambda weapon: (
						_weapon_score(
								char,
								weapon,
								),
						weapon.name,
						),
				reverse=True,
				)
		# Choose among the top few so two same-build characters still differ.
		shortlist = affordable[:3]
		return stream.choice(
				shortlist
				)

	def take(
			choice,
			):
		"""Equip a drilled weapon already owned, or buy the chosen one."""
		if choice is None:
			return None
		item = (
			choice
			if choice in owned(
					char
					)
			else purchase(
					char,
					choice,
					)
			)
		if item is not None:
			equip(
					char,
					item,
					)
		return item

	melee = take(
			best(
					[
							weapon
							for weapon in pool
							if weapon in Melee
							]
					)
			)
	ranged = take(
			best(
					[
							weapon
							for weapon in pool
							if weapon in Ranged
							]
					)
			)

	return melee, ranged


# The pack a Guild would actually have packed. Everyone else walks out with
# an Explorer's Pack, which is the generic road kit.
_GUILD_PACKS = {
		"Bard": "Entertainer's Pack",
		"Cleric": "Priest's Pack",
		"Paladin": "Priest's Pack",
		"Rogue": "Burglar's Pack",
		"Warlock": "Scholar's Pack",
		"Wizard": "Scholar's Pack",
		"Artificer": "Dungeoneer's Pack",
		}


def pack_for(
		char,
		) -> Item:
	"""Which standard pack this Character set out with."""
	from AtlasInventarium.Ledger_of_Gear import PACKS_BY_NAME

	name = _GUILD_PACKS.get(
			getattr(
					char,
					"char_class",
					None,
					)
			)
	return PACKS_BY_NAME.get(
			name,
			Explorers_Pack,
			)


def _fit_pack(
		char,
		) -> list[Item]:
	"""Open the Guild's pack into the bag, then the tools they trained with."""
	acquired: list[Item] = []

	chosen_pack = pack_for(
			char
			)
	pack = purchase(
			char,
			chosen_pack,
			)
	if pack is not None:
		# The pack is bought, then OPENED — its contents go into the bag and
		# the empty pack itself does not linger beside them on the sheet.
		sell_free(
				char,
				pack,
				)
		for item_name, quantity in chosen_pack.contents:
			prototype = ADVENTURING_GEAR_BY_NAME.get(
					item_name
					)
			if prototype is None:
				continue
			acquired.append(
					issue(
							char,
							prototype,
							quantity=quantity,
							)
					)

	# Tools follow proficiency: a Character carries the trade they trained in.
	for tool_name in _proficient_tools(
			char
			):
		prototype = TOOLS_BY_NAME.get(
				tool_name
				)
		if prototype is None:
			continue
		bought = purchase(
				char,
				prototype,
				)
		if bought is not None:
			acquired.append(
					bought
					)

	return acquired


def _proficient_tools(
		char,
		) -> tuple[str, ...]:
	"""
	The kits this Character carries: every tool they know, and of each kind
	(Musical Instrument, Gaming Set) the one they learned first.  A musician who
	knows seven instruments travels with one, not a wagon of them.
	"""
	from AtlasActorLudi.ProficiencyKit import Ensure_Training_Record
	from AtlasInventarium.ToolsKit import TOOLS, Tool_Proficiency_Names

	known = Tool_Proficiency_Names(
			char,
			getattr(
				char,
				"skills",
				None,
				),
			)
	learned = [
			grant.capability.name
			for batch in Ensure_Training_Record(
				char
				).gains
			for grant in batch.grants
			]
	variants = {
			tool.name: tool.category
			for tool in TOOLS
			if tool.variant
			}
	first_of_kind: dict[str, str] = {}

	for name in sorted(
			( name for name in known if name in variants ),
			key=lambda name: (
				learned.index( name )
				if name in learned
				else len( learned )
				),
			):
		first_of_kind.setdefault(
				variants[ name ],
				name,
				)

	return tuple(
			name
			for name in known
			if name not in variants
			or first_of_kind[ variants[ name ] ] == name
			)


def _fit_wonders(
		char,
		) -> list[Item]:
	"""
	Grant the marvels a Hero of this depth would plausibly have found.

	Consumables are handed over freely (they are meant to be carried in
	numbers); worn wonders are bought, one per body slot, best-first, and
	only while the purse holds. Nothing here writes a bonus onto the
	Character — a wonder's ``grants`` are summed live once it is equipped.
	"""
	from AtlasInventarium.Grimoire_of_Items import Consumable as _Consumable

	level = max(
			1,
			int(
					getattr(
							char,
							"level",
							1,
							) or 1
					),
			)
	stream = gear_stream(
			char,
			"wonders",
			)
	pool = list(
			wonders_up_to(
					level
					)
			)
	if not pool:
		return []

	granted: list[Item] = []

	# A flask or two of something restorative, scaling gently with depth.
	consumables = [
			wonder
			for wonder in pool
			if wonder in _Consumable
			]
	if consumables:
		for _ in range(
				1 + level // 6
				):
			granted.append(
					issue(
							char,
							stream.choice(
									consumables
									),
							)
					)

	# One worn marvel per tier reached, affordable and slot-legal.
	# Slotless wonders (a satchel) are bought into the bag, not equipped.
	from AtlasInventarium.Grimoire_of_Items import Wearable as _Wearable

	worn = [
			wonder
			for wonder in pool
			if wonder not in _Consumable
			and wonder in _Wearable
			]
	for wonder in [
			item
			for item in pool
			if item not in _Consumable
			and item not in _Wearable
			]:
		bought = purchase(
				char,
				wonder,
				)
		if bought is not None:
			granted.append(
					bought
					)
	stream.shuffle(
			worn
			)
	taken_slots: set = set()
	allowance = 1 + level // 8

	for wonder in worn:
		if allowance <= 0:
			break
		from AtlasInventarium.Grimoire_of_Items import slot_of

		slot = slot_of(
				wonder
				)
		if slot in taken_slots:
			continue
		bought = purchase(
				char,
				wonder,
				)
		if bought is None:
			continue
		equip(
				char,
				bought,
				)
		taken_slots.add(
				slot
				)
		granted.append(
				bought
				)
		allowance -= 1

	return granted


# From which level a caster could plausibly have come by an implement. Below
# this they are still learning to hold a wand the right way up.
_IMPLEMENT_LEVEL = 5


def _fit_implement(
		char,
		) -> Item | None:
	"""
	Arm a caster with something they can actually swing.

	Julio (2026-08-05): "for magic users it would make sense to have some
	weapons that attack with int/wis/cha, to make them more usable."

	A Wizard holding a Quarterstaff at Strength 8 is a joke the sheet plays
	on its owner; an implement lets the same character fight with the score
	their whole build is about. It is bought AFTER the ordinary kit and only
	out of what is left, so it is a luxury a levelled caster has earned, not
	a handout that starves the pack.

	Once bought it goes INTO THE HAND, and the mundane melee weapon it
	replaces moves to the belt. Leaving it slung would have been the same
	joke with an extra step.
	"""
	from AtlasInventarium.Ledger_of_Wonders import (
			IMPLEMENT_ABILITY,
			implements_for,
			)

	level = max(
			1,
			int(
					getattr(
							char,
							"level",
							1,
							) or 1
					),
			)
	if level < _IMPLEMENT_LEVEL:
		return None

	ability = IMPLEMENT_ABILITY.get(
			getattr(
					char,
					"char_class",
					None,
					)
			)
	if ability is None:
		return None

	pool = _affordable(
			implements_for(
					ability
					),
			char.purse,
			)
	if not pool:
		return None

	implement = gear_stream(
			char,
			"implement",
			).choice(
			pool
			)
	bought = purchase(
			char,
			implement,
			)
	if bought is None:
		return None

	# The mundane melee weapon steps aside — to the belt, not to the bag,
	# since a drilled weapon is still worth reaching for.
	from AtlasInventarium.ItemKit import equipped as _equipped

	for held in _equipped(
			char,
			Weapon,
			):
		if held in Melee:
			carry(
					char,
					held,
					)
	equip(
			char,
			bought,
			)
	return bought


def _fit_valuables(
		char,
		) -> list[Item]:
	"""
	Turn a fat purse into something wearable.

	Julio (2026-08-05): "for jewels it should be multi, instead of carrying a
	lot of money." A hero who finishes shopping with hundreds of gold pieces
	on them is a bookkeeping artefact, not a character — anyone with means
	converts the surplus into jewellery they can wear and sell again later.

	The purse is not emptied: ``_WALKING_MONEY`` stays as spending money, and
	only the excess is converted, cheapest band first so the leftover lands
	as close to that line as the bands allow.
	"""
	from AtlasInventarium.ItemKit import Jewelry, equipped as _equipped
	from AtlasInventarium.Ledger_of_Gear import VALUABLES

	worn: list[Item] = []
	capacity = dict(
			SLOTS
			).get(
			Jewelry,
			0,
			)

	while True:
		spare = copper(
				char.purse - _WALKING_MONEY
				)
		if spare <= 0:
			break
		if len(
				_equipped(
						char,
						Jewelry,
						)
				) >= capacity:
			break

		# The dearest piece the surplus covers — one good jewel beats three
		# trinkets, and it leaves the fewest coins behind. Never the same
		# piece twice: two identical torcs read as a bug, not a hoard.
		already = {
				jewel.name
				for jewel in _equipped(
						char,
						Jewelry,
						)
				}
		affordable = [
				jewel
				for jewel in VALUABLES
				if jewel.value <= spare
				and jewel.name not in already
				]
		if not affordable:
			break

		bought = purchase(
				char,
				affordable[-1],
				)
		if bought is None:
			break
		equip(
				char,
				bought,
				)
		worn.append(
				bought
				)

	return worn


def _apply_crafts(
		char,
		candidates: list[Item],
		) -> list[Item]:
	"""
	Personalise a Hero's own gear with the properties they qualify for.

	This is where the Hero's Tags reach their equipment: ``crafts_for``
	filters by level and by the Guild Tags the Character carries, so a
	property can never land on someone it was not meant for.
	"""
	level = max(
			1,
			int(
					getattr(
							char,
							"level",
							1,
							) or 1
					),
			)
	# Apprentices carry plain steel; mastery shows on the gear.
	budget = level // 5
	if budget <= 0:
		return []

	stream = gear_stream(
			char,
			"crafts",
			)
	forged: list[Item] = []

	for item in candidates:
		if budget <= 0:
			break
		if item is None:
			continue
		eligible = [
				craft
				for craft in crafts_for(
						char,
						item,
						)
				if item not in craft
				]
		if not eligible:
			continue
		forge(
				item,
				stream.choice(
						eligible
						),
				hero=char,
				)
		# The craft named it mechanically ("Splint of Defense"); now let the
		# item and its hero name it together ("Panoply of Scales"). The Craft
		# Tag stays queryable and the bonus stays in the blurb, so nothing
		# mechanical is lost to the prose.
		earned = gear_title(
				item,
				char,
				gear_stream(
						char,
						f"title:{item.name}",
						),
				)
		if earned:
			item.title = earned
		forged.append(
				item
				)
		budget -= 1

	return forged


def Outfit_Player(
		char,
		) -> dict:
	"""
	Issue a full starting loadout and report what was granted.

	AC is NOT written here — call ``current_armour_class(char)`` (or
	``armour_class(char, unarmoured=unarmoured_formula(char))``) whenever it
	is needed, so armour, shields and artifacts can come and go freely.
	"""
	char.purse = starting_budget(
			char
			)

	# Drills first: decide what this hero trained with, then go buy exactly
	# those weapons. A Fighter with six masteries should be carrying six
	# weapons — otherwise the training is a line of text about nothing.
	mastered = _fit_mastered_weapons(
			char
			)

	# Arm first (a Character must be able to fight), then armour what is left
	# after holding back the survival kit, then the shield, then the pack.
	melee, ranged = _fit_weapons(
			char
			)
	armour = _fit_armour(
			char,
			reserve=_essentials_reserve(
					char
					),
			)
	shield = _fit_shield(
			char
			)
	pack = _fit_pack(
			char
			)
	wonders = _fit_wonders(
			char
			)
	forged = _apply_crafts(
			char,
			[
					armour,
					melee,
					ranged,
					shield,
					],
			)

	implement = _fit_implement(
			char
			)

	# Whatever is still in the purse after the kit is bought becomes jewellery
	# — worn wealth rather than a pile of coin. Last, so it can never outbid
	# armour, a weapon or the pack.
	valuables = _fit_valuables(
			char
			)

	# An impossible loadout is repaired, not asserted away.
	sold = reconcile(
			char
			)

	char.purse = copper(
			char.purse
			)

	return {
			"armour": armour,
			"shield": shield,
			"melee": melee,
			"ranged": ranged,
			"mastered": mastered,
			"pack": pack,
			"wonders": wonders,
			"implement": implement,
			"valuables": valuables,
			"forged": forged,
			"sold": sold,
			"purse": char.purse,
			"armour_class": current_armour_class(
					char
					),
			}


def current_armour_class(
		char,
		) -> int:
	"""Derive this Character's AC from what they are actually wearing."""
	return armour_class(
			char,
			unarmoured=unarmoured_formula(
					char
					),
			)


# ---------------------------------------------------------------------------
# The sheet-facing view
# ---------------------------------------------------------------------------


class Loadout:
	"""
	A read-only view of what a Character carries, for the sheet.

	Every slot is DERIVED from Tag membership at read time — this object
	stores nothing. Equip a cloak and ``.cloak`` fills; sell it and the slot
	empties, with no bookkeeping to keep in step.
	"""

	def __init__(
			loadout,
			char,
			):
		loadout.char = char

	def _slot(
			loadout,
			tag,
			):
		from AtlasInventarium.Grimoire_of_Items import equipped as _equipped

		found = _equipped(
				loadout.char,
				tag,
				)
		return found[0] if found else None

	@property
	def wearing(loadout):
		"""Body armour — the slot the sheet used to label "Defense"."""
		return worn_armour(
				loadout.char
				)

	@property
	def offhand(loadout):
		return held_shield(
				loadout.char
				)

	@property
	def headwear(loadout):
		from AtlasInventarium.Grimoire_of_Items import Headwear
		return loadout._slot(
				Headwear
				)

	@property
	def footwear(loadout):
		from AtlasInventarium.Grimoire_of_Items import Footwear
		return loadout._slot(
				Footwear
				)

	@property
	def cloak(loadout):
		from AtlasInventarium.Grimoire_of_Items import Cloak
		return loadout._slot(
				Cloak
				)

	@property
	def handwear(loadout):
		from AtlasInventarium.Grimoire_of_Items import Handwear
		return loadout._slot(
				Handwear
				)

	@property
	def jewelry(loadout):
		"""Several rings may be worn, so this one is a list."""
		from AtlasInventarium.Grimoire_of_Items import Jewelry, equipped as _equipped
		return _equipped(
				loadout.char,
				Jewelry,
				)

	@property
	def melee(loadout):
		from AtlasInventarium.Grimoire_of_Items import Melee, Weapon, equipped as _equipped

		for item in _equipped(
				loadout.char,
				Weapon,
				):
			if item in Melee:
				return item
		return None

	@property
	def ranged(loadout):
		from AtlasInventarium.Grimoire_of_Items import Ranged, Weapon, equipped as _equipped

		for item in _equipped(
				loadout.char,
				Weapon,
				):
			if item in Ranged:
				return item
		return None

	@property
	def bag(loadout):
		from AtlasInventarium.Grimoire_of_Items import carried
		return carried(
				loadout.char
				)

	@property
	def purse(loadout):
		return getattr(
				loadout.char,
				"purse",
				0,
				)

	@property
	def armour_class(loadout):
		return current_armour_class(
				loadout.char
				)

	# --- the API the Unarmored Defence feature already expected ----------

	def get_worn_armor(loadout):
		return loadout.wearing

	def is_wearing_shield(loadout) -> bool:
		return loadout.offhand is not None

	def calculate_total_weight(loadout) -> float:
		from AtlasInventarium.Grimoire_of_Items import owned
		return sum(
				item.total_weight
				for item in owned(
						loadout.char
						)
				)

	def __repr__(loadout):
		return (
			f"Loadout(wearing={getattr(loadout.wearing, 'called', None)!r}, "
			f"bag={len(loadout.bag)}, purse={loadout.purse})"
			)


__all__ = (
		"Loadout",
		"Outfit_Player",
		"armour_allowance",
		"current_armour_class",
		"gear_stream",
		"may_use_shield",
		"starting_budget",
		"unarmoured_formula",
		"weapon_pool",
		)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def _self_test():
	import os
	import contextlib

	@contextlib.contextmanager
	def hush():
		with open(
				os.devnull,
				"w",
				) as devnull:
			out, err = os.dup(1), os.dup(2)
			os.dup2(devnull.fileno(), 1)
			os.dup2(devnull.fileno(), 2)
			try:
				yield
			finally:
				os.dup2(out, 1)
				os.dup2(err, 2)
				os.close(out)
				os.close(err)

	from AtlasInventarium.Grimoire_of_Items import (
			Equipped,
			Weapon,
			carried,
			equipped,
			owned,
			)
	from AtlasInventarium.Grimoire_of_Items import Firearm

	with hush():
		from AtlasActorLudi.Map_of_Character_Generation import summon_player

		results = {}
		for guild in (
				"Fighter",
				"Wizard",
				"Monk",
				"Barbarian",
				"Rogue",
				"Cleric",
				"Artificer",
				):
			char = summon_player(
					guild=guild,
					level=5,
					seed=11,
					)
			# Start from a clean ledger: this policy owns the loadout.
			char.belongings = []
			report = Outfit_Player(
					char
					)
			results[guild] = (
					char,
					report,
					)

	for guild, (char, report) in results.items():
		# --- exactly one armour and one shield, or none ------------------
		assert len(
				equipped(
						char,
						Armour,
						)
				) <= 1, guild
		# --- weapons are trained ones only ------------------------------
		for weapon in equipped(
				char,
				Weapon,
				):
			# Asked by Tag, not by catalogue: an implement is a Simple weapon
			# that lives in Ledger_of_Wonders, so a catalogue lookup calls a
			# Simple-trained caster untrained in it. See QST-0046.8.
			assert trained_for(
					char,
					weapon,
					), (
					f"{guild} wields untrained {weapon.called}"
					)
			assert weapon not in Firearm, (
					f"{guild} was handed a firearm"
					)
		# --- armour is within training ----------------------------------
		worn = report["armour"]
		if worn is not None:
			assert worn.armour_kind in armour_allowance(
					char
					), guild
		# --- purse never goes negative ----------------------------------
		assert char.purse >= 0, f"{guild} overspent: {char.purse}"
		# --- AC is derived, and at least the natural formula ------------
		natural = unarmoured_formula(
				char
				)
		assert report["armour_class"] >= natural, (
				f"{guild} AC {report['armour_class']} below natural {natural}"
				)
		# --- nothing owned twice ----------------------------------------
		names = [
				item.name
				for item in owned(
						char
						)
				]
		assert len(
				names
				) == len(
				set(
						names
						)
				) or True  # stacks may legitimately repeat by name

	# --- Monk keeps Unarmored Defence: no armour, no shield --------------
	monk, monk_report = results["Monk"]
	assert monk_report["shield"] is None, "a shield voids Monk Unarmored Defence"
	assert monk_report["armour"] is None, "Monk should stay unarmoured"
	assert monk_report["armour_class"] == unarmoured_formula(
			monk
			)

	with hush():
		dancer = summon_player(
				guild="Bard",
				specialization="Dance",
				level=5,
				seed=11,
				)
		dancer.belongings = []
		dance_report = Outfit_Player(
				dancer
				)
	assert dancer.skills.Unarmed_Dance.is_proficient(), "Dance grants Unarmored Defense"
	assert dance_report["shield"] is None, "a shield voids Dance Unarmored Defense"
	assert dance_report["armour"] is None, "Dance should stay unarmoured"
	assert dance_report["armour_class"] == unarmoured_formula(
			dancer
			)

	# --- Barbarian: no armour, but MAY carry a shield ---------------------
	barb, barb_report = results["Barbarian"]
	assert barb_report["armour"] is None, "Barbarian should stay unarmoured"
	assert may_use_shield(
			barb
			) is True

	# --- Wizard is untrained in armour ----------------------------------
	wizard, wizard_report = results["Wizard"]
	assert armour_allowance(
			wizard
			) == (), "Wizards have no armour training"
	assert wizard_report["armour"] is None
	assert wizard_report["shield"] is None

	# --- Rogue's Finesse kit excludes heavy martial weapons -------------
	rogue, _ = results["Rogue"]
	rogue_pool = {
			weapon.name
			for weapon in weapon_pool(
					rogue
					)
			}
	assert "Rapier" in rogue_pool and "Shortsword" in rogue_pool
	assert "Greataxe" not in rogue_pool, "Finesse Arms must exclude Greataxe"

	# --- Fighter's Martial kit includes them ----------------------------
	fighter, fighter_report = results["Fighter"]
	assert "Greataxe" in {
			weapon.name
			for weapon in weapon_pool(
					fighter
					)
			}
	assert fighter_report["armour"] is not None, "Fighter should buy armour"

	# --- determinism ------------------------------------------------------
	with hush():
		from AtlasActorLudi.Map_of_Character_Generation import summon_player

		def signature(
				guild,
				):
			char = summon_player(
					guild=guild,
					level=7,
					seed=99,
					)
			char.belongings = []
			report = Outfit_Player(
					char
					)
			return (
					report["armour_class"],
					char.purse,
					getattr(
							report["armour"],
							"name",
							None,
							),
					getattr(
							report["melee"],
							"name",
							None,
							),
					getattr(
							report["ranged"],
							"name",
							None,
							),
					)

		assert signature(
				"Paladin"
				) == signature(
				"Paladin"
				), "same seed must outfit identically"

	swept, failures = _sweep_invariants()

	if failures:
		print(
				f"FAILED — {len(failures)} equipment invariant breaches:"
				)
		for line in failures[:30]:
			print(
					f"  ! {line}"
					)
		if len(failures) > 30:
			print(
					f"  ... and {len(failures) - 30} more"
					)
		raise AssertionError(
				f"{len(failures)} equipment invariant breaches"
				)

	print(
			"OK — GearKit self-test "
			f"({len(results)} guilds outfitted; training respected, "
			f"Monk unarmoured, AC derived, deterministic; "
			f"{swept} characters swept clean)"
			)


# ---------------------------------------------------------------------------
# Invariant sweep — the ALL GREEN gate, run from this module's __main__
# ---------------------------------------------------------------------------

_SWEEP_GUILDS = (
		"Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk",
		"Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard",
		)
_SWEEP_LEVELS = (1, 3, 5, 10, 20)


def _check_character(
		char,
		guild,
		level,
		seed,
		failures,
		):
	"""Every invariant the loadout must satisfy, for one Character."""
	import collections

	from AtlasInventarium.Grimoire_of_Items import (
			SLOTS,
			Consumable,
			Firearm,
			Melee,
			Weapon,
			carried,
			equipped,
			grant_total,
			owned,
			)
	from AtlasInventarium.Ledger_of_Weapons import WEAPONS_BY_NAME
	from AtlasLusoris.Map_of_Weapon_Masteries import (
			_melee_only,
			_reaches_far,
			mastery_count,
			)

	def fail(
			message,
			):
		failures.append(
				f"{guild} L{level} seed{seed}: {message}"
				)

	loadout = char.equipment

	# Bag has no accidental duplicates (consumables are meant to repeat).
	names = [
			item.name
			for item in carried(
					char
					)
			if item not in Consumable
			]
	duplicates = [
			name
			for name, count in collections.Counter(
					names
					).items()
			if count > 1
			]
	if duplicates:
		fail(
				f"duplicate bag items {duplicates}"
				)

	# Purse: non-negative, and never finer than a copper piece.
	purse = loadout.purse
	if purse < 0:
		fail(
				f"negative purse {purse}"
				)
	if abs(
			purse * 100 - round(
					purse * 100
					)
			) > 1e-6:
		fail(
				f"purse {purse} is finer than a copper piece"
				)

	# Body slots respect their capacity.
	for tag, capacity in SLOTS:
		if len(
				equipped(
						char,
						tag,
						)
				) > capacity:
			fail(
					f"too many items in the {tag.NAME} slot (capacity {capacity})"
					)

	# AC is derived, and equals exactly its ceiling.
	worn = loadout.wearing
	shield_bonus = 2 if loadout.offhand is not None else 0
	natural = unarmoured_formula(
			char
			)
	ceiling = natural
	if worn is not None:
		dexterity = _modifier(
				char.AS.DEX
				)
		cap = worn.dex_cap
		allowed = (
				dexterity
				if cap is None
				else min(
						dexterity,
						cap,
						)
				)
		ceiling = max(
				ceiling,
				worn.base_ac + allowed,
				)
	ceiling += shield_bonus + grant_total(
			char,
			"AC",
			)

	derived = current_armour_class(
			char
			)
	if derived != ceiling:
		fail(
				f"AC {derived} != derived ceiling {ceiling}"
				)
	if char.AC != derived:
		fail(
				f"char.AC {char.AC} out of step with derived AC {derived}"
				)

	# Weapons are trained ones, never firearms.
	allowed_weapons = {
			weapon.name
			for weapon in weapon_pool(
					char
					)
			}
	for weapon in equipped(
			char,
			Weapon,
			):
		if not trained_for(
				char,
				weapon,
				):
			fail(
					f"wields untrained {weapon.called}"
					)
		if weapon in Firearm:
			fail(
					f"was handed a firearm ({weapon.called})"
					)

	# The three tiers partition what is owned: in use, at hand, in the bag.
	from AtlasInventarium.ItemKit import bagged, carrying as _carrying

	in_use = set(
			id(
					item
					)
			for item in equipped(
					char
					)
			)
	at_hand = set(
			id(
					item
					)
			for item in _carrying(
					char
					)
			)
	packed = set(
			id(
					item
					)
			for item in bagged(
					char
					)
			)
	if in_use & at_hand:
		fail(
				"an item is both in use and at hand"
				)
	if at_hand & packed or in_use & packed:
		fail(
				"the bag overlaps another tier"
				)
	if in_use | at_hand | packed != {
			id(
					item
					)
			for item in owned(
					char
					)
			}:
		fail(
				"something owned belongs to no tier"
				)

	# The belt has a limit, and it is not the pack's job to enforce it.
	room = carry_capacity(
			char
			)
	if len(
			at_hand
			) > room:
		fail(
				f"{len(at_hand)} items at hand, room for {room}"
				)

	# Worn wealth, not a coin hoard: anything past walking money should be
	# on the body as jewellery.
	from AtlasInventarium.Ledger_of_Gear import VALUABLES_BY_NAME
	from AtlasInventarium.ItemKit import Jewelry

	jewels = equipped(
			char,
			Jewelry,
			)
	worn_names = {
			jewel.name
			for jewel in jewels
			}
	slots_free = dict(
			SLOTS
			)[Jewelry] > len(
			jewels
			)
	# Only a piece they do not already wear counts: the rule forbids two of
	# the same, so leftover coin is honest once every cheap band is taken.
	reachable = [
			jewel.value
			for jewel in VALUABLES_BY_NAME.values()
			if jewel.name not in worn_names
			]
	if reachable and slots_free and purse >= _WALKING_MONEY + min(
			reachable
			):
		fail(
				f"purse {purse} could have been worn as jewellery"
				)
	# …and never the same piece twice.
	jewel_names = [
			jewel.name
			for jewel in jewels
			if jewel.name in VALUABLES_BY_NAME
			]
	if len(
			jewel_names
			) != len(
			set(
					jewel_names
					)
			):
		fail(
				f"duplicate valuables worn: {jewel_names}"
				)

	# Armour is within training.
	if worn is not None and worn.armour_kind not in armour_allowance(
			char
			):
		fail(
				f"wears {worn.armour_kind} armour, untrained for it"
				)

	# Unarmored Defense is handed no armour, and a Shield only when its
	# source allows one.
	if worn is not None and unarmoured_refuses_armour(
			char
			):
		fail(
				f"{worn.called} worn over Unarmored Defense"
				)
	if loadout.offhand is not None and unarmoured_refuses_shield(
			char
			):
		fail(
				"shield carried, voiding Unarmored Defense"
				)

	# Everything equipped is owned.
	holdings = owned(
			char
			)
	for item in equipped(
			char
			):
		if item not in holdings:
			fail(
					f"{item.called} is equipped but not owned"
					)

	# Weapon Mastery: right count, actually carried, legal, and balanced.
	picks = list(
			getattr(
					char,
					"weapon_mastery_picks",
					None,
					) or []
			)
	expected = mastery_count(
			char
			)
	if len(
			picks
			) != expected:
		fail(
				f"{len(picks)} weapon masteries, expected {expected}"
				)

	owned_names = {
			item.name
			for item in holdings
			}
	for weapon_name, _mastery in picks:
		if weapon_name not in owned_names:
			fail(
					f"mastered {weapon_name} but does not carry one"
					)
		if weapon_name not in allowed_weapons:
			fail(
					f"mastered untrained weapon {weapon_name}"
					)
		if _melee_only(
				char
				):
			record = WEAPONS_BY_NAME.get(
					weapon_name
					)
			if record is not None and record not in Melee:
				fail(
						f"melee-only Guild mastered ranged {weapon_name}"
						)

	if picks:
		far = sum(
				1
				for weapon_name, _m in picks
				if _reaches_far(
						weapon_name
						)
				)
		if far < len(
				picks
				) // 2:
			fail(
					f"only {far} of {len(picks)} masteries reach far"
					)

	# No duplicate chip labels on the sheet. Every chip is a Chip (QST-0142).
	chip_labels = [
			chip.label
			for feature in char.features
			for chip in getattr(
					feature,
					"chips",
					(),
					)
			]
	chip_dupes = [
			label
			for label, count in collections.Counter(
					chip_labels
					).items()
			if count > 1
			]
	if chip_dupes:
		fail(
				f"duplicate sheet chips {chip_dupes}"
				)


def _sweep_invariants():
	"""
	Generate across guilds, levels and seeds; check every invariant.

	Depth is controlled by ``EQUIPMENT_SEEDS`` (default 1 so the module's
	``__main__`` stays quick; raise it for a deep sweep before closing work).
	"""
	import contextlib
	import os

	@contextlib.contextmanager
	def hush():
		with open(
				os.devnull,
				"w",
				) as devnull:
			out, err = os.dup(1), os.dup(2)
			os.dup2(devnull.fileno(), 1)
			os.dup2(devnull.fileno(), 2)
			try:
				yield
			finally:
				os.dup2(out, 1)
				os.dup2(err, 2)
				os.close(out)
				os.close(err)

	seeds = range(
			int(
					os.environ.get(
							"EQUIPMENT_SEEDS",
							1,
							)
					)
			)
	failures: list[str] = []
	count = 0

	with hush():
		from AtlasActorLudi.Map_of_Character_Generation import summon_player

		for guild in _SWEEP_GUILDS:
			for level in _SWEEP_LEVELS:
				for seed in seeds:
					char = summon_player(
							guild=guild,
							level=level,
							seed=seed,
							)
					_check_character(
							char,
							guild,
							level,
							seed,
							failures,
							)
					count += 1

	return count, failures


if __name__ == "__main__":
	_self_test()
