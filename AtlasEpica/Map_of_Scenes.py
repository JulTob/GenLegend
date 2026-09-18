"""
Map of Scenes — DM Character Oracle inspiration cards (QST-0037.16).

Kin to Map_of_Stories / Map_of_Titles: collapse flavor from a host. The host is
the **DM Character** — not assumed evil (villain, Quest Master, contested
guardian, …). Area and Lair Lodges grow here. Wave collapse uses
Charts_of_The_Monomyth (If / Choice / render) — same actuators as Stories.
One Generate → one presentation card; always mint scene NPCs with sheet links;
soft party hooks from Tags.
"""
#-- Recovered from the 2026-08-29 bytecode (QST-0134).  The module docstring,
#-- every function docstring, every line of table prose — the beats, the
#-- settings, the party hooks, the occupant lines, the card's own framing —
#-- and both failure messages are the original's, word for word.  The
#-- transcription was proved instruction for instruction against the vaulted
#-- .pyc before this layout was applied, and the three tables were printed out
#-- of the objects the bytecode builds rather than retyped.
#--
#-- Does this module own a domain axis (QST-0134)?  No, and its own docstring
#-- says where the axes live: Area and Lair are Adventure Tags in
#-- Grimoire_of_Adventure.  What grows here is the Lodge — which Area suits
#-- which DM Character, which Lair suits which Area — and the collapse that
#-- reads it.  A table of weights is content; the Tag it chooses among is
#-- structure, and that structure already exists.

from __future__ import annotations

import random
from urllib.parse import quote

from AtlasEpica.Charts_of_The_Monomyth import Choice, If, Weighted_Choice, render

from AtlasActorLudi.AtlasAlusoris.Map_of_NonPlayer_Projections import Resolve_Legacy_Attribute


try:
	from AtlasEpica.Grimoire_of_Adventure import (
			Adventure,
			Area,
			Collapse_Frame,
			Forge_Oracle,
			Lair,
			npc_keys,
			)
except ImportError:
	#-- The flat spelling, from before AtlasEpica was a package.  Kept because
	#-- removing it is a change, not a recovery; it is a QST-0093.3 candidate.
	from Grimoire_of_Adventure import (
			Adventure,
			Area,
			Collapse_Frame,
			Forge_Oracle,
			Lair,
			npc_keys,
			)


PLOT_CHANCE = 0.55
	#-- How often a card advances the DM Character's business rather than
	#-- offering the table something incidental.

HOST_APPEARS_CHANCE = 0.35
	#-- Within a plot card, how often the DM Character shows up in person.

FALLBACK_LAIRS = ("Tower", "Temple", "Cave", "Manor")
	#-- What an Area nobody has written a Lodge entry for may still hold.

UNGATED_LAIR_WEIGHT = 2
	#-- Every Lair the Area allows stays possible, even with no key matching it.


#-- Which Area a DM Character's keys pull toward.  Each row is the keys that
#-- open it, the Area, and its weight; a row whose keys are "" is a default
#-- used only when nothing else matched.
_AREA_SPEC = [
		(
			(
				"ANY",
				"Druid",
				"Ranger",
				"Treant",
				"Dryad",
				"Elf",
				),
			"Forest",
			12,
			),
		(
			(
				"ANY",
				"Criminal",
				"Thief",
				"Assassin",
				"Spy",
				),
			"Urban",
			10,
			),
		(
			(
				"ANY",
				"Criminal",
				"Smuggler",
				),
			"Coast",
			6,
			),
		(
			(
				"ANY",
				"Cultist",
				"Cleric",
				"Priest",
				"Paladin",
				),
			"Dungeon",
			8,
			),
		(
			(
				"ANY",
				"Cultist",
				"Cleric",
				),
			"Urban",
			4,
			),
		(
			(
				"ANY",
				"Wizard",
				"Sorcerer",
				"Warlock",
				"Mage",
				"Scholar",
				),
			"Urban",
			8,
			),
		(
			(
				"ANY",
				"Vampire",
				"Undead",
				"Skeleton",
				"Ghost",
				"Lich",
				"Necromancer",
				),
			"Graveyard",
			12,
			),
		(
			(
				"ANY",
				"Vampire",
				"Undead",
				"Lich",
				),
			"Dungeon",
			8,
			),
		(
			(
				"ANY",
				"Dragon",
				"Wyrm",
				),
			"Mountain",
			12,
			),
		(
			("Dragon",),
			"Dungeon",
			4,
			),
		(
			(
				"ANY",
				"Sailor",
				"Pirate",
				"Merfolk",
				),
			"Coast",
			10,
			),
		(
			(
				"ANY",
				"Barbarian",
				"Giant",
				),
			"Mountain",
			6,
			),
		(
			("Barbarian",),
			"Forest",
			4,
			),
		(
			(
				"ANY",
				"Fighter",
				"Knight",
				"Soldier",
				),
			"Urban",
			5,
			),
		(
			("Monk",),
			"Mountain",
			5,
			),
		(
			("Monk",),
			"Urban",
			4,
			),
		(
			(
				"ANY",
				"Swamp",
				"Lizardfolk",
				"Bullywug",
				),
			"Swamp",
			10,
			),
		(
			(
				"ANY",
				"Desert",
				"Yuan-ti",
				),
			"Desert",
			8,
			),
		(
			"",
			"Dungeon",
			3,
			),
		(
			"",
			"Urban",
			3,
			),
		(
			"",
			"Forest",
			2,
			),
		]


#-- Which Lairs belong inside which Area.  A Lair not listed here cannot
#-- appear in that Area, whatever the keys say.
_LAIR_BY_AREA = {
		"Forest": ("Circle", "Tower", "Cave", "Temple"),
		"Urban": ("Manor", "Tower", "Temple", "Port Den", "Castle"),
		"Dungeon": ("Catacomb", "Temple", "Cave", "Tower"),
		"Swamp": ("Circle", "Cave", "Temple"),
		"Mountain": ("Cave", "Castle", "Tower", "Temple"),
		"Desert": ("Temple", "Tower", "Cave", "Manor"),
		"Coast": ("Port Den", "Manor", "Temple", "Cave"),
		"Graveyard": ("Catacomb", "Temple", "Manor", "Tower"),
		}


#-- Which Lair a DM Character's keys pull toward, once the Area is fixed.
_LAIR_SPEC = [
		(
			(
				"ANY",
				"Druid",
				"Ranger",
				),
			"Circle",
			14,
			),
		(
			(
				"ANY",
				"Wizard",
				"Sorcerer",
				"Warlock",
				"Mage",
				),
			"Tower",
			14,
			),
		(
			(
				"ANY",
				"Cultist",
				"Cleric",
				"Priest",
				),
			"Temple",
			14,
			),
		(
			(
				"ANY",
				"Vampire",
				"Knight",
				"Noble",
				"Fighter",
				),
			"Castle",
			10,
			),
		(
			(
				"ANY",
				"Vampire",
				"Undead",
				"Lich",
				),
			"Catacomb",
			12,
			),
		(
			(
				"ANY",
				"Criminal",
				"Smuggler",
				"Pirate",
				),
			"Port Den",
			14,
			),
		(
			("Dragon",),
			"Cave",
			14,
			),
		(
			(
				"ANY",
				"Criminal",
				"Assassin",
				),
			"Manor",
			8,
			),
		(
			("Monk",),
			"Temple",
			8,
			),
		]


def pick_area(keys, rng):
	"""Collapse Area from DM Character keys — Stories-style If + weighted Choice."""
	hits = [
			(area, weight)
			for conds, area, weight in _AREA_SPEC
			if conds not in ("", None)
			and If(
					keys,
					conds,
					)
			]

	#-- Nothing about this figure suggested a place, so the defaults answer.
	if not hits:
		hits = [
				(area, weight)
				for conds, area, weight in _AREA_SPEC
				if conds in ("", None)
				]

	return Weighted_Choice(hits, rng=rng)


def pick_lair(keys, area_name, rng):
	"""Collapse Lair from keys + Area — gated by If, then weighted."""
	allowed = set(_LAIR_BY_AREA.get(area_name, FALLBACK_LAIRS))

	hits = [
			(lair, weight)
			for conds, lair, weight in _LAIR_SPEC
			if lair in allowed and If(keys, conds)
			]

	#-- Every Lair the Area allows stays on the table, so a figure with no
	#-- matching keys still gets somewhere to be.
	for lair in allowed:
		hits.append((lair, UNGATED_LAIR_WEIGHT))

	return Weighted_Choice(hits, rng=rng)


#-- Lines the DM may read aloud if the party happens to fit.  They never
#-- assert what the party is; they offer an "if".
_PARTY_HOOKS = [
		(
			(
				"ANY",
				"Paladin",
				"Knight",
				),
			"If a Paladin or knight is among you, this moment may call their oath into the light.",
			),
		(
			(
				"ANY",
				"Cleric",
				"Priest",
				),
			"If a Cleric is among you, the sacred (or formerly sacred) here may answer them first.",
			),
		(
			("Monk",),
			"If a Monk is among you, a remnant of their order's discipline may be recognizable here.",
			),
		(
			(
				"ANY",
				"Fighter",
				"Soldier",
				"Barbarian",
				),
			"If a warrior is among you, a challenge of arms may find them before the others.",
			),
		(
			(
				"ANY",
				"Rogue",
				"Criminal",
				"Thief",
				),
			"If a Criminal or Rogue is among you, this face may have been looking for them specifically.",
			),
		(
			(
				"ANY",
				"Wizard",
				"Sorcerer",
				"Warlock",
				),
			"If an arcane caster is among you, a sigil here may itch behind their eyes.",
			),
		(
			(
				"ANY",
				"Druid",
				"Ranger",
				),
			"If a Druid or Ranger is among you, the land itself may prefer to speak through them.",
			),
		(
			(
				"ANY",
				"Dragonborn",
				"Dragon",
				),
			"If a Dragonborn is among you, this character may be related to their bloodline — or hunting it.",
			),
		(
			("Elf",),
			"If an Elf is among you, an old kinship or grudge may surface in a glance.",
			),
		(
			("Dwarf",),
			"If a Dwarf is among you, stonework or craft here may mean more to them than to the rest.",
			),
		]


def soft_party_hooks(keys, rng, at_most=2):
	"""Optional lines the DM may use if the table fits — never verifies a party."""
	matched = [line for conds, line in _PARTY_HOOKS if If(keys, conds)]

	if not matched:
		return []

	rng.shuffle(matched)
	return matched[:at_most]


#-- What a plot card can be about: the DM Character's business, pressing.
_PLOT_BEATS = (
		"People bound to {dm_character}'s cause move through the {area} — not yet the end, only pressure.",
		"Something belonging to {dm_character} is being taken, moved, or hidden near the {lair}.",
		"A rumor of {dm_character} draws steel and gossip alike; the {lair} feels closer than it should.",
		"{dm_character} appears — briefly — then leaves a thread the table can refuse to pull.",
		"Followers of {dm_character} ask a toll of silence, coin, or aid on the way toward the {lair}.",
		"Evidence of {dm_character}'s work marks the {area}: a ward, a wound, a warning — or a plea.",
		)


#-- What an incidental card can be about: the world, minding its own business.
_INCIDENTAL_BEATS = (
		"A traveler's cart blocks the way — mundane goods, and one sealed thing that should not be for sale.",
		"A skill of patience, wit, or nerve is asked for by the place itself — no dice named; the table decides how.",
		"A face tied to {dm_character}'s past waits with a question, not a blade.",
		"Weather, crowd, or stone shifts — the {area} takes a side for a breath.",
		"Someone offers help that may be kindness, bait, or both.",
		)


#-- One line of place, per Area, to open a card with.
_SETTING_LINES = {
		"Forest": "Leaves hush the path; the {lair} is a clearing the wood remembers.",
		"Urban": "Streets press close; the {lair} hides behind a polite door.",
		"Dungeon": "Below, the complex opens — corridors like held breath toward the {lair}.",
		"Swamp": "Mist and root; the {lair} sits where dry ground is a rumor.",
		"Mountain": "Wind shears the stone; the {lair} clings where maps go thin.",
		"Desert": "Heat and distance; the {lair} is a dark mouth in the glare.",
		"Coast": "Salt and rope; the {lair} smells of tar and secrets.",
		"Graveyard": "Names in stone; the {lair} keeps company with the quiet.",
		}

_DEFAULT_SETTING = "The place holds its breath around the {lair}."

_SCENE_LABELS = ("Merchant", "Witness", "Agent", "Rival", "Wanderer", "Petitioner")
	#-- What a minted face is to the scene.  A plot card never calls one a
	#-- Merchant: on plot business, that face is an Agent.


def _npc_url(npc):
	"""The sheet link for one scene NPC, canonical if it has both axes."""
	from AtlasActorLudi.AtlasAlusoris.Map_of_NonPlayer_Paths import nonplayer_hash

	race = str(getattr(npc, "race", "Human"))
	guild = str(getattr(npc, "char_class", "") or "")
	background = str(getattr(npc, "background", "") or "")
	level = int(getattr(npc, "level", 1))
	seed = int(getattr(npc, "seed", getattr(npc, "_seed", 0)))

	if guild and background:
		return "/" + nonplayer_hash(
				race=race,
				guild=guild,
				background=background,
				level=level,
				seed=seed,
				)

	#-- Neither axis, or only one: the older four-part path still opens a sheet.
	legacy_identity = background or guild or "Commoner"

	return (
		f"/npc/{quote(race, safe='')}/"
		f"{quote(legacy_identity, safe='')}/"
		f"{level}/{seed}"
		)


def _occupant(npc, kind, why, link_dm_character=False):
	"""One face in a scene, as a record the Companion can render and link."""
	#-- `link_bbeg` carries the same answer as `link_dm_character` under the
	#-- name it had before the DM Character stopped being assumed evil
	#-- (QST-0081.9).  Both are written so an older reader still works.
	return {
			"kind": kind,
			"name": str(getattr(npc, "name", "Someone")),
			"why_here": why,
			"link_dm_character": link_dm_character,
			"link_bbeg": link_dm_character,
			"npc_seed": int(getattr(npc, "seed", getattr(npc, "_seed", 0))),
			"npc_level": int(getattr(npc, "level", 1)),
			"npc_race": str(getattr(npc, "race", "Human")),
			"npc_guild": str(getattr(npc, "char_class", "") or ""),
			"npc_background": str(getattr(npc, "background", "") or ""),
			"npc_url": _npc_url(npc),
			"trait": str(
					Resolve_Legacy_Attribute(
							npc,
							"trait",
							"",
							)
					or
					""
					),
			"title": str(getattr(npc, "title", "") or ""),
			}


def _mint_npc(adventure, rng):
	"""One fresh NonPlayer near the Adventure's tier, or nothing if none can be."""
	#-- Two refusals, both silent on purpose: the generator may not be
	#-- installed, and summoning may fail.  A card without a real sheet behind
	#-- it is still a usable card, so a stranger stands in instead.
	try:
		from AtlasActorLudi.AtlasAlusoris import summon_nonplayer
	except ImportError:
		return None

	seed = rng.randint(1, 65536)
	level = max(1, adventure.level + rng.choice([*(-1, 0, 0, 1)]))

	try:
		return summon_nonplayer(
				level=level,
				seed=seed,
				light=True,
				)
	except Exception:
		return None


def _framed(adventure, rite: str):
	"""The Adventure with its Area and Lair settled, and the host it frames."""
	#-- Both public rites need the same two things to be true before they can
	#-- say anything, so both ask for them the same way.
	if adventure.dm_character is None:
		raise ValueError(f"{rite} requires adventure.dm_character")
	if adventure not in Area or adventure not in Lair:
		Collapse_Frame(adventure)

	return adventure.dm_character


def frame_briefing(adventure):
	"""DM frame when a DM Character is set: who, Area, Lair — no plot graph."""
	host = _framed(adventure, "frame_briefing")
	name = str(getattr(host, "name", "the figure"))
	title = str(getattr(host, "title", "") or "")
	race = str(getattr(host, "race", ""))
	guild = str(getattr(host, "char_class", ""))
	background = str(getattr(host, "background", ""))
	who = name if not title else f"{name}, {title}"
	bits = " ".join(
			part
			for part in (
					race,
					guild,
					background,
					)
			if part
			)

	lines = [
			"This is for the Dungeon Master eyes only.",
			"",
			f"Your DM Character is {who}" + (f" — {bits}." if bits else "."),
			"They frame the session — villain, Quest Master, contested guardian, or another role you choose.",
			f"Area: {adventure.area} (the wider place).",
			f"Lair: {adventure.lair} (their seat inside it).",
			"",
			"Generate a scene when you need inspiration. Each card is presentation only — the table owns what happens next.",
			]

	return "\n".join(lines)


def _a_stranger(adventure, host_name, label, nseed):
	"""The face a card shows when no real NonPlayer could be minted."""
	return {
			"kind": label,
			"name": "A stranger",
			"why_here": f"They are tangled with {host_name}'s affairs in the {adventure.area}.",
			"link_dm_character": False,
			"link_bbeg": False,
			"npc_seed": nseed,
			"npc_level": adventure.level,
			"npc_race": "Human",
			"npc_guild": "",
			"npc_background": "Commoner",
			"npc_url": f"/npc/Human/Commoner/{adventure.level}/{nseed}",
			"trait": "",
			"title": "",
			}


def _why_this_face_is_here(name, host_name, adventure, npc_keys_str, keys, rng):
	"""One reason a minted face stands in this scene, drawn from the fitting ones."""
	why_options = [
			f"{name} is drawn into {host_name}'s cause — as ally, rival, or casualty.",
			f"{name} arrived because the {adventure.lair} draws the curious and the desperate.",
			f"{name} carries a rumor that points toward {host_name}, whether they know it or not.",
			]

	if If(npc_keys_str, "Criminal") or If(keys, "Criminal"):
		why_options.append(
				f"If a Criminal is in your party, {name} may have been looking for them specifically."
				)

	return Choice(why_options, rng=rng)


def _hooks_for(occupants, keys, rng):
	"""Soft hooks for the party, plus one apiece for the faces on the card."""
	hooks = soft_party_hooks(keys, rng)

	for occ in occupants:
		#-- The DM Character is not a hook for the party to recognise.
		if occ.get("link_dm_character"):
			continue
		if occ.get("link_bbeg"):
			continue

		extra = soft_party_hooks(
				f"{occ.get('npc_race', '')} "
				f"{occ.get('npc_guild', '')} "
				f"{occ.get('npc_background', '')} "
				f"{occ.get('name', '')}",
				rng,
				at_most=1,
				)

		for line in extra:
			if line not in hooks:
				hooks.append(line)

	return hooks


def _card_prose(title, setting, beat_line, occupants, hooks):
	"""The card as the Companion prints it: place, beat, faces, offers."""
	lines = [
			f"Inspiration — {title}",
			"",
			setting,
			beat_line,
			"",
			"Present:",
			]

	for occ in occupants:
		extra = f" ({occ['title']})" if occ.get("title") else ""
		lines.append(f"  • {occ['kind']}: {occ['name']}{extra}")
		lines.append(f"    {occ['why_here']}")
		if occ.get("trait"):
			lines.append(f"    Trait: {occ['trait']}")
		lines.append("    (Open their sheet for the rest — join threads yourself.)")

	if hooks:
		lines.append("")
		lines.append("Soft hooks (use only if they fit your table):")
		for h in hooks:
			lines.append(f"  — {h}")

	lines.append("")
	lines.append("Presentation only. No prescribed ending. Leave the rest to the players.")

	return "\n".join(lines)


def _the_occupants(adventure, host, host_name, kind, keys, rng):
	"""Who stands in this scene: the DM Character in person, or a minted face."""
	if kind == "plot" and rng.random() < HOST_APPEARS_CHANCE:
		why = Choice(
				(
						f"This is {host_name} — pressure, not necessarily a finale.",
						f"{host_name} is here to advance their will; leave the ending to the table.",
						),
				rng=rng,
				)
		return [_occupant(host, "DM Character", why, link_dm_character=True)]

	npc = _mint_npc(adventure, rng)
	label = Choice(_SCENE_LABELS, rng=rng)

	if kind == "plot" and label == "Merchant":
		label = "Agent"

	if npc is None:
		return [
				_a_stranger(
						adventure,
						host_name,
						label,
						rng.randint(1, 65536),
						)
				]

	name = str(getattr(npc, "name", "Someone"))
	why = _why_this_face_is_here(
			name,
			host_name,
			adventure,
			npc_keys(npc),
			keys,
			rng,
			)

	return [_occupant(npc, label, why)]


def inspiration_card(adventure):
	"""
Collapse one inspiration card under the locked Area/Lair.
Always includes at least one scene NPC (or the DM Character) with a sheet link.
"""
	host = _framed(adventure, "inspiration_card")
	host_name = str(getattr(host, "name", "the figure"))
	keys = npc_keys(host)
	beat = adventure.card_index
	rng = adventure.fork_rng("card", beat, adventure.area, adventure.lair, keys)

	kind = "plot" if rng.random() < PLOT_CHANCE else "incidental"
	myth = {
			"dm_character": host_name,
			"bbeg": host_name,
			"area": adventure.area,
			"lair": adventure.lair,
			"setting": _SETTING_LINES.get(
					adventure.area, _DEFAULT_SETTING
					),
			"beat": list(_PLOT_BEATS if kind == "plot" else _INCIDENTAL_BEATS),
			}

	setting = render(myth["setting"], myth, keys, rng=rng)
	beat_line = render(Choice(myth["beat"], rng=rng), myth, keys, rng=rng)

	occupants = _the_occupants(
			adventure,
			host,
			host_name,
			kind,
			keys,
			rng,
			)
	hooks = _hooks_for(
			occupants,
			keys,
			rng,
			)

	title = f"{adventure.area} · {adventure.lair}"

	#-- Counted here, so the next card drawn from the same Adventure differs.
	adventure.card_index += 1

	return {
			"title": title,
			"kind": kind,
			"prose": _card_prose(
					title,
					setting,
					beat_line,
					occupants,
					hooks,
					),
			"occupants": occupants,
			"area": adventure.area,
			"lair": adventure.lair,
			"hooks": hooks,
			}


def dm_briefing(adventure, master_name="the Master", master_blurb=""):
	"""The name frame_briefing had before the DM Character was named as such."""
	#-- Both extra arguments are ignored: the briefing reads the Character.
	return frame_briefing(adventure)


def collapse_scene(adventure, **_kwargs):
	"""The name inspiration_card had while a card was called a scene."""
	return inspiration_card(adventure)


class _A_DM_Character:
	"""A framing Character, fixed, so the collapse can be proved repeatable."""

	def __init__(
			self,
			guild="Druid",
			background="Guide",
			race="Elf",
			):
		self.seed = 7
		self.level = 5
		self.race = race
		self.subrace = ""
		self.char_class = guild
		self.background = background
		self.title = "The Green"
		self.name = "Alaxandar"
		self.trait = "Speaks to trees as equals."


def _a_framed_session(host, seed=None):
	"""An Adventure framed by this Character, in the shape this Map expects.

	The `dm_character` seat is set here rather than by Forge_Oracle, because
	live Adventure still stores `bbeg` and QST-0081.9 is the open question of
	which name wins.  That questa says plainly: do not map the names in one
	file only.  So this Map keeps reading `dm_character`, and its own proof
	supplies one — which is also the honest statement of what is not yet true
	in the running application.
	"""
	adventure = (
		Forge_Oracle(host, seed=seed)
		if seed is not None
		else Forge_Oracle(host)
		)
	adventure.dm_character = host
	return adventure


def _self_test() -> None:
	"""One DM Character frames one session, and the same seed frames it twice."""

	#-- The original's own proof, kept (recovered from the .pyc).
	host = _A_DM_Character()
	adv = _a_framed_session(host)
	text = frame_briefing(adv)
	assert "Area:" in text and "Lair:" in text
	assert "DM Character" in text
	assert adv.area == "Forest", \
			f"A Druid Elf belongs in a Forest, not {adv.area}."

	card = inspiration_card(adv)
	assert card["occupants"], "card must mint a face"
	assert "Presentation only" in card["prose"]
	inspiration_card(adv)

	again = _a_framed_session(host, seed=7)
	assert again.area == adv.area and again.lair == adv.lair

	#-- The Lair a card lands in is one the Area allows.
	assert adv.lair in _LAIR_BY_AREA[adv.area], \
			f"{adv.lair} does not belong in a {adv.area}."

	#-- A card names its place, says who is present, and links their sheet.
	for field in ("title", "kind", "prose", "occupants", "area", "lair", "hooks"):
		assert field in card, f"A card must carry {field}."
	assert card["kind"] in ("plot", "incidental")
	assert card["title"] == f"{adv.area} \u00b7 {adv.lair}"
	for occ in card["occupants"]:
		assert occ["npc_url"].startswith("/"), \
				f"Every face carries a sheet link: {occ}"
		assert occ["link_bbeg"] == occ["link_dm_character"], \
				"The old and new link names must agree."

	#-- Successive cards from one Adventure differ, because the count advances.
	fresh = _a_framed_session(_A_DM_Character(), seed=99)
	drawn = [inspiration_card(fresh) for _ in range(4)]
	assert len({ card["prose"] for card in drawn }) > 1, \
			"Four cards in a row should not be one card."

	#-- The same seed draws the same cards: the same place, the same kind of
	#-- beat, the same framing prose.  What this Map decides is reproducible.
	#--
	#-- What is NOT checked here, and why: the occupant's trait.  A minted
	#-- NonPlayer keeps its name, Race and Guild across summons of the same
	#-- (level, seed) but draws a *different* personality line each time, so a
	#-- card shared by seed does not yet read identically.  That draw is
	#-- unseeded inside summon_nonplayer, not here; this Map already funnels
	#-- every choice of its own through the Adventure's forked RNG.
	twin = _a_framed_session(_A_DM_Character(), seed=99)
	repeated = [inspiration_card(twin) for _ in range(4)]

	def _what_this_map_decides(card):
		return (
			card["title"],
			card["kind"],
			card["area"],
			card["lair"],
			[occ["kind"] for occ in card["occupants"]],
			card["hooks"],
			)

	assert [
			_what_this_map_decides(card)
			for card in repeated
			] == [
			_what_this_map_decides(card)
			for card in drawn
			], "A session shared by seed must collapse to the same scenes."

	#-- The Area a figure pulls toward follows its keys, not chance alone.
	import random as _random

	for guild, expected in (
			("Druid", "Forest"),
			("Wizard", "Urban"),
			):
		places = {
				pick_area(guild, _random.Random(seed))
				for seed in range(40)
				}
		assert expected in places, \
				f"A {guild} should be able to end up in a {expected}: {places}"

	#-- A figure whose keys match nothing still gets somewhere to be.
	nowhere = pick_area("Nonesuch", _random.Random(3))
	assert nowhere in ("Dungeon", "Urban", "Forest"), \
			f"An unmatched figure falls back to a default Area, not {nowhere}."

	#-- A Lair is always one the Area allows, whatever the keys.
	for area_name, allowed in _LAIR_BY_AREA.items():
		for seed in range(8):
			chosen = pick_lair("Nonesuch", area_name, _random.Random(seed))
			assert chosen in allowed, \
					f"{chosen} is not a Lair a {area_name} allows."

	#-- An Area nobody wrote a Lodge entry for still yields a Lair.
	assert pick_lair("Druid", "Nowhere", _random.Random(1)) in FALLBACK_LAIRS

	#-- Party hooks are offers, never assertions, and never more than asked.
	hooks = soft_party_hooks("Druid Elf", _random.Random(5))
	assert len(hooks) <= 2
	for line in hooks:
		assert line.startswith("If "), \
				f"A hook offers an if, it does not assert: {line!r}"
	assert soft_party_hooks("Nonesuch", _random.Random(5)) == []
	assert len(soft_party_hooks("Druid Elf", _random.Random(5), at_most=1)) <= 1

	#-- Both rites refuse a session with nobody framing it.
	unframed = _a_framed_session(_A_DM_Character())
	unframed.dm_character = None
	for rite in (frame_briefing, inspiration_card):
		try:
			rite(unframed)
		except ValueError as refusal:
			assert "requires adventure.dm_character" in str(refusal), \
					f"{rite.__name__} was refused, but not for the right reason: {refusal}"
		else:
			raise AssertionError(
					f"{rite.__name__} should refuse a session with no DM Character."
					)

	#-- The two older names still answer.
	assert dm_briefing(adv) == frame_briefing(adv)
	assert "prose" in collapse_scene(adv)

	print("AtlasEpica.Map_of_Scenes self-test OK")


if __name__ == "__main__":
	_self_test()
