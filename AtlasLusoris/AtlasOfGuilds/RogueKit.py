"""Rogue Specializations."""

from AtlasLusoris.GuildKit import Build_Specialization
from AtlasLusoris.GuildKit import Describe_Layer
from AtlasLusoris.GuildKit import Rogue


ROGUE_DESCRIPTION = (
	"Luck may offer an opening. Opportunity is what you do with it. The "
	"moment demands an answer. You know the answer. You do not let it "
	"close. You do not waste your shot.\n\n"
	"You know the game. You know the board. You move first. Sometimes you "
	"wait. Sometimes you taunt. Sometimes you win before the room knows. "
	"Sometimes you are gone before you lose. And when no opening comes, "
	"you make one: a word, a flourish, a risk taken so confidently that "
	"everyone mistakes it for a plan. Call it half skill, half luck. All "
	"of it is why you play."
	)

Rogue.DESCRIPTION = ROGUE_DESCRIPTION
Rogue.Describe = Describe_Layer(
	ROGUE_DESCRIPTION,
	extend=True,
	heading=None,
	)


ARCANE_TRICKSTER_DESCRIPTION = (
	"You stage the opportunity. Every eye is part of the trick. First, the "
	"setup: an empty hand, an easy smile, nothing to hide. Then, the "
	"distraction: a flash, a flourish, the one hand everyone watches. "
	"Then, the turn: a coin changes hands, a card switches places, or a "
	"rose appears. But the trick is somewhere nobody is looking. The purse "
	"changes pockets, a key slips away, or the wrong envelope is given. "
	"Half sleight of hand. Half spell. Which half was which? They never "
	"know.\n\n"
	"The room watches the show. Your crew watches the opening. The "
	"lookout, the muscle, and the distraction. They all know their signs. "
	"One nod. One step. By the time anyone looks where they should, the "
	"lock is open, the prize is gone, and the crew is through. You show "
	"the empty hand. You take the bow. That is the prestige."
	)
ArcaneTrickster = Build_Specialization(
	guild=Rogue,
	name="Arcane Trickster",
	module=__name__,
	extends=ARCANE_TRICKSTER_DESCRIPTION,
	heading="Arcane Trickster",
	)

ASSASSIN_DESCRIPTION = (
	"You understand the courage of waiting. Patience is not inaction. It is "
	"the waiting game: attention held steady while false openings come and "
	"go. You learn the room, the route, the hand, the voice. You keep your "
	"head in the game. You ready the crew. You let the target breathe. "
	"Everyone is in position.\n\n"
	"Stay still. Stay ready. You move first. Game over."
	)
Assassin = Build_Specialization(
	guild=Rogue,
	name="Assassin",
	module=__name__,
	extends=ASSASSIN_DESCRIPTION,
	heading="Assassin",
	)

SOULKNIFE_DESCRIPTION = (
	"You read the opportunity. Three ways in. Two ways out. One chance. "
	"One look, next move. One change, new game. Your plan travels at the "
	"speed of thought. No words. No pause. Your crew moves as quickly as "
	"you think.\n\n"
	"They search for steel. Let them. Your mind is the instrument. Empty "
	"hands tell a lovely lie. A thought takes an edge. The room changes; "
	"you change faster. What looks like the mistake is the gambit. What "
	"looks like the retreat puts your crew behind them. By the time they "
	"understand, they are standing in the trap and falling."
	)
Soulknife = Build_Specialization(
	guild=Rogue,
	name="Soulknife",
	module=__name__,
	extends=SOULKNIFE_DESCRIPTION,
	heading="Soulknife",
	)

THIEF_DESCRIPTION = (
	"You take the opportunity. A lock leaves a question in the door. Your "
	"hands answer. By the time the guards come, you are already on the roof. "
	"While everyone else decides whether the thing can be done, you jump "
	"in.\n\n"
	"Guarded things, strange things, magical things: you take them. You do "
	"not need a proper entrance. You need a loose hinge, a turned head, one "
	"locked door. Crew's ready. Lock's open. Prize's moving. You are already "
	"gone."
	)
Thief = Build_Specialization(
	guild=Rogue,
	name="Thief",
	module=__name__,
	extends=THIEF_DESCRIPTION,
	heading="Thief",
	)

SPECIALIZATIONS = (
	ArcaneTrickster,
	Assassin,
	Soulknife,
	Thief,
	)
