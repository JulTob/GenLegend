"""
Grimoire of Backgrounds — one declarative record per Character Background.

A :class:`Background` carries the full 2024 record set — three ability scores,
an Origin feat, two skill proficiencies, one tool proficiency, and an equipment
package — alongside a **Name**, a **Description** of who the character is, and a
**Hook**: an ``Entry`` whose title and text the sheet prints as its own entry,
the benefit that is also a price.  ``roleplay`` is the post-wipe form of the
same text, glued to the description, and is kept only until every record
declares its Hook (QST-0122.3).

The record is the single authoring surface: write one ``Background(...)`` and
feed it through ``BackgroundKit.Make_Background`` (``OfficialBackgroundsKit``
re-exports this class as ``Official_Background_Record``) — no parallel lists.

When a de-coupled entry is adapted from an official Background, credit it with a
docstring comment above the definition (attribution is for maintainers, not the
generator, so it is not a record field)::

    # Based on the Background Chondathan Freebooter
    # source: Forgotten Realms: Heroes of Faerûn
    Vagabond = Background(
        name="Vagabond",
        ...
        )
"""

from __future__ import annotations

from dataclasses import dataclass

from AtlasVenustas import Entry


def _human(
		term: str,
		) -> str:
	"""Render a canonical snake_case game term for reading (Sleight_of_Hand)."""
	return term.replace(
		"_",
		" ",
		)


def _tool_line(
		tools,
		) -> str:
	"""Render a tool proficiency, whether a specific tool or a choice pool."""
	if isinstance(
		tools,
		str,
		):
		return _human(
			tools
			)

	return "an Artisan's Tool of your choice"


@dataclass(
	frozen=True,
	)
class Background:
	"""One Character Background in the canonical 2024 record format."""

	name: str
	description: str
	abilities: tuple[str, str, str]
	origin_feat: str
	skills: tuple[str, str]
	tools: str | tuple[str, ...]
	roleplay: str = ""
	hook: Entry | None = None
	equipment: str = "50 GP"
	origin_feat_options: tuple[str, ...] = ()

	def __str__(
			self,
			) -> str:
		return "\n\n".join(
			block
			for block in [
				f"# {self.name}",
				self.description,
				self.roleplay,
				(
					f"**{self.hook.title}.** {self.hook.definition}"
					if self.hook
					else ""
					),
				f"**Ability Scores:** {', '.join(self.abilities)}",
				f"**Feat:** {self.origin_feat}",
				"**Skill Proficiencies:** "
				+ ", ".join(
					_human(skill)
					for skill in self.skills
					),
				f"**Tool Proficiency:** {_tool_line(self.tools)}",
				f"**Equipment:** {self.equipment}",
				]
			if block
			)


__all__ = (
	"Background",
	)
