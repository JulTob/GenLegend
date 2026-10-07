"""
Map of Ideals — what an Aasimar descends from, and how it shows.

A Celestial is an Ideal with a shape: not a god and not a servant of one, but Justice itself, or Mercy, or Honor, standing where mortals can see it.  An Aasimar carries a spark of one, and the spark is visible in two places.

**Talaria** are the small vestigial wings.  They sit only where a wing could plausibly take a body's weight, which is why none of them are on the face or the front side, and each folds into something a tailor could explain: a bracer, a sash, the straps of a sandal.

**The aureola** is the halo, and it answers to *fidelity to the Ideal* rather than to virtue.  A tyrant whose ring stays perfect is entirely possible, and is a better story than a tyrant whose halo goes out.  Every tell is written so that it never names the Ideal it belongs to: watching somebody's halo dim tells you they lied, not that they descend from Justice.

An Aasimar descends from two Ideals, each drawn from the whole list at uniform random, and the same Ideal may come up twice: that is a single descent, and it is neither rarer nor commoner than any particular pair.  A mixed descent then splits across three axes that are drawn apart: the first lends the aureola its **form**, both lend the **gem** it glows like, and either may lend the **tell**.  Honor's standing flame, glowing like Beauty's opal, beating once when you see something you like, belongs to that pair and to nobody else at the table.

Nothing here is mechanical. Celestial Revelation carries the rules; this carries the face.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
	frozen=True,
	)
class Ideal:
	"""One Platonic principle, and the mark it leaves on the mortal wearing it."""

	name: str
	# The shape the aureola takes, phrased so it can follow "an aureola of" or
	# stand as its own sentence.
	form: str
	# What it looks like it is made of.  Two options so that a mixed descent has
	# something to choose between, and so the metals nod at the dwarves without
	# ever confirming anything.
	metal: str
	gem: str
	# What the halo does, never naming the Ideal that causes it.
	tell: str
	# The Muse who holds this domain, where one does.  The Muses are the main
	# Celestials, not the whole set, so an Ideal may answer to none of them: an
	# empty Muse says that, and never that the entry is unfinished.  The list is
	# open on purpose and is not counted anywhere.
	muse: str = ""


IDEALS = {
	record.name: record
	for record in (
		Ideal(
			name="Justice",
			# Justice is blind, so it lives in darkness.
			form="a circle perfectly round from wherever anyone stands",
			metal="black iron",
			gem="onyx",
			tell="It dims when you are not being honest.",
			muse="History",
			),
		Ideal(
			name="Mercy",
			form="a glow with no edge, light that fades",
			metal="gold",
			gem="amber",
			tell="When someone near you is afraid, it sends a cold feeling down your spine.",
			muse="Sacred Song",
			),
		Ideal(
			name="Sacrifice",
			# Blood is red iron.  The metal is the meaning twice over.
			form="a broken ring, with an arc of it missing",
			metal="red iron",
			gem="ruby",
			tell="It darkens for a moment whenever you see someone die.",
			muse="Tragedy",
			),
		Ideal(
			name="Truth",
			form="a ring of small lights, each orbiting on its own",
			metal="silver",
			gem="diamond",
			tell="It falls into chaos when you feel anything strongly, good or bad.",
			muse="Astronomy",
			),
		Ideal(
			name="Freedom",
			# Verdigris because that is the colour copper goes when it has
			# stood outdoors a long time and nobody has taken it down.
			form="a star of many points, set like a compass rose",
			metal="verdigris",
			gem="aquamarine",
			tell="It twinkles when you run, and beats when you fly.",
			muse="Dance",
			),
		Ideal(
			name="Beauty",
			form="slow waves of colour, one running after another",
			metal="pearl",
			gem="opal",
			tell="It beats once when you look at something you find beautiful.",
			muse="Love Poetry",
			),
		Ideal(
			name="Hope",
			# The laurel of the victor, worn before the victory.
			form="a band crowning your temples",
			metal="tin",
			gem="moonstone",
			tell="It is faint when you wake up, but brighter as you get tired.",
			muse="Comedy",
			),
		Ideal(
			name="Honor",
			form="a standing flame that burns without moving",
			metal="bronze",
			gem="jade",
			tell="Its colour changes with your mood.",
			muse="Epic Tales",
			),
		Ideal(
			name="Harmony",
			# Brass is what the instrument is made of and quartz is what keeps
			# the time.  Both of them only work by holding a ratio.
			form="rotating triangles with perfect proportions",
			metal="brass",
			gem="quartz",
			tell="It stutters when you are in pain, of body or of mind.",
			muse="Lyric & Flute",
			),
		)
	}


@dataclass(
	frozen=True,
	)
class Descent:
	"""A kind of Celestial, and the ones anybody can name.

	These are *categories*, not a ladder.  An Angel does not answer to a
	Seraph and a Muse is not junior to a Planetar: they are different sorts of
	thing, drawn from three mythologies, and none of them outranks another.
	"""

	kind: str
	names: tuple[str, ...]


# What the thing you descend from is called, which depends entirely on who is
# telling it.  The Ideal is the same either way.
DESCENTS = (
	Descent(
		kind="Angel",
		names=(
			"Raziel",
			"Camael",
			"Haniel",
			"Jofiel",
			"Barakiel",
			"Sealtiel",
			"Raguel",
			"Sariel",
			),
		),
	Descent(
		kind="Muse",
		names=(
			"Calliope",
			"Clio",
			"Erato",
			"Euterpe",
			"Melpomene",
			"Polihimnia",
			"Terpsicore",
			"Talia",
			"Urania",
			),
		),
	Descent(
		kind="Constellation",
		names=(
			"Cassiopeia",
			"Andromeda",
			"Lyra",
			"Draco",
			"Perseus",
			"Aquila",
			"Corvus",
			"Cignus",
			"Carina",
			),
		),
	Descent(
		kind="Star",
		names=(
			"Polaris",
			"Vega",
			"Sirius",
			"Altair",
			"Antares",
			"Rigel",
			"Deneb",
			"Arcturus",
			"Spica",
			"Canopus",
			),
		),
	Descent(
		# The wandering stars, under the names the Greeks gave them.
		kind="Planetar",
		names=(
			"Lucifer",
			"Hesperus",
			"Fosforos",
			"Eosforus",
			"Piroeis",
			"Faezon",
			"Stilbon",
			"Fainon",
			"Ermis",
			"Aris",
			"Saturnus",
			"Ploutunas",
			),
		),
	Descent(
		kind="Throne",
		names=(
			"Zafkiel",
			"Ofaniel",
			"Orifiel",
			"Galgaliel",
			),
		),
	# The burning ones.
	Descent(
		kind="Seraph",
		names=(
			"Serafiel",
			"Jehoel",
			"Kemuel",
			"Nazanael",
			),
		),
	Descent(
		# Sphinxes wear the names of the things they guard.
		kind="Sphinx",
		names=(
			"Aramakis",
			"Memoris",
			"Mnemosine",
			"Sofrosine",
			"Ananke",
			"Metis",
			"Peizo",
			"Nemesis",
			"Temis",
			"Eleos",
			"Tisia",
			"Aletia",
			"Eleuteria",
			"Aglaya",
			"Elpis",
			"Aidos",
			"Dike",
			),
		),
	)


# How two metals share one pair of wings.  {a} is the first Ideal's metal and
# {b} is the second's; the drawing picks the arrangement.
PLUMAGES = (
	"{a} on the back and {b} beneath",
	"{a} at the base, running to {b} at the tips",
	"{a}, every feather edged in {b}",
	"{a}, barred across with {b}",
	"{a}, speckled with {b}",
	"{a} above, and {b} that only shows when they open",
	"{a} with one band of {b} across them",
	)

# And how one metal wears them alone.
SINGLE_PLUMAGES = (
	"{a}",
	"{a}, darker at the tips",
	"{a}, paler underneath",
	"{a} all the way through",
	)


@dataclass(
	frozen=True,
	)
class Perch:
	"""Where the talaria sit, and what they pass for when folded."""

	place: str
	disguise: str


# Only where a wing could take a body's weight: nothing on the face, nothing on
# the front side.  The arms, the legs and the back, and nowhere else.
PERCHES = (
	Perch("your wrists", "a pair of bracelets"),
	Perch("your forearms", "wound bracers"),
	Perch("your shoulders", "a mantle clasp"),
	Perch("your shoulder blades", "the seams of a toga"),
	Perch("the small of your back", "a wide sash"),
	Perch("the base of your spine", "a belted overskirt"),
	Perch("your ankles", "anklets"),
	Perch("your heels", "the straps of your sandals"),
	)



@dataclass(
	frozen=True,
	)
class Celestial_Mark:
	"""
	One Aasimar's visible descent, drawn once and kept.

	Two axes, deliberately separate.  The talaria take their **metal** and the aureola takes its **gem**, so a silver-winged aasimar under a ruby halo is a different creature from a red-iron-winged one under diamond, and neither is a restatement of the other.  Nothing is *made* of either: the wings shine like a metal and the halo glows like a stone.  Comparison, not actual material.
	"""

	ideals: tuple[Ideal, ...]
	# "the Muse Talia": kind and name spoken together, article included.
	ancestor: str
	perch: Perch
	plumage: str
	# Which Ideal lends the aureola its form, and which the gem it glows like.
	shape_from: Ideal
	glow_from: Ideal
	# What the halo does, drawn from either Ideal, never naming it.
	tell: str
	# His, her, their, or its: how the ancestor's line is spoken of.
	ancestor_possessive: str
	# Which of the sentence patterns below this Aasimar was written with.  Drawn
	# with everything else, so the same Character reads the same way twice.
	voice: int = 0
	arrangement: int = 0

	@property
	def names(
			self,
			) -> tuple[str, ...]:
		return tuple(
			ideal.name
			for ideal in self.ideals
			)

	@property
	def metal(
			self,
			) -> str:
		"""What the talaria catch the light like."""
		return self.plumage.format(
			a=self.ideals[
				0
				].metal,
			b=self.ideals[
				-1
				].metal,
			)

	@property
	def gem(
			self,
			) -> str:
		"""What the aureola glows like."""
		if len(
			self.ideals
			) > 1:
			return (
				f"{self.ideals[0].gem} shading into "
				f"{self.ideals[1].gem}"
				)

		return self.ideals[
			0
			].gem

	def _pick(
			self,
			patterns: tuple[str, ...],
			) -> str:
		return patterns[
			self.voice % len(
				patterns
				)
			]

	def opening(
			self,
			) -> str:
		"""The line that names the ancestor, before the marks are described."""
		return self._pick(
			(
				f"The marks suggest a tie to {self.ancestor}; you may belong to "
				f"{self.ancestor_possessive} lineage.",
				f"Your talaria and aureola resemble the traits of "
				f"{self.ancestor}, so you may belong to "
				f"{self.ancestor_possessive} lineage.",
				f"Whatever is in you resembles {self.ancestor}; you may have a place in "
				f"{self.ancestor_possessive} lineage.",
				)
			)

	def closing(
			self,
			) -> str:
		"""The same line, said after the marks instead of before."""
		return self._pick(
			(
				f"These are the traits of {self.ancestor}, so you may belong to "
				f"{self.ancestor_possessive} lineage.",
				f"Together, these marks resemble {self.ancestor}; you may belong to "
				f"{self.ancestor_possessive} lineage.",
				f"They echo the signs of {self.ancestor}, so you may have a place in "
				f"{self.ancestor_possessive} lineage.",
				)
			)

	def talaria(
			self,
			) -> str:
		"""The wings."""
		place = self.perch.place
		disguise = self.perch.disguise
		metal = self.metal

		return self._pick(
			(
				f"Your talaria rest at {place} and fold away as {disguise}, shining like {metal}.",
				f"At {place} you carry talaria that catch the light like {metal}, and folded they pass for {disguise}.",
				f"Talaria sit at {place}, shining like {metal}, and whoever notices takes them for {disguise}.",
				f"Most people wouldn't suspect {disguise} could hide talarian wings, but yours rest at {place}, shining like {metal}.",
				)
			)

	def aureola(
			self,
			) -> str:
		"""The halo, and the one thing it does."""
		form = self.shape_from.form
		gem = self.gem

		return self._pick(
			(
				f"Above your head, {form}, glowing like {gem}. {self.tell}",
				f"Your aureola is {form}, and it glows like {gem}. {self.tell}",
				f"Floating behind your head, your aureola is {form}, lit like {gem}. {self.tell}",
				f"Suspended above your head like a dim reflection, your aureola is {form}, lit like {gem}. {self.tell}",
				)
			)

	def paragraph(
			self,
			) -> str:
		"""
		The three sentences, in the order this Aasimar was drawn with.

		Four arrangements, so two Aasimar at one table do not read as the
		same hand.
		"""

		arrangements = (
			(
				self.opening(),
				self.talaria(),
				self.aureola(),
				),
			(
				self.talaria(),
				self.aureola(),
				self.closing(),
				),
			(
				self.aureola(),
				self.talaria(),
				self.closing(),
				),
			(
				self.opening(),
				self.aureola(),
				self.talaria(),
				),
			)

		return " ".join(
			arrangements[
				self.arrangement % len(
					arrangements
					)
				]
			)


def celestial_marks(
		char,
		) -> Celestial_Mark:
	"""
	Draw this Aasimar's visible descent, once and for life.

	The bag is named and level-free, so the same Character is answered the same way whenever anybody asks, and a level-up never hands somebody a different face.
	"""
	standing = getattr(
		char,
		"celestial_mark",
		None,
		)

	if standing is not None:
		return standing

	dice = char.Dice_Bag( "Aasimar.descent" )
	pool = list(
		IDEALS
		)
	# A Spark comes from two Ideals, each drawn from the whole list at uniform
	# random.  The same Ideal may be drawn twice, and that is a single descent:
	# not a separate roll, and not weighted against a mixed one.  Nothing is
	# taken out of the pool between the two draws.
	first = IDEALS[
		char.Pick(
			pool,
			dice=dice,
			)
		]
	second = IDEALS[
		char.Pick(
			pool,
			dice=dice,
			)
		]
	mixed = second.name != first.name
	ideals = (
		(
			first,
			second,
			)
		if mixed
		else (
			first,
			)
		)

	# The form and the glow; with a single descent both are the same Ideal.
	shape_from = ideals[
		0
		]
	glow_from = ideals[
		-1
		]
	kind = char.Pick(
		list(
			DESCENTS
			),
		dice=dice,
		)
	pronoun_dice = char.Dice_Bag( "Aasimar.descent.pronoun" )
	mark = Celestial_Mark(
		ideals=ideals,
		# The kind and one of its names, told together the way anyone would.
		ancestor=f"the {kind.kind} "
		+ char.Pick(
			list(
				kind.names
				),
			dice=dice,
			),
		perch=char.Pick(
			list(
				PERCHES
				),
			dice=dice,
			),
		plumage=char.Pick(
			list(
				PLUMAGES
				if mixed
				else SINGLE_PLUMAGES
				),
			dice=dice,
			),
		shape_from=shape_from,
		glow_from=glow_from,
		# The tell is its own draw.  Either Ideal may lend it, so two Aasimar
		# sharing a pair can still read differently: same form, same glow,
		# different habit.
		tell=char.Pick(
			[
				ideal.tell
				for ideal in ideals
				],
			dice=dice,
			),
		ancestor_possessive=char.Pick(
			(
				"his",
				"her",
				"their",
				"its",
				),
			dice=pronoun_dice,
			),
		voice=char.Pick(
			(
				0,
				1,
				2,
				3,
				),
			dice=dice,
			),
		arrangement=char.Pick(
			(
				0,
				1,
				2,
				3,
				),
			dice=dice,
			),
		)
	char.celestial_mark = mark

	return mark


__all__ = (
	"Celestial_Mark",
	"DESCENTS",
	"IDEALS",
	"Ideal",
	"PERCHES",
	"Perch",
	"celestial_marks",
	)


def _test_dice_purposes() -> None:
	#-- Ruling 8 (QST-0144.6): the descent comes from one Dice Bag opened as
	#-- "Aasimar.descent" and the ancestor's pronoun from its own,
	#-- "Aasimar.descent.pronoun", both with the default key and from the
	#-- pools they always had; a second ask returns the standing mark.
	from AtlasActorLudi.CharactersKit import Character

	opened = []
	purpose_of_bag = {}
	drawn = []
	original_dice_bag = Character.Dice_Bag
	original_pick = Character.Pick

	def recording_dice_bag(
		char,
		purpose,
		**key,
		):
		bag = original_dice_bag(
			char,
			purpose,
			**key,
			)
		opened.append(
			(
				purpose,
				key,
				)
			)
		purpose_of_bag[
			id(
				bag
				)
			] = purpose
		return bag

	def recording_pick(
		char,
		ledger,
		weights=None,
		**options,
		):
		drawn.append(
			(
				purpose_of_bag.get(
					id(
						options.get(
							"dice"
							)
						)
					),
				tuple(
					ledger
					),
				)
			)
		return original_pick(
			char,
			ledger,
			weights,
			**options,
			)

	Character.Dice_Bag = recording_dice_bag
	Character.Pick = recording_pick
	try:
		character = Character(
			seed=7,
			)
		mark = celestial_marks( character )
		again = celestial_marks( character )
	finally:
		Character.Dice_Bag = original_dice_bag
		Character.Pick = original_pick

	assert again is mark
	assert opened == [
		(
			"Aasimar.descent",
			{},
			),
		(
			"Aasimar.descent.pronoun",
			{},
			),
		], opened
	kind = next(
		descent
		for descent in DESCENTS
		if mark.ancestor.startswith(
			f"the {descent.kind} "
			)
		)
	plumages = (
		PLUMAGES
		if len(
			mark.ideals
			) == 2
		else SINGLE_PLUMAGES
		)
	assert drawn == [
		( "Aasimar.descent", tuple( IDEALS ) ),
		( "Aasimar.descent", tuple( IDEALS ) ),
		( "Aasimar.descent", tuple( DESCENTS ) ),
		( "Aasimar.descent", tuple( kind.names ) ),
		( "Aasimar.descent", tuple( PERCHES ) ),
		( "Aasimar.descent", tuple( plumages ) ),
		( "Aasimar.descent", tuple( ideal.tell for ideal in mark.ideals ) ),
		( "Aasimar.descent.pronoun", ( "his", "her", "their", "its" ) ),
		( "Aasimar.descent", ( 0, 1, 2, 3 ) ),
		( "Aasimar.descent", ( 0, 1, 2, 3 ) ),
		], drawn


if __name__ == "__main__":
	_test_dice_purposes()
	print( "OK: SpeciesKit.Aasimar.Map_of_Ideals self-test" )
