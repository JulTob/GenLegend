"""
BackgroundKit

One declarative construction point for every TOP Background.

Background Tags own their abilities, training, Origin Feature, narrative
Entry, and role eligibility. Pins classify each Background Tag directly:

    background_tag in Available
    background_tag in NPC_Background

The Pin Fields derive every public registry.  Adding a homebrew
Background therefore requires one ``Build_Background`` call and no parallel
choice lists.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from typing import Iterable

from TopKit import Action, Imprint, Pin, Pre, Tag, Underlay

from AtlasActorLudi.CharactersKit import Report_Of

from AtlasActorLudi.CharactersKit import (
	Character,
	NonPlayer,
	Player,
	)
from AtlasActorLudi.Grimoire_of_AbilityScores import AbilityScores
# A Background's Skills and Tool are training like any Feature's: they are
# committed to the ledger, which projects them onto the sheet (QST-0116.4).
from AtlasActorLudi.ProficiencyKit import (
	Apply_Training_Record,
	Commit_Training_Gain,
	Ensure_Training_Record,
	Is_Trained,
	Provenance,
	Training_Batch,
	Training_Grant,
	)
from AtlasActorLudi.SkillsKit import SKILLS_BY_KEY
from AtlasInventarium.ToolsKit import (
	ARTISAN_TOOLS as _ARTISAN_TOOL_DEFINITIONS,
	)
from AtlasLusoris.AtlasOfBackgrounds import (
	Register_Official_2024_Backgrounds,
	)
from AtlasLusoris.AtlasOfFeatures import BACKGROUND_ORIGIN_FEATS
from AtlasLusoris.FeaturesKit import (
	Alert,
	CORE_SKILLS,
	Crafter as Crafter_Feature,
	Healer as Healer_Feature,
	Lucky,
	Magic_Initiate_Cleric,
	Magic_Initiate_Druid,
	Magic_Initiate_Wizard,
	Musician,
	Origin_Feat,
	Savage_Attacker,
	Skilled,
	Tavern_Brawler,
	Tough,
	Background_Tool_Menu,
	grant,
	)
from AtlasLusoris.GuildKit import guild_ability_prefs
from AtlasVenustas import Entry


_ALL_ABILITIES = (
	"STR",
	"DEX",
	"CON",
	"INT",
	"WIS",
	"CHA",
	)

# The Artisan's Tools menu, as keys.  ToolsKit authors the list (QST-0116): a
# copy kept here drifted once, listing Carpenter's and Woodcarver's Tools after
# they became one tool and drawing Woodworker's Tools twice as often.
ARTISAN_TOOLS = tuple(
	tool.key
	for tool in _ARTISAN_TOOL_DEFINITIONS
	)


# ---------------------------------------------------------------------------
# Character Background Tags
# ---------------------------------------------------------------------------


class Background(Tag):
	"""Root Tag for exactly one Character Background."""

	NAME = "Background"

	@Pre
	def Character_Only(
		target,
		):
		return isinstance(
			target,
			Character,
			)

	@Pre
	def Single_Background(
		target,
		):
		return sum(
			target in tag
			for tag in globals().get(
				"BACKGROUNDS",
				{},
				).values()
			) <= 1

	@Imprint
	def Ensure_Feature_Bag(
		target,
		):
		if getattr(
			target,
			"features",
			None,
			) is None:
			target.features = []

	@Action
	@Underlay
	def __format__(
			target,
			prior,
			specification,
			):
		"""Render Background from current Tag membership."""
		if specification.strip().casefold() == "background":
			return Find_Background( target )

		return prior( specification )

# ---------------------------------------------------------------------------
# Pins for Background Tags
# ---------------------------------------------------------------------------


@Pin
class Background_Audience(Tag):
	"""Root Pin classifying Background Tags by Character Role."""

	NAME = "Background Audience"

	@Pre
	def Background_Tag_Only(
		target,
		):
		return (
			isinstance(
				target,
				type,
				)
			and issubclass(
				target,
				Background,
				)
			)


class Available(Background_Audience):
	"""Pin for Backgrounds available to Player Characters."""

	NAME = "Available"


class NPC_Background(Background_Audience):
	"""Pin for Backgrounds available to NonPlayer Characters."""

	NAME = "NPC Background"


def _class_name(
	name: str,
	) -> str:
	safe_name = "".join(
		character
		if character.isalnum()
		else "_"
		for character in name
		)

	if not safe_name:
		raise ValueError(
			"A Background requires a non-empty semantic name."
			)

	if safe_name[0].isdigit():
		safe_name = f"Background_{safe_name}"

	return safe_name


def _validate_background_construction(
	*,
	name: str,
	audiences: tuple[type[Background_Audience], ...],
	abilities: tuple[str, str, str],
	skills: tuple[str, str],
	tools: str | tuple[str, ...],
	origin_feat: type[Origin_Feat],
	title: str,
	description: str,
	hook: Entry | None,
	origin_feat_options: tuple[str, ...],
	source_title: str,
	source_url: str,
	source_locator: str,
	source_kind: str,
	) -> None:
	if (
		not isinstance(
			name,
			str,
			)
		or not name.strip()
		):
		raise ValueError(
			"A Background requires a non-empty name."
			)

	if any(
		tag.NAME.casefold() == name.casefold()
		for tag in Background_Audience[:]
		):
		raise ValueError(
			f"Background {name!r} is already declared."
			)

	if (
		not audiences
		or any(
			audience not in (
				Available,
				NPC_Background,
				)
			for audience in audiences
			)
		):
		raise ValueError(
			f"Background {name!r} requires a PC and/or NPC audience."
			)

	if (
		len(
			set(
				abilities
				)
			) != 3
		or any(
			ability not in _ALL_ABILITIES
			for ability in abilities
			)
		):
		raise ValueError(
			f"Background {name!r} requires three distinct valid abilities."
			)

	if (
		len(
			skills
			) != 2
		or len(
			set(
				skills
				)
			) != 2
		or any(
			skill not in CORE_SKILLS
			for skill in skills
			)
		):
		raise ValueError(
			f"Background {name!r} requires two distinct canonical skills."
			)

	if (
		not tools
		or (
			isinstance(
				tools,
				str,
				)
			and not tools.strip()
			)
		or (
			isinstance(
				tools,
				tuple,
				)
			and not all(
				isinstance(
					tool,
					str,
					)
				and tool.strip()
				for tool in tools
				)
			)
		or not isinstance(
			tools,
			(
				str,
				tuple,
				),
			)
		):
		raise ValueError(
			f"Background {name!r} requires at least one valid tool."
			)

	if (
		not isinstance(
			origin_feat,
			type,
			)
		or not issubclass(
			origin_feat,
			Origin_Feat,
			)
		):
		raise TypeError(
			f"Background {name!r} requires an Origin Feature Tag."
			)

	if (
		origin_feat_options
		and (
			origin_feat.NAME not in origin_feat_options
			or any(
				not isinstance(
					option,
					str,
					)
				or not option.strip()
				for option in origin_feat_options
				)
			)
		):
		raise ValueError(
			f"Background {name!r} has invalid Origin Feature options."
			)

	if (
		not isinstance(
			title,
			str,
			)
		or not title.strip()
		or not isinstance(
			description,
			str,
			)
		or not description.strip()
		):
		raise ValueError(
			f"Background {name!r} requires a title and description."
			)

	if hook is not None and (
		not isinstance(
			hook,
			Entry,
			)
		or not hook.title.strip()
		or not hook.definition.strip()
		):
		raise ValueError(
			f"Background {name!r} declares a Hook without a title and text."
			)

	if (
		not isinstance(
			source_title,
			str,
			)
		or not source_title.strip()
		or not isinstance(
			source_kind,
			str,
			)
		or not source_kind.strip()
		or not isinstance(
			source_url,
			str,
			)
		or not isinstance(
			source_locator,
			str,
			)
		):
		raise ValueError(
			f"Background {name!r} requires valid source metadata."
			)


def _eligible_for(
	target,
	tag: type[Background],
	) -> bool:
	return (
		target in Player
		and tag in Available
		) or (
			target in NonPlayer
			and tag in NPC_Background
			)


# ---------------------------------------------------------------------------
# Shared application modules
# ---------------------------------------------------------------------------


def _pick_boost_ability(
	char,
	pool,
	scores,
	):
	"""Prefer odd scores and the Character's Guild abilities."""
	primary, secondary = guild_ability_prefs(
		char
		)

	def priority(
		key,
		):
		if key == primary:
			return 0

		if key == secondary:
			return 1

		return 2

	def rank(
		key,
		):
		value = (
			getattr(
				scores,
				key,
				)
			if scores is not None
			else 10
			)

		return (
			value % 2 == 0,
			priority(
				key
				),
			-value,
			)

	best = min(
		rank(
			key
			)
		for key in pool
		)
	tied = [
		key
		for key in pool
		if rank(
			key
			) == best
		]

	return (
		char.Pick(
			tied
			)
		if len(
			tied
			) > 1
		else tied[0]
		)


def _grant_ability_boosts(
	char,
	abilities=None,
	):
	"""Apply one Background's +2/+1 or +1/+1/+1 ability pattern."""
	if abilities is None:
		name = getattr(
			char,
			"background",
			None,
			)
		tag = BACKGROUNDS.get(
			name
			)

		if tag is None:
			raise ValueError(
				"Ability boosts require a declared Background Tag."
				)

		abilities = tag.ABILITIES

	pattern = char.Pick(
		[
			(
				2,
				1,
				),
			(
				1,
				1,
				1,
				),
			]
		)
	pool = list(
		abilities
		)
	scores = getattr(
		char,
		"AS",
		None,
		)

	if (
		scores is not None
		and not isinstance(
			scores,
			AbilityScores,
			)
		):
		scores = None

	chosen = []
	remaining = list(
		pool
		)

	for bonus in sorted(
		pattern,
		reverse=True,
		):
		stat = _pick_boost_ability(
			char,
			remaining,
			scores,
			)
		remaining.remove(
			stat
			)
		chosen.append(
			(
				stat,
				bonus,
				)
			)

	if scores is None:
		char.background_asi = chosen
		return

	for stat, bonus in chosen:
		setattr(
			scores,
			stat,
			getattr(
				scores,
				stat,
				)
			+ bonus,
			)


def _commit_background_training(
	char,
	tag,
	part: str,
	capabilities,
	):
	"""
	Commit one part of a Background's training (its Skills or its Tool), once.

	The grant ID is the Background's and the part's, so a replay finds the batch
	already in the ledger and only projects it onto the sheet.  Nothing is drawn
	twice, which matters for the Tool: a second draw could name another one under
	the same ID.
	"""
	grant_id = f"Background.{tag.__name__}.{part}"

	if any(
		batch.grant_id == grant_id
		for batch in Ensure_Training_Record(
			char
			).gains
		):
		Apply_Training_Record(
			char
			)
		return

	Commit_Training_Gain(
		char,
		Training_Batch(
			grant_id=grant_id,
			feature=tag,
			grants=tuple(
				Training_Grant(
					capability
					)
				for capability in capabilities
				),
			provenance=Provenance(
				source="Background",
				locator=tag.NAME,
				),
			),
		)


def _grant_skills(
	char,
	tag,
	):
	_commit_background_training(
		char,
		tag,
		"skills",
		tuple(
			SKILLS_BY_KEY[ name ]
			for name in tag.SKILLS
			),
		)


# ---------------------------------------------------------------------------
# RECOVERY NOTE 2026-08-30 -- restored by hand; lost once already.
#
# This function was written on 2026-08-29 as one half of the Crafter / Musician
# pool fix, and was then destroyed when this file was restored from a copy that
# predated it.  It was re-applied on 2026-08-30.  Vault bytecode for
# BackgroundKit is OLDER than this fix: restoring this file from
# ``.recovery-vault`` will silently delete _still_open again.
#
# THE PAIR.  Two files, one behaviour, neither half works alone:
#
#   1. FeaturesKit     Reserved_Background_Training reserves only what a
#                      Background CERTAINLY grants, so an Origin Feat is no
#                      longer excluded from a whole Tool menu it should be able
#                      to draw from.  (Reserving the menu made the Artisan,
#                      Crafter and Entertainer Backgrounds 100% unbuildable.)
#   2. HERE            The Background, which grants its Tool AFTER the Feat and
#                      therefore knows what the Feat took, picks from what is
#                      left.  That is what keeps Artisan's one Artisan's Tool
#                      distinct from Crafter's three, giving four Tools rather
#                      than a collision.
#
# See the matching banner in ``FeaturesKit.Background_Tool_Menu`` for the full
# reasoning, including why a Precondition was rejected.
# ---------------------------------------------------------------------------

def _still_open(
	char,
	capabilities,
	):
	"""
	Narrow a Background's Tool menu to what the Character has yet to learn.

	A Background grants its Tool *after* its Origin Feat, and the two often
	draw on the same menu: Artisan grants one Artisan's Tool and Crafter grants
	three.  Reading the ledger at this point is what keeps those four distinct,
	and it is why the Feat itself no longer has to reserve anything -- see
	``FeaturesKit.Reserved_Background_Training``.

	Falls back to the full menu when the Character somehow knows all of it, so
	a Background that has nothing new to teach still grants a Tool rather than
	failing to pick one.
	"""
	open_capabilities = [
		capability
		for capability in capabilities
		if not Is_Trained(
			char,
			capability,
			)
		]

	return open_capabilities or list( capabilities )


def _grant_tool(
	char,
	tag,
	):
	"""
	Grant a Background's one Tool: a named Tool, a pick from a menu, or a kind
	drawn from a category.  A category is never granted as itself: "a Musical
	Instrument" names no instrument, and the ledger can only answer for one it
	was told (QST-0116.3).
	"""
	menu = Background_Tool_Menu(
		tag
		)

	if not menu:
		return

	if any(
		batch.grant_id == f"Background.{tag.__name__}.tool"
		for batch in Ensure_Training_Record(
			char
			).gains
		):
		pick = None
	else:
		pick = char.Pick(
			_still_open(
				char,
				menu,
				),
			purpose="background.tool",
			)

	_commit_background_training(
		char,
		tag,
		"tool",
		(
			pick,
			) if pick is not None else (),
		)


def _background_slots(
	char,
	) -> dict[str, str]:
	"""The values a Background's prose may name: ``{guild}`` for now."""
	guild = str(
		getattr(
			char,
			"char_class",
			"",
			)
		or ""
		).strip()

	return {
		"guild": guild or "guild",
		}


def _describe(
	text: str,
	):
	"""
	Project a Background's prose, filling any slots it declares.

	Returned as a callable when there is anything to fill, so the text resolves
	when the sheet is read rather than when the Background is applied.  See
	FeaturesKit.Feature: an Entry is a projection.
	"""
	if "{" not in text:
		return text

	return lambda char: text.format(
		**_background_slots(
			char
			)
		)


def _grant_narrative(
	char,
	title: str,
	description: str,
	):
	grant(
		char,
		name=title,
		description=_describe(
			description
			),
		source="Background",
		narrative=True,
		)


def _grant_hook(
	char,
	hook: Entry | None,
	):
	"""Carry a Background's Hook onto the sheet as its own titled entry."""
	if hook is None:
		return

	grant(
		char,
		name=hook.title,
		description=_describe(
			hook.definition
			),
		source="Background Hook",
		narrative=True,
		)


def _awaken(
	char,
	tag,
	):
	"""Apply the common modules owned by one Background Tag."""
	char.background = tag.NAME
	_grant_ability_boosts(
		char,
		tag.ABILITIES,
		)
	_grant_skills(
		char,
		tag,
		)
	_grant_tool(
		char,
		tag,
		)
	_grant_narrative(
		char,
		tag.TITLE,
		tag.DESCRIPTION,
		)
	_grant_hook(
		char,
		tag.HOOK,
		)


def Build_Background(
	*,
	name: str,
	audiences: Iterable[type[Background_Audience]],
	abilities: tuple[str, str, str],
	skills: tuple[str, str],
	tools: str | tuple[str, ...],
	origin_feat: type[Origin_Feat],
	title: str,
	description: str,
	hook: Entry | None = None,
	origin_feat_options: tuple[str, ...] = (),
	source_title: str = "Project Original",
	source_url: str = "",
	source_locator: str = "",
	source_kind: str = "project-original",
	) -> type[Background]:
	"""Construct one complete Background Shape and apply its Pins."""
	resolved_audiences = tuple(
		dict.fromkeys(
			audiences
			)
		)
	resolved_abilities = tuple(
		abilities
		)
	resolved_skills = tuple(
		skills
		)
	resolved_tools = (
		tuple(
			tools
			)
		if isinstance(
			tools,
			list,
			)
		else tools
		)
	resolved_origin_feat_options = (
		tuple(
			origin_feat_options
			)
		or (
			origin_feat.NAME,
			)
		)

	_validate_background_construction(
		name=name,
		audiences=resolved_audiences,
		abilities=resolved_abilities,
		skills=resolved_skills,
		tools=resolved_tools,
		origin_feat=origin_feat,
		title=title,
		description=description,
		hook=hook,
		origin_feat_options=resolved_origin_feat_options,
		source_title=source_title,
		source_url=source_url,
		source_locator=source_locator,
		source_kind=source_kind,
		)

	background_tag = None

	@Pre
	def Eligible_Role(
		target,
		):
		return _eligible_for(
			target,
			background_tag,
			)

	@Imprint
	def Awaken(
		target,
		):
		_awaken(
			target,
			background_tag,
			)

	background_tag = type(
		_class_name(
			name
			),
		(
			Background,
			origin_feat,
			),
		{
			"NAME": name,
			"TITLE": Report_Of(
				title
				),
			"DESCRIPTION": Report_Of(
				description
				),
			"HOOK": Report_Of(
				hook
				),
			"ABILITIES": Report_Of(
				resolved_abilities
				),
			"SKILLS": Report_Of(
				resolved_skills
				),
			"TOOLS": Report_Of(
				resolved_tools
				),
			"ORIGIN_FEAT": Report_Of(
				origin_feat
				),
			"ORIGIN_FEAT_OPTIONS": Report_Of(
				resolved_origin_feat_options
				),
			"SOURCE_TITLE": Report_Of(
				source_title
				),
			"SOURCE_URL": Report_Of(
				source_url
				),
			"SOURCE_LOCATOR": Report_Of(
				source_locator
				),
			"SOURCE_KIND": Report_Of(
				source_kind
				),
			"Eligible_Role": Eligible_Role,
			"Awaken": Awaken,
			"__module__": __name__,
			},
		)

	for audience in resolved_audiences:
		audience(
			background_tag
			)

	return background_tag


# ---------------------------------------------------------------------------
# Shared 2024 Player's Handbook Backgrounds
# ---------------------------------------------------------------------------


def _Build_Player_Handbook_Background(
		**record,
		) -> type[Background]:
	return Build_Background(
		source_title="Player's Handbook (2024)",
		source_url="https://www.dndbeyond.com/sources/dnd/phb-2024",
		source_locator="Chapter 4: Character Origins — Background Descriptions",
		source_kind="official-reference",
		**record,
		)


Acolyte = _Build_Player_Handbook_Background(
	name="Acolyte",
	audiences=(
		Available,
		NPC_Background,
		),
	abilities=(
		"INT",
		"WIS",
		"CHA",
		),
	skills=(
		"Insight",
		"Religion",
		),
	tools="Calligrapher_Supplies",
	origin_feat=Magic_Initiate_Cleric,
	title="Acolyte",
	description=(
		"You belong to something greater than yourself (a god, a pantheon, a "
		"cause, a truth), and in its service you found a purpose the world "
		"could not give you. You learned its rites and its scriptures, copied "
		"its holy words by candlelight until they were written on your heart, "
		"and learned to read the soul beneath the face of everyone who knelt to "
		"you for comfort or confession. Sometimes, when the need is real and "
		"your faith is steady, a prayer is answered, and even you cannot always "
		"say whether it was your hand or the power you serve. Whether you tend "
		"a quiet shrine or carry the word into the streets, you move through "
		"the world as its instrument, and those who share your faith will "
		"always know you for one of their own."
		),
	hook=Entry(
		title="Shelter of the Faithful",
		definition=(
			"Anywhere your faith has taken root (a grand temple, a roadside shrine, "
			"a few believers gathered in secret), you and your companions can count "
			"on a welcome: a meal, a bed, care for your wounds, and sanctuary when "
			"you have nowhere else to turn. The faithful ask only that you honor "
			"the creed while you shelter beneath it. And where there is a "
			"congregation, there is always someone who needs what the devout can "
			"give (a blessing, a burial, a wrong set right), and they will bring it "
			"to you."
			),
		),
	)

Artisan = _Build_Player_Handbook_Background(
	name="Artisan",
	audiences=(
		Available,
		NPC_Background,
		),
	abilities=(
		"STR",
		"DEX",
		"INT",
		),
	skills=(
		"Investigation",
		"Persuasion",
		),
	tools=ARTISAN_TOOLS,
	origin_feat=Crafter_Feature,
	title="Artisan",
	description=(
		"You make things, and you make them well. Somewhere there is a guild "
		"hall with your mark in its ledgers, a master who taught you, and a "
		"trade that shaped your hands long before it shaped your character. You "
		"can look at a lock, a hinge, a flawed casting, or a rival's handiwork "
		"and see at a glance how it was made and where it will fail. You know "
		"the worth of honest work and the true cost of cutting corners, and you "
		"have bargained with enough suppliers and patrons to talk your way to a "
		"fair price (or a workshop after closing). Whatever road you walk now, "
		"you still measure the world by whether it was built to last."
		),
	hook=Entry(
		title="The Guild",
		definition=(
			"Your trade opens doors that coin alone cannot. In most towns you can "
			"find the guild, workshop, or craftsfolk of your art, and among them "
			"your skill earns a fair hearing: a place to work, tools and materials "
			"at cost, and word of who needs a thing made or mended. Build a "
			"reputation and the commissions come to you, some stranger than they "
			"first appear (a key for a lock no one will name, a repair no honest "
			"smith would touch), and every odd request is a call worth answering to "
			"make a name for yourself."
			),
		),
	)

Charlatan = _Build_Player_Handbook_Background(
	name="Charlatan",
	audiences=(
		Available,
		NPC_Background,
		),
	abilities=(
		"DEX",
		"CON",
		"CHA",
		),
	skills=(
		"Deception",
		"Sleight_of_Hand",
		),
	tools="Forgery_Kit",
	origin_feat=Skilled,
	title="Charlatan",
	description=(
		"You have never met a mark you couldn't read or a story you couldn't "
		"improve. Somewhere along the way you learned that the truth is not as "
		"important as your objective. Facts are to be used or set aside as the "
		"moment asks, and most people will believe a nice story over their own "
		"eyes. You mastered people, and learned how to move them, scare them, "
		"or even inspire them. Whether you turn that gift on the needy, the "
		"corrupt, or anyone with a full purse is your own affair. But a life of "
		"masks has shaped you into someone you barely recognize, and brought "
		"you enemies who would like their gold back."
		),
	hook=Entry(
		title="False Identity",
		definition=(
			"You are never only one person. You can be a grieving widow, a visiting "
			"dignitary, a healer with a miracle cure, or a nobody not worth a "
			"second glance, complete with the reputation, the papers, the quick "
			"hands, and the steady nerve to carry it off. You keep at least one "
			"false identity fully dressed: a name, a history, papers that pass "
			"inspection, and people who will swear they have known that name for "
			"years. Given time and something to copy, you can forge a document to "
			"suit almost any need, from a letter of introduction to an official "
			"writ. The danger, and the opportunity, is that a good lie takes on a "
			"life of its own: sooner or later someone comes looking for the person "
			"you invented, wanting something only they can give."
			),
		),
	)

Criminal = _Build_Player_Handbook_Background(
	name="Criminal",
	audiences=(
		Available,
		NPC_Background,
		),
	abilities=(
		"DEX",
		"CON",
		"INT",
		),
	skills=(
		"Sleight_of_Hand",
		"Stealth",
		),
	tools="Thieves_Tools",
	origin_feat=Alert,
	title="Criminal",
	description=(
		"You have lived on the wrong side of the law, and you learned its "
		"lessons well: how to move without being seen, how to open what someone "
		"wanted kept shut, how to read a room for the exits and the easy marks "
		"and the one person watching too closely. You know the folk who work "
		"the dark hours (the fences, the smugglers, the lookouts, the ones who "
		"never give a straight name) and how to speak to them without saying "
		"too much. Maybe you did it to survive, or for the thrill, or because "
		"the law protected everyone but you. Whatever set you on that road, the "
		"habits it taught you do not wash off, and neither, sometimes, do the "
		"debts. Even the ones you thought were already paid off."
		),
	hook=Entry(
		title="Criminal Contact",
		definition=(
			"You know how the underworld passes what it does not want overheard. "
			"Wherever you go, you can find the local version of the people you used "
			"to run with (a fence, a smuggler, a tavern that asks no questions) and "
			"make yourself known without a word out of place. Through them you can "
			"get a message to almost anyone, quietly, or learn who really runs the "
			"streets and what they are afraid of. The catch is that favors in that "
			"world are never free, and the people who trade in them remember "
			"exactly what they are owed."
			),
		),
	)

Entertainer = _Build_Player_Handbook_Background(
	name="Entertainer",
	audiences=(
		Available,
		NPC_Background,
		),
	abilities=(
		"STR",
		"DEX",
		"CHA",
		),
	skills=(
		"Acrobatics",
		"Performance",
		),
	tools="Musical_Instrument",
	origin_feat=Musician,
	title="Entertainer",
	description=(
		"You were born for an audience, or you found one and never looked back. "
		"You know how to hold a room: the timing of a joke, the hush before the "
		"high note, the tumble that looks like an accident and lands like a "
		"promise. You have played to drunk sailors and bored nobles and "
		"children who had never seen a coin spent on wonder, and you learned "
		"that the right performance can lift a room's sorrow, or its silver, or "
		"just its attention for one shining hour. The road is hard on "
		"performers, but you would rather be booed than forgotten, and you have "
		"never once wanted the quiet life."
		),
	hook=Entry(
		title="By Popular Demand",
		definition=(
			"Give you a stage, a crate, or a cleared corner of a common room, and "
			"you can earn your keep: a meal, a bed, a few coins, and the goodwill "
			"of a crowd that came in strangers and leaves knowing your name. A "
			"performer who pleases is remembered, and being remembered has a way of "
			"finding you work, and trouble: an admirer with a request, a rival who "
			"wants you gone, a patron who needs a message carried somewhere only a "
			"minstrel can go unremarked. So take your bow, and always leave them "
			"wanting more: a face a crowd cheers for is worth more than a full "
			"purse on the road, and it opens doors that stay shut to strangers."
			),
		),
	)

Farmer = _Build_Player_Handbook_Background(
	name="Farmer",
	audiences=(
		Available,
		NPC_Background,
		),
	abilities=(
		"STR",
		"CON",
		"WIS",
		),
	skills=(
		"Animal_Handling",
		"Nature",
		),
	tools="Woodworker_Tools",
	origin_feat=Tough,
	title="Farmer",
	description=(
		"You came up with dirt under your nails and the seasons in your bones. "
		"You know the weight of real work: the ache of a long harvest, the "
		"patience of raising a beast from a shaking newborn to a plow-puller, "
		"the quiet arithmetic of whether the rain will come before the seed "
		"rots. You can build a fence that holds, mend what breaks, read a sky, "
		"and calm a frightened animal with a hand and a low word. The land does "
		"not care who your father was or what gods you keep, and neither, in "
		"the end, do you. It taught you that anything worth having is grown "
		"slowly, and that a person who will not do the hard, dull work is not "
		"to be trusted with the rest."
		),
	hook=Entry(
		title="Rustic Hospitality",
		definition=(
			"Working people know one of their own. In any village, farmstead, or "
			"waystation, you can find a dry barn to sleep in, a plain meal, and "
			"hands willing to help someone who has clearly done a day's labor in "
			"their life. They will hide you from those who ride fine horses and ask "
			"hard questions, tend you when you are hurt, and in return they will "
			"tell you their troubles: the beast that has been taking the sheep, the "
			"tax collector who takes too much, the neighbor who walked into the "
			"woods and never came back. Small troubles, until they are yours to "
			"solve."
			),
		),
	)

Guard = _Build_Player_Handbook_Background(
	name="Guard",
	audiences=(
		Available,
		NPC_Background,
		),
	abilities=(
		"STR",
		"INT",
		"WIS",
		),
	skills=(
		"Athletics",
		"Perception",
		),
	tools="Gaming_Set",
	origin_feat=Alert,
	title="Guard",
	description=(
		"Rain on the cobbles, a lantern guttering out, and one detail that "
		"refuses to sit right. Your mind goes back to that one case when the "
		"world finally quiets. The one you can't let go. You protect the city. "
		"You are the watcher, and the enforcer. The city needs eyes, fists, and "
		"compromise. You learned your part of it cold. You can run a suspect "
		"down three streets, hear the rehearsed line in a story told too "
		"smoothly, and sit across from a criminal with only a bluff. You do "
		"your best thinking at a dark window with a glass you are not drinking. "
		"You are good at it. But then came the case that would not close, and "
		"it cost you the post, or the sleep, or the people who used to trust "
		"you. You are still working it. You always will be."
		),
	hook=Entry(
		title="Network of Favors",
		definition=(
			"You never worked alone, and you never worked clean. The years left you "
			"names on both sides of the lamplight: a sergeant who owes you for a "
			"night that never made it into the report, a clerk who lets you read "
			"what you should not, a fence, a beggar, a dock hand who notices every "
			"crate that comes in wrong. Any of them can tell you what is moving "
			"through their district (who arrived, who vanished, who is suddenly "
			"paying old debts), and some will look the other way while you do what "
			"the law will not, or cannot. But every favor is a loan, and you have "
			"borrowed from dangerous people on both sides of that law. One night "
			"they will come to collect, and coin may not be enough."
			),
		),
	)

Guide = _Build_Player_Handbook_Background(
	name="Guide",
	audiences=(
		Available,
		NPC_Background,
		),
	abilities=(
		"DEX",
		"CON",
		"WIS",
		),
	skills=(
		"Stealth",
		"Survival",
		),
	tools="Cartographer_Tools",
	origin_feat=Magic_Initiate_Druid,
	title="Guide",
	description=(
		"You know the ways that are not on any map, and you made the maps for "
		"the ones that are. Far from roads and lanterns, you learned to move "
		"quietly enough that the wood forgets you are in it, to sleep light, to "
		"find water, and to be somewhere else by the time the thing that was "
		"following gives up. You have led pilgrims, smugglers, surveyors, and "
		"fools through country that kills the unprepared, and buried a few who "
		"would not listen. Out there you picked up something else, too: a word "
		"for the weather that sometimes answers, a way of asking the green "
		"things to let you pass. You do not talk about that part. You just know "
		"that the wild is not empty, and that it notices whoever walks through "
		"it."
		),
	hook=Entry(
		title="The Ways Between",
		definition=(
			"There is a whole country of people who live off the roads: trappers, "
			"hermits, herders, border-runners, the last family on the last farm "
			"before the trees. You know how to find them, and how to be welcome: a "
			"night by their fire, a meal, and a warning about what has changed "
			"since you last came through. From them you hear what never reaches a "
			"town (a pass gone bad, lights in the hills, a village that has stopped "
			"sending anyone to market, something in the deep wood that has begun to "
			"hunt in daylight). Guiding pays well, and there is always someone who "
			"needs to reach a place no sensible person will take them."
			),
		),
	)

Hermit = _Build_Player_Handbook_Background(
	name="Hermit",
	audiences=(
		Available,
		NPC_Background,
		),
	abilities=(
		"CON",
		"WIS",
		"CHA",
		),
	skills=(
		"Medicine",
		"Religion",
		),
	tools="Herbalism_Kit",
	origin_feat=Healer_Feature,
	title="Hermit",
	description=(
		"You went out to the quiet places and stayed long enough for the noise "
		"to drain out of you. A cave, a cliff cell, a hut past the last field: "
		"it does not matter which, only that no one was there to interrupt the "
		"thinking. You learned which roots break a fever and which look "
		"identical and stop a heart, how to set a bone with nobody to hold the "
		"patient still, and how to sit with the dying without flinching. You "
		"prayed, or studied, or simply listened, until something answered: an "
		"insight, a vision, a truth you have never been able to put down. Then "
		"you came back to a world that talks constantly and says very little. "
		"You are out of practice with people, but not with what matters."
		),
	hook=Entry(
		title="What You Found Out There",
		definition=(
			"In your solitude you came to know one thing the world does not (the "
			"meaning of a symbol nobody can read, where something old was buried "
			"and why, a heresy that happens to be true, the cure for a sickness "
			"that has no cure). Work it out with your GM. You are not the only one "
			"who wants it: scholars, priests, and quieter parties come looking for "
			"the hermit who knows, and not all of them ask politely. And wherever "
			"you go, the sick and the desperate find you, because someone always "
			"remembers a healer who asks for nothing."
			),
		),
	)

Merchant = _Build_Player_Handbook_Background(
	name="Merchant",
	audiences=(
		Available,
		NPC_Background,
		),
	abilities=(
		"CON",
		"INT",
		"CHA",
		),
	skills=(
		"Animal_Handling",
		"Persuasion",
		),
	tools="Cartographer_Tools",
	origin_feat=Lucky,
	title="Merchant",
	description=(
		"Anyone can sell trinkets in a town square. You wanted the long routes: "
		"the spice from the desert nomads, the dyes of emperors, the items "
		"nobody in this land has ever seen. You knew it was hard, but you made "
		"it worth it. You heard the tales: the dunes where something moves "
		"underneath, the route where sailors sing of sirens, the valley where "
		"the old dragon counts every coin that crosses. And you loaded up and "
		"went anyway. Determined not to just survive, but to make a profit. You "
		"respect your beasts as more than carriers, you can find your road by "
		"the stars or by the smell of the wind, and you have turned an ambush "
		"into a business partner. Everyone in this trade is out there. Willing "
		"to go beyond reason. But when a stranger admires something in your "
		"pack and asks where it came from, you get to smile and say: if you "
		"like it, I know where to get more."
		),
	hook=Entry(
		title="I Know Where to Get It",
		definition=(
			"You do not need to own a thing to sell it. Put an object in your hands "
			"and you can tell what it is worth, whose workshop or century it came "
			"out of, and who in this world would pay stupid money to own it. Better "
			"still: you know where, and how, to get it and sell it. A book no one "
			"dares to open, a sword nobody has managed to pull from the stone (with "
			"the stone included), the heirloom a family has been mourning for three "
			"generations, the relic a temple would empty its vaults to have back... "
			"You may ask favors and promise cuts, but you will make your sale. Word "
			"gets around, so the commissions will come to you: appraise an "
			"antiquity, retrieve a unique item, or open a trade deal for a guild. "
			"The world is full of wonders, and people who want them. You are merely "
			"helping and getting your skills' worth. And when a job is beyond you? "
			"You know exactly which unreasonable people to put in a tavern together "
			"for the (almost) perfect plan."
			),
		),
	)

Noble = _Build_Player_Handbook_Background(
	name="Noble",
	audiences=(
		Available,
		NPC_Background,
		),
	abilities=(
		"STR",
		"INT",
		"CHA",
		),
	skills=(
		"History",
		"Persuasion",
		),
	tools="Gaming_Set",
	origin_feat=Skilled,
	title="Noble",
	description=(
		"*There is a seat others watch, and it bears your name. Perhaps your "
		"claim came by birth, election, promise, victory on a field, or merit "
		"alone. The seat waits ahead while you are preparing for it, and people "
		"measure every step you take toward it. You know the factions and their "
		"old precedents, their alliances and rivalries, and that the difference "
		"between them often matters less than who survives to write it down. "
		"You learned that ceremony is a language, hospitality a negotiation, "
		"and a smile may carry farther than a command.*"
		"\n"
		"\n"
		"*The war games are never merely games. They are lessons: which piece "
		"may be risked, which must be protected, and how to keep defeat from "
		"becoming destruction. Never mistake the board for the game. Your "
		"pieces will have families, your opponents will have heirs, and some "
		"pieces will change color for the right price. One day, you will make "
		"the call. Soldiers will move, granaries will empty, cells will open, "
		"and names will end. Your predecessors made such calls. So did theirs. "
		"The echoes of their commands have followed you and now lurk in the "
		"shadows. Whether you inherit that power, seize it, refuse it, or lose "
		"it, it has already shaped the way others see you. You have not once "
		"felt entirely safe.*"
		),
	hook=Entry(
		title="The Weight of the Crown",
		definition=(
			"*Crown, throne, seat, baton, council, the right to speak first: "
			"whatever your people call it, you bear a recognized claim to "
			"authority. Your name is not only a key. It is a blade hanging over "
			"your head.*"
			"\n"
			"\n"
			"Define the reach of your station with the GM: who recognizes it, what "
			"community or institution it touches, and what duties accompany it. "
			"Where your authority is recognized, you can usually secure an audience "
			"and hospitality appropriate to your station, and the attention of "
			"subjects or allies. Every request tests a loyalty, spends a favor, or "
			"creates an obligation."
			"\n"
			"\n"
			"*The price is that you are always watched. Responsibilities and old "
			"grudges sharpen the blade. Every public promise may be treated as "
			"policy. Every insult may become a grievance. Blood spilled may become "
			"war. Everything you do is read as a move: who you court, who you "
			"insult, whose table you sit at, whose funeral you attend. One "
			"misjudgment, and the people you love may pay before you do. A crown is "
			"not a gift. It is a golden cage with your name already written on it.*"
			),
		),
	)

Sage = _Build_Player_Handbook_Background(
	name="Sage",
	audiences=(
		Available,
		NPC_Background,
		),
	abilities=(
		"CON",
		"INT",
		"WIS",
		),
	skills=(
		"Arcana",
		"History",
		),
	tools="Calligrapher_Supplies",
	origin_feat=Magic_Initiate_Wizard,
	title="Sage",
	description=(
		"You wanted to know, and wanting to know is a harder master than any "
		"lord. You have spent years where the good books are kept: copying "
		"failing manuscripts before the ink gave out entirely, chasing one "
		"citation through four libraries, arguing with people three centuries "
		"dead in the margins of their own work. You know which empires told the "
		"truth about themselves and which are still being believed, and you can "
		"read a spell's structure the way a mason reads a wall, seeing where "
		"the weight sits and what would happen if you pulled the wrong stone. "
		"You have cast a little of it yourself, carefully, because theory is "
		"not the same as practice and you have read what happens to those who "
		"forget the difference. There is always one more question. That is the "
		"trouble with answers."
		),
	hook=Entry(
		title="Working Hypothesis",
		definition=(
			"You may not have the answer, but you always know where it might be "
			"kept, and who to ask. Archives, temple libraries, private collections, "
			"a retired scholar who has not spoken to anyone about her life's work "
			"in twenty years: you can find the door and, more often than not, get "
			"through it, because scholars extend to one another a professional "
			"courtesy that has nothing to do with liking each other. What you learn "
			"is never the whole of it. A book will be missing its final pages, a "
			"source will contradict a better source, and a name will appear where "
			"no name should be. Word travels that you chase such things, so people "
			"bring you what they cannot read: an inscription, a diary in a dead "
			"hand, a map of somewhere that is not supposed to exist."
			),
		),
	)

Sailor = _Build_Player_Handbook_Background(
	name="Sailor",
	audiences=(
		Available,
		NPC_Background,
		),
	abilities=(
		"STR",
		"DEX",
		"WIS",
		),
	skills=(
		"Acrobatics",
		"Perception",
		),
	tools="Cartographer_Tools",
	origin_feat=Tavern_Brawler,
	title="Sailor",
	description=(
		"The sea has its own law, and none of it is written down on land. It "
		"does not care whose flag you fly or what a magistrate decided about "
		"you in some other country: it asks only whether you can hold a course, "
		"hold your watch, and hold your nerve. You go up wet rigging in a gale "
		"and come down faster, smell weather an hour before it breaks, hear the "
		"one rope in a hundred that is about to part, and steer by stars half "
		"the world never bothered to name. You have slept soundly through a "
		"storm that had landsmen praying. You have turned back for a boat when "
		"nobody would have blamed you for sailing on, because that is the law "
		"too. In port you drink like someone with one night to live, because "
		"that is the arithmetic, and you have brawled over a card game, a song, "
		"and an insult in a language you do not speak. Let others keep their "
		"fields and their fences. Out there the sea is honest with you, and you "
		"would rather be lost on it than safe anywhere else."
		),
	hook=Entry(
		title="Ship's Passage",
		definition=(
			"You speak the language of decks and harbors, and it opens the water to "
			"you. In any port you can find a berth: work your passage, or trade on "
			"a name that some captain in the crowd will recognize, and bring your "
			"companions aboard on your word (with the understanding that they will "
			"be expected to earn it, and that a captain's mercy has limits). "
			"Dockside, you hear what sailors hear before anyone on land does: which "
			"ships came in short-crewed and why, what the harbor master is being "
			"paid to overlook, which vessel sailed for a coast that no chart shows "
			"and has not come back. And there is always a berth going on a voyage "
			"that no sensible sailor will sign for."
			),
		),
	)

Scribe = _Build_Player_Handbook_Background(
	name="Scribe",
	audiences=(
		Available,
		NPC_Background,
		),
	abilities=(
		"DEX",
		"INT",
		"WIS",
		),
	skills=(
		"Investigation",
		"Perception",
		),
	tools="Calligrapher_Supplies",
	origin_feat=Skilled,
	title="Scribe",
	description=(
		"Few people reach the highest levels of education: a University, an "
		"Academy, the {guild} School. Somebody paid for yours. A family that "
		"could not afford it, a patron with expectations, or years of your own "
		"life signed away in advance: the door opened, and you have been paying "
		"for it ever since. You have watched a master do something impossible, "
		"and you knew it would be worth it. You draw diagrams, write notes, and "
		"watch closely. Then you practice, practice, and practice, until you "
		"can replicate your own wonders. Good is not good enough. You have to "
		"be perfect. You are not finished. You may never be. But you have "
		"already seen what knowledge does to a room, to a wound, to a mind, to "
		"a system... and you would gladly trade years of your life to master "
		"it. Knowledge is power. Power to change things. To make them better. "
		"To give back what you received."
		),
	hook=Entry(
		title="Alumni",
		definition=(
			"There is a bond unique to learning together. You made friends, you "
			"made rivals, you even made enemies. All of them, you know them better "
			"than their families do. You helped a classmate prepare for a "
			"challenge, and unexpectedly received a pen worth a year's salary. You "
			"needed help when you were sick, and somebody gave you their notes and "
			"brought you a warm meal. You celebrated together, and mourned "
			"together. Now those bonds stay with you. You may find colleagues now "
			"working in positions of power, making the best of their skills and "
			"knowledge. They have goals, and so do you. But you can still help each "
			"other. Your network is tight, and refusing to participate and help "
			"others may cut you off completely, but favors move like waves on a "
			"string. You may find a name, a job opportunity, a document that was "
			"meant to stay hidden, or a door left open after hours. But others may "
			"come to you with their own favors to ask. You are part of the team, so "
			"will you play your part?"
			),
		),
	)

Soldier = _Build_Player_Handbook_Background(
	name="Soldier",
	audiences=(
		Available,
		NPC_Background,
		),
	abilities=(
		"STR",
		"DEX",
		"CON",
		),
	skills=(
		"Athletics",
		"Intimidation",
		),
	tools="Gaming_Set",
	origin_feat=Savage_Attacker,
	title="Soldier",
	description=(
		"You know what a formation sounds like when it is about to break. "
		"Someone taught you to march, to dig, to carry a pack until the straps "
		"wore through your shirt, and to hold a line with people you did not "
		"choose and would now die for. You learned that violence is a craft "
		"like any other: where to put your weight, which threats end a fight "
		"before it starts, how to make yourself look like too much trouble to "
		"be worth it. You have won and lost, buried friends, and taken orders "
		"you have not stopped thinking about since. Between all that there were "
		"the long stretches of nothing, and the dice and cards that kept a "
		"company from turning on itself. You still count the exits like a "
		"soldier, and some part of you is still waiting for a horn that is not "
		"going to sound."
		),
	hook=Entry(
		title="Old Company",
		definition=(
			"You were baptized into an army with your first blood, and that stain "
			"cannot be washed away. You know the ranks and the courtesies, how to "
			"talk to a quartermaster, and which requests get answered and which get "
			"you laughed out of the tent, so soldiers, guards, and mercenaries tend "
			"to treat you as one of theirs: a meal, a bunk, and honest talk about "
			"what has been moving through the district. Better still, your old "
			"company is scattered across the world now, in garrisons, in gutters, "
			"in service to people you would not have chosen for them, and they "
			"remember who carried whom. Any one of them will hear you out. Some of "
			"them will need you to come at once, and no letter that begins \"you owe "
			"me\" has ever been about something small."
			),
		),
	)

Wayfarer = _Build_Player_Handbook_Background(
	name="Wayfarer",
	audiences=(
		Available,
		NPC_Background,
		),
	abilities=(
		"DEX",
		"WIS",
		"CHA",
		),
	skills=(
		"Insight",
		"Stealth",
		),
	tools="Thieves_Tools",
	origin_feat=Lucky,
	title="Wayfarer",
	description=(
		"You have slept in doorways, in haylofts, in the bottom of a boat, and "
		"in places you would rather not describe. Nobody was coming to help, so "
		"you learned to read people quickly: who gives, who takes, who is about "
		"to become a problem, and who is lying about which. You can be gone "
		"before a hand closes on your shoulder, get a lock open when the "
		"alternative is a night in the rain, and eat a real meal without "
		"letting on how long it has been since the last one. You have been "
		"shown kindness by people with nothing to spare and cruelty by people "
		"who had everything, and you have never once confused the two. By "
		"rights you should have died three or four times over. You did not. "
		"Either somebody is watching over you or nobody is, and it makes no "
		"difference: you yourself are always watching."
		),
	hook=Entry(
		title="The Overlooked",
		definition=(
			"There is a second nation inside every city, and no map shows it. "
			"Beggars, urchins, day laborers, the woman who sweeps the temple steps, "
			"the drifters under the bridge: no crown, no captain, no borders, and "
			"yet rules older than the ones carved above the courthouse door. Share "
			"what you have. Do not sell your own. Pass it on. You are one of them, "
			"so wherever you go there is a fire, a doorway, a name to ask for, and "
			"hands willing to hide you from anyone carrying a warrant. And they see "
			"everything, because nobody guards their tongue in front of the "
			"invisible: which magistrate is bought and by whom, which faction is "
			"quietly arming, which street not to walk tonight, who vanished last "
			"month and through which door they were dragged. Nobody asks them. They "
			"will tell you. What they ask in return is never small: speak where "
			"they will not be heard, stand between a fist and a child, find the one "
			"no officer will look for. They own nothing and they say nothing, but "
			"they are everywhere, and there are more of them than of anyone else. A "
			"word from you can move through them like wind across a field of wheat, "
			"and no city that has ignored them for a century could survive a week "
			"without them."
			),
		),
	)


# ---------------------------------------------------------------------------
# Actualized former Archetypes: full NonPlayer Backgrounds
# ---------------------------------------------------------------------------


Artist = Build_Background(
	name="Artist",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"DEX",
		"WIS",
		"CHA",
		),
	skills=(
		"Insight",
		"Performance",
		),
	tools="Painter_Supplies",
	origin_feat=Musician,
	title="Expressive Eye",
	description=(
		"You notice telling details and turn them into performances or works "
		"that move an audience."
		),
	)

Bandit = Build_Background(
	name="Bandit",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"STR",
		"DEX",
		"CHA",
		),
	skills=(
		"Intimidation",
		"Stealth",
		),
	tools="Thieves_Tools",
	origin_feat=Alert,
	title="Roadside Instinct",
	description=(
		"You understand ambush sites, frightened travelers, hidden camps, and "
		"the shifting loyalties of an outlaw company."
		),
	)

Berserker = Build_Background(
	name="Berserker",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"STR",
		"CON",
		"WIS",
		),
	skills=(
		"Athletics",
		"Intimidation",
		),
	tools="Gaming_Set",
	origin_feat=Tavern_Brawler,
	title="Fury Tempered",
	description=(
		"You learned to survive violent confrontations by committing fully "
		"when hesitation would be fatal."
		),
	)

Commoner = Build_Background(
	name="Commoner",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"STR",
		"CON",
		"WIS",
		),
	skills=(
		"Animal_Handling",
		"Insight",
		),
	tools="Woodworker_Tools",
	origin_feat=Tough,
	title="Local Roots",
	description=(
		"You know the rhythms, favors, worries, and practical work that hold "
		"an ordinary community together."
		),
	)

Crafter = Build_Background(
	name="Crafter",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"DEX",
		"INT",
		"WIS",
		),
	skills=(
		"Investigation",
		"Sleight_of_Hand",
		),
	tools=ARTISAN_TOOLS,
	origin_feat=Crafter_Feature,
	title="Practiced Hands",
	description=(
		"You diagnose material problems quickly and know how to repair, alter, "
		"or reproduce useful objects."
		),
	)

Cultist = Build_Background(
	name="Cultist",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"INT",
		"WIS",
		"CHA",
		),
	skills=(
		"Deception",
		"Religion",
		),
	tools="Disguise_Kit",
	origin_feat=Magic_Initiate_Cleric,
	title="Secret Doctrine",
	description=(
		"You know the signs, passwords, rituals, and hidden hierarchies of a "
		"secretive faith or forbidden cause."
		),
	)

Doctor = Build_Background(
	name="Doctor",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"INT",
		"WIS",
		"CHA",
		),
	skills=(
		"Investigation",
		"Medicine",
		),
	tools="Herbalism_Kit",
	origin_feat=Healer_Feature,
	title="Clinical Practice",
	description=(
		"You assess symptoms methodically, stabilize patients, and recognize "
		"when an injury or illness has an unusual cause."
		),
	)

Expert = Build_Background(
	name="Expert",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"DEX",
		"INT",
		"WIS",
		),
	skills=(
		"Insight",
		"Investigation",
		),
	tools=ARTISAN_TOOLS,
	origin_feat=Skilled,
	title="Specialist",
	description=(
		"Long practice in a narrow discipline lets you recognize fine details "
		"and solve problems others overlook."
		),
	)

Explorer = Build_Background(
	name="Explorer",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"DEX",
		"CON",
		"WIS",
		),
	skills=(
		"Perception",
		"Survival",
		),
	tools="Cartographer_Tools",
	origin_feat=Alert,
	title="Beyond the Map",
	description=(
		"You are accustomed to uncertain routes, incomplete maps, changing "
		"weather, and discoveries that reward careful preparation."
		),
	)

Guardian = Build_Background(
	name="Guardian",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"STR",
		"CON",
		"WIS",
		),
	skills=(
		"Athletics",
		"Perception",
		),
	tools="Gaming_Set",
	origin_feat=Tough,
	title="Watchful Charge",
	description=(
		"You have accepted responsibility for a person, place, threshold, or "
		"tradition and remain alert to dangers around it."
		),
	)

Healer = Build_Background(
	name="Healer",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"INT",
		"WIS",
		"CHA",
		),
	skills=(
		"Insight",
		"Medicine",
		),
	tools="Herbalism_Kit",
	origin_feat=Healer_Feature,
	title="Restorative Care",
	description=(
		"You combine practical treatment with an understanding of fear, pain, "
		"and the patience recovery often demands."
		),
	)

Hero = Build_Background(
	name="Hero",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"STR",
		"CON",
		"CHA",
		),
	skills=(
		"Athletics",
		"Persuasion",
		),
	tools="Gaming_Set",
	origin_feat=Lucky,
	title="Local Legend",
	description=(
		"A remembered deed made you a symbol to a community, whether or not "
		"you feel worthy of the story now told about you."
		),
	)

Hunter = Build_Background(
	name="Hunter",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"DEX",
		"CON",
		"WIS",
		),
	skills=(
		"Perception",
		"Survival",
		),
	tools="Leatherworker_Tools",
	origin_feat=Alert,
	title="Patient Pursuit",
	description=(
		"You read spoor, habits, terrain, and silence to follow quarry without "
		"wasting movement or revealing your approach."
		),
	)

Knight = Build_Background(
	name="Knight",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"STR",
		"CON",
		"CHA",
		),
	skills=(
		"Athletics",
		"Persuasion",
		),
	tools="Gaming_Set",
	origin_feat=Savage_Attacker,
	title="Sworn Service",
	description=(
		"An oath, patron, or martial order grants you recognizable duties and "
		"a place within a wider chain of obligation."
		),
	)

Mage = Build_Background(
	name="Mage",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"INT",
		"WIS",
		"CHA",
		),
	skills=(
		"Arcana",
		"Investigation",
		),
	tools="Calligrapher_Supplies",
	origin_feat=Magic_Initiate_Wizard,
	title="Arcane Practice",
	description=(
		"You learned magic through fragmented study, service, inheritance, or "
		"another path outside a formal adventuring Guild."
		),
	)

Mentor = Build_Background(
	name="Mentor",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"INT",
		"WIS",
		"CHA",
		),
	skills=(
		"Insight",
		"Persuasion",
		),
	tools="Calligrapher_Supplies",
	origin_feat=Skilled,
	title="Guiding Hand",
	description=(
		"You recognize developing talent and know how to turn experience into "
		"questions, exercises, warnings, and useful encouragement."
		),
	)

Ninja = Build_Background(
	name="Ninja",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"DEX",
		"INT",
		"WIS",
		),
	skills=(
		"Acrobatics",
		"Stealth",
		),
	tools="Poisoners_Kit",
	origin_feat=Alert,
	title="Hidden Discipline",
	description=(
		"You trained to enter guarded places, observe without notice, and act "
		"with precision before an alarm can spread."
		),
	)

Pirate = Build_Background(
	name="Pirate",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"STR",
		"DEX",
		"CHA",
		),
	skills=(
		"Acrobatics",
		"Intimidation",
		),
	tools="Cartographer_Tools",
	origin_feat=Tavern_Brawler,
	title="Freebooter's Reputation",
	description=(
		"You understand unruly crews, dangerous ports, divided prizes, and "
		"the value of a reputation that arrives before the ship."
		),
	)

Priest = Build_Background(
	name="Priest",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"INT",
		"WIS",
		"CHA",
		),
	skills=(
		"Insight",
		"Religion",
		),
	tools="Calligrapher_Supplies",
	origin_feat=Magic_Initiate_Cleric,
	title="Pastoral Office",
	description=(
		"You conduct rites, preserve doctrine, and help a community interpret "
		"its obligations, griefs, celebrations, and hopes."
		),
	)

Scholar = Build_Background(
	name="Scholar",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"INT",
		"WIS",
		"CHA",
		),
	skills=(
		"Arcana",
		"History",
		),
	tools="Calligrapher_Supplies",
	origin_feat=Skilled,
	title="Learned Correspondence",
	description=(
		"You exchange findings with other specialists and know how to compare "
		"sources, claims, translations, and competing schools of thought."
		),
	)

Shaman = Build_Background(
	name="Shaman",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"CON",
		"WIS",
		"CHA",
		),
	skills=(
		"Animal_Handling",
		"Nature",
		),
	tools="Herbalism_Kit",
	origin_feat=Magic_Initiate_Druid,
	title="Spirit Mediator",
	description=(
		"You interpret signs and maintain practical relationships between a "
		"community, its land, its ancestors, and unseen presences."
		),
	)

Spy = Build_Background(
	name="Spy",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"DEX",
		"INT",
		"CHA",
		),
	skills=(
		"Deception",
		"Stealth",
		),
	tools="Disguise_Kit",
	origin_feat=Skilled,
	title="Network of Whispers",
	description=(
		"You cultivate sources, conceal your purpose, and understand how a "
		"small observation becomes useful intelligence."
		),
	)

Trickster = Build_Background(
	name="Trickster",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"DEX",
		"INT",
		"CHA",
		),
	skills=(
		"Deception",
		"Sleight_of_Hand",
		),
	tools="Disguise_Kit",
	origin_feat=Lucky,
	title="Misdirection",
	description=(
		"You redirect attention with timing, confidence, and a practiced sense "
		"of what an observer expects to see."
		),
	)

Traveler = Build_Background(
	name="Traveler",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"DEX",
		"CON",
		"WIS",
		),
	skills=(
		"Insight",
		"Survival",
		),
	tools="Cartographer_Tools",
	origin_feat=Lucky,
	title="Roadwise",
	description=(
		"You adapt quickly to unfamiliar customs, temporary shelter, uncertain "
		"roads, and the small negotiations every journey requires."
		),
	)

Warrior = Build_Background(
	name="Warrior",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"STR",
		"DEX",
		"CON",
		),
	skills=(
		"Athletics",
		"Intimidation",
		),
	tools="Gaming_Set",
	origin_feat=Savage_Attacker,
	title="Battle Proven",
	description=(
		"You learned violence through service, necessity, or tradition and can "
		"read the mood and readiness of other fighting people."
		),
	)

Witch = Build_Background(
	name="Witch",
	audiences=(
		NPC_Background,
		),
	abilities=(
		"INT",
		"WIS",
		"CHA",
		),
	skills=(
		"Arcana",
		"Nature",
		),
	tools="Herbalism_Kit",
	origin_feat=Magic_Initiate_Wizard,
	title="Hedge Mysteries",
	description=(
		"You preserve a personal body of charms, remedies, warnings, and "
		"unsettling lore learned beyond formal institutions."
		),
	)


# ---------------------------------------------------------------------------
# Later official 2024-format source Maps
# ---------------------------------------------------------------------------


OFFICIAL_2024_BACKGROUNDS = Register_Official_2024_Backgrounds(
	build_background=Build_Background,
	pc_background=Available,
	npc_background=NPC_Background,
	artisan_tools=ARTISAN_TOOLS,
	origin_feats=BACKGROUND_ORIGIN_FEATS,
	)

globals().update(
	{
		tag.__name__: tag
		for tag in OFFICIAL_2024_BACKGROUNDS
		}
	)


# ---------------------------------------------------------------------------
# Field-derived registries
# ---------------------------------------------------------------------------


class Background_Registry(
	Mapping[
		str,
		type[Background],
	],
	):
	"""Live read-only view over Background Pin Fields."""

	def __init__(
			registry,
			*,
			source: type[Background_Audience] | None = None,
			required: tuple[type[Background_Audience], ...] = (),
			excluded: tuple[type[Background_Audience], ...] = (),
			):
		registry.source = source
		registry.required = required
		registry.excluded = excluded

	def _tags(
			registry,
			) -> tuple[type[Background], ...]:
		candidates = (
			tuple(
				registry.source[:]
				)
			if registry.source is not None
			else tuple(
				Background_Audience[:]
				)
			)

		return tuple(
			tag
			for tag in candidates
			if all(
				tag in audience
				for audience in registry.required
				)
			and all(
				tag not in audience
				for audience in registry.excluded
				)
			)

	def __getitem__(
			registry,
			name: str,
			) -> type[Background]:
		for tag in registry._tags():
			if tag.NAME == name:
				return tag

		raise KeyError(
			name
			)

	def __iter__(
			registry,
			) -> Iterator[str]:
		return (
			tag.NAME
			for tag in registry._tags()
			)

	def __len__(
			registry,
			) -> int:
		return len(
			registry._tags()
			)


def Backgrounds_For(
	audience: type[Background_Audience],
	):
	"""Return a live read-only registry derived from one audience Field."""
	if audience not in (
		Available,
		NPC_Background,
		):
		raise ValueError(
			"Backgrounds_For requires Available or NPC_Background."
			)

	return Background_Registry(
		source=audience
		)


PLAYER_BACKGROUNDS = Backgrounds_For(
	Available
	)
NONPLAYER_BACKGROUNDS = Backgrounds_For(
	NPC_Background
	)
SHARED_BACKGROUNDS = Background_Registry(
	source=Available,
	required=(
		NPC_Background,
		),
	)
NONPLAYER_ONLY_BACKGROUNDS = Background_Registry(
	source=NPC_Background,
	excluded=(
		Available,
		),
	)
NONPLAYER_ONLY_BACKGROUND_NAMES = tuple(
	NONPLAYER_ONLY_BACKGROUNDS
	)
BACKGROUNDS = Background_Registry(
	source=Background_Audience
	)


def Find_Background(
		target,
		) -> str:
	"""Find the narrative Background label from current Tag membership."""
	carried = tuple(
		tag
		for tag in BACKGROUNDS.values()
		if target in tag
		)

	if len( carried ) > 1:
		raise ValueError(
			"A Character carries conflicting Backgrounds: "
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


def Background_Is_Available(
	char,
	tag,
	) -> bool:
	"""Return whether the Character Role matches a Pin on the Background Tag."""
	if (
		not isinstance(
			tag,
			type,
			)
		or not issubclass(
			tag,
			Background,
			)
		):
		return False

	return _eligible_for(
		char,
		tag,
		)


def Apply_Background(
	char,
	name=None,
	):
	"""Apply one declared Background allowed by the Character's Role."""
	resolved_name = (
		name
		or getattr(
			char,
			"background",
			None,
			)
		)

	if not resolved_name:
		available_names = tuple(
			sorted(
				tag.NAME
				for tag in BACKGROUNDS.values()
				if Background_Is_Available(
					char,
					tag,
					)
				)
			)

		if not available_names:
			raise ValueError(
				"No Background is available to this Character Role."
				)

		dice_bag = char.Dice_Bag(
			"identity.background",
			version="1",
			namespace="GenLegendActor",
			)
		resolved_name = char.Pick(
			available_names,
			dice=dice_bag,
			)

	current = getattr(
		char,
		"background",
		None,
		)

	if (
		current
		and current != resolved_name
		):
		raise ValueError(
			"A Character cannot carry two Backgrounds: "
			f"{current!r} and {resolved_name!r}."
			)

	tag = BACKGROUNDS.get(
		resolved_name
		)

	if tag is None:
		raise KeyError(
			f"BackgroundKit has no Tag for {resolved_name!r}."
			)

	if not Background_Is_Available(
		char,
		tag,
		):
		raise ValueError(
			f"Background {resolved_name!r} is not available to this "
			"Character Role."
			)

	if char not in tag:
		# The Origin Feat awakens as a base of this Tag, before the Background
		# grants its Tool.  Passing the Background lets the Feat reserve what
		# the Background will certainly grant, so a random draw cannot spend a
		# proficiency on it twice (Hermeticist's Crafter took Jeweler's Tools in
		# 13 of 60 seeds without it).
		tag(
			char,
			background_tag=tag,
			)

	return tag


def Apply_Background_Training(
	char,
	):
	"""Replay the applied Background's Tag-owned training onto its skill bag."""
	name = getattr(
		char,
		"background",
		None,
		)
	tag = BACKGROUNDS.get(
		name
		)

	if tag is None:
		raise ValueError(
			f"Cannot apply training for unknown Background {name!r}."
			)

	# Both parts are already in the ledger from the Background's Imprint; this
	# projects them onto the sheet that now exists.
	_grant_skills(
		char,
		tag,
		)
	_grant_tool(
		char,
		tag,
		)

	return char.skills


def Apply_Background_Abilities(
	char,
	):
	"""Materialize the Background ability Record after scores exist."""
	if getattr(
		char,
		"background_abilities_applied",
		False,
		):
		return char.AS

	chosen = getattr(
		char,
		"background_asi",
		None,
		)

	if not chosen:
		return char.AS

	for stat, bonus in chosen:
		setattr(
			char.AS,
			stat,
			getattr(
				char.AS,
				stat,
				)
			+ bonus,
			)

	char.background_abilities_applied = True

	return char.AS


# ---------------------------------------------------------------------------
# Focused contracts
# ---------------------------------------------------------------------------


def _test_meta_fields():
	assert len(
		tuple(
			Background_Audience[:]
			)
		) == 87
	assert len(
		tuple(
			Available[:]
			)
		) == 61
	assert len(
		tuple(
			NPC_Background[:]
			)
		) == 87
	assert Merchant in Available
	assert Merchant in NPC_Background
	assert Doctor not in Available
	assert Doctor in NPC_Background


def _test_all_backgrounds():
	for index, (
		name,
		tag,
		) in enumerate(
			BACKGROUNDS.items()
			):
		character = Character(
			seed=100 + index
			)

		if tag in Available:
			Player(
				character
				)
		else:
			NonPlayer(
				character
				)

		tag(
			character
			)

		assert character in tag
		assert character in Background
		assert character.background == name
		assert character in tag.ORIGIN_FEAT
		assert len(
			tag.ABILITIES
			) == 3
		assert len(
			tag.SKILLS
			) == 2
		assert tag.TOOLS


def _test_ability_boost_soft_opt():
	from AtlasLusoris.GuildKit import Rogue

	character = Character(
		seed=24
		)
	Player(
		character
		)
	Rogue(
		character
		)
	character.AS = AbilityScores(
		STR=10,
		DEX=15,
		CON=12,
		INT=11,
		WIS=13,
		CHA=14,
		character=character,
		)

	assert _pick_boost_ability(
		character,
		[
			"DEX",
			"CHA",
			"WIS",
			],
		character.AS,
		) == "DEX"


def _test_apply_by_name():
	character = Character(
		seed=23
		)
	Player(
		character
		)
	Apply_Background(
		character,
		"Soldier",
		)

	assert character in Soldier
	assert character in Savage_Attacker
	assert Find_Background( character ) == "Soldier"
	assert f"{character:Background}" == "Soldier"


def _test_hook_and_slots():
	"""A Hook is its own titled entry, and ``{guild}`` resolves on reading."""
	character = Character(
		seed=25
		)
	Player(
		character
		)
	character.char_class = "Barbarian"

	_grant_narrative(
		character,
		"Scribe",
		"the {guild} School",
		)
	_grant_hook(
		character,
		Entry(
			title="Alumni",
			definition="Your {guild} classmates remember you.",
			),
		)
	background, hook = character.features[ -2: ]

	assert (
		background.name,
		background.source,
		background.description,
		) == (
		"Scribe",
		"Background",
		"the Barbarian School",
		)
	assert (
		hook.name,
		hook.source,
		hook.description,
		) == (
		"Alumni",
		"Background Hook",
		"Your Barbarian classmates remember you.",
		)
	assert background.narrative and hook.narrative

	_grant_hook(
		character,
		None,
		)
	assert character.features[ -1 ] is hook

	try:
		_validate_background_construction(
			name="Untitled Hook",
			audiences=(
				Available,
				),
			abilities=Soldier.ABILITIES,
			skills=Soldier.SKILLS,
			tools=Soldier.TOOLS,
			origin_feat=Soldier.ORIGIN_FEAT,
			title="Untitled Hook",
			description="A life.",
			hook=Entry(
				definition="A price with no name.",
				),
			origin_feat_options=Soldier.ORIGIN_FEAT_OPTIONS,
			source_title="Test",
			source_url="",
			source_locator="",
			source_kind="test",
			)
	except ValueError as error:
		assert "Hook" in str(
			error
			), error
	else:
		raise AssertionError(
			"A Hook without a title must be refused."
			)


def _test_official_hooks():
	"""The sixteen settled officials: own name as title, and a titled Hook."""
	hooks = {
		Acolyte: "Shelter of the Faithful",
		Artisan: "The Guild",
		Charlatan: "False Identity",
		Criminal: "Criminal Contact",
		Entertainer: "By Popular Demand",
		Farmer: "Rustic Hospitality",
		Guard: "Network of Favors",
		Guide: "The Ways Between",
		Hermit: "What You Found Out There",
		Merchant: "I Know Where to Get It",
		Noble: "The Weight of the Crown",
		Sage: "Working Hypothesis",
		Sailor: "Ship's Passage",
		Scribe: "Alumni",
		Soldier: "Old Company",
		Wayfarer: "The Overlooked",
		}

	for tag, hook_title in hooks.items():
		assert tag.TITLE == tag.NAME, tag.NAME
		assert tag.HOOK.title == hook_title, tag.NAME
		assert tag.HOOK.definition.strip(), tag.NAME

	assert "the {guild} School" in Scribe.DESCRIPTION


def _test_background_training_reaches_the_ledger():
	"""Skills and a named Tool reach the ledger once, and replay adds nothing."""
	from AtlasInventarium.ToolsKit import MUSICAL_INSTRUMENTS

	character = Character(
		seed=26
		)
	Player(
		character
		)
	Entertainer(
		character
		)

	def batches():
		return {
			batch.grant_id: batch
			for batch in Ensure_Training_Record(
				character
				).gains
			if batch.grant_id.startswith( "Background." )
			}

	first = batches()
	skills = first[ "Background.Entertainer.skills" ]
	tool = first[ "Background.Entertainer.tool" ]

	assert [
		grant.capability.key
		for grant in skills.grants
		] == list( Entertainer.SKILLS )
	assert len( tool.grants ) == 1
	assert tool.grants[ 0 ].capability in MUSICAL_INSTRUMENTS
	assert Is_Trained(
		character,
		tool.grants[ 0 ].capability,
		)

	_grant_skills(
		character,
		Entertainer,
		)
	_grant_tool(
		character,
		Entertainer,
		)
	assert batches() == first


def _test_one_tool_is_never_spent_twice():
	"""No menu offers one tool twice, and no Background re-grants its Feat's."""
	from collections import Counter

	for name, tag in BACKGROUNDS.items():
		menu = Background_Tool_Menu(
			tag
			)
		assert len( menu ) == len( set( menu ) ), name

	for name in (
			"Hermeticist",
			"Archaeologist",
			"Artisan",
			):
		for seed in range( 20 ):
			character = Character(
				seed=seed
				)
			Player(
				character
				)
			Apply_Background(
				character,
				name,
				)
			spent = Counter(
				grant.capability
				for batch in Ensure_Training_Record(
					character
					).gains
				for grant in batch.grants
				)
			assert max( spent.values() ) == 1, ( name, seed, spent )


def _self_test():
	_test_meta_fields()
	_test_all_backgrounds()
	_test_ability_boost_soft_opt()
	_test_apply_by_name()
	_test_hook_and_slots()
	_test_official_hooks()
	_test_background_training_reaches_the_ledger()
	_test_one_tool_is_never_spent_twice()

	print(
		"OK — BackgroundKit MetaTOP self-test "
		f"({len(BACKGROUNDS)} backgrounds)"
		)


__all__ = (
	"ARTISAN_TOOLS",
	"Available",
	"BACKGROUNDS",
	"Background",
	"Background_Audience",
	"Background_Is_Available",
	"Backgrounds_For",
	"Build_Background",
	"Find_Background",
	"NPC_Background",
	"NONPLAYER_BACKGROUNDS",
	"NONPLAYER_ONLY_BACKGROUNDS",
	"NONPLAYER_ONLY_BACKGROUND_NAMES",
	"OFFICIAL_2024_BACKGROUNDS",
	"PLAYER_BACKGROUNDS",
	"SHARED_BACKGROUNDS",
	"Apply_Background",
	"Apply_Background_Training",
	*tuple(
		tag.__name__
		for tag in BACKGROUNDS.values()
		),
	)


if __name__ == "__main__":
	_self_test()
