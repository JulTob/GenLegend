"""
FeaturesKit

TOP implementation of Character features / feats / invocations.

Depends on: CharactersKit.Character

Parallel to CharactersKit
	Feature  — OOP skeleton (title, description, source) carried on the Character
	Trait / Feat / Origin_Feat / Invocation — Tags applied to the Character

Parameter naming
	Imprints and helpers take char — the Character that bears the grant.
	We avoid TOP's word agent here so it is not confused with "Character
	as Agent" in prose, or with other Agent meanings in the project.

When a Tag awakens, it:
	1. builds a Feature object (plain attributes, not @Record for fixed prose)
	2. carries it onto char.features (sheet text the user reads)
	3. records stable choices

Stateful effects that require later ledgers (skills, HP) are reconciled by
Resolve_Feature_Mechanics once those ledgers exist. They never become runtime
"can_*" engine flags.

This is a generator: Tags + Feature prose are the deliverable. Capability
booleans belong to a game engine; we do not store them.

The Grimoire_of_Features factories are legacy; new grants live here.
"""

from contextlib import redirect_stdout
from io import StringIO

from TopKit import Action, Imprint, Post, Pre, Record, Tag

from AtlasActorLudi.CharactersKit import Character
from AtlasActorLudi.ProficiencyKit import (
	Apply_Training_Record,
	Commit_Training_Gain,
	Feature_Training_Record,
	Find_Training_Rank,
	New_Feature_Training_Record,
	Provenance,
	Training_Batch,
	Training_Grant,
	Training_Rank,
	)
from AtlasActorLudi.SkillsKit import SKILLS, SKILLS_BY_KEY
from AtlasInventarium.ToolsKit import (
	ARTISAN_TOOLS,
	Thieves_Tools,
	GAMING_SETS,
	MUSICAL_INSTRUMENTS,
	TOOLS,
	TOOLS_BY_KEY,
	)


# ---------------------------------------------------------------------------
# Skeleton — the Feature object (sheet entry + grant identity)
# ---------------------------------------------------------------------------

def Name_Slots(
		char,
		) -> dict:
	"""
	What ``{name}`` and ``{full_name}`` mean in authored prose.

	``{name}`` is what you would call the Character to their face, so it is the
	first name alone.  ``{full_name}`` is the whole thing, for the rare line
	that wants the formality.  Defined once because both the Species entry and
	the Guild entry substitute into prose and must not drift apart.
	"""
	whole = str(
			getattr(
					char,
					"name",
					"",
					)
			or ""
			).strip()

	if not whole:
		return {
			"name": "them",
			"full_name": "them",
			}

	return {
		"name": whole.split()[0],
		"full_name": whole,
		}


def _project(
		source,
		subject,
		):
	"""Resolve one Entry or Chip value against the Character, if it is live."""
	return source( subject ) if callable( source ) else source


class Not_A_Chip( TypeError ):
	"""Something other than an ``AtlasVenustas.Chip`` was given as a chip."""


def _require_chip(
		chip,
		) -> None:
	"""One shape only (QST-0142 station 2): refuse anything else by name."""
	from AtlasVenustas import Chip
	if not isinstance(
			chip,
			Chip,
			):
		raise Not_A_Chip(
				f"{chip!r} is not a Chip; write Chip( symbol, label, value )."
				)


def _store_rail_chip(
		chip,
		live,
		):
	"""Keep a declared Chip, checking that a reader has a subject to read."""
	_require_chip(
			chip
			)
	live(
			chip.value,
			f"chip {chip.label!r}",
			)
	return chip


def _project_rail_chip(
		chip,
		subject,
		):
	"""The Chip read against the Character, its value rendered as text."""
	from dataclasses import replace
	return replace(
			chip,
			value=str(
					_project(
							chip.value,
							subject,
							)
					),
			)


def _chip_as_dict(
		chip,
		) -> dict:
	return {
			"label": chip.label,
			"value": chip.value,
			"symbol": chip.symbol,
			}


class Feature:
	"""
	One grant carried by a Character (trait, feat, or invocation line).

	**An Entry is a projection, not a snapshot.**  ``description`` and each
	Chip value may be a callable taking the Character, and it is resolved when
	the sheet is *read* rather than when the Feature is granted.  That ordering
	is the whole point: features are granted in level order, so a Feature
	granted at level 14 would otherwise freeze its text before a level-20
	capstone changed the numbers underneath it.  A Barbarian's Intimidating
	Presence printed a save DC two points low for exactly this reason, because
	Primal Champion raises Strength six levels after that Entry was written.

	**The invariant this depends on: an Entry callable must be a pure read.**
	It may look at anything on the Character and must decide nothing.  Anything
	that draws, picks or assigns belongs in ``apply``, which runs once, guarded,
	against a named Dice Bag.  An Entry that decided would silently re-decide
	every time the sheet was rendered.  (One did: the Druid's Primal Order.)
	"""

	def __init__(
			self,
			name="",
			description="",
			source="",
			level=0,
			apply=None,
			title=None,
			chips=None,
			narrative=False,
			subject=None,
			):
		self.title = title if title is not None else name
		self.name = self.title  # renderer / to_dict still read .name
		# The Character this Entry projects against.  Required whenever the
		# description or a Chip is callable, and checked below rather than
		# left to fail as an empty string at render time.
		self.subject = subject
		self.description = description
		self.source = source
		self.level = level
		self.apply = apply
		# Compact sheet values (e.g. Second Wind uses) — Entry stays in description.
		self.chips = chips
		self.narrative = bool( narrative )

	def _live(
			self,
			value,
			what,
			):
		if callable( value ) and self.subject is None:
			raise ValueError(
					f"Feature {self.name!r} was given a callable {what} but no "
					"subject to project it against. Pass subject=<Character>."
					)
		return value

	@property
	def description(self):
		return _project(
				self._description,
				self.subject,
				)

	@description.setter
	def description(
			self,
			value,
			):
		self._description = self._live(
				value,
				"description",
				)

	@property
	def chips(self):
		# Chip values are always rendered as text, so they are coerced here.
		# The renderer and ``to_dict`` have always received strings; projecting
		# lazily must not quietly start handing them ints.
		return tuple(
				_project_rail_chip(
						chip,
						self.subject,
						)
				for chip in self._chips
				)

	@chips.setter
	def chips(
			self,
			value,
			):
		self._chips = tuple(
				_store_rail_chip(
						chip,
						self._live,
						)
				for chip in ( value or () )
				)

	def __call__(self, char):
		if self.apply:
			self.apply(char)

	def __str__(self):
		return self.html()

	def html(self) -> str:
		# Chips belong on the sheet's left rail, not inside Entry prose.
		return f"""
		<div class="npc-textbox" style="grid-column: span 1; ">
			<h2 style="font-family: 'Manufacturing Consent' ; font-size:	1.8em;">
			{self.name}</h2>
		 {self.description}
		</div>
		"""

	def to_html(self) -> str:
		return self.html()

	def to_dict(self) -> dict:
		return {
			"name": self.name,
			"source": self.source,
			"level": self.level,
			"description": self.description,
			"chips": [
					_chip_as_dict(
							chip
							)
					for chip in self.chips
					],
			"narrative": self.narrative,
			}


def carry(char, feature: Feature) -> Feature:
	"""Append a Feature object onto the Character's grant list."""
	if getattr(char, "features", None) is None:
		char.features = []
	char.features.append(feature)
	return feature


def Grant_Resistance(
		char,
		*damage_types: str,
		) -> tuple[str, ...]:
	"""
	Make a Resistance true on the sheet, not merely described in the prose.

	Whatever names a Resistance should call this, so that anything reading
	``damage_resistances`` finds it without knowing whether a Dwarf, a pact or a
	Circle put it there.  Order is kept and repeats are dropped, so a Dragonborn
	of Cold ancestry with a Cold-resistant Circle still lists Cold once.

	The reason this exists is that a feature which only *says* it grants
	Resistance is invisible: it reads correctly and plays wrong.  That bug has
	been found four times in this codebase, in the Dwarf, the Dragonborn, the
	Celestial pact and the Sea Druid.
	"""
	current = tuple(
		getattr(
			char,
			"damage_resistances",
			(),
			) or ()
		)
	char.damage_resistances = tuple(
		dict.fromkeys(
			(
				*current,
				*(
					str(
						damage
						).strip()
					for damage in damage_types
					if damage
					),
				)
			)
		)

	return char.damage_resistances


def Grant_Resistance(
		char,
		*damage_types: str,
		) -> tuple[str, ...]:
	"""
	Make a Resistance true on the sheet, not merely described in the prose.

	Whatever names a Resistance should call this, so that anything reading
	``damage_resistances`` finds it without knowing whether a Dwarf, a pact or a
	Circle put it there.  Order is kept and repeats are dropped, so a Dragonborn
	of Cold ancestry with a Cold-resistant Circle still lists Cold once.

	The reason this exists is that a feature which only *says* it grants
	Resistance is invisible: it reads correctly and plays wrong.  That bug has
	been found four times in this codebase, in the Dwarf, the Dragonborn, the
	Celestial pact and the Sea Druid.
	"""
	current = tuple(
		getattr(
			char,
			"damage_resistances",
			(),
			) or ()
		)
	char.damage_resistances = tuple(
		dict.fromkeys(
			(
				*current,
				*(
					str(
						damage
						).strip()
					for damage in damage_types
					if damage
					),
				)
			)
		)

	return char.damage_resistances


def grant(
		char,
		name,
		description,
		source="Feat",
		level=0,
	apply=None,
	chips=None,
	narrative=False,
	) -> Feature:
	"""Build a Feature, optionally run apply, carry it on the Character."""
	feature = Feature(
		name=name,
		description=description,
		source=source,
		level=level,
		apply=apply,
		chips=chips,
		narrative=narrative,
		# The Character an Entry projects against.  Without it a callable
		# description cannot resolve, which is why Feature refuses one.
		subject=char,
		)
	if apply is not None:
		feature(char)
	return carry(char, feature)


# ---------------------------------------------------------------------------
# Tag roots — kinds of grant (applied to Character)
# ---------------------------------------------------------------------------

class Trait(Tag):
	"""Built-in grant from species, class, or background (not a chosen Feat)."""

	@Pre
	def Character_Only(char):
		return isinstance(char, Character)

	@Imprint
	def ensure_bag(char):
		if getattr(char, "features", None) is None:
			char.features = []


class Feat(Tag):
	"""Chosen feat. Tag identity is idempotent; repeat rules use Actions."""

	@Pre
	def Character_Only(char):
		return isinstance(char, Character)

	@Imprint
	def ensure_bag(char):
		if getattr(char, "features", None) is None:
			char.features = []


class Origin_Feat(Feat):
	"""Origin feat — backgrounds grant one; Human Versatile picks one."""


class Invocation(Tag):
	"""Reserved root — peel into InvocationKit when the list grows."""

	@Pre
	def Character_Only(char):
		return isinstance(char, Character)


# ---------------------------------------------------------------------------
# General skill ledger
# ---------------------------------------------------------------------------

CORE_SKILLS = tuple(
	skill.key
	for skill in SKILLS
	)


def _List_Names(
		capabilities,
		) -> str:
	names = [
		capability.name
		for capability in capabilities
		]

	if not names:
		return ""

	if len( names ) == 1:
		return names[ 0 ]

	if len( names ) == 2:
		return f"{names[0]} and {names[1]}"

	return (
		", ".join(
			names[ :-1 ]
			)
		+ f", and {names[-1]}"
		)


def Untrained_In(
		char,
		candidates,
		) -> tuple:
	"""The candidates this Character has yet to learn."""
	return tuple(
		capability
		for capability in candidates
		if Find_Training_Rank(
			char,
			capability,
			) is None
		)


def _Tool_Proficiency_Clause(
		gain,
		*,
		label: str = "Tool Proficiency",
		) -> str:
	"""
	Open a Feature's Entry with the training it actually granted.

	A pooled Feature can come up short, and can grant nothing at all, so this
	clause is written from the gain rather than from the Feature's promise.  No
	gain drops the clause entirely: a sheet reading "You have proficiency with
	." would be worse than one that never raises the subject, and the Feature's
	other benefits are unaffected either way.
	"""
	names = _List_Names(
		grant.capability
		for grant in (
			gain.grants
			if gain is not None
			else ()
			)
		)

	if not names:
		return ""

	return f"<b>{label}.</b> You have proficiency with {names}. <br>"


# ---------------------------------------------------------------------------
# RECOVERY NOTE 2026-08-30 -- Crafter / Musician training pool.  Read before
# editing, reverting, or restoring this file from vault bytecode.
#
# WHAT THIS IS.  Crafter and Musician each draw three capabilities from a pool
# (the sixteen Artisan's Tools, the ten Musical Instruments) while excluding
# whatever the Character's Background is about to grant.  The exclusion used to
# be computed from the Background's TOOLS field as though every entry in it were
# a certain grant.  It is not: a Background grants exactly ONE Tool, and most
# write that Tool as a sixteen-item menu or as a category name.  Excluding the
# whole menu emptied the pool, _Plan_Training raised, and the Imprint failed.
#
# WHAT IT COST.  The Artisan, Crafter and Entertainer Backgrounds were 100%
# unbuildable -- not intermittently, always.  It read as a ~7% random crash only
# because that is how often those Backgrounds came up in a draw.
#
# THE PAIR.  This is HALF of a two-file fix and neither half works alone:
#
#   1. HERE            Reserved_Background_Training reserves only what the
#                      Background is CERTAIN to grant (its two Skills, and its
#                      Tool only when there is exactly one option).  A choice
#                      reserves nothing.
#   2. BackgroundKit   _still_open() has the Background pick its Tool from what
#                      the Character has not learnt yet.  It runs AFTER the Feat
#                      and so knows what the Feat took, which is knowledge no
#                      reservation written in advance could have had.
#
# Restore or rewrite one without the other and you get back either the crash
# (drop 1) or duplicate Tool grants (drop 2).  Cross-reference:
# ``BackgroundKit._still_open``.
#
# WHY NOT A @Pre.  Making the Feat decline when its pool is short was considered
# and rejected.  _take_first_that_applies (FeatKit) only guards General feats;
# an Origin feat reaches a Character through Tag inheritance in Make_Background
# and through Grant_Origin_Feat, neither of which catches TagPreconditionError.
# A refusing @Pre would therefore trade one crash for another, and because a
# Background's Origin feat is not optional (Artisan *is* Crafter) it would have
# deleted three Backgrounds from the game.  Short grants are the answer instead;
# see _Plan_Training's allow_short.
# ---------------------------------------------------------------------------

def Background_Tool_Menu(
		background_tag,
		):
	"""
	The Tool capabilities one Background chooses between.

	A Background writes its Tool in one of three ways, and all three mean the
	same thing -- the Character ends up with exactly one of them.  It may name
	a single Tool, list a menu to pick from (the sixteen Artisan's Tools), or
	name a whole category ("Musical_Instrument", "Gaming_Set").  Answering in
	capabilities rather than in keys lets a caller reason about the choice
	without knowing which of the three spellings it was written in.
	"""
	if background_tag is None:
		return ()

	tools = getattr(
		background_tag,
		"TOOLS",
		(),
		) or ()

	if isinstance(
			tools,
			str,
			):
		if tools == "Musical_Instrument":
			return MUSICAL_INSTRUMENTS

		if tools == "Gaming_Set":
			return GAMING_SETS

		tools = (
			tools,
			)

	return tuple(
		capability
		for capability in (
			TOOLS_BY_KEY.get(
				key
				)
			for key in tools
			)
		if capability is not None
		)


def Reserved_Background_Training(
		background_tag,
		):
	"""
	Capabilities a Background is *certain* to grant after its Origin Feat Base.

	Certain is the whole of it.  A Background grants both of its Skills, but
	only ever one Tool, and most of them write that Tool as a menu or as a
	category name.  Reserving the menu counted one grant as sixteen and left
	the Origin Feat drawing from an empty pool, which is why Artisan, Crafter
	and Entertainer could not be built at all.

	A choice therefore reserves nothing here, and nothing is lost by that: the
	Background grants its Tool *after* the Feat, so ``BackgroundKit._grant_tool``
	sees what the Feat took and picks around it. That is knowledge no
	reservation written in advance could have had.
	"""
	if background_tag is None:
		return ()

	reserved = [
		capability
		for capability in (
			SKILLS_BY_KEY.get(
				key
				)
			or TOOLS_BY_KEY.get(
				key
				)
			for key in getattr(
				background_tag,
				"SKILLS",
				(),
				) or ()
			)
		if capability is not None
		]
	menu = Background_Tool_Menu(
		background_tag
		)

	# One option is not a choice, so it is as certain as a Skill.
	if len( menu ) == 1:
		reserved.extend( menu )

	return tuple( reserved )


def _Feature_Gains(
		char,
		feature,
		) -> tuple[Training_Batch, ...]:
	return New_Feature_Training_Record(
		char,
		feature,
		).gains


def _Next_Grant_Id(
		char,
		feature,
		) -> str:
	return (
		f"Feature:{feature.NAME}:"
		f"{len(_Feature_Gains(char, feature)) + 1}"
		)


def _Plan_Training(
		char,
		feature,
		candidates,
		count: int,
		*,
		source: str,
		purpose: str,
		grant_id: str | None = None,
		allow_trained: bool = False,
		rank: Training_Rank = Training_Rank.PROFICIENT,
		rank_for=None,
		exclude=(),
		allow_short: bool = False,
		) -> Training_Batch | None:
	excluded = set( exclude )
	pool = tuple(
		capability
		for capability in candidates
		if (
			capability not in excluded
			and (
				allow_trained
				or Find_Training_Rank(
					char,
					capability,
					) is None
				)
			)
		)

	# RECOVERY NOTE 2026-08-30: allow_short is what lets a Feature exist when
	# its pool cannot fill the whole count.  Do not "simplify" it back into an
	# unconditional raise: the raise is what made three Backgrounds unbuildable.
	# Callers that pass it (Crafter, Musician, Skilled) also handle the None
	# below and validate with at_most rather than count.
	if len( pool ) < count:
		if not allow_short:
			raise ValueError(
				f"{feature.__name__} requires {count} distinct training "
				f"choices; only {len(pool)} remain available."
				)

		# A Feature whose pool has run low grants what is left rather than
		# refusing to exist.  The Character earned the Feature; only the
		# breadth of its training is limited, and the Entry says so, because
		# it names the capabilities it actually granted.
		#
		# A pool with nothing left in it answers None rather than an empty
		# Batch: ProficiencyKit holds that a Batch grants something, and a
		# Feature that trained the Character in nothing did not gain one.
		if not pool:
			return None

		count = len( pool )

	resolved_id = (
		grant_id
		or _Next_Grant_Id(
			char,
			feature,
			)
		)
	dice = char.Dice_Bag(
		f"{purpose}.{resolved_id}",
		version="2024",
		namespace="GenLegendTraining",
		)
	selected = tuple(
		dice.sample(
			list(
				pool
				),
			k=count,
			)
		)

	return Training_Batch(
		grant_id=resolved_id,
		feature=feature,
		grants=tuple(
			Training_Grant(
				capability=capability,
				rank=(
					rank_for(
						char,
						capability,
						)
					if rank_for is not None
					else rank
					),
				)
			for capability in selected
			),
		provenance=Provenance(
			source=source,
			edition="2024",
			),
		)


def Plan_Feature_Training(
		char,
		feature,
		candidates,
		count: int,
		*,
		source: str,
		purpose: str,
		grant_id: str | None = None,
		allow_trained: bool = False,
		rank: Training_Rank = Training_Rank.PROFICIENT,
		rank_for=None,
		exclude=(),
		allow_short: bool = False,
		) -> Training_Batch | None:
	"""
	Plan a Feature gain from one homogeneous capability pool.

	Answers None only under ``allow_short``, and only when the pool holds
	nothing the Character has yet to learn.
	"""
	return _Plan_Training(
		char,
		feature,
		candidates,
		count,
		source=source,
		purpose=purpose,
		grant_id=grant_id,
		allow_trained=allow_trained,
		rank=rank,
		rank_for=rank_for,
		exclude=exclude,
		allow_short=allow_short,
		)


def New_Training_Batch(
		char,
		feature,
		grants,
		*,
		source: str,
		grant_id: str | None = None,
		) -> Training_Batch:
	"""Build one batch from capability grants already resolved by a Feature."""
	return Training_Batch(
		grant_id=(
			grant_id
			or _Next_Grant_Id(
				char,
				feature,
				)
			),
		feature=feature,
		grants=tuple(
			grants
			),
		provenance=Provenance(
			source=source,
			edition="2024",
			),
		)


def _Validate_Feature_Gain(
		gain,
		feature,
		*,
		count: int | None = None,
		at_most: int | None = None,
		) -> Training_Batch:
	"""
	Check one gain before it is committed.

	``count`` is an exact size, ``at_most`` a ceiling.  A Feature that draws
	from a pool takes the ceiling, because a pool can run dry: see
	``_Plan_Training``'s ``allow_short``.  A Feature whose grants are fixed by
	its own text keeps the exact count.
	"""
	if gain is None:
		# The pool held nothing left to teach.  See _Plan_Training.
		return None

	if not isinstance(
			gain,
			Training_Batch,
			):
		raise TypeError(
			f"{feature.__name__} requires a Training_Batch."
			)

	if gain.feature is not feature:
		raise ValueError(
			f"{feature.__name__} cannot commit a gain for "
			f"{gain.feature.__name__}."
			)

	if count is not None and len( gain.grants ) != count:
		raise ValueError(
			f"{feature.__name__} requires exactly {count} training grants."
			)

	if at_most is not None and len( gain.grants ) > at_most:
		raise ValueError(
			f"{feature.__name__} allows at most {at_most} training grants; "
			f"was given {len(gain.grants)}."
			)

	return gain


def _Training_Description(
		inspiration: str,
		batches,
		) -> str:
	grants = tuple(
		grant
		for batch in batches
		for grant in batch.grants
		)
	proficiencies = tuple(
		grant.capability
		for grant in grants
		if grant.rank is Training_Rank.PROFICIENT
		)
	expertise = tuple(
		grant.capability
		for grant in grants
		if grant.rank is Training_Rank.EXPERTISE
		)
	parts = [
		inspiration.strip()
		] if inspiration.strip() else []

	if proficiencies:
		parts.append(
			"You have proficiency in "
			f"{_List_Names(proficiencies)}."
			)

	if expertise:
		parts.append(
			"You have Expertise in "
			f"{_List_Names(expertise)}."
			)

	return "\n\n".join( parts )


# ---------------------------------------------------------------------------
# Species Traits (2024 Human)
# ---------------------------------------------------------------------------

class Resourceful(Trait):
	NAME = "Resourceful"
	DESCRIPTION = (
		# ``**the**`` rather than ``*the*``: inside an italic line a second
		# ``*`` nests <em> in <em>, which renders identically to the italic
		# around it, so the stress on "the" disappears exactly where it is
		# doing the work. <strong> inside <em> shows.
		"*Today is **the** day, my friend.*\n\n"
		"You have Heroic Inspiration after every Long Rest."
		)

	@Imprint
	def awaken(char):
		grant(
			char,
			name=Resourceful.NAME,
			description=Resourceful.DESCRIPTION,
			source="Species Feature",
			level=1,
			)


class Skillful(Trait):
	NAME = "Skillful"
	# Shared with Resolve_Skillful below, which overwrites this description
	# once the chosen skill is known -- the inspiration line has to survive
	# that rewrite, not just the placeholder text.
	INSPIRATION = (
		"*You learnt by trying.*"
		)
	# _Training_Description joins the inspiration and the proficiency with a
	# blank line, so the placeholder below has to do the same or the two forms
	# of this entry would be laid out differently.
	DESCRIPTION = (
		f"{INSPIRATION}\n\nYou have proficiency in one skill of your "
		"choice."
		)

	@Imprint
	def awaken(
			char,
			first_gain,
			):
		# RECOVERY NOTE 2026-08-30: allow_short was added here for the same
		# reason it exists on Crafter, Musician and Skilled -- a pooled
		# Feature must not raise when its pool runs dry.  Skillful draws one
		# Skill out of SKILLS, so it only empties for a Character who already
		# knows every Skill; rare, but "rare" is exactly what the Crafter crash
		# was mistaken for before it turned out to be certain.  A Human keeps
		# the Trait either way; only its one Skill is missing.
		gain = (
			first_gain
			or _Plan_Training(
				char,
				Skillful,
				SKILLS,
				1,
				source="Species Feature",
				purpose="identity.species.Human.skillful",
				allow_short=True,
				)
			)
		gain = _Validate_Feature_Gain(
			gain,
			Skillful,
			at_most=1,
			)
		batches = ()

		if gain is not None:
			Commit_Training_Gain(
				char,
				gain,
				)
			batches = (
				gain,
				)

		description = _Training_Description(
			Skillful.INSPIRATION,
			batches,
			)
		grant(
			char,
			name=Skillful.NAME,
			description=description,
			source="Species Feature",
			level=1,
			)

	@Record
	def skillful(
			char,
			) -> Feature_Training_Record:
		return New_Feature_Training_Record(
			char,
			Skillful,
			)

	@Post
	def Has_Skillful_Training(
			char,
			):
		# RECOVERY NOTE 2026-08-30: the second arm matches Crafter's and
		# Skilled's Postconditions.  Without it, a Character who knows every
		# Skill turns an empty pool into a TagPostconditionError instead of a
		# Trait that simply had nothing left to teach.
		return bool(
			char.skillful.gains
			) or not Untrained_In(
				char,
				SKILLS,
				)


class Versatile(Trait):
	NAME = "Versatile"
	DESCRIPTION = (
		"Whatever the moment called for, your people learned to "
		"become it. You gain one Origin feat of your choice. "
		"You must still meet its prerequisites."
		)


# ---------------------------------------------------------------------------
# Origin Feats
# ---------------------------------------------------------------------------

class Alert(Origin_Feat):
	NAME = "Alert"
	DESCRIPTION = (
		"<b>Initiative Proficiency.</b> Add your Proficiency Bonus to Initiative. "
		"<br><b>Initiative Swap.</b> After you roll Initiative, you may swap with a willing ally."
		)

	@Imprint
	def awaken(char):
		grant(char, Alert.NAME, Alert.DESCRIPTION, source="Origin Feat")


class Crafter(Origin_Feat):
	NAME = "Crafter"
	DESCRIPTION = (
		"<b>Tool Proficiency.</b> Proficiency with three Artisan's Tools. "
		"<br><b>Discount.</b> 20% off nonmagical items. "
		"<br><b>Fast Crafting.</b> You can craft items as part of a Long "
		"Rest and still receive the benefits."
		)

	@Imprint
	def awaken(
			char,
			first_gain,
			background_tag,
			):
		gain = (
			first_gain
			or _Plan_Training(
				char,
				Crafter,
				ARTISAN_TOOLS,
				3,
				source="Origin Feat",
				purpose="identity.feat.Crafter.tools",
				exclude=Reserved_Background_Training(
					background_tag
					),
				allow_short=True,
				)
			)
		gain = _Validate_Feature_Gain(
			gain,
			Crafter,
			at_most=3,
			)

		if gain is not None:
			Commit_Training_Gain(
				char,
				gain,
				)

		description = "".join(
			(
				_Tool_Proficiency_Clause(
					gain,
					),
				"<b>Discount.</b> 20% off nonmagical items. ",
				"<br><b>Fast Crafting.</b> You can craft items as part of "
				"a Long Rest and still receive the benefits.",
				)
			)
		grant(
			char,
			Crafter.NAME,
			description,
			source="Origin Feat",
			)

	@Record
	def crafter(
			char,
			) -> Feature_Training_Record:
		return New_Feature_Training_Record(
			char,
			Crafter,
			)

	@Post
	def Has_Crafter_Training(
			char,
			):
		# RECOVERY NOTE 2026-08-30: the "or not Untrained_In(...)" arm is load
		# bearing.  This Postcondition used to read bool(char.crafter.gains)
		# alone, which refused any Crafter that granted nothing and turned an
		# empty pool into a TagPostconditionError instead of a short grant.
		#
		# Training, unless there was none left to give.  A Character who
		# already knows the whole pool still earns Crafter: only the
		# training part of it is empty, and _Plan_Training says so by
		# answering None rather than by refusing.
		return bool(
			char.crafter.gains
			) or not Untrained_In(
				char,
				ARTISAN_TOOLS,
				)


class Healer(Origin_Feat):
	NAME = "Healer"
	DESCRIPTION = (
		"<b>Battle Medic.</b> With a Healer's Kit, tend a creature to restore hit points. "
		"Reroll 1s on healing dice."
		)

	@Imprint
	def awaken(char):
		grant(char, Healer.NAME, Healer.DESCRIPTION, source="Origin Feat")


class Lucky(Origin_Feat):
	NAME = "Lucky"
	DESCRIPTION = (
		"<b>Luck Points.</b> Equal to your Proficiency Bonus; regain on a Long Rest. "
		"<br><b>Advantage / Disadvantage.</b> Spend 1 Luck Point to gain Advantage on a d20 Test "
		"or impose Disadvantage on an attack against you."
		)

	@Imprint
	def awaken(char):
		grant(char, Lucky.NAME, Lucky.DESCRIPTION, source="Origin Feat")


class Magic_Initiate_Cleric(Origin_Feat):
	NAME = "Magic Initiate (Cleric)"
	DESCRIPTION = (
		"Two cantrips and one 1st-level spell from the Cleric list; "
		"cast the 1st-level spell once without a slot per Long Rest."
		)

	@Imprint
	def awaken(char):
		grant(
			char,
			Magic_Initiate_Cleric.NAME,
			Magic_Initiate_Cleric.DESCRIPTION,
			source="Origin Feat",
			)


class Magic_Initiate_Druid(Origin_Feat):
	NAME = "Magic Initiate (Druid)"
	DESCRIPTION = (
		"Two cantrips and one 1st-level spell from the Druid list; "
		"cast the 1st-level spell once without a slot per Long Rest."
		)

	@Imprint
	def awaken(char):
		grant(
			char,
			Magic_Initiate_Druid.NAME,
			Magic_Initiate_Druid.DESCRIPTION,
			source="Origin Feat",
			)


class Magic_Initiate_Wizard(Origin_Feat):
	NAME = "Magic Initiate (Wizard)"
	DESCRIPTION = (
		"Two cantrips and one 1st-level spell from the Wizard list; "
		"cast the 1st-level spell once without a slot per Long Rest."
		)

	@Imprint
	def awaken(char):
		grant(
			char,
			Magic_Initiate_Wizard.NAME,
			Magic_Initiate_Wizard.DESCRIPTION,
			source="Origin Feat",
			)


class Musician(Origin_Feat):
	NAME = "Musician"
	DESCRIPTION = (
		"<b>Instrument Training.</b> Proficiency with three Musical Instruments. "
		"<br><b>Encouraging Song.</b> After a Short or Long Rest, grant Heroic Inspiration "
		"to a number of allies equal to your Proficiency Bonus."
		)

	@Imprint
	def awaken(
			char,
			first_gain,
			background_tag,
			):
		gain = (
			first_gain
			or _Plan_Training(
				char,
				Musician,
				MUSICAL_INSTRUMENTS,
				3,
				source="Origin Feat",
				purpose="identity.feat.Musician.instruments",
				exclude=Reserved_Background_Training(
					background_tag
					),
				allow_short=True,
				)
			)
		gain = _Validate_Feature_Gain(
			gain,
			Musician,
			at_most=3,
			)

		if gain is not None:
			Commit_Training_Gain(
				char,
				gain,
				)

		description = "".join(
			(
				_Tool_Proficiency_Clause(
					gain,
					label="Instrument Training",
					),
				"<b>Encouraging Song.</b> After a Short or Long Rest, grant "
				"Heroic Inspiration to a number of allies equal to your "
				"Proficiency Bonus.",
				)
			)
		grant(
			char,
			Musician.NAME,
			description,
			source="Origin Feat",
			)

	@Record
	def musician(
			char,
			) -> Feature_Training_Record:
		return New_Feature_Training_Record(
			char,
			Musician,
			)

	@Post
	def Has_Musician_Training(
			char,
			):
		# RECOVERY NOTE 2026-08-30: the "or not Untrained_In(...)" arm is load
		# bearing.  This Postcondition used to read bool(char.musician.gains)
		# alone, which refused any Musician that granted nothing and turned an
		# empty pool into a TagPostconditionError instead of a short grant.
		#
		# Training, unless there was none left to give.  A Character who
		# already knows the whole pool still earns Musician: only the
		# training part of it is empty, and _Plan_Training says so by
		# answering None rather than by refusing.
		return bool(
			char.musician.gains
			) or not Untrained_In(
				char,
				MUSICAL_INSTRUMENTS,
				)


class Savage_Attacker(Origin_Feat):
	NAME = "Savage Attacker"
	DESCRIPTION = (
		"Once per turn when you hit with a weapon, roll the weapon's damage dice twice "
		"and use either result."
		)

	@Imprint
	def awaken(char):
		grant(
			char,
			Savage_Attacker.NAME,
			Savage_Attacker.DESCRIPTION,
			source="Origin Feat",
			)


# Craft and larceny only.  The rules allow any tool, but a generated Scribe
# turning up proficient in a lute and a deck of cards reads as clutter rather
# than as training.
SKILLED_POOL = (
	*SKILLS,
	*ARTISAN_TOOLS,
	Thieves_Tools,
	)


class Skilled(Origin_Feat):
	NAME = "Skilled"
	REPEATABLE = True
	# Shown only until Resolve_Skilled below can name the three actual skills.
	# This is a generator, not a character builder: the Dice Bag already made
	# every choice by the time the sheet prints, so nothing here should read
	# as though the player still has a pick to make.
	INSPIRATION = (
		"*You trained and studied, gaining a few skills along the way. "
		"Time will tell which of them you'll need.*"
		)
	DESCRIPTION = (
		f"{INSPIRATION}\n\nYou have proficiency in three skills."
		)

	@Imprint
	def awaken(
			char,
			first_gain,
			background_tag,
			):
		gain = (
			first_gain
			or Plan_Skilled_Gain(
				char,
				source="Origin Feat",
				background_tag=background_tag,
				)
			)
		gain = _Validate_Feature_Gain(
			gain,
			Skilled,
			at_most=3,
			)
		batches = ()

		if gain is not None:
			Commit_Training_Gain(
				char,
				gain,
				)
			batches = (
				gain,
				)

		description = _Training_Description(
			Skilled.INSPIRATION,
			batches,
			)
		grant(
			char,
			Skilled.NAME,
			description,
			source="Origin Feat",
			)

	@Record
	def skilled(
			char,
			) -> Feature_Training_Record:
		return New_Feature_Training_Record(
			char,
			Skilled,
			)

	@Action
	def Gain_Skilled(
			char,
			gain,
			) -> Training_Batch | None:
		gain = _Validate_Feature_Gain(
			gain,
			Skilled,
			at_most=3,
			)

		if gain is None:
			return None

		committed = Commit_Training_Gain(
			char,
			gain,
			)
		_update_feature_description(
			char,
			Skilled.NAME,
			_Training_Description(
				Skilled.INSPIRATION,
				char.skilled.gains,
				),
			"Origin Feat",
			)

		return committed

	@Post
	def Has_A_Gain(
			char,
			):
		# RECOVERY NOTE 2026-08-30: same shape as Crafter's Postcondition, and
		# load bearing for the same reason.  Skilled is REPEATABLE, so it is the
		# Feature most likely to meet a genuinely exhausted pool.
		#
		# See Crafter.Has_Crafter_Training: an exhausted pool is a legal,
		# if joyless, outcome.
		return bool(
			char.skilled.gains
			) or not Untrained_In(
				char,
				SKILLED_POOL,
				)


class Tavern_Brawler(Origin_Feat):
	NAME = "Tavern Brawler"
	DESCRIPTION = (
		"Enhanced unarmed strikes, improvised-weapon proficiency, "
		"reroll 1s on damage, and shove on a hit."
		)

	@Imprint
	def awaken(char):
		grant(
			char,
			Tavern_Brawler.NAME,
			Tavern_Brawler.DESCRIPTION,
			source="Origin Feat",
			)


class Tough(Origin_Feat):
	NAME = "Tough"
	DESCRIPTION = (
		"Hit point maximum increases by twice your level, "
		"and by 2 again whenever you gain a level."
		)

	@Imprint
	def awaken(char):
		Resolve_Tough( char )
		grant(char, Tough.NAME, Tough.DESCRIPTION, source="Origin Feat")


ORIGIN_FEATS = {
	"Alert": Alert,
	"Crafter": Crafter,
	"Healer": Healer,
	"Lucky": Lucky,
	"Magic Initiate (Cleric)": Magic_Initiate_Cleric,
	"Magic Initiate (Druid)": Magic_Initiate_Druid,
	"Magic Initiate (Wizard)": Magic_Initiate_Wizard,
	"Musician": Musician,
	"Savage Attacker": Savage_Attacker,
	"Skilled": Skilled,
	"Tavern Brawler": Tavern_Brawler,
	"Tough": Tough,
	}


def _update_feature_description(
	char,
	name,
	description,
	source,
	) -> None:
	for feature in getattr(
		char,
		"features",
		(),
		) or ():
		if (
			getattr(
				feature,
				"name",
				None,
				) == name
			and getattr(
				feature,
				"source",
				None,
				) == source
			):
			feature.description = description
			return


def Resolve_Skillful(
		char,
		):
	"""Compatibility route: project Skillful's typed Record to the old sheet."""
	if char not in Skillful:
		return None

	Apply_Training_Record( char )
	_update_feature_description(
		char,
		Skillful.NAME,
		_Training_Description(
			Skillful.INSPIRATION,
			char.skillful.gains,
			),
		"Species Feature",
		)

	return char.skillful.grants[ 0 ].capability.key


def Plan_Skilled_Gain(
		char,
		*,
		source: str,
		grant_id: str | None = None,
		background_tag=None,
		) -> Training_Batch | None:
	"""Resolve one legal Skilled acquisition before committing it."""
	return _Plan_Training(
		char,
		Skilled,
		SKILLED_POOL,
		3,
		source=source,
		purpose="identity.feat.Skilled.training",
		grant_id=grant_id,
		exclude=Reserved_Background_Training(
			background_tag
			),
		allow_short=True,
		)


def Acquire_Skilled(
		char,
		*,
		source: str = "Origin Feat",
		grant_id: str | None = None,
		) -> Training_Batch | None:
	"""Acquire Skilled once, or use its Action for a legal repeat gain."""
	gain = Plan_Skilled_Gain(
		char,
		source=source,
		grant_id=grant_id,
		)

	if char not in Skilled:
		Skilled(
			char,
			first_gain=gain,
			)
		return gain

	return char.Gain_Skilled( gain )


def Resolve_Skilled(
		char,
		):
	"""Compatibility route: project Skilled's typed Record to the old sheet."""
	if char not in Skilled:
		return ()

	Apply_Training_Record( char )
	_update_feature_description(
		char,
		Skilled.NAME,
		_Training_Description(
			Skilled.INSPIRATION,
			char.skilled.gains,
			),
		"Origin Feat",
		)

	return tuple(
		grant.capability.key
		for grant in char.skilled.grants
		)


def Resolve_Tough(
	char,
	) -> int:
	"""Bring Tough's hit-point contribution up to the current level."""
	if not hasattr(
		char,
		"base_health",
		):
		return 0

	required = 2 * max(
		1,
		int(
			getattr(
				char,
				"level",
				1,
				)
			),
		)
	applied = int(
		getattr(
			char,
			"_tough_health_bonus",
			0,
			)
		)
	increase = max(
		0,
		required - applied,
		)

	if increase:
		char.base_health += increase
		char._tough_health_bonus = (
			applied
			+ increase
			)

	return increase


def Resolve_Feature_Mechanics(
	char,
	) -> None:
	"""Project stateful feat and trait choices onto a completed sheet."""
	Apply_Training_Record( char )

	if char in Skillful:
		Resolve_Skillful( char )

	if char in Skilled:
		Resolve_Skilled( char )

	if char in Tough:
		Resolve_Tough( char )


def Grant_Origin_Feat(
		char,
		feat=None,
		*,
		source: str = "Origin Feat",
		):
	"""Apply an Origin feat Tag (default: Pick from ORIGIN_FEATS)."""
	if feat is None:
		def imprint(
				candidate,
				):
			if candidate is Skilled:
				Acquire_Skilled(
					char,
					source=source,
					)
				return
			carried = getattr(
				char,
				"features",
				None,
				) or ()
			before = len( carried )
			candidate(
				char
				)
			if source != "Origin Feat":
				for feature in (
					getattr(
						char,
						"features",
						None,
						) or ()
					)[ before: ]:
					if getattr(
						feature,
						"source",
						None,
						) == "Origin Feat":
						feature.source = source

		return char.Accept(
			list(
				ORIGIN_FEATS.values()
				),
			imprint=imprint,
			)

	if isinstance(
		feat,
		str,
		):
		feat = ORIGIN_FEATS[
			feat
			]

	if feat is Skilled:
		Acquire_Skilled(
			char,
			source=source,
			)
	else:
		# Each feat Tag's own Imprint grants with a hardcoded "Origin Feat"
		# source, so a caller-supplied one was accepted and then dropped.
		# A sheet then showed two Origin Feats on a Character entitled to
		# one, with nothing to say the second came from an Invocation.
		# Re-source whatever this application just carried on.
		carried = getattr(
			char,
			"features",
			None,
			) or ()
		before = len( carried )
		feat( char )

		if source != "Origin Feat":
			for feature in (
				getattr(
					char,
					"features",
					None,
					) or ()
				)[ before: ]:
				if getattr(
					feature,
					"source",
					None,
					) == "Origin Feat":
					feature.source = source

	return feat


def Grant_Versatile(
	char,
	feat=None,
	):
	"""Apply Versatile, then grant its dynamic Origin Feat choice."""
	if char not in Versatile:
		Versatile( char )

	granted = getattr(
		char,
		"_versatile_origin_feat",
		None,
		)

	if granted is not None:
		if (
			feat is not None
			and feat not in (
				granted,
				granted.NAME,
				)
			):
			raise ValueError(
				"Versatile has already granted "
				f"{granted.NAME!r}."
				)

		return granted

	granted = Grant_Origin_Feat(
		char,
		feat,
		source="Species Feature — Versatile",
		)
	char._versatile_origin_feat = granted

	return granted


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def _test_traits():
	char = Character(seed=11)
	Resourceful(char)
	Skillful(char)
	assert char in Resourceful and char in Trait
	assert char in Skillful
	assert any(
		isinstance(f, Feature) and f.name == "Skillful"
		for f in char.features
		)
	assert any(
		isinstance(f, Feature) and f.name == "Resourceful"
		for f in char.features
		)


def _completed_skill_ledger(
	char,
	) -> None:
	from AtlasActorLudi.Grimoire_of_AbilityScores import AbilityScores
	from AtlasActorLudi.Grimoire_of_Skills import Char_Skills
	from AtlasActorLudi.Map_of_Scores import PB

	char.AS = AbilityScores(
		STR=10,
		DEX=12,
		CON=14,
		INT=16,
		WIS=15,
		CHA=13,
		character=char,
		)
	char.proficiency_bonus = PB( char.level )
	char.skills = Char_Skills(
		char,
		char.AS,
		char.proficiency_bonus,
		)


def _test_skillful_resolves_at_the_available_lifecycle() -> None:
	completed = Character(
		seed=13,
		)
	_completed_skill_ledger( completed )
	Skillful( completed )

	selected = completed.skillful.grants[ 0 ].capability.key
	feature = next(
		current
		for current in completed.features
		if current.name == Skillful.NAME
		)

	assert getattr(
		completed.skills,
		selected,
		).proficiency_level == 1
	assert selected.replace(
		"_",
		" ",
		) in feature.description
	assert "you gain" not in feature.description.casefold()

	deferred = Character(
		seed=17,
		)
	Skillful( deferred )

	deferred_choice = deferred.skillful.grants[ 0 ].capability.key

	_completed_skill_ledger( deferred )
	Resolve_Feature_Mechanics( deferred )

	before = tuple( deferred.features )

	Resolve_Feature_Mechanics( deferred )

	assert deferred.skillful.grants[ 0 ].capability.key == deferred_choice
	assert tuple( deferred.features ) == before
	assert getattr(
		deferred.skills,
		deferred_choice,
		).proficiency_level == 1


def _test_skilled_repeat_action() -> None:
	char = Character(
		seed=19,
		)
	Acquire_Skilled(
		char,
		grant_id="Skilled:1",
		)
	Acquire_Skilled(
		char,
		grant_id="Skilled:2",
		)

	assert char in Skilled
	assert len( char.skilled.gains ) == 2
	assert len( char.skilled.grants ) == 6


def _test_training_features_project_after_sheet_creation() -> None:
	char = Character(
		seed=23,
		)
	Crafter( char )
	Musician( char )

	assert len( char.crafter.grants ) == 3
	assert len( char.musician.grants ) == 3

	_completed_skill_ledger( char )
	Resolve_Feature_Mechanics( char )

	for training_grant in (
			*char.crafter.grants,
			*char.musician.grants,
			):
		legacy = getattr(
			char.skills,
			training_grant.capability.legacy_attribute,
			)
		assert legacy.proficiency_level >= 1


def _test_origin_catalog():
	char = Character(seed=5)
	for index, (
		name,
		tag,
		) in enumerate(
			ORIGIN_FEATS.items()
			):
		probe = Character(
			seed=100 + index
			)
		tag(probe)
		assert probe in tag and probe in Origin_Feat and probe in Feat
		assert any(isinstance(f, Feature) and f.name == name for f in probe.features)
	Lucky(char)
	assert char in Lucky and char in Origin_Feat


def _test_versatile_grants_origin_feat():
	char = Character(
		seed=7
		)
	granted = Grant_Versatile(
		char
		)

	assert char in Versatile
	assert char in granted
	assert any(
		char in tag
		for tag in ORIGIN_FEATS.values()
		)
	names = {
		getattr(
			feature,
			"name",
			None,
			)
		for feature in (
			char.features
			or []
			)
		}
	assert "Versatile" not in names
	assert "Origin Feat" not in names
	assert any(
		name in ORIGIN_FEATS
		for name in names
		)

	before = tuple( char.features )

	assert Grant_Versatile( char ) is granted
	assert tuple( char.features ) == before


def _test_reapply_is_noop():
	char = Character(seed=3)
	Resourceful(char)
	Resourceful(char)
	assert len([f for f in char.features if f.name == "Resourceful"]) == 1


def _test_a_background_reserves_only_what_it_certainly_grants() -> None:
	"""A Background's Tool choice must not reserve the menu it chooses from."""
	from AtlasLusoris.BackgroundKit import BACKGROUNDS

	for name, expected in (
			# Sixteen Artisan's Tools written out as a menu, one granted.
			( "Artisan", 0 ),
			# A category name standing for one pick out of ten instruments.
			( "Entertainer", 0 ),
			):
		tag = BACKGROUNDS[ name ]
		reserved = Reserved_Background_Training( tag )
		menu = Background_Tool_Menu( tag )

		assert len( menu ) > 1, name
		assert sum(
			capability in menu
			for capability in reserved
			) == expected, name
		# Both Skills are certain, and are still reserved.
		assert len( reserved ) == len( tag.SKILLS ), name


def _test_a_short_pool_grants_what_is_left() -> None:
	"""``allow_short`` trades breadth for existence, and says what it granted."""
	# The fixtures below credit Skilled, not Crafter.  Crediting Crafter would
	# satisfy its own Postcondition by the back door and hide what is tested.
	def already_knows(
			char,
			capabilities,
			grant_id,
			):
		Commit_Training_Gain(
			char,
			New_Training_Batch(
				char,
				Skilled,
				tuple(
					Training_Grant(
						capability=capability,
						rank=Training_Rank.PROFICIENT,
						)
					for capability in capabilities
					),
				source="Test Fixture",
				grant_id=grant_id,
				),
			)

	def plan(
			char,
			):
		return _Plan_Training(
			char,
			Crafter,
			ARTISAN_TOOLS,
			3,
			source="Origin Feat",
			purpose="identity.feat.Crafter.tools",
			allow_short=True,
			)

	# One Artisan's Tool left: three were asked for, one is granted.
	crowded = Character( seed=17 )
	already_knows(
		crowded,
		ARTISAN_TOOLS[ 1: ],
		"Test:Crowded",
		)
	gain = plan( crowded )

	assert len( gain.grants ) == 1
	assert gain.grants[ 0 ].capability is ARTISAN_TOOLS[ 0 ]
	assert ARTISAN_TOOLS[ 0 ].name in _Tool_Proficiency_Clause( gain )

	# Nothing left at all: no Batch, because a Batch grants something.
	drained = Character( seed=23 )
	already_knows(
		drained,
		ARTISAN_TOOLS,
		"Test:Full",
		)
	nothing = plan( drained )

	assert nothing is None
	assert _Tool_Proficiency_Clause( nothing ) == ""
	assert _Validate_Feature_Gain(
		nothing,
		Crafter,
		at_most=3,
		) is None

	# And the Feat still awakens, keeping the benefits that were never about
	# training, rather than an unfinished sentence where the tools would be.
	Crafter( drained )
	entry = next(
		feature
		for feature in drained.features
		if feature.name == Crafter.NAME
		)

	assert not drained.crafter.gains
	assert "proficiency with" not in entry.description
	assert "Fast Crafting" in entry.description


def _test_skillful_survives_a_full_skill_list() -> None:
	"""
	Skillful is pooled too, so it gets the same guarantee as the Origin Feats.

	Found by sweeping every _Plan_Training call site after the Crafter fix:
	Skillful was the one draw still missing allow_short, and would have raised
	for a Character who already knew every Skill.
	"""
	char = Character( seed=29 )
	# Credit every Skill to Skilled, so Skillful's own Record stays empty and
	# its Postcondition is tested rather than satisfied by the fixture.
	Commit_Training_Gain(
		char,
		New_Training_Batch(
			char,
			Skilled,
			tuple(
				Training_Grant(
					capability=capability,
					rank=Training_Rank.PROFICIENT,
					)
				for capability in SKILLS
				),
			source="Test Fixture",
			grant_id="Test:AllSkills",
			),
		)

	assert not Untrained_In(
		char,
		SKILLS,
		)

	Skillful( char )
	entry = next(
		feature
		for feature in char.features
		if feature.name == Skillful.NAME
		)

	# The Trait lands, with its inspiration line and no dangling promise.
	assert not char.skillful.gains
	assert Skillful.INSPIRATION.strip() in entry.description
	assert "You have proficiency in" not in entry.description


def _feature_tag_names() -> frozenset:
	"""Every Feature Tag this module declares, by class name and by NAME."""
	names = set()

	for value in globals().values():
		if (
			isinstance(
				value,
				type,
				)
			and issubclass(
				value,
				(
					Feat,
					Trait,
					),
				)
			and value.__module__ == __name__
			):
			names.add( value.__name__ )
			names.add(
				getattr(
					value,
					"NAME",
					"",
					)
				)

	return frozenset( names ) - {
		"",
		}


def _blames_this_module(
		error,
		) -> bool:
	"""
	Whether this failure came out of awakening one of this module's Features.

	Two ways to tell, because a Feature can fail in two shapes.  An Imprint
	that raises leaves its frames on the traceback.  A refused Postcondition
	does not -- the hook returned False rather than raising, so TagKit's own
	frames are all there is -- and only the message names the Feature.

	Both are followed through ``__cause__`` and ``__context__`` as well as the
	direct traceback, because ``Minion.guardian`` swallows what a generation
	step raised and reports its own exhaustion instead: the original survives
	only as context.

	The test's own frame lives in this file and would match every failure
	alike, so the ``_test_`` functions are not evidence of anything.
	"""
	labels = _feature_tag_names()
	seen = set()
	pending = [
		error,
		]

	while pending:
		current = pending.pop()

		if current is None or id( current ) in seen:
			continue

		seen.add( id( current ) )
		pending.extend(
			(
				current.__cause__,
				current.__context__,
				)
			)

		# A TagKit hook failure names the Tag whose hook refused.
		if type( current ).__name__.startswith( "Tag" ):
			words = set(
				str( current )
				.replace(
					".",
					" ",
					)
				.replace(
					"'",
					" ",
					)
				.split()
				)

			if any(
					label in words
					or f"Has_{label}_Training" in words
					for label in labels
					):
				return True

		traceback = current.__traceback__

		while traceback is not None:
			code = traceback.tb_frame.f_code

			if (
				code.co_filename == __file__
				and not code.co_name.startswith( "_test_" )
				):
				return True

			traceback = traceback.tb_next

	return False


def _test_feat_awakening_survives_bulk_generation() -> None:
	"""
	Generate across every Guild and the levels that hand out feats.

	The Crafter and Musician crashes were invisible to a focused test: they
	needed the Artisan, Crafter or Entertainer Background to come up, which is
	a few percent of draws, so only volume showed them.  Volume is therefore
	the test.

	RECOVERY NOTE 2026-08-30: this test has TWO assertions and they mean
	different things.  ``feature_failures`` must be zero -- that is this
	module's own contract, and a regression there is ours.  ``generated >= 300``
	is a coarse health check on the rest of the generator; while the 2026-08-29
	recovery is unfinished it fails at ~238/312 for reasons in other Atlases
	(Artificer, Ranger, Rogue, Bard).  Do not "fix" that second number by
	loosening the first.

	Only failures raised from this module fail it.  A generator this size has
	other faults -- an Elf name can still raise -- and folding those in here
	would make the Feature contract unreadable from its own test.
	"""
	from AtlasActorLudi.Map_of_Character_Generation import summon_player
	from AtlasLusoris.GuildKit import GUILDS

	guilds = sorted( GUILDS )
	levels = (
		1,
		4,
		8,
		12,
		16,
		20,
		)
	feature_failures = []
	other_failures = []
	generated = 0

	for index in range( 312 ):
		guild = guilds[ index % len( guilds ) ]
		level = levels[ ( index // len( guilds ) ) % len( levels ) ]

		try:
			with redirect_stdout( StringIO() ):
				summon_player(
					guild=guild,
					level=level,
					seed=index,
					)
		except Exception as error:
			record = (
				guild,
				level,
				index,
				f"{type(error).__name__}: {error}",
				)

			if _blames_this_module( error ):
				feature_failures.append( record )
			else:
				other_failures.append( record )

			continue

		generated += 1

	assert not feature_failures, (
		f"{len(feature_failures)} of 312 Characters failed while awakening a "
		f"Feature: {feature_failures[:5]}"
		)
	assert generated >= 300, (
		f"only {generated} of 312 Characters were generated; "
		f"{len(other_failures)} failed outside FeaturesKit: "
		f"{other_failures[:5]}"
		)


def _self_test():
	_test_traits()
	_test_skillful_resolves_at_the_available_lifecycle()
	_test_skilled_repeat_action()
	_test_training_features_project_after_sheet_creation()
	_test_origin_catalog()
	_test_versatile_grants_origin_feat()
	_test_reapply_is_noop()
	_test_a_background_reserves_only_what_it_certainly_grants()
	_test_a_short_pool_grants_what_is_left()
	_test_skillful_survives_a_full_skill_list()
	_test_feat_awakening_survives_bulk_generation()
	print("OK — FeaturesKit self-test")


if __name__ == "__main__":
	_self_test()
