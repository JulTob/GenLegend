"""
The vocabulary of a Tiefling's aspect, as Tags catalogued by Pins.

Every piece of the look (one shape of horns, one scent, one way the fur is
patterned) is a small Tag, an ``Aspect_Mark``.  Marks are never applied to a
Character; they are words in a vocabulary, and two kinds of Pin say things
about them:

- an **Aspect_Part** Pin says which slot of the aspect a mark can fill:
  ``crown in Horn_Shape``;
- a **Lent_By** Pin says which legacy lends it: ``crown in Chthonic_Marks``.
  A mark lent by every legacy (a plain fur pattern) is pinned to all three.

``Aspect_Part`` also keeps one Record on each mark, its ``KEYS``: the salient
words it brings to the page.  The collapse never lets two marks with a word in
common sit in the same aspect, so nobody gets a gold iris, a gold sheen and
ember-gold fur at once.

Structures are marks too (``Structure``): one way of ordering the sentences.
They belong to no legacy.

The rows themselves live in ``Map_of_Marks``.
"""

from __future__ import annotations

from TopKit import Pin
from TopKit import Pre
from TopKit import Record
from TopKit import Tag


class Aspect_Mark(Tag):
	"""One piece of a Tiefling's look: a word in the aspect's vocabulary."""

	# A phrase that fills its slot; see each Aspect_Part for the grammar.
	TEXT = ""


class Structure_Mark(Aspect_Mark):
	"""One way of ordering the aspect's sentences."""

	# The sentences, in order, each written as symbols of the aspect's grammar
	# (``Grammar_of_Aspect``).  A sentence that derives to nothing is dropped.
	SENTENCES: tuple[str, ...] = ()


def _is_mark(
		target,
		) -> bool:
	return isinstance(
			target,
			type,
			) and issubclass(
			target,
			Aspect_Mark,
			)


@Pin
class Aspect_Part(Tag):
	"""Root Pin: which slot of the aspect a mark can fill."""

	@Pre
	def Marks_Only(
			target,
			):
		return _is_mark( target )

	@Record
	def KEYS(
			target,
			*,
			keys=(),
			) -> tuple[str, ...]:
		return tuple(
				sorted(
						set( keys )
						)
				)


class Structure(Aspect_Part):
	"""How the sentences are ordered.  Marks here are ``Structure_Mark``."""


class Horn_Shape(Aspect_Part):
	"""
	Completes "Your horns ___": a verb phrase, plural, present tense, with no
	comma and no "and" of its own (the grammar adds clauses after it).
	"""


class Horn_Material(Aspect_Part):
	"""What the horns look made of: a bare noun phrase, no article ("old ivory")."""


class Eyes(Aspect_Part):
	"""Completes "Your eyes ___": a verb phrase, plural, present tense."""


class Coat(Aspect_Part):
	"""A fur colour, as a noun phrase that follows "Your fur is"."""


class Coat_Pattern(Aspect_Part):
	"""How the fur wears its colours: a template with {a}, and {b} when two."""


class Sheen(Aspect_Part):
	"""The metal the fur catches the light like: a noun ("copper")."""


class Scent(Aspect_Part):
	"""A faint smell: a noun phrase that follows "a trace of"."""


class Tail(Aspect_Part):
	"""A whole sentence about the tail."""


@Pin
class Lent_By(Tag):
	"""Root Pin: which legacy lends a mark to a Tiefling's aspect."""

	@Pre
	def Marks_Only(
			target,
			):
		return _is_mark( target )


class Abyssal_Marks(Lent_By):
	"""Marks the Abyss lends."""


class Chthonic_Marks(Lent_By):
	"""Marks Hades lends."""


class Infernal_Marks(Lent_By):
	"""Marks the Nine Hells lend."""


def Make_Mark(
		name: str,
		*,
		part: type[Aspect_Part],
		lent_by: tuple[type[Lent_By], ...],
		text: str,
		keys: tuple[str, ...] = (),
		) -> type[Aspect_Mark]:
	"""Make one mark, pin it to its part and to every legacy that lends it."""
	if part is Structure:
		raise ValueError(
				"Make_Mark: a Structure is made with Make_Structure."
				)
	if not lent_by:
		raise ValueError(
				f"Make_Mark: {name} must be lent by at least one legacy."
				)
	mark = type(
			name,
			( Aspect_Mark, ),
			{
					"TEXT": text,
					"__module__": __name__,
					"__doc__": f"Aspect mark: {text}",
					},
			)
	part(
			mark,
			keys=keys,
			)
	for legacy_marks in lent_by:
		legacy_marks( mark )
	return mark


def Make_Structure(
		name: str,
		*sentences: str,
		) -> type[Structure_Mark]:
	"""Make one sentence order and pin it as a Structure."""
	if not sentences:
		raise ValueError(
				f"Make_Structure: {name} needs at least one sentence."
				)
	structure = type(
			name,
			( Structure_Mark, ),
			{
					"SENTENCES": tuple( sentences ),
					"__module__": __name__,
					"__doc__": f"Aspect structure: {name}",
					},
			)
	Structure( structure )
	return structure


def Marks_Of(
		part: type[Aspect_Part],
		) -> tuple[type[Aspect_Mark], ...]:
	"""Every mark pinned to a part, in a stable order (by name)."""
	return tuple(
			sorted(
					part[:],
					key=lambda mark: mark.__name__,
					)
			)
		#-- Sorted by name so no draw ever depends on registration or set order.
