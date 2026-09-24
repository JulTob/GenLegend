"""
Compass of Progression

The vocabulary a Guild uses to declare what its levels bring.

A Guild kit does not narrate its progression in an if-ladder.  It declares it
as data on its Tag, in four shapes, and the Training Maps read those Reports
back when a lesson needs a number:

	Feature_Grant          a lesson earned at a level
	Choice_Progression     a pick whose total grows at named levels
	Resource_Progression   a pool whose maximum grows at named levels
	Always_Prepared        spells a Specialization keeps ready, by level

The first three were born inside FighterKit, the first Guild declared this
way.  The Sorcerer is the second, so they move here, where every Guild can
reach them without importing another Guild.  FighterKit re-exports them under
their old names.
"""

from __future__ import annotations

from dataclasses import dataclass


def _Ordered_By_Level(
		rows,
		) -> bool:
	"""True when the rows climb by level and never go back down."""
	levels = [
		level
		for level, _ in rows
		]
	return levels == sorted(
		levels
		)


@dataclass(frozen=True, slots=True)
class Feature_Grant:
	"""One feature earned at a Guild level."""

	level: int
	name: str

	def __post_init__(self) -> None:
		if self.level < 1:
			raise ValueError(
				"Feature_Grant level must be at least 1."
				)
		if not self.name:
			raise ValueError(
				"Feature_Grant name is required."
				)


@dataclass(frozen=True, slots=True)
class Choice_Progression:
	"""A stable choice whose total grows at specified Guild levels."""

	name: str
	gains: tuple[tuple[int, int], ...] = ()
	options: tuple[str, ...] = ()

	def __post_init__(self) -> None:
		if not self.name:
			raise ValueError(
				"Choice_Progression name is required."
				)
		if not all(
				level > 0 and count > 0
				for level, count in self.gains
				):
			raise ValueError(
				"Choice_Progression gains require positive levels and counts."
				)
		if not _Ordered_By_Level(
				self.gains
				):
			raise ValueError(
				"Choice_Progression gains must be ordered by level."
				)

	def total_at(
			self,
			level: int,
			) -> int:
		return sum(
			count
			for gained, count in self.gains
			if gained <= level
			)


@dataclass(frozen=True, slots=True)
class Resource_Progression:
	"""A level-indexed mutable resource maximum."""

	name: str
	values: tuple[tuple[int, str], ...]

	def __post_init__(self) -> None:
		if not self.name or not self.values:
			raise ValueError(
				"Resource_Progression requires a name and values."
				)
		if not all(
				level > 0 and value
				for level, value in self.values
				):
			raise ValueError(
				"Resource_Progression values require positive levels and non-empty values."
				)
		if not _Ordered_By_Level(
				self.values
				):
			raise ValueError(
				"Resource_Progression values must be ordered by level."
				)

	def at(
			self,
			level: int,
			) -> str | None:
		current = None
		for gained, value in self.values:
			if gained <= level:
				current = value
		return current


@dataclass(frozen=True, slots=True)
class Always_Prepared:
	"""
	Spells a Specialization keeps prepared, unlocked by Guild level.

	They never count against the number of spells the Character prepares.
	The rows hold Spell objects, not names, so a misspelt spell fails at
	import instead of vanishing from a sheet.
	"""

	gains: tuple[tuple[int, tuple], ...]

	def __post_init__(self) -> None:
		if not self.gains:
			raise ValueError(
				"Always_Prepared requires at least one row of spells."
				)
		if not all(
				level > 0 and spells
				for level, spells in self.gains
				):
			raise ValueError(
				"Always_Prepared rows require a positive level and spells."
				)
		if not _Ordered_By_Level(
				self.gains
				):
			raise ValueError(
				"Always_Prepared rows must be ordered by level."
				)
		unnamed = [
			spell
			for _, spells in self.gains
			for spell in spells
			if not getattr(
				spell,
				"name",
				None,
				)
			]
		if unnamed:
			raise ValueError(
				f"Always_Prepared expects Spell objects; got {unnamed!r}."
				)

	def at(
			self,
			level: int,
			) -> tuple:
		"""Every spell unlocked at or below this Guild level, in order."""
		return tuple(
			spell
			for gained, spells in self.gains
			if gained <= level
			for spell in spells
			)


__all__ = (
	"Always_Prepared",
	"Choice_Progression",
	"Feature_Grant",
	"Resource_Progression",
	)
