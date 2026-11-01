"""
Grammar — a small generative grammar, in the manner of Chomsky's rewrite rules.

A **grammar** is a set of rewrite rules.  Each rule names a **symbol** and the
**productions** it may be rewritten as:

	LIKENESS -> "they hold the deep lustre of {horn_material}"
	          | "they resemble the finest {horn_material}"
	          | "they might have been carved from {horn_material}"

A production is text with two kinds of slot in braces:

- ``{UPPER_CASE}`` is a **non-terminal**: another symbol of the grammar, to be
  rewritten in its turn (so rules can nest, as phrases nest in a sentence);
- ``{lower_case}`` is a **lexical item**: a word or phrase supplied from
  outside (the **lexicon**).  An item may come with several realisations (a
  tuple), one drawn like a production; and an item may hold slots of its own,
  filled in turn, so a word can bring its own frame ("Ram's horns of
  {horn_material} curl back over your ears").

Generating a text is a **derivation**: start from one symbol, choose one of
its productions with the Character's own dice (Decree 0002), and rewrite the
non-terminals inside it, leftmost first, until only words are left.  A few
choices at every level multiply: small variations accumulate into a text that
is new each time, and the same seed always derives the same text.

Nothing here knows about Tieflings.
"""

from __future__ import annotations

import re


MAX_DEPTH = 24

_SLOT = re.compile(
		r"\{([A-Za-z_]+)\}"
		)

Grammar = dict[str, tuple[str, ...]]
Lexicon = dict[str, str | tuple[str, ...]]


class Grammar_Error(ValueError):
	"""A grammar that cannot derive: an unknown symbol, or endless recursion."""


def _is_non_terminal(
		name: str,
		) -> bool:
	"""Non-terminals are written in upper case; lexical items in lower case."""
	return name.isupper()


def _choose(
		target,
		productions: tuple[str, ...],
		dice,
		) -> str:
	"""One production: the only one, or one drawn with the Character's dice."""
	if len( productions ) == 1:
		return productions[0]
	return target.Pick(
			list( productions ),
			dice=dice,
			)


def _rewrite(
		target,
		grammar: Grammar,
		symbol: str,
		lexicon: Lexicon,
		dice,
		depth: int,
		) -> str:
	"""Derive one symbol into words, rewriting nested symbols leftmost first."""
	if depth > MAX_DEPTH:
		raise Grammar_Error(
				f"Grammar: {symbol} recurses deeper than {MAX_DEPTH}."
				)
	if symbol not in grammar:
		raise Grammar_Error(
				f"Grammar: no rule for {symbol}."
				)
	production = _choose(
			target,
			grammar[symbol],
			dice,
			)
	return _fill(
			target,
			grammar,
			production,
			lexicon,
			dice,
			depth + 1,
			)


def _realise(
		target,
		grammar: Grammar,
		name: str,
		lexicon: Lexicon,
		dice,
		depth: int,
		) -> str:
	"""One lexical item: one of its realisations, with its own slots filled."""
	if depth > MAX_DEPTH:
		raise Grammar_Error(
				f"Grammar: {name} recurses deeper than {MAX_DEPTH}."
				)
	if name not in lexicon:
		raise Grammar_Error(
				f"Grammar: the lexicon has no {name}."
				)
	entry = lexicon[name]
	realisations = entry
	if isinstance( entry, str ):
		realisations = ( entry, )
	chosen = _choose(
			target,
			tuple( realisations ),
			dice,
			)
	return _fill(
			target,
			grammar,
			chosen,
			lexicon,
			dice,
			depth + 1,
			)


def _fill(
		target,
		grammar: Grammar,
		text: str,
		lexicon: Lexicon,
		dice,
		depth: int,
		) -> str:
	"""Replace every slot in a text: symbols by derivation, items from the lexicon."""
	pieces = []
	position = 0
	for slot in _SLOT.finditer( text ):
		pieces.append( text[position:slot.start()] )
		name = slot.group( 1 )
		if _is_non_terminal( name ):
			pieces.append(
					_rewrite(
							target,
							grammar,
							name,
							lexicon,
							dice,
							depth,
							)
					)
		else:
			pieces.append(
					_realise(
							target,
							grammar,
							name,
							lexicon,
							dice,
							depth,
							)
					)
		position = slot.end()
	pieces.append( text[position:] )
	return "".join( pieces )


def Derive(
		target,
		grammar: Grammar,
		text: str,
		lexicon: Lexicon,
		dice,
		) -> str:
	"""
	Derive a text: rewrite every symbol in it until only words remain.

	``text`` may be a single symbol (``"{HORNS}"``) or any text with slots.
	The derivation consumes the dice in reading order, so it is deterministic
	for a given seed and Dice Bag.
	"""
	return _fill(
			target,
			grammar,
			text,
			lexicon,
			dice,
			0,
			)
