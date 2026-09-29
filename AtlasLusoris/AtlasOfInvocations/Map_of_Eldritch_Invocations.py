"""
Eldritch Invocations — 2024 PHB catalogue.

Registered via InvocationKit.Make_Invocation.
"""

from __future__ import annotations

from AtlasLusoris.InvocationKit import Make_Invocation


ArmorOfShadows = Make_Invocation(
	name='Armor of Shadows',
	min_level=1,
	description='You can cast Mage Armor on yourself at will, without expending a spell slot.',
	)

EldritchMind = Make_Invocation(
	name='Eldritch Mind',
	min_level=1,
	description='You have Advantage on Constitution saving throws that you make to maintain Concentration.',
	)

PactOfTheBlade = Make_Invocation(
	name='Pact of the Blade',
	min_level=1,
	description='As a Bonus Action, you can conjure a pact weapon or bond with a magic weapon. You can use Charisma for its attack and damage rolls, use it as a spellcasting focus, and when you hit you can deal Necrotic, Psychic, or Radiant damage instead of its normal type.',
	)

PactOfTheChain = Make_Invocation(
	name='Pact of the Chain',
	min_level=1,
	description='You learn Find Familiar and can cast it as a Magic action without a spell slot. You can choose special familiar forms (such as Imp, Quasit, Sprite, or Sphinx of Wonder). When you take the Attack action, you can forgo one attack to let your familiar attack with its Reaction.',
	)

PactOfTheTome = Make_Invocation(
	name='Pact of the Tome',
	min_level=1,
	description='Your Book of Shadows grants three cantrips and two level-1 Ritual spells from any class lists. They count as Warlock spells for you and are always prepared. The book is a spellcasting focus.',
	)

AgonizingBlast = Make_Invocation(
	name='Agonizing Blast',
	min_level=2,
	description="Choose one of your known Warlock cantrips that deals damage. You can add your Charisma modifier to that spell's damage rolls.",
	)

DevilsSight = Make_Invocation(
	name="Devil's Sight",
	min_level=2,
	description='You can see normally in Dim Light and Darkness — both magical and nonmagical — to a range of 120 feet.',
	)

EldritchSpear = Make_Invocation(
	name='Eldritch Spear',
	min_level=2,
	description="Choose one of your known Warlock cantrips that deals damage and has a range of at least 10 feet. That cantrip's range increases by a number of feet equal to 30 times your Warlock level.",
	)

FiendishVigor = Make_Invocation(
	name='Fiendish Vigor',
	min_level=2,
	description="You can cast False Life on yourself at will as a Magic action, without a spell slot. When you cast it with this Invocation, you don't roll the die; you gain the maximum Temporary Hit Points.",
	)

LessonsOfTheFirstOnes = Make_Invocation(
	name='Lessons of the First Ones',
	min_level=2,
	description='You have manifested your life experiences into an Origin feat of your choice (see Origin Feats in FeaturesKit).',
	)

MaskOfManyFaces = Make_Invocation(
	name='Mask of Many Faces',
	min_level=2,
	description='You can cast Disguise Self at will, without expending a spell slot.',
	)

MistyVisions = Make_Invocation(
	name='Misty Visions',
	min_level=2,
	description='You can cast Silent Image at will, without expending a spell slot.',
	)

OtherworldlyLeap = Make_Invocation(
	name='Otherworldly Leap',
	min_level=2,
	description='You can cast Jump on yourself at will, without expending a spell slot.',
	)

RepellingBlast = Make_Invocation(
	name='Repelling Blast',
	min_level=2,
	description='Choose one of your known Warlock cantrips that requires an attack roll. When you hit a Large or smaller creature with that cantrip, you can push the creature up to 10 feet straight away from you.',
	)

AscendantStep = Make_Invocation(
	name='Ascendant Step',
	min_level=5,
	description='You can cast Levitate on yourself at will, without expending a spell slot.',
	)

EldritchSmite = Make_Invocation(
	name='Eldritch Smite',
	min_level=5,
	description='Once per turn when you hit a creature with your pact weapon, you can expend a Pact Magic slot to deal an extra 1d8 Force damage, plus 1d8 per spell slot level, and you can knock the target Prone if it is Huge or smaller.',
	requires='Pact of the Blade',
	)

GazeOfTwoMinds = Make_Invocation(
	name='Gaze of Two Minds',
	min_level=5,
	description='As a Bonus Action, choose a willing creature you can see within 60 feet. Until the end of your next turn, you can perceive through its senses. You can maintain the link by using a Bonus Action each turn, and while within 60 feet you can cast spells as if you were in either space.',
	)

GiftOfTheDepths = Make_Invocation(
	name='Gift of the Depths',
	min_level=5,
	description='You can breathe underwater, and you gain a Swim Speed equal to your Speed. You can also cast Water Breathing once per Long Rest without a spell slot.',
	)

InvestmentOfTheChainMaster = Make_Invocation(
	name='Investment of the Chain Master',
	min_level=5,
	description='When you cast Find Familiar, you infuse the familiar with additional vigor: it gains a Fly or Swim Speed of 40 feet (your choice when you cast), you can command it to Attack as a Bonus Action, its weapon attacks can deal Necrotic or Radiant damage, it uses your spell save DC, and you can take a Reaction to grant it Resistance to damage from one attack.',
	requires='Pact of the Chain',
	)

MasterOfMyriadForms = Make_Invocation(
	name='Master of Myriad Forms',
	min_level=5,
	description='You can cast Alter Self at will, without expending a spell slot.',
	)

OneWithShadows = Make_Invocation(
	name='One with Shadows',
	min_level=5,
	description='While entirely within Dim Light or Darkness, you can cast Invisibility on yourself at will, without a spell slot.',
	)

ThirstingBlade = Make_Invocation(
	name='Thirsting Blade',
	min_level=5,
	description='You can attack with your pact weapon twice, instead of once, whenever you take the Attack action on your turn.',
	requires='Pact of the Blade',
	)

WhispersOfTheGrave = Make_Invocation(
	name='Whispers of the Grave',
	min_level=7,
	description='You can cast Speak with Dead at will, without expending a spell slot.',
	)

GiftOfTheProtectors = Make_Invocation(
	name='Gift of the Protectors',
	min_level=9,
	description="Your Book of Shadows gains names (a number equal to your Charisma modifier, minimum of one). When a named creature drops to 0 Hit Points but isn't killed outright, that creature's Hit Points instead change to 1. Once this Invocation saves a creature, it can't do so again until you finish a Long Rest.",
	requires='Pact of the Tome',
	)

Lifedrinker = Make_Invocation(
	name='Lifedrinker',
	min_level=9,
	description='Once per turn when you hit a creature with your pact weapon, you can deal an extra 1d6 Necrotic, Psychic, or Radiant damage (your choice). You can also expend one of your Hit Point Dice to regain Hit Points equal to the roll plus your Constitution modifier (minimum of 1).',
	requires='Pact of the Blade',
	)

VisionsOfDistantRealms = Make_Invocation(
	name='Visions of Distant Realms',
	min_level=9,
	description='You can cast Arcane Eye at will, without expending a spell slot.',
	)

DevouringBlade = Make_Invocation(
	name='Devouring Blade',
	min_level=12,
	description='The extra attack from Thirsting Blade becomes two extra attacks instead of one (three attacks total with your pact weapon when you take the Attack action).',
	requires='Thirsting Blade',
	)

WitchSight = Make_Invocation(
	name='Witch Sight',
	min_level=15,
	description='You have Truesight with a range of 30 feet.',
	)
