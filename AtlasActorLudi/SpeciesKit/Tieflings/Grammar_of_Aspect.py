"""
Grammar of Aspect — the rewrite rules a Tiefling's aspect is written with.

The collapse (``Fiendish_Aspect``) chooses *what* a Tiefling looks like and
which few things the presentation dwells on.  This grammar chooses *how it is
said*.  Each structure is a sequence of sentence symbols (``Map_of_Marks``);
every symbol here rewrites to one of several productions.  The marks are the
lexicon, slotted in by name, and the marks said on their own bring whole
sentences of their own, several each:

- ``{horns}``       a horn shape's sentences, with ``{horn_material}`` inside
- ``{horn_material}`` a bare noun phrase ("old ivory", "polished jet")
- ``{eyes}``        the eyes' sentences
- ``{fur}``         a noun phrase ("fox red, spotted with onyx black")
- ``{sheen}``       a bare metal ("silver", "copper")
- ``{scent}``       a scent's sentences
- ``{tail}``        a tail's sentences
- ``{place}``       where the bloodline is suggested to start ("Hades")

Every production must read as English for every item its slots can hold, and
none breaks the flow with a semicolon.  The self-test checks that the grammar
is closed (every symbol has a rule, every rule is used, every lexical item is
one the aspect fills); whether each derivation reads well is checked by
reading them.  Words a production adds are not keyed, so a production should
not reuse a word a mark may bring.
"""

from __future__ import annotations


GRAMMAR: dict[str, tuple[str, ...]] = {

	# --- Sentences -------------------------------------------------------

	"HORNS": (
		"{horns}",
		),

	"EYES": (
		"{eyes}",
		),

	# The fur and its sheen are one image.  {fur} may carry commas of its own
	# ("wolf grey, striped with onyx black"), so the sheen comes first and
	# every sentence ends on {fur}.
	"FUR": (
		"Lamplight finds {sheen} in your fur, which is {fur}.",
		"A glint of {sheen} runs through your fur, which is {fur}.",
		"Your fur carries a sheen of {sheen}: {fur}.",
		"When you turn, a sheen of {sheen} moves through your coat of {fur}.",
		),

	"TAIL": (
		"{tail}",
		),

	"SCENT": (
		"{scent}",
		),

	"PLACE": (
		"Your looks suggest your {LINE} {BEGINS} {place}.",
		"{WHO} would say your {LINE} {BEGINS} {place}.",
		"{WHO} would trace your {LINE} to {place}.",
		"Some whisper that your {LINE} comes straight from {place}.",
		),

	"PLACE_OPENING": (
		"Your looks suggest your {LINE} {BEGINS} {place}, though nobody can say how many generations ago.",
		"{WHO} would trace your {LINE} to {place}, though not how far.",
		"Some whisper that your {LINE} comes straight from {place}, and nobody asks twice.",
		),

	# --- Phrases ---------------------------------------------------------

	"WHO": (
		"Anyone who knows the signs",
		"Those who read such things",
		"A scholar of such matters",
		"The stories",
		),

	"LINE": (
		"bloodline",
		"line",
		"blood",
		),

	# No "back" and no "old" anywhere in the grammar's own words: the marks
	# use both ("curl back", "along your back", "old ivory").
	"BEGINS": (
		"starts in",
		"begins in",
		"rises from",
		"was first kindled in",
		),
	}
