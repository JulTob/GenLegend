"""
Collapse — a small wave-function collapse over named slots.

A **wave** is a handful of slots, and each slot holds the candidates it may
still become.  Collapsing repeats three steps until every slot holds exactly
one value:

1. **Choose the slot.**  The open slot with the fewest candidates left (the
   lowest entropy) goes first; on a tie, the one declared first.
2. **Draw its value.**  One of its candidates, with the Character's own dice
   (Decree 0002).  A slot with a single candidate takes it without rolling.
3. **Propagate.**  Every rule may narrow the other slots, given what has been
   drawn so far, and the rules run again until nothing changes.

A slot left with no candidates is a contradiction.  The wave then starts again
from its first state, drawing on from the same dice, so the result is still a
pure function of the Character's seed.  After ``ATTEMPTS`` contradictions in a
row the collapse fails loudly: the data cannot be satisfied.  The error names
the last dead end: the slot left empty, and the rule that emptied it.

Retries are deterministic, but they shape the odds.  A wave that often runs
into a contradiction keeps only the attempts that succeed, so its results
lean toward whatever the rules let through, not toward an even draw over the
candidates.  A rule that empties slots often is a rule that reshapes the
distribution, and is worth measuring.

``ABSENT`` is a candidate like any other, meaning "this slot stays empty".

Nothing here knows about Tieflings.  A rule is a plain function

	rule( drawn, domains ) -> domains

where ``drawn`` maps each collapsed slot to its value, and ``domains`` maps
every slot to the candidates it still holds.  A rule returns the domains it
narrowed; it never adds a candidate back.  A rule that did could undo another
rule's work forever, so propagation checks every rule's answer and fails
loudly (``Collapse_Rule_Error``) on a rule that widens a slot, adds one or
drops one.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


ATTEMPTS = 12


class _Absent:
	"""The value of a slot that stays empty."""

	def __repr__(
			self,
			) -> str:
		return "ABSENT"


ABSENT = _Absent()


@dataclass(
		frozen=True,
		)
class Slot:
	"""One place in the wave, and every candidate it starts with."""

	name: str
	candidates: tuple


Domains = dict[str, tuple]
Drawn = dict[str, object]
Rule = Callable[[Drawn, Domains], Domains]


@dataclass(
		frozen=True,
		)
class Dead_End:
	"""Where one attempt failed: the slot left empty, and the rule that emptied it."""

	slot: str
	rule: str


class Collapse_Contradiction(RuntimeError):
	"""The rules left a slot with no candidate, every time."""

	def __init__(
			self,
			dead_end: Dead_End,
			) -> None:
		self.dead_end = dead_end
		super().__init__(
				f"Collapse: no attempt in {ATTEMPTS} filled every slot.  "
				f"The last one left slot {dead_end.slot!r} empty "
				f"(emptied by {dead_end.rule})."
				)


class Collapse_Rule_Error(ValueError):
	"""A rule broke the contract: it may only narrow the slots it is given."""


def _lowest_entropy(
		slots: tuple[Slot, ...],
		drawn: Drawn,
		domains: Domains,
		) -> str:
	"""The open slot with the fewest candidates; the first declared on a tie."""
	open_slots = [
			slot.name
			for slot in slots
			if slot.name not in drawn
			]
	return min(
			open_slots,
			key=lambda name: len( domains[name] ),
			)
		#-- min() keeps the first of equals, so declaration order breaks ties.


def _draw(
		target,
		candidates: tuple,
		dice,
		):
	"""One candidate: the only one, or one drawn from the Character's dice."""
	if len( candidates ) == 1:
		return candidates[0]
	return target.Pick(
			list( candidates ),
			dice=dice,
			)


def _rule_name(
		rule: Rule,
		) -> str:
	"""A rule's name for an error message (a partial has none of its own)."""
	return getattr(
			rule,
			"__name__",
			repr( rule ),
			)


def _check_only_narrows(
		rule: Rule,
		before: Domains,
		after: Domains,
		) -> None:
	"""Fail loudly unless the rule kept every slot and only removed candidates."""
	if set( after ) != set( before ):
		raise Collapse_Rule_Error(
				f"Collapse: rule {_rule_name( rule )} added or dropped a slot."
				)
	for name, candidates in after.items():
		if not set( candidates ) <= set( before[name] ):
			raise Collapse_Rule_Error(
					f"Collapse: rule {_rule_name( rule )} added a candidate "
					f"back to slot {name!r}."
					)


def _newly_emptied(
		before: Domains,
		after: Domains,
		) -> str | None:
	"""The first slot, in wave order, that held candidates before and none after."""
	for name, candidates in after.items():
		if not candidates and before[name]:
			return name
	return None


def _propagate(
		rules: tuple[Rule, ...],
		drawn: Drawn,
		domains: Domains,
		) -> tuple[Domains, Dead_End | None]:
	"""
	Run every rule until no domain narrows any further.

	This ends because every pass either removes a candidate or stops, and a
	wave holds finitely many.  That holds only while rules never add a
	candidate back, so each rule's answer is checked (``_check_only_narrows``).

	Returns the narrowed domains, and the first dead end met on the way (the
	first slot a rule emptied), or ``None``.
	"""
	dead_end = None
	while True:
		narrowed = dict( domains )
		for rule in rules:
			answer = rule(
					drawn,
					narrowed,
					)
			_check_only_narrows(
					rule,
					narrowed,
					answer,
					)
			emptied = _newly_emptied(
					narrowed,
					answer,
					)
			if dead_end is None and emptied is not None:
				dead_end = Dead_End(
						slot=emptied,
						rule=f"rule {_rule_name( rule )}",
						)
			narrowed = answer
		if narrowed == domains:
			return domains, dead_end
		domains = narrowed


def _empty_from_the_start(
		slots: tuple[Slot, ...],
		) -> Dead_End | None:
	"""A slot declared with no candidates at all: a dead end before any rule."""
	for slot in slots:
		if not slot.candidates:
			return Dead_End(
					slot=slot.name,
					rule="its own declaration (no candidates to begin with)",
					)
	return None


def _collapse_once(
		target,
		slots: tuple[Slot, ...],
		rules: tuple[Rule, ...],
		dice,
		) -> Drawn | Dead_End:
	"""One attempt at the whole wave: every slot drawn, or where it failed."""
	empty = _empty_from_the_start( slots )
	if empty is not None:
		return empty
	drawn: Drawn = {}
	domains: Domains = {
			slot.name: tuple( slot.candidates )
			for slot in slots
			}
	domains, dead_end = _propagate(
			rules,
			drawn,
			domains,
			)
	while len( drawn ) < len( slots ):
		if dead_end is not None:
			return dead_end
		name = _lowest_entropy(
				slots,
				drawn,
				domains,
				)
		value = _draw(
				target,
				domains[name],
				dice,
				)
		drawn[name] = value
		domains[name] = ( value, )
		domains, dead_end = _propagate(
				rules,
				drawn,
				domains,
				)
	if dead_end is not None:
		return dead_end
	return drawn


def Collapse(
		target,
		slots: tuple[Slot, ...],
		rules: tuple[Rule, ...],
		dice,
		) -> Drawn:
	"""
	Collapse the wave into one value per slot, with the Character's dice.

	Deterministic for a given seed and Dice Bag: the slot order, the rules and
	the dice decide everything, and no set or hash order is ever consulted.
	"""
	if not slots:
		raise ValueError(
				"Collapse: a wave needs at least one slot."
				)
	names = [
			slot.name
			for slot in slots
			]
	if len( set( names ) ) != len( names ):
		raise ValueError(
				"Collapse: every slot needs its own name."
				)
	last_dead_end = None
	for _attempt in range( ATTEMPTS ):
		result = _collapse_once(
				target,
				slots,
				rules,
				dice,
				)
		if not isinstance( result, Dead_End ):
			return result
		last_dead_end = result
	raise Collapse_Contradiction(
			last_dead_end,
			)
