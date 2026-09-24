"""
Warlock Specializations, and the kinds of Warlock.

Two axes, and a Character carries one of each.  The Specialization is who the
pact is *with*.  The Casting Variant is what the pact answers *to*, and it is
deliberately rare: a table that has never met one can play the published
Warlock forever and never notice it exists.
"""

from AtlasLusoris.GuildKit import Make_Casting_Variant
from AtlasLusoris.GuildKit import Make_Specialization
from AtlasLusoris.GuildKit import Warlock


# Julio's, 2026-08-21.  The organising idea is **spectacle rather than
# cruelty**, which is how this one buys the alignment-independence the Fiend
# buys with toxicity and the Celestial with instrumentality.  Nobody here is
# wicked.  You are being watched, and kept alive for the third act.
#
# They are made of dream and they are bored of it, because nothing in a dream
# was ever actually at risk.  You can lose.  That is the whole attraction, and
# it is the one thing they cannot supply themselves.  So the power is not a
# reward, it is apparatus: they handed over what they had in order to see what
# you would do while holding it.  The test that follows is aesthetic and not
# moral, which is the cruelty of it.  Do the task and you may still fail.  Fail
# and you may still pass, if it was worth watching.
#
# **Why this one is in verse.**  Shakespeare's fairies have their own meter:
# the mortals in A Midsummer Night's Dream speak blank verse, and the moment
# you cross into the wood the fairies drop into short rhymed lines.  The change
# of form *is* the crossing, so the Archfey being the only patron written as a
# poem is the device rather than an inconsistency.  The meter is trochaic
# tetrameter, which is Puck's epilogue and also the witches in Macbeth, so the
# form itself carries the Fae/Fata point: Titania and Baba Yaga speak in one
# rhythm.  See Documenta/Canon/Elves-and-the-Dreaming.md.
#
# Every line is end-stopped on purpose.  A charm does not enjamb.
#
# The closing couplet answers Puck, who says "Think but this, and all is
# mended" at the *end* of the play, which is why it sits at the end here.  This
# one refuses the apology.  And "we shadows" is not modesty: Fae, Fata and
# Shadow are three mortal names for one substance, so the patron is being
# literal and the mortal will hear poetry.  Used once, and never explained.
#
# Four things worth not "fixing":
#   "Power was the dream you had"   doubled, because they *are* dream
#   "a witch would hold"            Yubaba, so Fae and Fata share one quatrain
#   "We shall never see quite where"  they lose sight of you: the only privacy
#                                     in the poem, and the only thing not given
#   "make an end"                   an ending, and your ending, at once
#
# The four wishes are Arthur, Ofelia, Chihiro and Peter, none of them named.
#
# Breaks are explicit per Documenta/Canon/Feature-Text.md.  Nothing may reflow
# this, and a renderer that inserts its own breaks would destroy the couplets.
ARCHFEY_DESCRIPTION = (
	"Fae of dream. We do not die.<br>"
	"We have never wondered why.<br>"
	"You can lose. That is the art.<br>"
	"We have cast you. Play your part.<br>"
	"Power was the dream you had.<br>"
	"Take it. We are only glad.<br>"
	"Show us swords drawn out of stone,<br>"
	"crowns in kingdoms overgrown,<br>"
	"give the name a witch would hold,<br>"
	"take the wind and not grow old.<br>"
	"You were here. You then were there.<br>"
	"We shall never see quite where.<br>"
	"Arrows sent to find your head<br>"
	"find a friend of yours instead.<br>"
	"Do the task, still fail the test.<br>"
	"Fail it well. We like that best.<br>"
	"Only never bore us, friend.<br>"
	"We know how to make an end.<br>"
	"If we shadows have offended,<br>"
	"nothing played shall be mended."
	)
Archfey = Make_Specialization(
	guild=Warlock,
	name="Archfey",
	module=__name__,
	extends=ARCHFEY_DESCRIPTION,
	heading="Archfey Patron",
	)
# Julio's, 2026-08-21.  The organising idea is **instrumentality rather than
# evil**, and it buys the same alignment-independence the Fiend buys with
# toxicity rather than malice.  The patron here is genuinely good and the
# arrangement is still uncomfortable, because the discomfort lives in the
# terms rather than in anyone's intent.
#
# A Celestial is an Ideal with a shape (AtlasActorLudi/SpeciesKit/Aasimar/
# Map_of_Ideals.py), so it is not a god, has no cult, and cannot want a
# worshipper.  What it *can* want is somebody permitted to be inconsistent:
# Justice itself cannot lie to a guard or take the shortcut, and you can.
# Three things are being bought, and none of them is virtue: expendability,
# deniability, and access to ground where it has no invitation.
#
# The voice is deliberately not the Fiend's.  That one is interior and
# solitary, one person alone with a crack nobody else can see.  This one is a
# briefing, given by a superior in the Men In White who is containing his
# tongue, which is why "pusillanimous" stands where a swear would.  The first
# person plural is the device the Species descriptions already use (Dragonborn,
# Tiefling, Goliath): the community talking to the character.  Here the
# community is the other operatives, and that crew is what keeps this register
# adventure rather than nightmare.
#
# Two jokes that are not errors.  "High cloud" is "high horse", and it lands
# because they are stars and planets rather than cloud-dwellers, so it calls
# them the postcard version of themselves.  "The one you crossed" is doubled:
# to cross somebody, and the cross you would talk to them with.
#
# The two ellipses are the same man twice.  The first trails off a list he
# cannot be bothered to finish, the second trails off the one thing he cannot
# actually promise, and "At least try" is him settling for less out loud.
#
# The rules were read for this, and every signature feature is a fund you
# administer on somebody else's behalf:
#   Healing Light         a metered pool, spent as a Bonus Action on others
#   Celestial Resilience  temporary Hit Points handed to five other creatures
#   Searing Vengeance     saves someone else, blinds whoever is standing near
#   Radiant Soul          the Fiend's own fire, differently branded
# The Fiend consumes what is nearest and rises.  The Celestial is a conduit,
# and a conduit keeps nothing.
#
# The opening list is four long to match the Aasimar's own, which reads
# "Angels, Muses, Constellations, Celestials..." (AtlasActorLudi/SpeciesKit/
# Aasimar/__init__.py).  Sphinxes are deliberately *not* in it even though a
# patron can be drawn as one: the ellipsis says there are more nobody bothers
# to name, and it is better if the sheet then names one of them.
CELESTIAL_DESCRIPTION_TEMPLATE = (
	"Planetars, Muses, Constellations, Celestials... a pusillanimous "
	"bunch, all of them, but especially that patron of yours, {patron}. "
	"Up there on their high cloud, judging us. And yet they need people "
	"like you: expendable and able to walk into a cursed shrine, or the "
	"Courts of the Fae, where they have no invitation. You wanted "
	"redemption? You got a job offer in hell. All that light and healing "
	"is not a blessing, it is the standard kit they issue. You do what "
	"they say, but they never tell you how. The right thing, done the "
	"wrong way. You know why. They will tell the one you crossed that it "
	"was your own free will. Damned we are. But somehow still on our way "
	"to redemption. Somewhere there is a balance with your heart on one "
	"side and a celestial feather on the other. If you die in the work, "
	"you will not go to hell. That is a good perk. Just... try to get to "
	"Elysium. At least try."
	)


def CELESTIAL_DESCRIPTION(
		character,
		) -> str:
	"""
	The Celestial patron paragraph, naming the one who hired you.

	Drawn from the Aasimar's own pool of Celestials, so the two Atlases agree
	about who is up there.  The kind and the Ideal come out of one named Dice
	Bag, which is seeded from the Character rather than from call order, so
	the paragraph names the same patron every time it renders.

	The Ideal is deliberately not printed as a doctrine, the same way the
	Aasimar's mark never prints it: you know who hired you, you do not know
	what they are for.  Which is also the joke the ending turns on, since
	nobody ever sends you a statement.
	"""
	from AtlasActorLudi.SpeciesKit.Aasimar.Map_of_Ideals import (
			DESCENTS,
			IDEALS,
			)

	dice = character.Dice_Bag(
		"warlock.patron.celestial",
		version="1",
		namespace="GenLegendClass",
		)
	descent = character.Pick(
		list(
			DESCENTS
			),
		dice=dice,
		)
	ideal = character.Pick(
		list(
			IDEALS.values()
			),
		dice=dice,
		)
	return CELESTIAL_DESCRIPTION_TEMPLATE.format(
		patron=f"the {descent.kind} of {ideal.name}",
		)


Celestial = Make_Specialization(
	guild=Warlock,
	name="Celestial",
	module=__name__,
	extends=CELESTIAL_DESCRIPTION,
	heading="Celestial Patron",
	)
# Julio's, 2026-08-19.  The organising idea is a **symmetry**: the crack in
# yourself you refuse to look at is the same crack that opens onto hell.  One
# flaw, two sides.
#
# What that buys is **toxicity rather than malice**, which is why this sits on
# any alignment without contradiction.  A Lawful Good Fiend warlock is still
# extracting: they take risks, other people absorb them, and the two "Maybe"
# lines are the character arguing his own case, because nobody carrying an
# unmanaged flaw believes they are the villain.  They believe they are owed.
#
# The rules were read for this, and they say the same thing:
#   Dark One's Blessing   things die near you and you are topped up
#   Dark One's Own Luck   a d10 out of nowhere, and luck is zero-sum
#   the fire spell list   flames and brimstone, and fire burns what is nearest
#   Hurl Through Hell     a door in you, and someone else always goes through
#
# One deliberate tense clash, which is not an error: "Not what you **need**,
# but what you truly **wanted**."  The wanting was settled in the past by the
# pact.  The need is present because the wound is still open and looking at it
# is the thing that would heal it.  That is the seed of an arc through play,
# not backstory.
FIEND_DESCRIPTION = (
	"Everyone has a place in themselves they have decided not to look "
	"at. Yours goes all the way down to hell. Something on the other "
	"side of it noticed, and it did not have to break anything to get "
	"in. It came up like flame and sulfur. It saw you, broken, and "
	"promised. Not what you need, but what you truly wanted. It gave you "
	"flames and brimstone, ember and shadows. Since then you understand "
	"it better: your needs are yours to fulfill. You take risks and "
	"others pay for them. You feed on their misfortune. You consume and "
	"rise, like hellfire. Maybe you aim it at the ones who truly deserve "
	"it. Maybe you finally deserve a long shot. But your crack is a "
	"two-way street, slowly opening. And you still do not look."
	)
Fiend = Make_Specialization(
	guild=Warlock,
	name="Fiend",
	module=__name__,
	extends=FIEND_DESCRIPTION,
	heading="Fiend Patron",
	)
# Julio's, 2026-08-21.  Two words, and the shortest description in the project
# by an order of magnitude.  That is the argument: across the four patrons the
# form itself contracts toward silence.  The Fiend gets a paragraph, the
# Celestial a longer one, the Archfey twenty lines of verse, and this one says
# everything it has to say and stops.
#
# **The description is not the text, it is what the text does.**  The letters
# are periodically replaced, one at a time, by alchemical, planetary and
# mathematical glyphs, and then they come back.  Nothing is ever permanently
# wrong, so the reader cannot check, which is the whole effect: the horror is
# that you are not certain you saw it.  The rules underwrite this exactly.
# Thought Shield does not arrive until level 10, so from 3 to 9 the character's
# thoughts *can* be read and the sheet never says by whom, and Modify Memory
# sits on the level 9 list, which means "it changed and you did not notice" is
# the subclass's own spell rather than a trick we invented.
#
# Alignment-independence, completing the set: the Fiend buys it with toxicity
# rather than malice, the Celestial with instrumentality rather than evil, the
# Archfey with spectacle rather than cruelty, and this one with **indifference
# rather than hostility**.  Nothing here wants to hurt you.  It has simply
# already finished deciding.
#
# "You, mine." has no verb, and the missing verb is the point.  It is not a
# threat and not an offer, it is a label, stated as something already true.
# And it addresses the *player*, not the character: this is the only patron
# that can, because Awakened Mind is telepathy and Detect Thoughts is on the
# list, and it is the only one that ever will.
#
# The glyph pools are plain Unicode rather than a webfont, which was deliberate:
# a general standard is a better dependency than a CDN, and on machines that
# cannot render a glyph the failure is the effect rather than a defect.
# Alchemical lives in Plane 1 and its coverage genuinely varies, so the same
# sheet resolves differently for different players and nobody can compare
# notes.  Rate and hold are slow on purpose (one per second, held 280ms): this
# patron is asleep, and it is not in a hurry about you.
#
# The span is what makes this explicit rather than inferred, per
# Documenta/Canon/Feature-Text.md.  The source declares which text is affected;
# app/static/js/eldritch.js decides what affected means.  The original letters
# are never removed from the document, only painted over, so copy-paste,
# find-in-page and screen readers all still see "You, mine."
GREAT_OLD_ONE_DESCRIPTION = (
	'<span class="eldritch" data-eldritch-rate="10" '
	'data-eldritch-hold="280">You, mine.</span>'
	)
GreatOldOne = Make_Specialization(
	guild=Warlock,
	name="Great Old One",
	module=__name__,
	extends=GREAT_OLD_ONE_DESCRIPTION,
	heading="Great Old One Patron",
	)


# The pact answering to something other than Charisma: five in a hundred each,
# leaving the plain Warlock the remaining ninety.  An easter egg, not a rules
# change, so a rules lawyer meets one Occultist in twenty rather than a new
# subsystem.  Charisma needs no Variant of its own: the Guild already answers
# it, and a Warlock of Charisma is simply a Warlock.
Occultist = Make_Casting_Variant(
	guild=Warlock,
	name="Occultist",
	ability="INT",
	module=__name__,
	weight=5,
	)
Covenantor = Make_Casting_Variant(
	guild=Warlock,
	name="Covenantor",
	ability="WIS",
	module=__name__,
	weight=5,
	)

SPECIALIZATIONS = Warlock.SPECIALIZATIONS
CASTING_VARIANTS = (
	Covenantor,
	Occultist,
	)
