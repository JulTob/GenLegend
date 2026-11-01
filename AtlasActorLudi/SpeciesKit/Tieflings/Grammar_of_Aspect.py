"""
Grammar of Aspect — the rewrite rules a Tiefling's aspect is written with.

The register is **punk** (Julio, 2026-11-01): strangely beautiful, born this
way, a rough past and, mysteriously, a road still open.  The world's regard is
a seasoning, never the meal: one or two touches in a paragraph (a scar, a
stare outlasted, a hood thrown away) change the whole vibe; a paragraph made
only of them is merely sad.

So variety comes from structure inside structure, not from more lines:

- a **sentence** is a core clause, and sometimes an **afterthought**, a short
  sentence of its own: "{horns}.{HORN_AFTER}", where most afterthoughts are
  empty and a few carry the attitude (" You have never once filed them
  down.").  An afterthought never joins the clause with a comma, so it can
  never pile onto a clause that already has one;
- a feature may instead be opened by a **frame** and finished by the mark as
  a noun phrase: "You were born with them: ram's horns of polished jet,
  curling back over your ears.";
- a **closing** line is a past half and a future half, drawn apart:
  "{PAST}, {FUTURE}." (four times four lines from eight).

A production listed more than once is weighted on purpose: an empty coda is
listed several times so the attitude stays rare.  The marks are the lexicon
(each mark sentence is a clause, with no full stop of its own):

- ``{horns}`` / ``{eyes}`` / ``{scent}`` / ``{tail}`` / ``{bearing}``: a
  mark's own clauses
- ``{horn_phrase}`` / ``{eyes_phrase}`` / ``{scent_phrase}``: the marks as
  noun phrases; ``{omen}``: what people say a scent means
- ``{horn_material}``, ``{fur}``, ``{sheen}``, ``{place}``
- ``{full_name}``: kept, and filled when the sheet is printed (#124)

Every production must read as English for every item its slots can hold;
no semicolons.  Words a production adds are not keyed, so a production
should not reuse a word a mark may bring.
"""

from __future__ import annotations


GRAMMAR: dict[str, tuple[str, ...]] = {

	# --- Sentences -------------------------------------------------------

	"HORNS": (
		"{horns}.{HORN_AFTER}",
		"{horns}.{HORN_AFTER}",
		"{horns}.{HORN_AFTER}",
		"{HORN_FRAME}: {horn_phrase}.",
		),

	"EYES": (
		"{eyes}.{EYE_AFTER}",
		"{eyes}.{EYE_AFTER}",
		"{eyes}.{EYE_AFTER}",
		"{EYE_FRAME}: {eyes_phrase}.",
		),

	# {fur} may carry commas of its own, so the body ends on it, and any
	# afterthought is a sentence of its own.
	"FUR": (
		"{FUR_BODY}{FUR_AFTER}",
		),

	"FUR_BODY": (
		"Lamplight finds {sheen} in your fur, which is {fur}.",
		"A glint of {sheen} runs through your fur, which is {fur}.",
		"Your fur carries a sheen of {sheen}: {fur}.",
		"When you turn, a sheen of {sheen} moves through your coat of {fur}.",
		),

	"FUR_AFTER": (
		"",
		"",
		"",
		"",
		" An old scar runs through it, and you never bothered to hide it.",
		" You keep it short, wild, and entirely your own.",
		" Here and there it grows back paler, over scars you no longer explain.",
		),

	"SCENT": (
		"{scent}.{SCENT_AFTER}",
		"{scent}.{SCENT_AFTER}",
		"{SAY_SCENT} you smell like {omen}, of {scent_phrase}.{SCENT_AFTER}",
		),

	"TAIL": (
		"{tail}.",
		),

	"BEARING": (
		"{bearing}.",
		),

	"CLOSE": (
		"{PAST}, {FUTURE}.",
		),

	"PLACE": (
		"Your looks suggest your {LINE} {BEGINS} {place}.",
		"{WHO} would say your {LINE} {BEGINS} {place}.",
		"{WHO} would trace your {LINE} to {place}.",
		"Some whisper that your {LINE} comes straight from {place}.",
		"{HOSTILE} say your {LINE} {BEGINS} {place}, as if that settled anything.",
		),

	"PLACE_OPENING": (
		"Your looks suggest your {LINE} {BEGINS} {place}, though nobody can say how many generations ago.",
		"{WHO} would trace your {LINE} to {place}, though not how far.",
		"Some whisper that your {LINE} comes straight from {place}, and nobody asks twice.",
		),

	# --- Afterthoughts: the attitude, rarely ------------------------------

	"HORN_AFTER": (
		"",
		"",
		"",
		"",
		" You have never once filed them down.",
		" One was chipped in an old fight, and it is no less beautiful for it.",
		" Strangers stare until they forget to be afraid.",
		" You wear them like a crown you chose.",
		" Children point, and these days you point back.",
		),

	"EYE_AFTER": (
		"",
		"",
		"",
		"",
		" You have stopped looking away first.",
		" People call them unsettling, right up until they call them beautiful.",
		" They have seen worse than whoever is staring back.",
		" Someone once told you they were beautiful, and you still remember who.",
		),

	"SCENT_AFTER": (
		"",
		"",
		"",
		" You have made your peace with it.",
		" Some find it unsettling, and a few find it irresistible.",
		" You wear it like a perfume you chose.",
		" Nobody has ever washed it off you, and you stopped letting them try.",
		),

	# No afterthought for the tail: its own sentences already carry how it is
	# kept (wound under a coat, or lashing in the open).

	# --- Frames: a feature opened by how it is met -----------------------

	"HORN_FRAME": (
		"You were born with them",
		"Nobody forgets your horns",
		"Strangers see the horns first, and you a little after",
		"{full_name}'s face is strangely beautiful, but most people remember the horns",
		),

	"EYE_FRAME": (
		"People remember your eyes long after your name",
		"Few people hold your gaze for long",
		"Your eyes are the strangest thing about you, and the loveliest",
		),

	"SAY_SCENT": (
		"People say",
		"Behind your back, they say",
		"You have been told, more than once, that",
		),

	# --- The closing: a rough past, and the road still open --------------

	"PAST": (
		"Your past is rough at the edges",
		"You have been run out of more towns than you can name",
		"You were born this way",
		"You have walked a hard road to get here",
		),

	"FUTURE": (
		"but the road ahead is wide open",
		"and still you walk as if the world owes you a song",
		"but you have decided the best part has not happened yet",
		"and you have decided that is the interesting part",
		),

	# --- The place: named, never described --------------------------------

	"WHO": (
		"Anyone who knows the signs",
		"Those who read such things",
		"A scholar of such matters",
		),

	"HOSTILE": (
		"Those who spit at your feet",
		"The priests who turned you away",
		),

	"LINE": (
		"bloodline",
		"line",
		"blood",
		),

	"BEGINS": (
		"starts in",
		"begins in",
		"rises from",
		"was first kindled in",
		),
	}
