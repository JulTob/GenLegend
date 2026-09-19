"""
Grimoire_of_Guilds: the Guild construction body (GuildKit is its spec).

Guild = a D&D class / vocation.

Why "Guild"?
	Python's word ``class`` is overloaded.  The Tag family is Guild;
	the character sheet may still say Class.  Awaken keeps
	``char.char_class`` in sync for legacy Maps.

Thought pattern (read this before the code)
	1. Helper Tags name leanings and kit shapes in plain language —
	   Wise, LightlyArmored, Martial, Mage.  They are preferences and
	   kit facts, not exclusive locks.  A Wise Character leans Wisdom;
	   they may still grow Strength.
	2. Build_Guild is the one construction point for a 2024 Guild chassis
	   (hit die, saves, armor / weapon helpers, vocation, multiclass gains).
	3. Awaken stamps the Guild Tag, syncs the legacy primary string, and
	   applies the helper Tags so later Maps can ask
	   ``if char in Mage`` rather than parse class-name strings.
	4. Multiclass: a Character may carry several Guild Tags (budgeted).
	   ``char.char_class`` names the *primary* Guild for legacy Maps;
	   ``char.guild_levels`` records levels per Guild; ``Multiclassed``
	   marks the Character when more than one Guild is present.
	5. Level lessons are Training Tags (TrainingKit) — you train in a
	   Guild.  Legacy Map_of_Classes/Training still fills unmigrated ranks.

Usage
	from AtlasLusoris.GuildKit import Rogue, Apply_Guild, Join_Guild, Wise
	Rogue(char)
	assert char in Rogue and char in Guild
	assert char in Dexterous and char in Clever
	assert char.primary_ability == "DEX"
	Join_Guild(char, "Wizard", levels=2)  # multiclass dip
"""

from __future__ import annotations

from collections.abc import Iterable
from collections.abc import Mapping
from types import MappingProxyType

from TagKit import Action, Has, Imprint, Pre, Report, Tag, Tags, Underlay

from AtlasActorLudi.CharactersKit import Character
from AtlasActorLudi.ProficiencyKit import (
	Capability_Definition,
	Commit_Training_Gain,
	Ensure_Training_Record,
	Find_Training_Rank,
	Provenance,
	Training_Batch,
	Training_Grant,
	)
from AtlasInventarium.ToolsKit import MUSICAL_INSTRUMENTS


# How many Guild Tags one Character may carry (primary + dips).
# Generation still defaults to one Guild; Join_Guild uses this budget.
MAX_GUILDS = 3


# The ability-weight scale.  Declared here because the Guild root itself
# names its own band; the model that reads them is further down, under
# "Ability weights".
ABILITY_KEYS = (
	"STR",
	"DEX",
	"CON",
	"INT",
	"WIS",
	"CHA",
	)

WEIGHT_CLASS = 100
WEIGHT_SPECIALIZATION = 95
RANK_STEP = 10
WEIGHT_CASTING = 5
WEIGHT_ORIGIN = 1
PARITY_BONUS = 1.25


# ---------------------------------------------------------------------------
# Root Guild Tag
# ---------------------------------------------------------------------------


class Guild(Tag):
	"""
	Root Tag for character guilds (D&D 2024 classes / vocations).

	**The description composes.**  ``DESCRIPTION`` is ordinary public Tag data
	holding a layer's own paragraphs, and ``Describe`` is the Action that renders
	the whole stack.  Every layer -- this root, the concrete Guild, a
	Specialization, later a casting-ability variant or an Invocation --
	contributes to that one name through ``@Action @Underlay``, which is the
	composition mode the Doctrine requires when two Tags contribute one name.

	An Underlay receives the captured contribution beneath it, so one mechanism
	covers both things a patron might want:

	    extend   read what is beneath and add to it
	    crunch   answer with your own text and let the rest go

	Neither re-searches nor rebuilds the prior text.  Declare a layer with
	``Describe_Layer``, or through ``Build_Specialization``'s ``extends`` and
	``crunches`` arguments, whose names *are* the mode declaration.  Reading the
	result is ``character.Describe()``: the visible Overlay is already composed,
	and no caller needs to know how many layers made it.
	"""

	NAME = "Guild"
	DESCRIPTION = ""

	@Action
	@Underlay
	def __format__(
			target,
			prior,
			specification,
			):
		"""Render Guild identity from current Tag membership."""
		view = specification.strip().casefold()

		if view in (
			"guild",
			"class",
			):
			return Find_Guild( target )

		if view in (
			"specialization",
			"subclass",
			):
			return Find_Specialization( target )

		return prior( specification )

	@staticmethod
	def ABILITY_WEIGHT(
			char,
			source,
			):
		"""
		What this Guild's opinion about ability scores is worth, here.

		A Guild says what a Character is *for*, so the one they actually are
		outranks every origin and keeps its order intact.  A multiclass **dip**
		is a different matter: two levels of Wizard is a thing you did, not a
		thing you are, and it may nudge Intelligence without deciding that a
		Rogue rolls their best score there.  So a dip speaks with an origin's
		voice.  See ``ability_weights``.
		"""
		return (
			WEIGHT_CLASS
			if getattr(
					source,
					"NAME",
					None,
					) == getattr(
							char,
							"char_class",
							None,
							)
			else WEIGHT_ORIGIN
			)

	@Action
	def Describe(
			target,
			) -> str:
		"""
		The floor of the description stack, which is deliberately empty.

		A concrete Guild contributes its own paragraphs over this one, and every
		later layer extends or crunches that.  The root still has to contribute,
		because TagKit fails an ``@Underlay`` that finds nothing beneath it
		rather than inventing behavior, and a Guild with no paragraphs of its own
		must still accept layers.
		"""
		return Guild.DESCRIPTION

	@Pre
	def Character_Only(
			target,
			):
		return isinstance(
				target,
				Character,
				)

	@Pre
	def Guild_Budget(
			target,
			):
		"""Allow several Guilds — enough room for multiclass dips."""
		return sum(
				target in tag
				for tag in globals().get(
						"GUILDS",
						{},
						).values()
				) < MAX_GUILDS

# ---------------------------------------------------------------------------
# Helper Tags — leanings (preference, not exclusive)
# ---------------------------------------------------------------------------


class Ability_Leaning(Tag):
	"""
	A soft preference toward one ability.

	Membership means the Character's Guild leans this way for ASI,
	stat placement, and later choice heuristics — not that other
	abilities are forbidden.
	"""

	NAME = "Ability Leaning"
	ABILITY = ""

	@Pre
	def Character_Only(
			target,
			):
		return isinstance(
				target,
				Character,
				)


class Strong(Ability_Leaning):
	"""Prefers Strength."""

	NAME = "Strong"
	ABILITY = "STR"


class Dexterous(Ability_Leaning):
	"""Prefers Dexterity."""

	NAME = "Dexterous"
	ABILITY = "DEX"


class Hardy(Ability_Leaning):
	"""Prefers Constitution."""

	NAME = "Hardy"
	ABILITY = "CON"


class Clever(Ability_Leaning):
	"""Prefers Intelligence."""

	NAME = "Clever"
	ABILITY = "INT"


class Wise(Ability_Leaning):
	"""Prefers Wisdom."""

	NAME = "Wise"
	ABILITY = "WIS"


class Charming(Ability_Leaning):
	"""Prefers Charisma."""

	NAME = "Charming"
	ABILITY = "CHA"


_LEANING_BY_ABILITY = {
	"STR": Strong,
	"DEX": Dexterous,
	"CON": Hardy,
	"INT": Clever,
	"WIS": Wise,
	"CHA": Charming,
	}


# ---------------------------------------------------------------------------
# Helper Tags — armor training shapes
# ---------------------------------------------------------------------------


class Armor_Training(Tag):
	"""How the Guild expects the body to be protected."""

	NAME = "Armor Training"

	@Pre
	def Character_Only(
			target,
			):
		return isinstance(
				target,
				Character,
				)


class Unarmored(Armor_Training):
	"""No armor training (robe / discipline traditions)."""

	NAME = "Unarmored"


class LightlyArmored(Armor_Training):
	"""
	Light armor (and often no shields).

	The three armour trainings are a **ladder, declared by inheritance**, not
	three unrelated Tags: heavier training brings the lighter with it, so
	``char in LightlyArmored`` is true of a Fighter as well as a Rogue.  That
	is what lets anything asking "was this Character trained to wear armour?"
	ask one Tag instead of testing three and getting the order right.
	""" 

	NAME = "Lightly Armored"


class ModeratelyArmored(LightlyArmored):
	"""Light and medium armor, usually with shields."""

	NAME = "Moderately Armored"


class HeavilyArmored(ModeratelyArmored):
	"""All armor and shields — the heavy line."""

	NAME = "Heavily Armored"


# ---------------------------------------------------------------------------
# Helper Tags — weapon kit
# ---------------------------------------------------------------------------


class Weapon_Training(Tag):
	"""Arms the Guild trains as a matter of course."""

	NAME = "Weapon Training"

	@Pre
	def Character_Only(
			target,
			):
		return isinstance(
				target,
				Character,
				)


class SimpleArms(Weapon_Training):
	"""Simple weapons."""

	NAME = "Simple Arms"


class MartialArms(Weapon_Training):
	"""Simple and Martial weapons — the full arms kit."""

	NAME = "Martial Arms"


class FinesseArms(Weapon_Training):
	"""
	2024 Rogue kit: Simple weapons, plus Martial weapons that have
	the Finesse or Light property.
	"""

	NAME = "Finesse Arms"


class LightMartialArms(Weapon_Training):
	"""
	2024 Monk kit: Simple weapons, plus Martial weapons that have
	the Light property.
	"""

	NAME = "Light Martial Arms"


# ---------------------------------------------------------------------------
# Helper Tags — vocation shape (optimization / choice heuristics)
# ---------------------------------------------------------------------------


class Vocation(Tag):
	"""
	Broad vocation shape for choice and optimization.

	Martial, Mage, and Adept overlap with armor helpers on purpose:
	a ModeratelyArmored Adept (Ranger) is not the same thought as a
	HeavilyArmored Martial (Fighter).
	"""

	NAME = "Vocation"

	@Pre
	def Character_Only(
			target,
			):
		return isinstance(
				target,
				Character,
				)


class Martial(Vocation):
	"""Weapon-first vocation — the front line and skirmishers."""

	NAME = "Martial"


class Mage(Vocation):
	"""Spell-first vocation — full casters and pact magic."""

	NAME = "Mage"


class Adept(Vocation):
	"""Hybrid vocation — half-casters, inventors, sacred warriors."""

	NAME = "Adept"


class Multiclassed(Tag):
	"""
	The Character walks more than one Guild path.

	Stamped when a second Guild joins.  Primary vocation for legacy
	Maps remains ``char.char_class``; per-Guild levels live in
	``char.guild_levels``.
	"""

	NAME = "Multiclassed"

	@Pre
	def Character_Only(
			target,
			):
		return isinstance(
				target,
				Character,
				)


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


_GUILD_DECLARATIONS: list[type[Guild]] = []


def _class_name(
		name: str,
		) -> str:
	return "".join(
			part.capitalize()
			for part in name.replace(
					"-",
					" ",
					).split()
			)


def _as_tag_tuple(
		value: type[Tag] | Iterable[type[Tag]] | None,
		) -> tuple[type[Tag], ...]:
	if value is None:
		return ()
	if isinstance(
			value,
			type,
			) and issubclass(
			value,
			Tag,
			):
		return (
				value,
				)
	return tuple(
			value
			)


def _validate_guild_construction(
		*,
		name: str,
		primary: str,
		secondary: str | None = None,
		hit_die: int,
		saves: tuple[str, str],
		) -> None:
	if not name or not name.strip():
		raise ValueError(
				"Build_Guild: name is required."
				)
	primary = primary.upper()
	if primary not in _LEANING_BY_ABILITY:
		raise ValueError(
				f"Build_Guild: unknown primary ability {primary!r}."
				)
	if secondary is not None:
		secondary = secondary.upper()
		if secondary not in _LEANING_BY_ABILITY:
			raise ValueError(
					f"Build_Guild: unknown secondary ability {secondary!r}."
					)
	if hit_die not in {
			6,
			8,
			10,
			12,
			}:
		raise ValueError(
				f"Build_Guild: unusual hit die {hit_die!r}."
				)
	if len(
			saves
			) != 2:
		raise ValueError(
				"Build_Guild: exactly two saving-throw proficiencies."
				)
	for save in saves:
		if save.upper() not in _LEANING_BY_ABILITY:
			raise ValueError(
					f"Build_Guild: unknown save {save!r}."
					)



def _ensure_guild_levels(
		char,
		) -> dict:
	"""Per-Guild level ledger for multiclass Characters."""
	levels = getattr(
			char,
			"guild_levels",
			None,
			)
	if not isinstance(
			levels,
			dict,
			):
		levels = {}
		char.guild_levels = levels
	return levels


def _grant_guild_tools(
		char,
		tag: type[Guild],
		) -> None:
	"""Resolve one Guild's typed Tool training exactly once."""
	tools = tuple(
		getattr(
			tag,
			"TOOLS",
			(),
			)
		)

	if not tools:
		return

	primary = getattr(
		char,
		"char_class",
		None,
		) in (
		None,
		tag.NAME,
		)
	count = int(
		getattr(
			tag,
			(
				"TOOL_PICKS"
				if primary
				else "MULTICLASS_TOOL_PICKS"
				),
			0,
			)
		)

	if count <= 0:
		return

	grant_id = f"Guild:{tag.__name__}:Tools"
	training = Ensure_Training_Record( char )

	if any(
		batch.grant_id == grant_id
		for batch in training.gains
		):
		return

	available = tuple(
		tool
		for tool in tools
		if Find_Training_Rank(
			char,
			tool,
			) is None
		)
	count = min(
		count,
		len( available ),
		)

	if count == 0:
		return

	dice = char.Dice_Bag(
		f"identity.guild.{tag.NAME}.tools",
		version="2024",
		namespace="GenLegendTraining",
		)
	selected = tuple(
		dice.sample(
			list( available ),
			k=count,
			)
		)

	Commit_Training_Gain(
		char,
		Training_Batch(
			grant_id=grant_id,
			feature=tag,
			grants=tuple(
				Training_Grant( tool )
				for tool in selected
				),
			provenance=Provenance(
				source="Guild",
				locator=tag.NAME,
				),
			)
		)


def _awaken_guild(
		char,
		tag: type[Guild],
		) -> None:
	"""
	Keep the primary and per-Guild level books honest.

	``char.char_class`` is the *primary* Guild for legacy Maps.
	A later Guild leaves that primary alone. Stable helper relations are
	expressed by the Guild Shape's Bases; the outer application helper marks
	dynamic multiclass state after the Guild Tagging commits.
	"""
	levels = _ensure_guild_levels(
			char
			)
	if tag.NAME not in levels:
		levels[tag.NAME] = 1

	current = getattr(
			char,
			"char_class",
			None,
			)
	if not current:
		char.char_class = tag.NAME
	elif current == tag.NAME:
		char.char_class = tag.NAME

	_grant_guild_tools(
		char,
		tag,
		)


def _casting_ability_action(
		guild_name: str,
		):
	"""
	Which ability this Guild's magic answers to, as a contributed Action.

	Read from ``CASTING_ABILITY`` when asked rather than captured when built,
	because that table is declared after the Guilds are and because it must stay
	the only place the answer is written down.  It is emphatically *not* the
	Guild's primary ability: a Paladin leads with Strength and casts with
	Charisma, and a Fighter casts with nothing at all.

	A Specialization that casts where its Guild does not is honoured too, so an
	Eldritch Knight answers Intelligence.  This is the floor that a Casting
	Variant crunches; see ``Build_Casting_Variant``.  There is nothing here to
	extend, an ability being one answer rather than a stack of paragraphs.
	"""
	@Action
	def Casting_Ability(
			target,
			) -> str:
		return (
			SUBCLASS_CASTING_ABILITY.get(
					getattr(
							target,
							"subclass",
							None,
							)
					)
			or CASTING_ABILITY.get(
					guild_name,
					"",
					)
			)

	return Casting_Ability


def Describe_Layer(
		description,
		*,
		extend: bool,
		heading=None,
		):
	"""
	One layer of a Guild's description, as a contributed ``Describe``.

	Both composition modes are the same TagKit mechanism, ``@Action @Underlay``,
	and differ only in whether the captured prior contribution is called:

	``extend=True``
		the layer reads what is beneath and adds to it, so a Warlock of the
		Archfey still opens with the paragraphs every Warlock shares;

	``extend=False``
		the layer crunches, answering with its own text alone, for the rare
		layer that genuinely replaces the account beneath it.

	``description`` may be a string, or a callable taking the Character, for
	text that has to resolve against the sheet (a drawn patron title, a level, a
	pact ability).  Passing the mode as a required keyword is the point: the
	Doctrine asks that the composition mode be explicit wherever two Tags
	contribute one name, and this makes it impossible to leave implicit.

	``heading`` renders as a Markdown subtitle above this layer's own
	paragraphs, so a reader can see where one voice stops and the next begins.
	"""
	@Action
	@Underlay
	def Describe(
			target,
			prior,
			) -> str:
		own = str(
				description(
						target
						)
				if callable(
						description
						)
				else description
				)
		if own and heading:
			own = f"### {heading}\n\n{own}"

		if not extend:
			return own
		beneath = str(
				prior()
				or ""
				)
		if not beneath:
			return own
		if not own:
			return beneath
		return f"{beneath}\n\n{own}"

	return Describe


def Project_Guild_Description(
		character,
		) -> None:
	"""
	Head the Guild section with the composed description.

	This is the one caller of ``Describe``, and it asks the Character rather
	than any particular Tag: whatever layers are on -- the Guild's own
	paragraphs, a Specialization extending or crunching them, a casting-ability
	variant -- the visible Overlay is already the answer.  Nothing here knows
	how many layers there were.

	Like the Species entry it sits at level 0, carries no rule, and refreshes in
	place, because a layer may address the Character by ``{name}`` and the name
	is settled after features resolve.

	It is *placed* rather than appended.  The sheet renders one flat list in
	creation order, and every class Feature is created later than this runs, so
	appending would print the class's account of itself after its own rules.
	The entry goes immediately above the first ``Training:`` Feature, which is
	where every class keeps its lessons.
	"""
	from AtlasLusoris.FeaturesKit import Feature

	describe = getattr(
			character,
			"Describe",
			None,
			)

	if describe is None:
		return

	text = str(
			describe()
			or ""
			)

	if not text.strip():
		return

	# ``replace`` rather than ``format``, so that a brace anywhere else in the
	# prose is prose and not a crash.
	from AtlasLusoris.FeaturesKit import Name_Slots

	for slot, value in Name_Slots(
			character
			).items():
		text = text.replace(
				"{" + slot + "}",
				value,
				)

	# The qualified name heads the section: this is where a reader learns which
	# rules are underneath, so the Guild stays legible even when the Character
	# answers to something else.
	guild_name = casting_heading(
			character
			) or "Guild"
	source = "Guild"
	features = getattr(
			character,
			"features",
			None,
			)

	if features is None:
		features = character.features = []

	for feature in features:
		if getattr(
				feature,
				"source",
				None,
				) == source:
			feature.name = guild_name
			feature.description = text
			feature.level = 0
			feature.narrative = True
			return

	entry = Feature(
			name=guild_name,
		description=text,
		source=source,
		level=0,
		narrative=True,
		)
	lessons = [
		index
		for index, feature in enumerate(
				features
				)
		if str(
				getattr(
						feature,
						"source",
						"",
						)
				or ""
				).startswith(
						"Training:"
						)
		]
	features.insert(
			min(
					lessons
					)
			if lessons
			else len(
					features
					),
			entry,
			)


def Build_Guild(
		*,
		name: str,
		primary: str,
		secondary: str | None = None,
		hit_die: int,
		saves: tuple[str, str],
		armor: type[Tag] | Iterable[type[Tag]],
		weapons: type[Tag] | Iterable[type[Tag]],
		vocation: type[Tag] | Iterable[type[Tag]],
		leanings: Iterable[type[Tag]] | None = None,
		skill_picks: int = 2,
		tools: Iterable[Capability_Definition] = (),
		tool_picks: int = 0,
		multiclass_tool_picks: int = 0,
		alternate_primary: str | None = None,
		multiclass_gains: tuple[str, ...] = (),
		description: str = "",
		edition: str = "2024",
		source_title: str = "Player's Handbook (2024)",
		source_kind: str = "official-reference",
		) -> type[Guild]:
	"""
	Construct one 2024 Guild Tag with chassis Reports and helper Tags.

	``leanings`` defaults to the Soft Tags for primary then secondary —
	so a Cleric is Wise and Strong without repeating that prose.
	``alternate_primary`` (e.g. Fighter DEX) adds another leaning.
	``multiclass_gains`` records what a dip into this Guild grants.
	"""
	primary = primary.upper()
	secondary = secondary.upper() if secondary else None
	resolved_alternate = (
			alternate_primary.upper()
			if alternate_primary
			else None
			)
	resolved_saves = tuple(
		save.upper()
		for save in saves
		)
	resolved_tools = tuple( tools )

	if not all(
		isinstance(
			tool,
			Capability_Definition,
			)
		for tool in resolved_tools
		):
		raise TypeError(
			"Build_Guild: tools require Capability_Definition values."
			)

	if not (
		0 <= tool_picks <= len( resolved_tools )
		and 0 <= multiclass_tool_picks <= len( resolved_tools )
		):
		raise ValueError(
			"Build_Guild: Tool picks must fit the declared Tool pool."
			)
	_validate_guild_construction(
			name=name,
			primary=primary,
			secondary=secondary,
			hit_die=hit_die,
			saves=resolved_saves,
			)
	if (
			resolved_alternate is not None
			and resolved_alternate not in _LEANING_BY_ABILITY
			):
		raise ValueError(
				f"Build_Guild: unknown alternate primary "
				f"{resolved_alternate!r}."
				)

	armor_tags = _as_tag_tuple(
			armor
			)
	weapon_tags = _as_tag_tuple(
			weapons
			)
	vocation_tags = _as_tag_tuple(
			vocation
			)
	if leanings is None:
		leaning_keys = [
				primary,
				]
		if secondary:
			leaning_keys.append(secondary)
		if (
				resolved_alternate
				and resolved_alternate not in leaning_keys
				):
			leaning_keys.append(
					resolved_alternate
					)
		leaning_tags = tuple(
				_LEANING_BY_ABILITY[key]
				for key in leaning_keys
				)
	else:
		leaning_tags = tuple(
				leanings
				)

	# Order is readable: vocation → armor → arms → ability leanings.
	helpers = (
			*vocation_tags,
			*armor_tags,
			*weapon_tags,
			*leaning_tags,
			)

	guild_tag = None

	@Imprint
	def Awaken(
			target,
			):
		_awaken_guild(
				target,
				guild_tag,
				)

	@Action
	def primary_ability(
			target,
			) -> str:
		p = primary
		alt = resolved_alternate
		if alt is not None:
			scores = getattr(target, "AS", None)
			if scores is not None:
				val_p = getattr(scores, p.lower(), 10)
				val_alt = getattr(scores, alt.lower(), 10)
				if val_alt > val_p:
					return alt
		return p

	guild_tag = type(
			_class_name(
					name
					),
			(
					Guild,
					*helpers,
					),
			{
					"NAME": name,
					"DESCRIPTION": description,
					# The concrete Guild is itself a layer, over the root's
					# empty floor.  One mechanism the whole way up.
					"Describe": Describe_Layer(
							description,
							extend=True,
							),
					"Casting_Ability": _casting_ability_action(
							name
							),
					"PRIMARY": primary,
					"SECONDARY": secondary,
					"ABILITY_PREFERENCE": Report(
							tuple(
									dict.fromkeys(
											key
											for key in (
													primary,
													secondary,
													resolved_alternate,
													)
											if key
											)
									)
							),
					"HIT_DIE": Report(
							hit_die
							),
					"SAVES": Report(
							resolved_saves
							),
					"SKILL_PICKS": Report(
							skill_picks
							),
					"TOOLS": Report(
							resolved_tools
							),
					"TOOL_PICKS": Report(
							tool_picks
							),
					"MULTICLASS_TOOL_PICKS": Report(
							multiclass_tool_picks
							),
					"MULTICLASS_GAINS": Report(
							tuple(
									multiclass_gains
									)
							),
					"EDITION": Report(
							edition
							),
					"HELPERS": Report(
							helpers
							),
					"SOURCE_TITLE": Report(
							source_title
							),
					"SOURCE_KIND": Report(
							source_kind
							),
					"Awaken": Awaken,
					"primary_ability": primary_ability,
					"__module__": __name__,
					},
			)

	_GUILD_DECLARATIONS.append(
			guild_tag
			)
	return guild_tag


# ---------------------------------------------------------------------------
# PHB 2024 Guilds — Core Traits chassis (features / subclasses later)
# ---------------------------------------------------------------------------


def _PHB_Guild(
		**record,
		) -> type[Guild]:
	return Build_Guild(
			edition="2024",
			source_title="Player's Handbook (2024)",
			source_kind="official-reference",
			**record,
			)


BARBARIAN_DESCRIPTION = """Rage is more than just anger. What you carry is more primal: the patience of a predator, the turn of a storm, the cold weight of a sea. You will not be tamed. Your Rage is your will, expressed. You rage for life. Rage against death. Rage against being tamed. Rage to protect your people. Barbarians we are, for we live out our inner nature.

When it comes, you do not lose control. You lose hesitation. You see further, you move sooner, you fixate on your enemy. You move by instinct, without thought, without grace, directly to where you want to hit. Then you run into danger fist first, because someone has to, and because you can.

Nobody agrees what this Rage is. Some name a spirit. Some name a blessing, or a legacy. Some say it is the world's own pain, finding a mouth at last. Maybe they are all right, maybe they are all wrong. You do not have to understand it. You have to feel it."""


Barbarian = _PHB_Guild(
		name="Barbarian",
		description=BARBARIAN_DESCRIPTION,
		primary="STR",
		secondary="CON",
		hit_die=12,
		saves=(
				"STR",
				"CON",
				),
		armor=ModeratelyArmored,
		weapons=MartialArms,
		vocation=Martial,
		skill_picks=2,
		multiclass_gains=(
				"Hit Point Die",
				"Martial weapons",
				"Shields",
				),
		)

# Julio's, settled in the wiki (Class: Bard).  The Bard's core is
# **attention**, and it runs both ways: you command it, and you pay it.
# "All eyes on you" is the first direction, "you have eyes on them" the
# second.  The Bard notices, recalls and works it out; it never steals.
#
# The register is the stadium song and the text is shaped like one: two
# hooks around a turn, with the refrain returning changed.  "The show is
# on" opens and "The show goes on" closes, and the second is the promise
# the first only implied.
#
# Every line is meant to read twice, as a stage direction and as an order
# given in a fight.  "Start the beat" is a count-in or the rhythm of a
# melee.  "All eyes on you" is an audience or a rank of enemies choosing a
# target.  The ambiguity is the class: attention does not care which room
# it is in.  The close pays for all of it, because the bow is only taken
# by someone who is still standing to take it.
#
# Nothing here restates a rule.  The lessons carry those, each under its
# own line, also Julio's.
#
# Breaks are explicit per Documenta/Canon/Feature-Text.md.  This is a
# song.  A renderer that reflowed it would destroy the verses.
BARD_DESCRIPTION = (
	"Start the beat.<br>"
	"Put on a smile.<br>"
	"The show is on.\n\n"
	"All eyes on you.<br>"
	"And you have eyes on them.<br>"
	"You get your spotlight. That is all you need.<br>"
	"Time to show your own kind of magic.\n\n"
	"You have heard this one before. You remember how it ends.<br>"
	"Then the beat stops. Take a bow. The show goes on.<br>"
	"You will live this life for another day."
	)


Bard = _PHB_Guild(
		name="Bard",
		description=BARD_DESCRIPTION,
		primary="CHA",
		secondary="DEX",
		hit_die=8,
		saves=(
				"DEX",
				"CHA",
				),
		armor=LightlyArmored,
		weapons=SimpleArms,
		vocation=Mage,
		skill_picks=3,
		tools=MUSICAL_INSTRUMENTS,
		tool_picks=3,
		multiclass_tool_picks=1,
		multiclass_gains=(
				"Hit Point Die",
				"One skill",
				"One Musical Instrument",
				"Light armor",
				),
		)

Cleric = _PHB_Guild(
		name="Cleric",
		primary="WIS",
		secondary="STR",
		hit_die=8,
		saves=(
				"WIS",
				"CHA",
				),
		armor=ModeratelyArmored,
		weapons=SimpleArms,
		vocation=Adept,
		skill_picks=2,
		multiclass_gains=(
				"Hit Point Die",
				"Light armor",
				"Medium armor",
				"Shields",
				),
		)

Druid = _PHB_Guild(
		name="Druid",
		primary="WIS",
		secondary="CON",
		hit_die=8,
		saves=(
				"INT",
				"WIS",
				),
		armor=ModeratelyArmored,
		weapons=SimpleArms,
		vocation=Adept,
		skill_picks=2,
		multiclass_gains=(
				"Hit Point Die",
				"Light armor",
				"Medium armor",
				"Shields",
				),
		)

FIGHTER_DESCRIPTION = """Nobody gave you this. Everyone else was given something. You were not. You made yourself.

You got up at dawn and swung a piece of metal at a post until your hands split. Then you wrapped them and did it again. Every weapon you could lift. Every tactic anyone would teach. Every stance, until fatigue arrives. But you don't stay down.

There is no secret. That is the secret. You did the boring thing every day for years, so that when the danger comes you are still standing at the end of it. When Death comes for you, it will not collect. You don't stay down."""


Fighter = _PHB_Guild(
		name="Fighter",
		description=FIGHTER_DESCRIPTION,
		primary="STR",
		secondary="CON",
		# 2024: Strength *or* Dexterity as primary.
		alternate_primary="DEX",
		hit_die=10,
		saves=(
				"STR",
				"CON",
				),
		armor=HeavilyArmored,
		weapons=MartialArms,
		vocation=Martial,
		skill_picks=2,
		multiclass_gains=(
				"Hit Point Die",
				"Martial weapons",
				"Light armor",
				"Medium armor",
				"Shields",
				),
		)

Monk = _PHB_Guild(
		name="Monk",
		# 2024: Dexterity *and* Wisdom are primary; DEX leads placement.
		primary="DEX",
		secondary="WIS",
		hit_die=8,
		saves=(
				"STR",
				"DEX",
				),
		armor=Unarmored,
		weapons=LightMartialArms,
		vocation=Martial,
		skill_picks=2,
		multiclass_gains=(
				"Hit Point Die",
				),
		)

Paladin = _PHB_Guild(
		name="Paladin",
		primary="STR",
		secondary="CHA",
		hit_die=10,
		saves=(
				"WIS",
				"CHA",
				),
		armor=HeavilyArmored,
		weapons=MartialArms,
		vocation=Adept,
		skill_picks=2,
		multiclass_gains=(
				"Hit Point Die",
				"Martial weapons",
				"Light armor",
				"Medium armor",
				"Shields",
				),
		)

Ranger = _PHB_Guild(
		name="Ranger",
		primary="DEX",
		secondary="WIS",
		hit_die=10,
		saves=(
				"STR",
				"DEX",
				),
		armor=ModeratelyArmored,
		weapons=MartialArms,
		vocation=Adept,
		skill_picks=3,
		multiclass_gains=(
				"Hit Point Die",
				"Martial weapons",
				"Light armor",
				"Medium armor",
				"Shields",
				"One skill",
				),
		)

Rogue = _PHB_Guild(
		name="Rogue",
		primary="DEX",
		secondary="INT",
		hit_die=8,
		saves=(
				"DEX",
				"INT",
				),
		armor=LightlyArmored,
		weapons=FinesseArms,
		vocation=Martial,
		skill_picks=4,
		multiclass_gains=(
				"Hit Point Die",
				"One skill",
				"Thieves' Tools",
				"Light armor",
				),
		)

Sorcerer = _PHB_Guild(
		name="Sorcerer",
		primary="CHA",
		secondary="CON",
		hit_die=6,
		saves=(
				"CON",
				"CHA",
				),
		armor=Unarmored,
		weapons=SimpleArms,
		vocation=Mage,
		skill_picks=2,
		multiclass_gains=(
				"Hit Point Die",
				),
		)

WARLOCK_DESCRIPTION = """A single moment changed your life forever. Now it marks every choice you have made since. You swore a covenant, sealed a pact, or uncovered a key never meant for you. Power was the payment you received. That moment you heard the voice, like a dream, and felt the presence. Doubtful and curious, you accepted. By word, by blood, or by a simple honest smile. The pact is now a bond that cannot be unmade without breaking the laws of magic themselves.

Every time you reach, something reaches back. Every time you were in danger, it granted its power. Every time you needed it, it protected you. Some would call that love. You know better: you are an investment worth protecting. You are still useful.

It has not asked for anything yet. Some nights you understand it does not need to ask. A game is being played, and you are just one of the pieces. Your patron is the player. You can only hope to be standing after the gambit resolves."""


Warlock = _PHB_Guild(
		name="Warlock",
		description=WARLOCK_DESCRIPTION,
		primary="CHA",
		secondary="CON",
		hit_die=8,
		saves=(
				"WIS",
				"CHA",
				),
		armor=LightlyArmored,
		weapons=SimpleArms,
		vocation=Mage,
		skill_picks=2,
		multiclass_gains=(
				"Hit Point Die",
				"Light armor",
				),
		)

# The Dao De Jing's chapter 48 with one word changed: 為學日益，為道日損, in
# the pursuit of learning something is gained every day, in the pursuit of the
# Way something is lost every day.  "Magic" stands where "the Way" stood, and
# the whole class follows from it.  The second paragraph is chapter 1, the name
# that can be named is not the eternal name, which is also where Le Guin got
# the true names of Earthsea.
#
# The thinning book is the same verse arriving at its conclusion, and it is
# deliberately NOT stated here: Canon/Dragons-and-the-Overcoming says the
# mechanism of Ascending is forgotten or kept quiet in-world, and a paragraph
# that has just argued the true thing cannot be written must not then write it.
# It lives as a reference in the features instead.
WIZARD_DESCRIPTION = """In the pursuit of learning, something is gained every day. In the pursuit of magic, something is lost every day.

No symbol has ever held a True Name. No wizard ever expected one to. A mark, a rune, a knot tied in a string, a scratch on a doorpost, those are notes left for the person you are going to be. A mark can be a sign to carry you back, and that turns out to be enough. Every page you have filled is one more argument against the entropy of memory.

Which is why you went out there in the first place. A map is irrelevant to someone who has never walked the road. A map is not a country. So you went out there, a long way from any library, walking towards the names you wanted to learn.

Wonder was never something a book could hold. Wonder is what happens to you in the world. The book is only how you carry the memory of it along."""

Wizard = _PHB_Guild(
		name="Wizard",
		description=WIZARD_DESCRIPTION,
		primary="INT",
		secondary="CON",
		hit_die=6,
		saves=(
				"INT",
				"WIS",
				),
		armor=Unarmored,
		weapons=SimpleArms,
		vocation=Mage,
		skill_picks=2,
		multiclass_gains=(
				"Hit Point Die",
				),
		)


# 2024 Artificer (Eberron: Forge of the Artificer).
Artificer = Build_Guild(
		name="Artificer",
		primary="INT",
		secondary="CON",
		hit_die=8,
		saves=(
				"CON",
				"INT",
				),
		armor=ModeratelyArmored,
		weapons=SimpleArms,
		vocation=Adept,
		skill_picks=2,
		multiclass_gains=(
				"Hit Point Die",
				"Tinker's Tools",
				"One skill",
				"Light armor",
				"Medium armor",
				"Shields",
				),
		edition="2024",
		source_title="Eberron: Forge of the Artificer (2024)",
		source_kind="official-reference",
		)


GUILDS = {
		tag.NAME: tag
		for tag in _GUILD_DECLARATIONS
		}

# Alias — sheet / Maps still say "class"
CLASSES = GUILDS


# ---------------------------------------------------------------------------
# Guild-owned Specialization Shapes
# ---------------------------------------------------------------------------


_SPECIALIZATION_TAGS_BY_GUILD: dict[
	str,
	dict[
		str,
		type[Guild],
		],
	] = {}
_SPECIALIZATION_NAMES_BY_GUILD: dict[
	str,
	tuple[str, ...],
	] = {}

SPECIALIZATIONS_BY_GUILD = MappingProxyType(
	_SPECIALIZATION_NAMES_BY_GUILD
	)


def Build_Specialization(
		*,
		guild: type[Guild],
		name: str,
		module: str,
		reports: Mapping[str, object] | None = None,
		awaken=None,
		after=None,
		extends=None,
		crunches=None,
		heading=None,
		) -> type[Guild]:
	"""
	Build one more-specific Shape of a concrete Guild Tag.

	``reports`` lets the owning Guild library publish only the context it
	actually has: progression, choices, magic, or another domain Report.
	``awaken`` materializes specialization-owned Records after the semantic
	Shape has been selected. ``after`` runs from the outer application rite,
	after the Tag transaction commits, for any follow-up Tag applications.

	``extends`` and ``crunches`` are the two description modes, and naming one
	is how a Specialization declares which it means.  ``extends`` keeps the
	Guild's own paragraphs and adds to them; ``crunches`` answers with its own
	text instead.  Either may be a string or a callable taking the Character.
	See ``Describe_Layer``.

	``heading`` puts a subtitle above this layer's paragraphs so a reader can
	see where the Guild stops speaking and the Specialization starts.  It is
	written per Guild rather than derived, because each one has its own word
	for the thing: a Warlock has a Patron, a Cleric a Domain, a Bard a
	College.  Omit it and the layer runs on unannounced.
	"""
	if guild not in GUILDS.values():
		raise ValueError(
			"Build_Specialization requires a registered concrete Guild."
			)
	if not name or not name.strip():
		raise ValueError(
			"Build_Specialization requires a name."
			)

	guild_name = guild.NAME
	catalogue = _SPECIALIZATION_TAGS_BY_GUILD.setdefault(
			guild_name,
			{},
			)

	if name in catalogue:
		raise ValueError(
			f"{guild_name} already declares Specialization {name!r}."
			)

	if (
		extends is not None
		and crunches is not None
		):
		raise ValueError(
			f"Specialization {name!r} must either extend or crunch its "
			"Guild's description, not both."
			)

	@Pre
	def Matching_Primary_Guild(
			target,
			):
		return getattr(
			target,
			"char_class",
			None,
			) == guild_name

	@Imprint
	def Set_Specialization(
			target,
			):
		target.specialization = name
		target.subclass = name
		if awaken is not None:
			awaken(
					target
					)

	namespace = {
		"__doc__": f"{name}, a more specific {guild_name} Guild Shape.",
		"__module__": module,
		"NAME": name,
		"GUILD_NAME": guild_name,
		"Matching_Primary_Guild": Matching_Primary_Guild,
		"Set_Specialization": Set_Specialization,
		# A Specialization speaks under its Guild, never over it: it may add an
		# ability the Guild never mentioned, and cannot displace the one the
		# Guild leads with.  Only a Specialization that declares its own
		# ``ABILITY_PREFERENCE`` is heard at all; inheriting the Guild's is not
		# a second vote for the Guild.
		"ABILITY_WEIGHT": WEIGHT_SPECIALIZATION,
		"_AFTER_SPECIALIZATION": after,
		}
	if extends is not None:
		namespace[
			"DESCRIPTION"
			] = extends
		namespace[
			"Describe"
			] = Describe_Layer(
				extends,
				extend=True,
				heading=heading,
				)
	elif crunches is not None:
		namespace[
			"DESCRIPTION"
			] = crunches
		namespace[
			"Describe"
			] = Describe_Layer(
				crunches,
				extend=False,
				heading=heading,
				)
	for report_name, report_value in (
			reports or {}
			).items():
		if (
			not report_name
			or report_name.startswith(
					"_"
					)
			):
			raise ValueError(
					"Specialization Report names must be public."
					)
		if report_name in namespace:
			raise ValueError(
					f"Specialization Report {report_name!r} conflicts "
					f"with the {name!r} Shape contract."
					)
		namespace[
			report_name
			] = Report(
				report_value
				)

	tag = type(
		_class_name(
			name
			),
		(
			guild,
			),
		namespace,
		)
	catalogue[
		name
		] = tag
	guild.SPECIALIZATIONS = tuple(
		catalogue.values()
		)
	_SPECIALIZATION_NAMES_BY_GUILD[
		guild_name
		] = tuple(
			catalogue
			)

	return tag


class Casting_Variant(Tag):
	"""
	Classifies the Guild layers that answer to a different ability.

	This is a Pin rather than a list: a Variant is classified by applying this
	Tag *to the Variant Tag*, and ``Casting_Variant[:]`` is then the catalogue.
	Nothing has to keep a register of which Guilds happen to have variants, and
	a new one is discoverable the moment it is declared.
	"""


def Build_Casting_Variant(
		*,
		guild: type[Guild],
		name: str,
		ability: str,
		module: str,
		weight: int = 5,
		title: str | None = None,
		extends=None,
		crunches=None,
		) -> type[Guild]:
	"""
	Build one kind of a Guild that answers to another ability.

	A Warlock's pact is with Charisma, and an Occultist's is with the same
	Guild's rules read by a scholar.  That is not a Specialization: the patron
	is a separate axis, and a Character carries one of each.  So this is a layer
	over the Guild, a sibling of the patron, and the two compose.

	It **crunches** ``Casting_Ability``: it contributes to the name the Guild
	already contributes to, through ``@Action @Underlay``, and answers without
	consulting what is beneath.  That is the composition mode the Doctrine
	requires, stated by not calling ``prior``.

	The ability scores follow from that one crunch and not from a second
	opinion: ``ability_weights`` rewrites the Guild's own casting ability into
	whatever ``Casting_Ability`` answers, so a Covenantor wants exactly what a
	Warlock wants with Wisdom standing where Charisma stood.  A Covenantor who
	rolled Wisdom 9 would be a bug rather than an easter egg.

	``weight`` is how often the draw lands here, out of a hundred; the Guild
	keeps whatever its Variants do not claim.  ``extends`` and ``crunches``
	describe this kind in prose, exactly as they do for a Specialization.
	"""
	if guild not in GUILDS.values():
		raise ValueError(
			"Build_Casting_Variant requires a registered concrete Guild."
			)
	if not name or not name.strip():
		raise ValueError(
			"Build_Casting_Variant requires a name."
			)
	if not ability or not ability.strip():
		raise ValueError(
			f"Casting Variant {name!r} requires an ability."
			)
	if (
		extends is not None
		and crunches is not None
		):
		raise ValueError(
			f"Casting Variant {name!r} must either extend or crunch its "
			"Guild's description, not both."
			)
	if weight < 0:
		raise ValueError(
			f"Casting Variant {name!r} cannot claim a negative share."
			)

	ability = ability.strip().upper()

	@Action
	@Underlay
	def Casting_Ability(
			target,
			prior,
			) -> str:
		"""Crunch: the Guild's own ability is not consulted."""
		return ability

	namespace = {
		"__doc__": (
			f"{name}, a {guild.NAME} whose magic answers to {ability}."
			),
		"__module__": module,
		"NAME": name,
		"GUILD_NAME": guild.NAME,
		"CASTING_ABILITY": ability,
		"CASTING_WEIGHT": int(
			weight
			),
		# What this kind is called, in the two places a class is named.  The
		# short one stands alone beside the patron ("Covenantor, Contract with
		# the Archfey"); the qualified one heads the class's own section, where
		# the Guild still has to be legible ("Covenantor (Warlock)").
		"TITLE": (
			title
			or name
			),
		"HEADING": (
			f"{title or name} ({guild.NAME})"
			),
		"Casting_Ability": Casting_Ability,
		}

	if extends is not None:
		namespace[
			"DESCRIPTION"
			] = extends
		namespace[
			"Describe"
			] = Describe_Layer(
				extends,
				extend=True,
				)
	elif crunches is not None:
		namespace[
			"DESCRIPTION"
			] = crunches
		namespace[
			"Describe"
			] = Describe_Layer(
				crunches,
				extend=False,
				)

	tag = type(
		_class_name(
			name
			),
		(
			guild,
			),
		namespace,
		)
	Casting_Variant(
		tag
		)

	return tag


def casting_variants(
		guild,
		) -> tuple[type[Guild], ...]:
	"""
	Every Casting Variant declared for one Guild, by name.

	Read off the Pin Field rather than a side list, so declaring a Variant is
	the only step needed to make it real.
	"""
	name = getattr(
			guild,
			"NAME",
			guild,
			)

	return tuple(
			sorted(
					(
						tag
						for tag in Casting_Variant[:]
						if getattr(
								tag,
								"GUILD_NAME",
								None,
								) == name
						),
					key=lambda tag: tag.NAME,
					)
			)


def casting_variant_on(
		char,
		) -> type[Guild] | None:
	"""
	The Casting Variant this Character carries, if any.

	Asks the Character rather than a register: a Variant is a committed leaf
	Tag, so it is already on the answer that TagKit gives for what classifies
	this Character.
	"""
	for tag in Tags(
			char
			):
		if tag in Casting_Variant:
			return tag

	return None


def Apply_Casting_Variant(
		char,
		name=None,
		) -> type[Guild] | None:
	"""
	Draw and apply which kind of this Guild the Character turns out to be.

	Drawn from a named, level-free bag, so it follows from the seed rather than
	from the order anything else happened in, and it never changes: a pact does
	not renegotiate its own terms at level 5.

	Called from ``Apply_Guild``, which is *before* the ability scores are rolled
	and before the Specialization lands.  Both matter.  The scores can then be
	built around the answer instead of the answer being forced onto a bad score,
	and the description layers stack in reading order: the Guild, then the kind
	of it, then the patron.

	Returns the Variant applied, or ``None`` for the plain Guild.
	"""
	guild_name = getattr(
			char,
			"char_class",
			None,
			)
	guild = GUILDS.get(
			guild_name
			)

	if guild is None:
		return None

	standing = casting_variant_on(
			char
			)

	if standing is not None:
		return standing

	variants = casting_variants(
			guild
			)

	if not variants:
		return None

	if name is not None:
		for tag in variants:
			if tag.NAME == name:
				tag(
					char
					)
				return tag
		raise ValueError(
			f"{guild_name} has no Casting Variant {name!r}."
			)

	claimed = sum(
			tag.CASTING_WEIGHT
			for tag in variants
			)
	# The Guild keeps whatever its Variants have not claimed, so the plain
	# Guild's share never has to be restated anywhere.
	options = (
		None,
		*variants,
		)
	weights = (
		max(
			0,
			100 - claimed,
			),
		*(
			tag.CASTING_WEIGHT
			for tag in variants
			),
		)
	def imprint(
			chosen,
			):
		if chosen is not None:
			chosen(
				char
				)

	chosen = char.Accept(
			options,
			weights,
			dice=char.Dice_Bag(
					"guild.casting.variant",
					version="1",
					namespace="GenLegendActor",
					),
			imprint=imprint,
			)

	return chosen


def casting_ability(
		char,
		) -> str:
	"""
	Which ability this Character's Guild magic answers to.

	One question, one answer, and the Character is the one asked.  Whether a
	Variant crunched it is not this caller's business, which is the point.
	"""
	answer = getattr(
			char,
			"Casting_Ability",
			None,
			)

	if answer is None:
		return ""

	return str(
			answer()
			or ""
			)


def _named(
		char,
		attribute: str,
		) -> str:
	"""Whichever name this Character's kind answers to, or the plain Guild."""
	variant = casting_variant_on(
			char
			)

	if variant is not None:
		return str(
				getattr(
						variant,
						attribute,
						variant.NAME,
						)
				)

	return str(
			getattr(
					char,
					"char_class",
					"",
					)
			or ""
			)


def casting_heading(
		char,
		) -> str:
	"""
	What heads the class's own section: ``Covenantor (Warlock)``.

	The Guild stays legible here, because this is where a reader finds out what
	the rules underneath actually are.
	"""
	return _named(
			char,
			"HEADING",
			)


def casting_title(
		char,
		) -> str:
	"""
	What stands beside the patron: ``Covenantor``, or plain ``Warlock``.

	The short form, for the line that already carries the subclass after it and
	would only be cluttered by repeating the Guild.  The Variant carries its own
	names, so nothing here maps abilities to titles.
	"""
	return _named(
			char,
			"TITLE",
			)


def Specialization_Choices(
		guild_name: str | None = None,
		) -> tuple[str, ...]:
	"""Return the Specialization Reports owned by one or every Guild."""
	if guild_name is not None:
		return SPECIALIZATIONS_BY_GUILD.get(
			guild_name,
			(),
			)

	return tuple(
		sorted(
			name
			for names in SPECIALIZATIONS_BY_GUILD.values()
			for name in names
			)
		)


def Specialization_Tag(
		guild_name: str,
		name: str,
		) -> type[Guild]:
	"""Resolve one Specialization Shape inside its Guild namespace."""
	try:
		return _SPECIALIZATION_TAGS_BY_GUILD[
			guild_name
			][
			name
			]
	except KeyError as error:
		raise KeyError(
			f"{guild_name!r} has no Specialization {name!r}."
			) from error


def specializations_on(
		character,
		) -> tuple[type[Guild], ...]:
	"""Return the Guild-owned Specialization Shapes carried by a Character."""
	return tuple(
		tag
		for catalogue in _SPECIALIZATION_TAGS_BY_GUILD.values()
		for tag in catalogue.values()
		if character in tag
		)


def Apply_Specialization(
		character,
		name: str | None = None,
		) -> type[Guild] | None:
	"""Apply an explicit or stable-random Shape of the primary Guild."""
	guild_name = getattr(
		character,
		"char_class",
		None,
		)
	available = Specialization_Choices(
		guild_name
		)

	if not available:
		character.specialization = None
		character.subclass = None
		return None

	selected_name = (
		name
		or getattr(
			character,
			"specialization",
			None,
			)
		or getattr(
			character,
			"subclass",
			None,
			)
		)

	if selected_name is None:
		current = specializations_on(
			character
			)
		if current:
			tag = current[ 0 ]
			selected_name = tag.NAME
		else:
			dice_bag = character.Dice_Bag(
				"identity.specialization",
				version="1",
				namespace="GenLegendClass",
				)
			tag = character.Accept(
				tuple(
					Specialization_Tag(
						guild_name,
						choice,
						)
					for choice in available
					),
				dice=dice_bag,
				)
			selected_name = tag.NAME
	else:
		if selected_name not in available:
			raise ValueError(
				f"{selected_name!r} is not a {guild_name!r} Specialization."
				)

		tag = Specialization_Tag(
			guild_name,
			selected_name,
			)
		current = specializations_on(
			character
			)

		if (
			current
			and tag not in current
			):
			raise ValueError(
				"A Character cannot carry two Specializations: "
				f"{current[0].NAME!r} and {tag.NAME!r}."
				)

		if character not in tag:
			tag(
				character
				)
	after = getattr(
		tag,
		"_AFTER_SPECIALIZATION",
		None,
		)
	if after is not None:
		after(
			character
			)

	return tag


from AtlasLusoris.AtlasOfGuilds import Load_Guild_Libraries

# Called by GuildKit, never here.  Every kit opens with
# ``from AtlasLusoris.GuildKit import Build_Specialization``, so the spec has
# to finish re-exporting this body before the first kit is imported.  GuildKit
# makes the call as its last statement.


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------


def guild_ability_prefs(
		char,
		):
	"""
	Primary / secondary ability keys for the rolled array.

	The two heaviest wants, from the one model, so the array a Character is
	built with and the raises it takes later agree by construction.  A
	Specialization that leans elsewhere, a Casting Variant that crunched the
	casting ability, a Background pulling at Constitution: all of them are
	already in the weights, and none of them is special-cased here.
	"""
	ordered = ability_preference(
			char
			)

	return (
		ordered[ 0 ] if len( ordered ) > 0 else None,
		ordered[ 1 ] if len( ordered ) > 1 else None,
		)


# Back-compat name used by early BackgroundKit wiring
class_ability_prefs = guild_ability_prefs


# ---------------------------------------------------------------------------
# Ability weights — the one dictionary every "choose a score" site draws from
#
# There used to be three models of the same opinion, and they disagreed: an
# ordered tuple decided the rolled array, a weight dictionary decided raises,
# and a (primary, secondary) pair decided which two rolls came first.  A
# Character could therefore want Charisma raised while its array was built for
# Strength.  There is now one model, and the other two are views of it.
#
# Every opinion is an **ordered** list of abilities, and every opinion carries
# the weight of whoever holds it:
#
#   100   a Guild, decaying by 10 a place, so its declared order survives
#         intact: first place always outranks second, and no accumulation of
#         lesser voices can reorder it
#    95   a Specialization that asks for something its Guild did not, which
#         lands between the Guild's first and second choice.  An Eldritch
#         Knight wants Intelligence before its Guild's Constitution, and still
#         wants Strength most: it is a Fighter
#     5   the ability this Character's magic answers to, and only where nothing
#         above ranked it at all
#     1   a Background, Species or Feat, and these *stack*: one origin asking
#         for Constitution is noise, three of them is a decision
#   x1.25 landing the score on an even number
#
# Parity multiplies rather than adds, so it can only amplify interest that
# already exists.  Added, it *created* interest: a dump stat at 9 scored the
# same as the class primary purely for being odd, and the Fighter raised CHA
# as often as STR.
#
# Weights are collected from the Tags the Character carries, each declaring
# ``ABILITY_PREFERENCE`` (what it wants) and ``ABILITY_WEIGHT`` (what its
# opinion is worth).  Nothing here knows that Guilds or Backgrounds exist.
# ---------------------------------------------------------------------------

# The stat a Guild casts with.  Held here rather than reached for through the
# spellcaster objects, which need a live Character before they will answer.
CASTING_ABILITY = {
	"Artificer": "INT",
	"Bard": "CHA",
	"Cleric": "WIS",
	"Druid": "WIS",
	"Paladin": "CHA",
	"Ranger": "WIS",
	"Sorcerer": "CHA",
	"Warlock": "CHA",
	"Wizard": "INT",
	}

# Subclasses that cast without their Guild doing so.
SUBCLASS_CASTING_ABILITY = {
	"Eldritch Knight": "INT",
	"Arcane Trickster": "INT",
	}

def _ability_opinions(
		char,
		) -> list[tuple[tuple[str, ...], int]]:
	"""
	Every opinion held about this Character's abilities, ordered, with weight.

	Collected from the Tags the Character carries rather than from any register.
	A Tag states what it wants in ``ABILITY_PREFERENCE`` and what its word is
	worth in ``ABILITY_WEIGHT``, and an opinion is counted once per Tag that
	*declares* it: a Specialization inherits its Guild's preference, and the
	Guild is not entitled to two votes for that.

	Origins that publish onto the Character rather than as a Tag are read from
	their attribute and weighed as origins.
	"""
	opinions: list[tuple[tuple[str, ...], int]] = []
	seen: set[int] = set()

	for tag in Tags(
			char
			):
		for source in tag.__mro__:
			preference = source.__dict__.get(
					"ABILITY_PREFERENCE"
					)

			if preference is None or id( source ) in seen:
				continue

			seen.add(
					id( source )
					)
			ordered = tuple(
					getattr(
							source,
							"ABILITY_PREFERENCE",
							(),
							)
					or ()
					)

			if not ordered:
				continue

			weight = getattr(
					source,
					"ABILITY_WEIGHT",
					WEIGHT_ORIGIN,
					)
			opinions.append(
					(
						ordered,
						int(
								weight(
										char,
										source,
										)
								if callable(
										weight
										)
								else weight
								),
						)
					)

	# Published onto the Character instead of carried as a Tag.
	for attribute in (
			"background_ability_preference",
			"species_ability_preference",
			"feat_ability_preference",
			):
		ordered = tuple(
				getattr(
						char,
						attribute,
						None,
						)
				or ()
				)

		if ordered:
			opinions.append(
					(
						ordered,
						WEIGHT_ORIGIN,
						)
					)

	return opinions


def _cast_where_the_guild_casts(
		char,
		ordered: tuple[str, ...],
		) -> tuple[str, ...]:
	"""
	Rewrite the Guild's own casting ability into whatever this Character casts.

	This is how a Casting Variant reaches the ability scores, and it is the same
	crunch it performs on ``Casting_Ability`` rather than a second opinion: a
	Covenantor is a Warlock who wants exactly what a Warlock wants, with Wisdom
	standing where Charisma stood.  Substituting keeps the Guild's *order*, so a
	half-caster is untouched -- a Paladin still opens with Strength however it
	prays.
	"""
	published = CASTING_ABILITY.get(
			getattr(
					char,
					"char_class",
					None,
					)
			)
	actual = casting_ability(
			char
			)

	if not published or not actual or published == actual:
		return ordered

	return tuple(
			actual
			if key == published
			else key
			for key in ordered
			)


def ability_weights(
		char,
		pool=None,
		amount: int = 1,
		) -> dict[str, int]:
	"""
	How much this Character wants each ability raised.

	The one model.  ``ability_preference`` and ``guild_ability_prefs`` are
	orderings of this dictionary, and every "choose a score" site -- the rolled
	array, an Ability Score Improvement, a feat's half-feat bump -- reads the
	same numbers, so they can no longer disagree about what a Character is for.

	``amount`` is the size of the raise being considered, because parity is
	worth nothing in the abstract: +1 lands an odd score on an even one, and
	+2 lands an even one.  Passing the real amount is what lets a single rule
	replace the old +2/+1 special case.
	"""
	keys = tuple(
		pool
		or ABILITY_KEYS
		)
	weights = {
		key: 0
		for key in keys
		}

	for ordered, weight in _ability_opinions(
			char
			):
		if weight >= WEIGHT_CLASS:
			ordered = _cast_where_the_guild_casts(
					char,
					ordered,
					)

		for place, key in enumerate(
				ordered
				):
			if key not in weights:
				continue

			weights[
				key
				] += (
					max(
							weight - place * RANK_STEP,
							1,
							)
					if weight >= WEIGHT_CLASS
					else weight
					)

	# Add +1 affinity for saving throws of active guilds
	for guild_tag in guilds_on(char):
		saves = getattr(guild_tag, "SAVES", ())
		for save in saves:
			if save in weights:
				weights[save] += 1


	# Only bites where nothing else ranked it.  A Guild that already places its
	# casting ability has said everything there is to say, and adding to it
	# there would let the nudge reorder a declared preference.
	casting = casting_ability(
			char
			)

	if (
		casting in weights
		and not weights[
				casting
				]
		):
		weights[
			casting
			] = WEIGHT_CASTING

	scores = getattr(
		char,
		"AS",
		None,
		)

	# Parity is a property of a *raise*: +1 onto an odd score buys a modifier
	# and onto an even one buys nothing.  Ranking what a Character is for is
	# not a raise, so ``amount=0`` asks the question without it.  Left in, the
	# multiplier reordered declared preferences -- a 95 landing even beat a 100
	# landing odd, and Rogues came out of the roller wanting Intelligence.
	if scores is not None and amount:
		for key in keys:
			if (
				int(
					getattr(
						scores,
						key,
						10,
						) or 10
					)
				+ amount
				) % 2 == 0:
				weights[key] = round(
					weights[key] * PARITY_BONUS
					)

	return weights


def pick_ability(
		char,
		pool,
		amount: int = 1,
		):
	"""Draw one ability from ``pool``, weighted by what the Character wants."""
	keys = list(
		pool
		)

	if not keys:
		return None

	weights = ability_weights(
		char,
		pool=keys,
		amount=amount,
		)
	wanted = [
		key
		for key in keys
		if weights[key] > 0
		]

	if wanted:
		return char.Pick(
			wanted,
			[
				weights[key]
				for key in wanted
				],
			)

	return char.Pick(
		keys
		)


def ability_preference(
		char,
		) -> tuple[str, ...]:
	"""
	Ability keys a Character prefers to raise, best first.

	A view of ``ability_weights``, not a second opinion: the abilities that
	anything wants, heaviest first, ties broken by the canonical order so the
	answer is stable for one Character.  Callers rank by position, so an
	ability nobody asked for simply sorts last.
	"""
	weights = ability_weights(
			char,
			amount=0,
			)

	return tuple(
			key
			for key in sorted(
					ABILITY_KEYS,
					key=lambda name: (
						-weights.get(
								name,
								0,
								),
						ABILITY_KEYS.index(
								name
								),
						),
					)
			if weights.get(
					key,
					0,
					) > 0
			)


def guilds_on(
		char,
		) -> tuple[type[Guild], ...]:
	"""Guild Tags currently carried by the Character."""
	return tuple(
			tag
			for tag in GUILDS.values()
			if char in tag
		)


def Find_Guild(
		char,
		) -> str:
	"""Find the narrative Guild label from current Tag membership."""
	return " / ".join(
		tag.NAME
		for tag in guilds_on(
			char
			)
		)


def Find_Specialization(
		char,
		) -> str:
	"""Find the narrative Specialization from current Tag membership."""
	carried = specializations_on( char )

	if len( carried ) > 1:
		raise ValueError(
			"A Character carries conflicting Specializations: "
			+ ", ".join(
				tag.NAME
				for tag in carried
				)
			+ "."
			)

	return (
		carried[ 0 ].NAME
		if carried
		else ""
		)


def Apply_Guild(
		char,
		name=None,
		*,
		as_primary: bool = False,
		):
	"""
	Apply a Guild Tag by name (default: char.char_class).

	Single-class generation uses this for the primary Guild.
	For a deliberate multiclass dip, prefer ``Join_Guild``.
	``as_primary=True`` reassigns the legacy ``char.char_class`` label.
	"""
	name = name or getattr(
			char,
			"char_class",
			None,
			)
	if not name:
		dice_bag = char.Dice_Bag(
			"identity.guild",
			version="1",
			namespace="GenLegendActor",
			)
		tag = char.Accept(
			tuple(
				GUILDS[ guild_name ]
				for guild_name in sorted(
					GUILDS
					)
				),
			dice=dice_bag,
			)
		name = tag.NAME
	else:
		tag = None
	if tag is None:
		tag = GUILDS.get(
			name
			)
	if tag is None:
		raise KeyError(
				f"GuildKit has no Tag for {name!r}"
				)
	if as_primary or not getattr(
			char,
			"char_class",
			None,
			):
		char.char_class = name
	if char not in tag:
		tag(
				char
				)
	elif as_primary:
		char.char_class = name

	if (
			len(
					guilds_on(
							char
							)
					) > 1
			and char not in Multiclassed
			):
		Multiclassed(
				char
				)

	# Which kind of this Guild the Character is, drawn here so that the ability
	# scores and the Specialization both arrive after the answer is known.
	Apply_Casting_Variant(
			char
			)

	return tag


def Join_Guild(
		char,
		name: str,
		*,
		levels: int = 1,
		as_primary: bool = False,
		) -> type[Guild]:
	"""
	Add or deepen a Guild for multiclass Characters.

	Does not yet rewrite spell slots or Training features — that is the
	next slice.  This API only prepares Tag membership, levels, and
	the Multiclassed mark so later Maps have a clean seam.
	"""
	if name not in GUILDS:
		raise KeyError(
				f"GuildKit has no Tag for {name!r}"
				)
	if levels < 1:
		raise ValueError(
				"Join_Guild: levels must be at least 1."
				)
	present = guilds_on(
			char
			)
	already = any(
			tag.NAME == name
			for tag in present
			)
	if (
			not already
			and len(
					present
					) >= MAX_GUILDS
			):
		raise ValueError(
				f"Join_Guild: at most {MAX_GUILDS} Guilds "
				f"(already {tuple(t.NAME for t in present)})."
				)
	tag = Apply_Guild(
			char,
			name,
			as_primary=as_primary,
			)
	ledger = _ensure_guild_levels(
			char
			)
	ledger[name] = max(
			int(
					levels
					),
			ledger.get(
					name,
					0,
					),
			)
	if len(
			guilds_on(
					char
					)
			) > 1 and char not in Multiclassed:
		Multiclassed(
				char
				)
	return tag


Apply_Class = Apply_Guild


def guild_hit_die(
		char_or_name,
		) -> int | None:
	"""
	Hit-die size from a Guild Tag, Character, or class name.

	For multiclass Characters, returns the *primary* Guild's die —
	full HP math across dips is a later Map concern.
	"""
	if isinstance(
			char_or_name,
			str,
			):
		tag = GUILDS.get(
				char_or_name
				)
	else:
		tag = GUILDS.get(
				getattr(
						char_or_name,
						"char_class",
						None,
						)
				)
	if tag is None:
		return None
	return tag.HIT_DIE


def guild_saves(
		char_or_name,
		) -> tuple[str, ...] | None:
	"""
	Saving-throw proficiencies from a Guild Tag, Character, or name.

	Multiclass Characters keep the *first* Guild's two saves (2024 rule);
	this helper still reads the primary Guild until a dedicated Map merges.
	"""
	if isinstance(
			char_or_name,
			str,
			):
		tag = GUILDS.get(
				char_or_name
				)
	else:
		tag = GUILDS.get(
				getattr(
						char_or_name,
						"char_class",
						None,
						)
				)
	if tag is None:
		return None
	return tuple(
			tag.SAVES
			)


# ---------------------------------------------------------------------------
# The public surface
# ---------------------------------------------------------------------------


# Vocabulary imported from elsewhere: re-exported for the callers that have
# always read it off GuildKit, but it belongs to its own home module.
_NOT_OURS = frozenset(
	{
		"annotations",
		"Iterable",
		"Mapping",
		"MappingProxyType",
		}
	)

__all__ = tuple(
	name
	for name in tuple(
		globals()
		)
	if (
		not name.startswith(
			"_"
			)
		and name not in _NOT_OURS
		)
	)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def _self_test():
	char = Character(
			seed=9
			)
	Rogue(
			char
			)
	assert char in Rogue and char in Guild
	assert Find_Guild( char ) == "Rogue"
	assert f"{char:Guild}" == "Rogue"
	assert f"{char:Class}" == "Rogue"
	assert char.char_class == "Rogue"
	assert Rogue.PRIMARY == "DEX"
	assert Rogue.SECONDARY == "INT"
	assert char in Dexterous and char in Clever
	assert char in LightlyArmored and char in Martial
	assert char in FinesseArms
	assert Rogue.SKILL_PICKS == 4
	assert Rogue.EDITION == "2024"
	assert Has(
			char,
			Rogue,
			Guild,
			)
	assert guild_ability_prefs(
			char
			) == (
			"DEX",
			"INT",
			)
	assert guild_hit_die(
			char
			) == 8
	assert guild_saves(
		"Warlock"
			) == (
			"WIS",
			"CHA",
			)
	warlock = Character(
		seed=13
		)
	Warlock( warlock )
	Project_Guild_Description( warlock )
	warlock_description = next(
		feature
		for feature in warlock.features
		if feature.source == "Guild"
		)
	assert warlock_description.narrative is True
	assert warlock_description.description.startswith(
		"A single moment changed your life forever."
		)

	# Multiclass preparation: primary Rogue, dip Wizard.
	Join_Guild(
			char,
			"Wizard",
			levels=2,
			)
	assert char.char_class == "Rogue"
	assert char in Wizard and char in Multiclassed
	assert char.guild_levels["Rogue"] == 1
	assert char.guild_levels["Wizard"] == 2
	assert guild_ability_prefs(
			char
			) == (
			"DEX",
			"INT",
			)
	assert {
			tag.NAME
			for tag in guilds_on(
					char
					)
			} == {
			"Rogue",
			"Wizard",
			}

	probe = Character(
			seed=10
			)
	probe.char_class = "Wizard"
	# Nothing is wanted yet: ability weights are collected from the Tags a
	# Character carries, and naming a Guild in a legacy string is not carrying
	# one.  The opinion arrives with the Tag.
	assert guild_ability_prefs(
			probe
			) == (
			None,
			None,
			)
	Apply_Guild(
			probe
			)
	assert guild_ability_prefs(
			probe
			) == (
			"INT",
			"CON",
			)
	assert probe in Wizard and Wizard.PRIMARY == "INT"
	assert probe in Mage and probe in Unarmored and probe in Clever

	smith = Character(
			seed=11
			)
	Artificer(
			smith
			)
	assert smith in Artificer and smith in Adept
	assert smith in ModeratelyArmored and smith in Clever and smith in Hardy
	assert Artificer.HIT_DIE == 8
	assert guild_saves(
			smith
			) == (
			"CON",
			"INT",
			)

	assert Bard.SKILL_PICKS == 3
	assert Ranger.SKILL_PICKS == 3
	monk = Character(
			seed=12
			)
	Monk(
			monk
			)
	assert monk in LightMartialArms
	assert Fighter.ABILITY_PREFERENCE == ("STR", "CON", "DEX")

	for name, tag in GUILDS.items():
		assert tag.PRIMARY and tag.SECONDARY
		assert tag.NAME == name
		assert tag.EDITION == "2024"
		assert tag.HIT_DIE in {
				6,
				8,
				10,
				12,
				}
		assert len(
				tag.SAVES
				) == 2
		assert tag.HELPERS
		assert tag.MULTICLASS_GAINS is not None

	assert "Artificer" in GUILDS
	assert len(
			GUILDS
			) == 13
	print(
			"OK — GuildKit self-test (2024 + multiclass prep)"
			)


if __name__ == "__main__":
	_self_test()
