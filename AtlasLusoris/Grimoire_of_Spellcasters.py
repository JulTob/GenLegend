# AtlasLusoris/Grimoire_of_Spellcasters.py

from AtlasMagia.Lodge_of_Spells import *


def _pick_distinct(
		character,
		ledger,
		count,
		):
	"""Pick distinct entries through the owning Character."""
	available = list(
		ledger
		)
	selected = []

	while available and len(
			selected
			) < count:
		entry = character.Pick(
			available
			)
		available.remove(
			entry
			)
		selected.append(
			entry
			)

	return selected


def _shuffled_by_character(
		character,
		ledger,
		):
	return _pick_distinct(
		character,
		ledger,
		len(
			ledger
			),
		)


def title_font(class_name: str) -> str:
	"""Legacy HTML bridge until spellcaster rendering fully leaves this Grimoire."""
	if class_name == "Warlock":
		return "'UnifrakturMaguntia', var(--font-header)"
	return "'Manufacturing Consent', var(--font-header)"


SPELL_LISTS = {
	"test":  {
			0: [ ],
			1: [ ],
			2: [ ],
			3: [ ],
			4: [ ],
			5: [ ],
			6: [ ],
			7: [ ],
			8: [ ],
			9: [ ],
			},
	"Monk":  {
			0: [ ],
			1: [ ],
			2: [ ],
			3: [ ],
			4: [ ],
			5: [ ],
			6: [ ],
			7: [ ],
			8: [ ],
			9: [ ],
			},
	"Warlock":  {
			0: [
				BladeWard,    
				BoomingBlade, 
				ChillTouch, 
				CreateBonfire,
				EldritchBlast,    
				Friends, 
				Frostbite,    
				GreenFlameBlade,
				Infestation,    
				LightningLure,    
				MageHand,    
				MagicStone,
				MindSliver,    
				MinorIllusion,    
				PoisonSpray,    
				Prestidigitation,
				SwordBurst, 
				Thunderclap,    
				TolltheDead,    
				TrueStrike,
				],
			1: [
				ArmorofAgathys,    
				ArmsOfHadar,    
				Bane,    
				CauseFear, 
				CharmPerson,
				ComprehendLanguages,    
				DetectMagic,    
				DistortValue,
				ExpeditiousRetreat,    
				HellishRebuke,    
				Hex,    
				IllusoryScript,
				ProtectionfromEvilandGood,    
				SpeakwithAnimals,    
				HideousLaughter,
				UnseenServant,    
				WitchBolt,
				],
			2: [
				BorrowedKnowledge,    CloudofDaggers,    CrownofMadness, Darkness,
				Earthbind,    Enthrall, HoldPerson,    Invisibility,    MindSpike,
				MirrorImage,    RayofEnfeeblement,    ShadowBlade,    SpiderClimb,
				SprayOfCards,    Suggestion,    WarpSense, MistyStep,
				],
			3: [
				Antagonize,    Counterspell,    DispelMagic,    EnemiesAbound,
				Fear,    Fly,    GaseousForm,    HungerHadar,    HypnoticPattern,
				InciteGreed,    IntellectFortress,    MagicCircle,    MajorImage,
				RemoveCurse,    SpiritShroud,    SummonFey,    SummonLesserDemons,
				SummonShadowspawn,    SummonUndead,    ThunderStep,    Tongues,
				VampiricTouch,
				],
			4: [
				Banishment,    Blight,    CharmMonster,    DimensionDoor,
				ElementalBane,    GateSeal,    HallucinatoryTerrain,
				RaulothimPsychicLance,    ShadowofMoil,    SickeningRadiance,
				SpiritOfDeath,    SummonAberration,    SummonGreaterDemon,
				],
			5: [
				ContactOtherPlane,    DanseMacabre,    Dream,    Enervation,    FarStep,
				HoldMonster,    InfernalCalling,    JallarziStormofRadiance,
				Mislead,    NegativeEnergyFlood,    PlanarBinding,    Scrying,
				SynapticStatic,    TeleportationCircle,    WallLight,
				],
			6: [
				ArcaneGate,    CircleofDeath,    CreateUndead,    Eyebite,
				InvestitureFlame,    InvestitureIce,    InvestitureStone,
				InvestitureWind,    MentalPrison,    Scatter,    SoulCage,
				SummonFiend,    TashasBubblingCauldron,    TashaOtherworldlyGuise,
				TrueSeeing,
				],
			7: [
				CrownofStars,    DreamOfTheBlueVeil,    Etherealness,
				FingerofDeath,    Forcecage,    PlaneShift,    PowerWordPain
				],
			8: [
				Befuddlement,    Demiplane,    DominateMonster,    Glibness,
				MaddeningDarkness,    PowerWordStun,
				],
			9: [
				AstralProjection,    BladeofDisaster,    Foresight, Gate,
				Imprisonment,    PowerWordKill,    PsychicScream,    TruePolymorph,
				Weird
				],
			},
	"Wizard": {
			0: [
				AcidSplash,       BladeWard,
				ChillTouch,       DancingLights,
				Elementalism,     FireBolt,
				Friends,          Light,
				MageHand,         Mending,
				Message,          MindSliver,
				MinorIllusion,    PoisonSpray,
				Prestidigitation, RayofFrost,
				ShockingGrasp,    Thunderclap,
				TolltheDead,      TrueStrike,
				BoomingBlade,        ControlFlames,
				],
			1: [Thunderwave,    BurningHands,     IllusoryScript,
				MagicMissile, Alarm, CharmPerson, ChromaticOrb,
				ColorSpray,    ComprehendLanguages,    DetectMagic,
				DisguiseSelf,    ExpeditiousRetreat,    FalseLife,
				FeatherFall,    FindFamiliar,    FogCloud,    Grease,    IceKnife,
				Identify,    Jump,    Longstrider,    MageArmor,
				ProtectionfromEvilandGood,    RayofSickness,    Shield,
				SilentImage,    Sleep,    HideousLaughter, FloatingDisk,
				UnseenServant,    WitchBolt,
				],
			2: [Blur, MistyStep, AlterSelf,    ArcaneLock,    Augury,
				BlindnessDeafness,    Blur,    CloudofDaggers,    ContinualFlame,
				CrownofMadness,    Darkness,    Darkvision,    DetectThoughts,
				DragonsBreath,    EnhanceAbility,    EnlargeReduce,    FlamingSphere,
				GentleRepose,    GustOfWind,    HoldPerson,    Invisibility,    Knock,
				Levitate,    LocateObject,    MagicMouth,    MagicWeapon,
				AcidArrow,    MindSpike,    MirrorImage,    MistyStep,    MagicAura,
				PhantasmalForce,    RayOfEnfeeblement,    RopeTrick,
				ScorchingRay,    SeeInvisibility,    Shatter,    SpiderClimb,
				Suggestion,    Web,
				AlterSelf, ArcaneLock, ArcaneVigor, Augury, BlindnessDeafness, Blur,
				CloudofDaggers, ContinualFlame, CrownofMadness, Darkness, Darkvision,
				DetectThoughts, DragonsBreath, EnhanceAbility, EnlargeReduce,
				FlamingSphere, GentleRepose, GustOfWind, HoldPerson, Invisibility,
				Knock, Levitate, LocateObject, MagicMouth, MagicWeapon, AcidArrow,
				MindSpike, MirrorImage, MistyStep, MagicAura, PhantasmalForce,
				RayOfEnfeeblement, RopeTrick, ScorchingRay, SeeInvisibility, Shatter,
				SpiderClimb, Suggestion, Web,

				],
			3: [AnimateDead,    BestowCurse,
				Blink,            Clairvoyance,
				Counterspell,    DispelMagic,    Fear,
				FeignDeath,        Fireball,
				Fly,            GaseousForm,    GlyphWarding,
				Haste,            HypnoticPattern,
				TinyHut,        LightningBolt,
				MagicCircle,    MajorImage,
				Nondetection,    PhantomSteed,    ProtectionfromEnergy,
				RemoveCurse,    Sending,        SleetStorm,
				Slow,            SpeakwithDead,
				StinkingCloud,    SummonFey,
				SummonUndead,    Tongues,
				VampiricTouch,    WaterBreathing,
				],
			4: [ArcaneEye,    Banishment,    Blight,    CharmMonster,    Confusion,
				ConjureMinorElementals,    ControlWater,    DimensionDoor,
				Divination,    EvardsBlackTentacles,
				ArcaneEye, Banishment, Blight, CharmMonster, Confusion,
				ConjureMinorElementals, ControlWater, DimensionDoor, Divination,
				EvardsBlackTentacles, Fabricate, FireShield, GreaterInvisibility,
				HallucinatoryTerrain, IceStorm, SecretChest, LocateCreature,
				PrivateSanctum, OtilukeResilientSphere, PhantasmalKiller, Polymorph,
				StoneShape, Stoneskin, SummonAberration, SummonConstruct,
				SummonElemental, VitriolicSphere, WallofFire,
				],
			5: [
				AnimateObjects, BigbysHand, CircleofPower, Cloudkill, ConeCold,
				ConjureElemental, ContactOtherPlane, Creation, DominatePerson, Dream,
				Geas, HoldMonster, JallarziStormofRadiance, LegendLore, Mislead,
				ModifyMemory, Passwall, PlanarBinding, RarysTelepathicBond, Scrying,
				Seeming, SteelWindStrike, SummonDraconicSpirit, SynapticStatic,
				Telekinesis, TeleportationCircle, WallForce, WallStone,
				YolandeRegalPresence,
				],
			6: [
				ArcaneGate, ChainLightning, CircleofDeath, Contingency, CreateUndead,
				Disintegrate, DrawmijInstantSummons, Eyebite, FleshtoStone,
				GlobeInvulnerability, GuardsandWards, MagicJar, MassSuggestion,
				MoveEarth, OtilukeFreezingSphere, IrresistibleDance, ProgrammedIllusion,
				SummonFiend, Sunbeam, TashasBubblingCauldron, TrueSeeing, WallIce,
				],
			7: [
				DelayedBlastFireball, 
				Etherealness, FingerDeath, Forcecage,
				MirageArcane, 
				MagnificentMansion, MordenkainenSword, PlaneShift,
				PrismaticSpray, 
				ProjectImage, ReverseGravity, Sequester, Simulacrum,
				Symbol, 
				Teleport,
				],
			8: [
				AntimagicField, AntipathySympathy, 
				Befuddlement, Clone, ControlWeather,
				Demiplane, DominateMonster, 
				IncendiaryCloud, Maze, MindBlank,
				PowerWordStun, 
				Sunburst, Telepathy,
				],
			9: [
				AstralProjection, 
				Foresight, 
				Gate, Imprisonment, 
				MeteorSwarm,
				PowerWordKill, 
				PrismaticWall, 
				Shapechange, 
				TimeStop, TruePolymorph,
				Weird, Wish,
				],
			},
	"Sorcerer":  {
	0: [AcidSplash, BladeWard, ChillTouch, DancingLights, FireBolt,
		Friends, Light, MageHand, Mending, Message, MinorIllusion,
		PoisonSpray, Prestidigitation, RayofFrost, ShockingGrasp,
		TrueStrike],

	1: [BurningHands, CharmPerson, ChromaticOrb, ColorSpray,
		ComprehendLanguages, DetectMagic, DisguiseSelf, ExpeditiousRetreat,
		FalseLife, FeatherFall, FogCloud, Jump, MageArmor, MagicMissile,
		RayofSickness, Shield, SilentImage, Thunderwave, WitchBolt],

	2: [AlterSelf, BlindnessDeafness, Blur, CloudofDaggers, CrownofMadness,
		Darkness, Darkvision, DetectThoughts, EnhanceAbility, EnlargeReduce,
		GustOfWind, HoldPerson, Invisibility, Knock, Levitate, MistyStep,
		MirrorImage, PhantasmalForce, ScorchingRay, SeeInvisibility,
		SpiderClimb, Suggestion, Web],

	3: [Blink, Clairvoyance, Counterspell, Daylight, DispelMagic, Fireball,
		Fly, GaseousForm, Haste, HypnoticPattern, LightningBolt, MajorImage,
		ProtectionfromEnergy, SleetStorm, Slow, StinkingCloud, Tongues,
		WaterBreathing, WaterWalk],

	4: [
		Banishment, Blight, DimensionDoor, GreaterInvisibility,
		IceStorm, Polymorph, Stoneskin, WallofFire],

	5: [AnimateObjects, Cloudkill, ConeCold, Creation, DominatePerson,
		HoldMonster, InsectPlague, Seeming, Telekinesis,
		TeleportationCircle, WallStone],

	6: [ChainLightning, CircleofDeath, Disintegrate, Eyebite,
		GlobeInvulnerability, MassSuggestion, MoveEarth, Sunbeam,
		TrueSeeing],

	7: [DelayedBlastFireball, Etherealness, FingerofDeath, FireStorm,
		PlaneShift, PrismaticSpray, ReverseGravity, Teleport],

	8: [DominateMonster, Earthquake, IncendiaryCloud, PowerWordStun,
		Sunburst],

	9: [Gate, MeteorSwarm, PowerWordKill, TimeStop, Wish],
			},
	"Druid":  {
			0: [PrimalSavagery, Thunderclap, ThornWhip, StarryWisp, SparetheDying,
				Shillelagh, Resistance, ProduceFlame, PoisonSpray,	Message,
				Mending,	Guidance,	Elementalism,	Druidcraft],
			1: [ AnimalFriendship,	CharmPerson,	CreateorDestroyWater,
				CureWounds,	DetectMagic,	DetectPoisonandDisease,
				Entangle,	FaerieFire,	FogCloud, Goodberry,	HealingWord,
				IceKnife,	Jump,	Longstrider,	ProtectionfromEvilandGood,
				PurifyFoodandDrink, SpeakwithAnimals,	Thunderwave,
				],
			2: [
				Aid, AnimalMessenger,	Augury,	Barkskin,	BeastSense,
				ContinualFlame,	Darkvision,	EnhanceAbility,	EnlargeReduce,
				FindTraps,	FlameBlade,	FlamingSphere,	GustOfWind,	HeatMetal,
				HoldPerson,	LesserRestoration,	LocateAnimalsPlants,
				LocateObject,	Moonbeam,	PassWithoutTrace,
				ProtectionFromPoison,	SpikeGrowth,	SummonBeast,
				],
			3: [
				AuraofVitality, CallLightning,	ConjureAnimals,	Daylight,
				DispelMagic,	ElementalWeapon,	FeignDeath,	MeldIntoStone,
				PlantGrowth,	ProtectionfromEnergy,	Revivify,	SleetStorm,
				SpeakWithPlants,	SummonFey,	WaterBreathing,	WaterWalk,
				WindWall,
				],
			4: [
				Blight,	CharmMonster,	Confusion,	ConjureMinorElementals,
				ConjureWoodlandBeings,	ControlWater,	Divination,
				DominateBeast,	FireShield,	FountofMoonlight, FreedomofMovement,
				GiantInsect,	GraspingVine,	HallucinatoryTerrain,
				IceStorm,	LocateCreature,	Polymorph,	StoneShape,	Stoneskin,
				SummonElemental,	WallofFire,
				],
			5: [
				AntilifeShell,	Awaken,	CommuneWithNature,	ConeofCold,
				ConjureElemental,	Contagion,	Geas,	GreaterRestoration,
				InsectPlague,	MassCureWounds,	PlanarBinding,	Reincarnate,
				Scrying,	TreeStride,	WallStone,
				],
			6: [
				ConjureFey,	FindthePath,	FleshtoStone,	Heal,	HeroesFeast,
				MoveEarth,	Sunbeam,	TransportviaPlants,	WallThorns,	WindWalk
				],
			7: [
				FireStorm,	MirageArcane,	PlaneShift,	Regenerate,
				ReverseGravity,	Symbol
				],
			8: [
				AnimalShapes,	AntipathySympathy,	Befuddlement,
				ControlWeather,	Earthquake,	IncendiaryCloud,	Sunburst,
				Tsunami
				],
			9: [
				Foresight,	Shapechange,	StormofVengeance,	TrueResurrection
				],
			},
	"Artificer": {
			0: [
				AcidSplash, DancingLights, Elementalism, FireBolt, Guidance,
				Light, MageHand, Mending, Message, PoisonSpray,
				Prestidigitation, RayofFrost, Resistance, ShockingGrasp,
				SparetheDying, ThornWhip, Thunderclap, TrueStrike,
				],
			1: [
				Alarm, CureWounds, DetectMagic, DisguiseSelf,
				ExpeditiousRetreat, FaerieFire, FalseLife, FeatherFall,
				Grease, Identify, Jump, Longstrider, PurifyFoodandDrink,
				sanctuary,
				],
			2: [
				Aid, AlterSelf, ArcaneLock, ArcaneVigor, Blur, ContinualFlame,
				Darkvision, DragonsBreath, EnhanceAbility, EnlargeReduce,
				HeatMetal, Invisibility, LesserRestoration, Levitate,
				MagicMouth, MagicWeapon, ProtectionFromPoison, RopeTrick,
				SeeInvisibility, SpiderClimb, Web,
				],
			3: [
				Blink, CreateFoodWater, DispelMagic, ElementalWeapon, Fly,
				GlyphofWarding, Haste, ProtectionfromEnergy, Revivify,
				WaterBreathing, WaterWalk,
				],
			4: [
				ArcaneEye, Fabricate, FreedomofMovement, SecretChest,
				FaithfulHound, PrivateSanctum, OtilukeResilientSphere,
				StoneShape, Stoneskin, SummonConstruct,
				],
			5: [
				AnimateObjects, BigbysHand, CircleofPower, Creation,
				GreaterRestoration, WallStone,
				],
			},
	"Ranger":  {
			0: [PrimalSavagery, Thunderclap, ThornWhip, StarryWisp, SparetheDying,
				Shillelagh, Resistance, ProduceFlame, PoisonSpray,	Message,
				Mending,	Guidance,	Elementalism,	Druidcraft ],
			1: [Alarm, CureWounds, DetectMagic, Entangle, FogCloud,
				Goodberry, HuntersMark, HailofThorns, Longstrider, SpeakwithAnimals],
			2: [Aid, BeastSense, CordonofArrows, Darkvision, EnhanceAbility,
				FindTraps, GustOfWind, HealingSpirit, LesserRestoration,
				LocateObject, PassWithoutTrace, SpikeGrowth],
			3: [ConjureAnimals, ConjureBarrage, Daylight, LightningArrow,
				MeldIntoStone, Nondetection, PlantGrowth, ProtectionfromEnergy,
				SpeakPlants, WaterBreathing, WaterWalk],
			4: [ConjureWoodlandBeings, DominateBeast, FreedomofMovement,
				GraspingVine, LocateCreature, Stoneskin],
			5: [CommuneWithNature, ConjureVolley, SwiftQuiver, TreeStride,
				WrathNature],

			6: [ ],
			7: [ ],
			8: [ ],
			9: [ ],
			},
	"Eldritch Knight": {
			0: [    AcidSplash,           BladeWard,
					ChillTouch,           DancingLights,
					Elementalism,         FireBolt,
					Friends,              Light,
					MageHand,             Mending,
					Message,              MindSliver,
					MinorIllusion,        PoisonSpray,
					Prestidigitation,     RayofFrost,
					ShockingGrasp,        Thunderclap,
					TolltheDead,          TrueStrike,
					BoomingBlade,        ControlFlames
					],
			1: [     Shield,         MagicMissile,     AbsorbElements,
					BurningHands,     Alarm,             CharmPerson,
					ChromaticOrb,     ColorSpray,      DetectMagic,
					ExpeditiousRetreat,        FalseLife,
					],
			2: [     MistyStep,                 MirrorImage,
					HoldPerson,             Shatter,
					Blur,                    Web,
					MistyStep,                MagicWeapon,
					Invisibility,
					Darkness,                CrownofMadness,
					CloudofDaggers,            BlindnessDeafness,
					],
			3: [     Counterspell,             Fireball,
					DispelMagic,             Fly,
					Slow,                    SleetStorm,
					PhantomSteed,            Haste,
					Blink,
					],
			4: [     GreaterInvisibility,     IceStorm,
					DimensionDoor,             Stoneskin,
					Confusion,
					],
			5: [ ],
			6: [ ],
			7: [ ],
			8: [ ],
			9: [ ],
			},
	"Arcane Trickster": {
		0: [    AcidSplash,           
				BladeWard,
				BoomingBlade,
				ChillTouch,        
				ControlFlames,
				DancingLights,
				Elementalism,         
				FireBolt,
				Friends,              
				GreenFlameBlade,
				Light,
				MageHand,             
				Mending,
				Message,              
				MindSliver,
				MinorIllusion,        
				PoisonSpray,
				Prestidigitation,     
				RayofFrost,
				ShockingGrasp,        
				Thunderclap,
				TolltheDead,          
				TrueStrike,

				],
		1: [
					Alarm,             
					AbsorbElements,
					BurningHands,
					ChromaticOrb,     
					ColorSpray,      
					CharmPerson, 
					Catapult,
					CauseFear,    
					ComprehendLanguages,
					DetectMagic,    
					DisguiseSelf,
					ExpeditiousRetreat,
					FogCloud,    
					FalseLife, FeatherFall,    
					FindFamiliar,
					Grease,
					IceKnife,    
					Identify,    
					IllusoryScript,
					Jump,
					Longstrider,
					MagicMissile, 
					MageArmor,
					ProtectionfromEvilandGood,
					Shield, 
					SilentImage,    
					SilveryBarbs,    
					Sleep,    
					Snare,
					HideousLaughter,
					Thunderwave,
					UnseenServant,
					],
		2: [     AlterSelf,    ArcaneLock,    ArcaneVigor, Augury,
					BlindnessDeafness,    Blur,    BorrowedKnowledge,
					CloudofDaggers,        CrownofMadness,
					Darkness,    DetectThoughts,
					Earthbind,    EnhanceAbility,    EnlargeReduce,
					GustOfWind,
					HoldPerson,
					Invisibility,
					KineticJaunt, Knock,
					Levitate,    LocateObject,
					MagicMouth,    MagicWeapon, MindSpike,
						MistyStep,     MirrorImage, MagicAura,
					PhantasmalForce,    Pyrotechnics,
					RayOfEnfeeblement, RopeTrick,
					ScorchingRay,     Shatter,    SeeInvisibility,    ShadowBlade,
						Shatter,    SpiderClimb,    SprayOfCards,
						Suggestion,
					MindWhip,
					VortexWarp,
					Web,    WardingWind,    WarpSense,    WitherBloom,

					],
			3: [     AnimateDead,    Antagonize,
					BestowCurse,    Blink,
					Counterspell,     Catnap,    Clairvoyance,    Counterspell,
					DispelMagic,
					EnemiesAbound,
					Fear,    Fireball,     Fly,    FeignDeath,    FlameArrows,
					GaseousForm,    GlyphWarding,
					Haste,    HypnoticPattern,
					IntellectFortress,
					LifeTransference,    LightningBolt,
					MagicCircle,    MelfsMinuteMeteors,
					Nondetection,
					PhantomSteed,    ProtectionfromEnergy,
					RemoveCurse,
					Sending,    Slow,    SleetStorm,    SpeakwithDead,
					SpiritShroud,    StinkingCloud,    SummonFey,
						SummonLesserDemons,    SummonShadowspawn,    SummonUndead,
					TinyHut,    ThunderStep,    TidalWave,    TinyServant,
						Tongues,    VampiricTouch,    WallSand,    WallWater,
						WaterBreathing,
					],
			4: [     ArcaneEye,
					Banishment,    Blight,
					CharmMonster,    Confusion,    ConjureMinorElementals,
						ControlWater,
					DimensionDoor, Divination,
					Fabricate,
					GreaterInvisibility,
					HallucinatoryTerrain,
					LocateCreature,
					FaithfulHound,
					OtilukeResilientSphere,
					PhantasmalKiller,
					Polymorph,
					SpiritOfDeath,    StoneShape,    Stoneskin, StormSphere,
						SummonAberration,    SummonConstruct,    SummonElemental,
						SummonGreaterDemon,    WallofFire,
					],
			5: [ ],
			6: [ ],
			7: [ ],
			8: [ ],
			9: [ ],
			},
	"Cleric": {
		0: [Guidance, Light, Resistance, SacredFlame, SparetheDying, Thaumaturgy],

	1: [
		Bane, Bless, Command, CureWounds,
		DetectEvilandGood, DetectMagic, DetectPoisonandDisease,
		GuidingBolt, HealingWord, InflictWounds,
		ProtectionfromEvilandGood, PurifyFoodandDrink, Sanctuary,
		ShieldofFaith,
	],

	2: [
		Aid, Augury, BlindnessDeafness, CalmEmotions,
		FindTraps, GentleRepose, HoldPerson, LesserRestoration,
		LocateObject, MagicWeapon, PrayerOfHealing, ProtectionFromPoison,
		Silence, SpiritualWeapon, WardingBond, ZoneOfTruth
	],

	3: [
		AuraVitality, BeaconHope, Clairvoyance,
		CreateFoodWater,
		CrusadersMantle, Daylight, DispelMagic, FeignDeath, GlyphWarding,
		MagicCircle, MassHealingWord, RemoveCurse, Revivify,
		SpeakwithDead, SpiritGuardians, Tongues
	],

	4: [
		AuraLife, AuraofPurity, Banishment, DeathWard, Divination,
		FreedomOfMovement, GuardianFaith, LocateCreature,
	],

	5: [
		CircleofPower, Commune, Contagion, DestructiveWave,
		DispelEvilandGood, FlameStrike, Geas, GreaterRestoration, Hallow,
		LegendLore, MassCureWounds, PlanarBinding, RaiseDead, Scrying
	],

	6: [
		BladeBarrier, FindthePath, Forbiddance, Harm, Heal, HeroesFeast,
		PlanarAlly, Sunbeam, TrueSeeing, WordRecall   # a.k.a. WordofRecall
	],

	7: [
		ConjureCelestial, DivineWord, Etherealness, PlaneShift,
		Regenerate, Resurrection, Symbol
	],

	8: [
		AntimagicField, AntipathySympathy, HolyAura, Sunburst
	],

	9: [
		AstralProjection, Foresight, Gate, MassHeal,
		PowerWordHeal, TrueResurrection
	],

	},
	"Bard": {
		0: [
			BladeWard, DancingLights, Friends, Light, MageHand, Mending,
			Message, MinorIllusion, Prestidigitation, StarryWisp,
			Thunderclap, TrueStrike, ViciousMockery
			],
		1: [
			AnimalFriendship, Bane, CharmPerson, ColorSpray, Command,
			ComprehendLanguages, CureWounds, DetectMagic, DisguiseSelf,
			DissonantWhispers, FaerieFire, FeatherFall, HealingWord,
			Heroism, Identify, IllusoryScript, Longstrider, SilentImage,
			SilveryBarbs, Sleep, SpeakwithAnimals, TashaHideousLaughter,
			Thunderwave, UnseenServant
			],
		2: [
			Aid, AnimalMessenger, BlindnessDeafness, CalmEmotions,
			CloudofDaggers, CrownofMadness, DetectThoughts,
			EnhanceAbility, EnlargeReduce, Enthrall, HeatMetal,
			HoldPerson, Invisibility, Knock, LesserRestoration,
			LocateAnimalsorPlants, LocateObject, MagicMouth, MirrorImage,
			PhantasmalForce, SeeInvisibility, Shatter, Silence, Suggestion,
			ZoneofTruth
			],
		3: [
			BestowCurse, Clairvoyance, DispelMagic, Fear, FeignDeath,
			GlyphofWarding, HypnoticPattern, LeomundTinyHut, MajorImage,
			MassHealingWord, Nondetection, PlantGrowth, Sending, Slow,
			SpeakwithDead, SpeakwithPlants, StinkingCloud, Tongues
			],
		4: [
			CharmMonster, Compulsion, Confusion, DimensionDoor,
			FountofMoonlight, FreedomofMovement, GreaterInvisibility,
			HallucinatoryTerrain, LocateCreature, PhantasmalKiller,
			Polymorph
			],
		5: [
			AnimateObjects, Awaken, DominatePerson, Dream, Geas,
			GreaterRestoration, HoldMonster, LegendLore, MassCureWounds,
			Mislead, ModifyMemory, PlanarBinding, RaiseDead,
			TelepathicBond, Scrying, Seeming, SynapticStatic,
			TeleportationCircle, RegalPresence
			],
		6: [
			Eyebite, FindthePath, GuardsandWards, HeroesFeast, MassSuggestion,
			IrresistibleDance, ProgrammedIllusion, TrueSeeing
			],
		7: [
			Etherealness, Forcecage, MirageArcane, MagnificentMansion,
			MordenkainenSword, PrismaticSpray, ProjectImage, PowerWordFortify,
			Regenerate, Resurrection, Symbol, Teleport
			],
		8: [
			AntipathySympathy, Befuddlement, DominateMonster, Glibness,
			MindBlank, PowerWordStun
			],
		9: [
			Foresight, PowerWordHeal, PowerWordKill,
			PrismaticWall, TruePolymorph
			],
		},
	# 2024 PHB Paladin list (was missing — sheet showed slots with no spells).
	"Paladin": {
			1: [
					Bless, Command, CompelledDuel, CureWounds,
					DetectEvilandGood, DetectMagic, DetectPoisonandDisease,
					DivineFavor, Heroism, ProtectionfromEvilandGood,
					PurifyFoodandDrink, SearingSmite, ShieldofFaith,
					ThunderousSmite, WrathfulSmite,
					],
			2: [
					Aid, FindSteed, GentleRepose, LesserRestoration,
					LocateObject, MagicWeapon, PrayerOfHealing,
					ProtectionFromPoison, WardingBond, ZoneofTruth,
					],
			3: [
					AuraofVitality, BlindingSmite, CreateFoodWater,
					CrusadersMantle, Daylight, DispelMagic, ElementalWeapon,
					MagicCircle, RemoveCurse, Revivify,
					],
			4: [
					AuraLife, AuraofPurity, Banishment, DeathWard,
					LocateCreature, StaggeringSmite,
					],
			5: [
					BanishingSmite, CircleofPower, DestructiveWave,
					DispelEvilandGood, Geas, GreaterRestoration, RaiseDead,
					SummonCelestial,
					],
			},
	}


def _expanded_spell_table(
		character,
		base_table,
		):
	"""Return one spell table enriched by the Character's semantic context."""
	order_table = getattr(
			character,
			"order_spells_of_order",
			{},
			) or {}
	levels = tuple(
			sorted(
					set(
							base_table
							)
					| set(
							order_table
							)
					)
			)
	answer = {}

	for level in levels:
		spells = []
		seen = set()

		for spell in (
				tuple(
						base_table.get(
								level,
								(),
								)
						)
				+ tuple(
						order_table.get(
								level,
								(),
								)
						)
				):
			name = getattr(
					spell,
					"name",
					str(
							spell
							),
					)

			if name in seen:
				continue

			seen.add(
					name
					)
			spells.append(
					spell
					)

		answer[
				level
				] = tuple(
						spells
						)

	return answer



class Spellcaster:
	def __init__(caster, character, known=None):
		if known is None:      known = []
		caster.character     = character
		caster.level         = character.level
		caster.casting_stat  = caster.get_casting_stat()
		caster.spell_slots     =  caster.get_spell_slots()
		caster.spells_available = caster.available_spells()
		caster.spells_known = known + character.known_spells
		caster.prepare_spells()

	def get_casting_stat(caster):
		return "INT"  # default, override in subclasses

	def get_spell_slots(caster):
		slots_table = {}
		return slots_table

	def available_spells(caster):
		"""Return all spells this character can *learn* at their current level."""
		table = _expanded_spell_table(
				caster.character,
				SPELL_LISTS.get(
						caster.character.char_class,
						{},
						),
				)
		maximum_level = max(
				(
						level
						for level, count in caster.spell_slots.items()
						if count > 0
						),
				default=0,
				)
		unlocked = [
				level
				for level in table
				if (
						level == 0
						or 0 < level <= maximum_level
						)
				]
		spells = [s for lvl in unlocked for s in table[lvl]]
		return spells

	def prepare_spells(caster):
		pass

	def spell_save_dc(caster):
		# Use whatever you call your prof bonus and ability mod
		prof = getattr(caster.character, "proficiency_bonus", 2)  # or caster.character.get_prof_bonus()
		stat_mod = caster.modifier()
		return 8 + prof + stat_mod

	def spell_attack_bonus(caster):
		prof = getattr(caster.character, "proficiency_bonus", 2)
		stat_mod = caster.modifier()
		return prof + stat_mod

	def __str__(caster):
		spells_names = "".join(f"<li>〖{spell.level}〗{spell.name}</li>" for spell in caster.spells_known)
		slots_html = ", ".join(f"Level {lvl}: {num}" for lvl, num in caster.spell_slots.items())
		spells_html = "".join(f"""<div class="spell">{spell:html}</div>""" for spell in caster.spells_known)

		return f"""
			<h1 style="font-family: {title_font(caster.character.char_class)}; font-size:    3.1em; ">{caster.character.char_class} Spellcasting</h1>
			<p><b>Spell Slots:</b> {slots_html}</p>
			<ul style="list-style-type: '🪄'; text-align: left; font-family: var(--font-script)">{spells_names}</ul>
			<div class="spell" style="margin-bottom: 1em;">
				<b>Spell Save DC:</b> {caster.spell_save_dc()}<br>
				<b>Spell Attack Bonus:</b> +{caster.spell_attack_bonus()}
				</div>
			{spells_html}
		"""

	def html(caster):
		if not caster.spells_known:
			return "<i>No spells known</i>"
		list_items = "".join(f"<li>{s.name}</li>" for s in caster.spells_known)
		return f"""<div class="spell"><b>Spellcasting</b><ul>{list_items}</ul></div>"""


class SpeciesSpellcaster(Spellcaster):
	"""Presentation adapter for innate Species spells on non-casters."""

	def __init__(
			caster,
			character,
			):
		caster.class_name = (
			f"{getattr(character, 'heritage', character.species)} Lineage"
			)
		super().__init__(
			character,
			)

	def get_casting_stat(
			caster,
			):
		return caster.character.species_spellcasting_ability

	def available_spells(
			caster,
			):
		return []

	def modifier(
			caster,
			):
		score = getattr(
			caster.character.AS,
			caster.casting_stat,
			)

		return (
			score
			- 10
			) // 2


class Wizard(Spellcaster):
	def __init__(caster, character, known=None):
		if known is None:      known = []
		caster.class_name     = "Wizard"
		caster.character     = character
		caster.level         = character.level
		caster.spell_slots     =  caster.get_spell_slots()
		caster.spells_available = caster.available_spells()
		caster.spells_known = known
		caster.casting_stat = caster.get_casting_stat()
		caster.prepare_spells()

	def get_casting_stat(caster):
		return "INT"

	def get_stats(caster, key):
		table = {
			1:  {"cantrips": 3, "spells": 4,     "slots": (2,0,0,0,0,0,0,0,0)},
			2:  {"cantrips": 3, "spells": 5,      "slots": (3,0,0,0,0,0,0,0,0)},
			3:  {"cantrips": 3, "spells": 6,      "slots": (4,2,0,0,0,0,0,0,0)},
			4:  {"cantrips": 4, "spells": 7,      "slots": (4,3,0,0,0,0,0,0,0)},
			5:  {"cantrips": 4, "spells": 9,      "slots": (4,3,2,0,0,0,0,0,0)},
			6:  {"cantrips": 4, "spells": 10,      "slots": (4,3,3,0,0,0,0,0,0)},
			7:  {"cantrips": 4, "spells": 11,      "slots": (4,3,3,1,0,0,0,0,0)},
			8:  {"cantrips": 4, "spells": 12,      "slots": (4,3,3,2,0,0,0,0,0)},
			9:  {"cantrips": 4, "spells": 14,      "slots": (4,3,3,3,1,0,0,0,0)},
			10: {"cantrips": 5, "spells": 15,      "slots": (4,3,3,3,2,0,0,0,0)},
			11: {"cantrips": 5, "spells": 16,      "slots": (4,3,3,3,2,1,0,0,0)},
			12: {"cantrips": 5, "spells": 16,      "slots": (4,3,3,3,2,1,0,0,0)},
			13: {"cantrips": 5, "spells": 17,      "slots": (4,3,3,3,2,1,1,0,0)},
			14: {"cantrips": 5, "spells": 18,      "slots": (4,3,3,3,2,1,1,0,0)},
			15: {"cantrips": 5, "spells": 19,      "slots": (4,3,3,3,2,1,1,1,0)},
			16: {"cantrips": 5, "spells": 21,      "slots": (4,3,3,3,2,1,1,1,0)},
			17: {"cantrips": 5, "spells": 22,      "slots": (4,3,3,3,2,1,1,1,1)},
			18: {"cantrips": 5, "spells": 23,      "slots": (4,3,3,3,3,1,1,1,1)},
			19: {"cantrips": 5, "spells": 24,      "slots": (4,3,3,3,3,2,1,1,1)},
			20: {"cantrips": 5, "spells": 25,      "slots": (4,3,3,3,3,2,2,1,1)},
			}
		lvl = caster.level
		if lvl > 20: lvl = 20
		value = table.get(lvl, {"cantrips": 0, "spells": 0, "slots": (0,0,0,0)})
		if key == "cantrips":
			return value["cantrips"]
		if key == "spells":
			return value["spells"]
		if key == "slots":
			return {i + 1: val for i, val in enumerate(value["slots"])}

	def get_spell_slots(caster):
		return caster.get_stats("slots")

	def prepare_spells(caster):
		"""
		Draw the cantrips and the prepared spells as two separate quotas.

		This was ``num_spells = caster.level * 2 + 4`` over one mixed pool,
		which ignored the table twelve lines above and let the split between
		cantrips and levelled spells fall out of the dice: a level 6 Wizard
		was observed holding one cantrip, and a level 20 Wizard eight where
		the rules allow five.  ``__str__`` then trimmed with
		``other_spells[:n]``, so the page looked right while the data under
		it was wrong.
		"""
		available = caster.available_spells()
		cantrips = [
			spell
			for spell in available
			if spell.level == 0
			]
		higher = [
			spell
			for spell in available
			if spell.level > 0
			]
		caster.spells_known = _pick_distinct(
			caster.character,
			cantrips,
			min(len(cantrips), caster.get_stats("cantrips")),
			) + _pick_distinct(
			caster.character,
			higher,
			min(len(higher), caster.get_stats("spells")),
			)

	def modifier(caster):
		return (getattr(caster.character.AS, caster.casting_stat) - 10) // 2

	def html(caster):
		return str(caster)

	def __str__(caster):
		n = caster.get_stats("spells")
		cantrips = [s for s in caster.spells_known if s.level == 0]
		other_spells = [s for s in caster.spells_known if s.level > 0]

		prepared = other_spells[:n]
		unprepared = other_spells[n:]
		all_spells = sorted(prepared + unprepared, key=lambda s: (s.level, s.name))
		spells = ""
		for spell in cantrips:
			spells += f"<li>【{spell.level}】{spell.name}</li>"
		for spell in all_spells:
			if spell in prepared or spell.level==0:
				spells += f"<li>【{spell.level}】{spell.name}</li>"
			else:
				spells += f"<li>〖{spell.level}〗{spell.name}</li>"
		slots_html = "<br>".join(
			f"<b>Level {lvl}</b>: <i>{num}</i>"
			for lvl, num in caster.spell_slots.items()
			if num  # This skips levels with 0 slots
			)
		spells_html = "".join(
			f"""<div class="spell">{spell:html}</div>"""
			for spell in cantrips
			)
		spells_html += "".join(
			f"""<div class="spell">{spell:html}</div>"""
			for spell in all_spells
			)
		return f"""
			<div class="spell--full">
				<h1 style="font-family: {title_font('Wizard')}; font-size:    3.1em; ">
					Wizard Spellcasting</h1>
				<p> As a student of arcane magic, you have learned to cast spells. </p>
				</div>
			<div class="spell" style="grid-column: span 1;">
				<h2>Spell Slots:</h2>
				{slots_html} <br>
				You regain all expended slots when you finish a Long Rest.</p>
				<br><br>
				</div>
			<div class="spell" style="font-family: var(--font-script)">
				<h2 style="font-family: var(--font-script)">
					Spell Save DC:</h2> {caster.spell_save_dc()}<br>
				<h2 style="font-family: var(--font-script)">
					Spell Attack Bonus:</h2> +{caster.spell_attack_bonus()}
				</div>
			<div class="spell" style="grid-column: span 1;">
			<h3 style="font-family: var(--font-script); font-size:    3.1em; "> SpellBook </h3>
			You may prepare {n} spells whenever you finish a Long Rest, that you can use at any moment, from your book of spells:
			<ul style="list-style-type: '🪄'; text-align: left; font-family: var(--font-script) ">
				{spells}</ul>
			<h2>Arcane Focus</h2>
			<b>Intelligence</b> is your spellcasting ability for your Wizard spells. You can use an Arcane Focus (such as a wand or scepter) <b>or your Spellbook</b> as a Spellcasting Focus for them.
			</div>
			{spells_html}
			"""

class Druid(Spellcaster):

	def __init__(caster, character, known=None):
		if known is None:      known = []
		caster.class_name     = "Druid"
		caster.character     = character
		caster.level         = character.level
		caster.spell_slots     =  caster.get_spell_slots()
		caster.spells_available = caster.available_spells()
		caster.spells_known = known
		caster.casting_stat = caster.get_casting_stat()
		caster.prepare_spells()

	def get_casting_stat(caster):
		return "WIS"

	def get_stats(caster, key):
		table = {
			1:  {"cantrips": 2, "spells": 4,	"slots": (2,0,0,0,0,0,0,0,0)},
			2:  {"cantrips": 2, "spells": 5, 	"slots": (3,0,0,0,0,0,0,0,0)},
			3:  {"cantrips": 2, "spells": 6,	"slots": (4,2,0,0,0,0,0,0,0)},
			4:  {"cantrips": 3, "spells": 7, 	"slots": (4,3,0,0,0,0,0,0,0)},
			5:  {"cantrips": 3, "spells": 9, 	"slots": (4,3,2,0,0,0,0,0,0)},
			6:  {"cantrips": 3, "spells": 10, 	"slots": (4,3,3,0,0,0,0,0,0)},
			7:  {"cantrips": 3, "spells": 11, 	"slots": (4,3,3,1,0,0,0,0,0)},
			8:  {"cantrips": 3, "spells": 12, 	"slots": (4,3,3,2,0,0,0,0,0)},
			9:  {"cantrips": 3, "spells": 14, 	"slots": (4,3,3,3,1,0,0,0,0)},
			10: {"cantrips": 4, "spells": 15, 	"slots": (4,3,3,3,2,0,0,0,0)},
			11: {"cantrips": 4, "spells": 16, 	"slots": (4,3,3,3,2,1,0,0,0)},
			12: {"cantrips": 4, "spells": 16, 	"slots": (4,3,3,3,2,1,0,0,0)},
			13: {"cantrips": 4, "spells": 17, 	"slots": (4,3,3,3,2,1,1,0,0)},
			14: {"cantrips": 4, "spells": 17, 	"slots": (4,3,3,3,2,1,1,0,0)},
			15: {"cantrips": 4, "spells": 18, 	"slots": (4,3,3,3,2,1,1,1,0)},
			16: {"cantrips": 4, "spells": 18, 	"slots": (4,3,3,3,2,1,1,1,0)},
			17: {"cantrips": 4, "spells": 19, 	"slots": (4,3,3,3,2,1,1,1,1)},
			18: {"cantrips": 4, "spells": 20, 	"slots": (4,3,3,3,3,1,1,1,1)},
			19: {"cantrips": 4, "spells": 21, 	"slots": (4,3,3,3,3,2,1,1,1)},
			20: {"cantrips": 4, "spells": 22, 	"slots": (4,3,3,3,3,2,2,1,1)},
			}
		lvl = caster.level
		if lvl > 20: lvl = 20
		value = table.get(lvl, {"cantrips": 0, "spells": 0, "slots": (0,0,0,0)})
		if key == "cantrips":
			result = value["cantrips"]
			if character.Primal_Order and character.Primal_Order == "Magician":
				result += 1
			return result
		if key == "spells":
			return value["spells"]
		if key == "slots":
			return {i + 1: val for i, val in enumerate(value["slots"])}

	def get_spell_slots(caster):
		return caster.get_stats("slots")

	def prepare_spells(caster):
		num_spells = caster.level*2 + 4
		# Feature grants (Wild Companion, Spellfire Spark, …) reserve names
		# so random picks never duplicate them.
		reserved = {
			getattr(spell, "name", None)
			for spell in getattr(caster.character, "known_spells", None) or []
			if getattr(spell, "name", None)
			}
		pool = []
		seen = set()
		for spell in caster.available_spells():
			name = getattr(spell, "name", None)
			if not name or name in reserved or name in seen:
				continue
			seen.add(name)
			pool.append(spell)
		caster.spells_known = _pick_distinct(
			caster.character,
			pool,
			min(len(pool), num_spells),
			)
		known_names = {
			getattr(spell, "name", None)
			for spell in caster.spells_known
			}
		for spell in getattr(caster.character, "known_spells", None) or []:
			name = getattr(spell, "name", None)
			if name and name not in known_names:
				caster.spells_known.append(spell)
				known_names.add(name)

	def modifier(caster):
		return (getattr(caster.character.AS, caster.casting_stat) - 10) // 2

	def html(caster):
		return str(caster)

	def __str__(caster):
		n = caster.get_stats("spells")
		cantrips = [s for s in caster.spells_known if s.level == 0]
		other_spells = [s for s in caster.spells_known if s.level > 0]

		prepared = other_spells[:n]
		unprepared = other_spells[n:]
		all_spells = sorted(prepared + unprepared, key=lambda s: (s.level, s.name))
		spells = ""
		for spell in cantrips:
			spells += f"<li>【{spell.level}】{spell.name}</li>"
		for spell in all_spells:
			if spell in prepared or spell.level==0:
				spells += f"<li>【{spell.level}】{spell.name}</li>"
			else:
				spells += f"<li>〖{spell.level}〗{spell.name}</li>"
		slots_html = "<br>".join(
			f"<b>Level {lvl}</b>: <i>{num}</i>"
			for lvl, num in caster.spell_slots.items()
			if num  # This skips levels with 0 slots
			)
		spells_html = "".join(
			f"""<div class="spell">{spell:html}</div>"""
			for spell in cantrips
			)
		spells_html += "".join(
			f"""<div class="spell">{spell:html}</div>"""
			for spell in all_spells
			)
		return f"""
			<div class="spell--full">
				<h1 style="font-family: {title_font('Druid')}; font-size:    3.1em; ">
					Druid Spellcasting</h1>
				<p> As a student of natural magic, you have learned to cast spells. </p>
				</div>
			<div class="spell" style="grid-column: span 1;">
				<h2>Spell Slots:</h2>
				{slots_html} <br>
				You regain all expended slots when you finish a Long Rest.</p>
				<br><br>
				</div>
			<div class="spell" style="font-family: var(--font-script)">
				<h2 style="font-family: var(--font-script)">
					Spell Save DC:</h2> {caster.spell_save_dc()}<br>
				<h2 style="font-family: var(--font-script)">
					Spell Attack Bonus:</h2> +{caster.spell_attack_bonus()}
				</div>
			<div class="spell" style="grid-column: span 1;">
			<h3 style="font-family: var(--font-script); font-size:    3.1em; "> SpellBook </h3>
			You may prepare {n} spells whenever you finish a Long Rest, that you can use at any moment, from your book of spells:
			<ul style="list-style-type: '🍀'; text-align: left; font-family: var(--font-script) ">
				{spells}</ul>
			<h2>Arcane Focus</h2>
			You can use an Arcane Focus (such as a wand or scepter),  as a Spellcasting Focus for your Druid spells.
			</div>
			{spells_html}
			"""

class Cleric(Spellcaster):
	"""Full‑caster progression using Wisdom. Clerics prepare a number of spells equal to
	their cleric level ＋ Wisdom modifier each day and can choose from the entire Cleric list.
	They always know a fixed number of cantrips (see table)."""

	def __init__(caster, character, known=None):
		if known is None:      known = []
		caster.class_name     = "Cleric"
		caster.character     = character
		caster.level         = character.level
		caster.spell_slots     =  caster.get_spell_slots()
		caster.spells_available = caster.available_spells()
		caster.spells_known = known
		caster.casting_stat = caster.get_casting_stat()
		caster.prepare_spells()

	def get_casting_stat(caster):
		return "WIS"
	# Ability‑score helper

	def modifier(self) -> int:
		wis_score = getattr(self.character.AS, "WIS", 10)
		return (wis_score - 10) // 2

	def get_stats(caster, key):
		table = {
			1:  {"cantrips": 3, "spells": 4,	"slots": (2,0,0,0,0,0,0,0,0)},
			2:  {"cantrips": 3, "spells": 5, 	"slots": (3,0,0,0,0,0,0,0,0)},
			3:  {"cantrips": 3, "spells": 6,	"slots": (4,2,0,0,0,0,0,0,0)},
			4:  {"cantrips": 4, "spells": 7, 	"slots": (4,3,0,0,0,0,0,0,0)},
			5:  {"cantrips": 4, "spells": 9, 	"slots": (4,3,2,0,0,0,0,0,0)},
			6:  {"cantrips": 4, "spells": 10, 	"slots": (4,3,3,0,0,0,0,0,0)},
			7:  {"cantrips": 4, "spells": 11, 	"slots": (4,3,3,1,0,0,0,0,0)},
			8:  {"cantrips": 4, "spells": 12, 	"slots": (4,3,3,2,0,0,0,0,0)},
			9:  {"cantrips": 4, "spells": 14, 	"slots": (4,3,3,3,1,0,0,0,0)},
			10: {"cantrips": 5, "spells": 15, 	"slots": (4,3,3,3,2,0,0,0,0)},
			11: {"cantrips": 5, "spells": 16, 	"slots": (4,3,3,3,2,1,0,0,0)},
			12: {"cantrips": 5, "spells": 16, 	"slots": (4,3,3,3,2,1,0,0,0)},
			13: {"cantrips": 5, "spells": 17, 	"slots": (4,3,3,3,2,1,1,0,0)},
			14: {"cantrips": 5, "spells": 17, 	"slots": (4,3,3,3,2,1,1,0,0)},
			15: {"cantrips": 5, "spells": 18, 	"slots": (4,3,3,3,2,1,1,1,0)},
			16: {"cantrips": 5, "spells": 18, 	"slots": (4,3,3,3,2,1,1,1,0)},
			17: {"cantrips": 5, "spells": 19, 	"slots": (4,3,3,3,2,1,1,1,1)},
			18: {"cantrips": 5, "spells": 20, 	"slots": (4,3,3,3,3,1,1,1,1)},
			19: {"cantrips": 5, "spells": 21, 	"slots": (4,3,3,3,3,2,1,1,1)},
			20: {"cantrips": 5, "spells": 22, 	"slots": (4,3,3,3,3,2,2,1,1)},
			}
		lvl = caster.level
		if lvl > 20: lvl = 20
		value = table.get(lvl, {"cantrips": 0, "spells": 0, "slots": (0,0,0,0)})
		if key == "cantrips":
			result = value["cantrips"]
			# Thaumaturge Divine Order grants one extra Cleric cantrip.
			if getattr(caster.character, "divine_order", None) == "Thaumaturge":
				result += 1
			return result
		if key == "spells":
			return value["spells"]
		if key == "slots":
			return {i + 1: val for i, val in enumerate(value["slots"])}

	def get_spell_slots(caster):
		return caster.get_stats("slots")

	def prepare_spells(caster):
		"""
		Draw cantrips and prepared spells as two quotas from the 2024 table.

		``get_stats`` already includes the Thaumaturge extra cantrip.
		"""
		available = caster.available_spells()
		cantrips = [
			spell
			for spell in available
			if spell.level == 0
			]
		higher = [
			spell
			for spell in available
			if spell.level > 0
			]
		caster.spells_known = _pick_distinct(
			caster.character,
			cantrips,
			min(
				len(
					cantrips
					),
				caster.get_stats(
					"cantrips"
					),
				),
			) + _pick_distinct(
			caster.character,
			higher,
			min(
				len(
					higher
					),
				caster.get_stats(
					"spells"
					),
				),
			)

	def modifier(caster):
		return (getattr(caster.character.AS, caster.casting_stat) - 10) // 2

	def html(caster):
		return str(caster)

	def __str__(caster):
		n = caster.get_stats("spells")
		cantrips = [s for s in caster.spells_known if s.level == 0]
		spells = [s for s in caster.spells_known if s.level > 0]
		prepared_sorted = sorted(spells, key=lambda s: (s.level, s.name))

		list_items = "".join(f"<li>【{s.level}】{s.name}</li>" for s in cantrips)
		list_items += "".join(
			f"<li>【{s.level}】{s.name}</li>" for s in prepared_sorted
			)

		slots_html = "<br>".join(
			f"<b>Level {lvl}</b>: <i>{num}</i>" for lvl, num in caster.spell_slots.items()
			)

		spell_boxes = "".join(
			f'<div class="spell">{spell:html}</div>' for spell in cantrips + prepared_sorted
			)

		prep_cap = n

		return f"""
		<div class=\"spell--full\" >
			<h1 style=\"font-family: {title_font('Cleric')}; font-size: 3.1em;\">Cleric Spellcasting</h1>
			<p>Drawing on divine power, you prepare <b>{prep_cap}</b> Cleric spells of level 1+ (2024 table).<br>
			Your spellcasting ability is <b>Wisdom</b>.</p>
		</div>
		<div class=\"spell\">
			<h2>Spell Slots</h2>
			{slots_html}<br>
			<small>All slots refresh when you finish a long rest.</small>
		</div>
		<div class=\"spell\">
			<h2>Spell Save DC</h2> {caster.spell_save_dc()}<br>
			<h2>Spell Attack Bonus</h2> +{caster.spell_attack_bonus()}
		</div>
		<div class=\"npc-textbox\" style=\"grid-column: span 1;\">
			<h3 style=\"font-family:var(--font-script); font-size:2.5em;\">Prepared Spells</h3>
			<ul style=\"list-style-type:'📿'; font-family:var(--font-script); text-align:left;\">
				{list_items}
			</ul>
		</div>
		{spell_boxes}
		"""

class Ranger(Spellcaster):
	def __init__(self, character, known: list[Spell] | None = None):
		super().__init__(character, known or [])

	def get_casting_stat(caster):
		return "WIS"

	def get_known_cap(self) -> int:
		wis_mod = self.modifier()
		return max(1, (self.level // 2) + wis_mod)

	# map the slot tuple for this level into {level: slots}
	def get_spell_slots(self):
		row = Ranger.HALF_CASTER_SLOTS[self.level]
		return {i + 1: n for i, n in enumerate(row) if n}

	# same helper used by base class
	def modifier(self) -> int:
		return (getattr(self.character.AS, self.get_casting_stat()) - 10) // 2

	def get_stats(caster, key):
		"""Spellcasting stats: spell slots and number of prepared spells."""
		table = {
			1:  {"prepared": 2,  "slots": (2,0,0,0,0)},
			2:  {"prepared": 3,  "slots": (2,0,0,0,0)},
			3:  {"prepared": 4,  "slots": (3,0,0,0,0)},
			4:  {"prepared": 5,  "slots": (3,0,0,0,0)},
			5:  {"prepared": 6,  "slots": (4,2,0,0,0)},
			6:  {"prepared": 6,  "slots": (4,2,0,0,0)},
			7:  {"prepared": 7,  "slots": (4,3,0,0,0)},
			8:  {"prepared": 7,  "slots": (4,3,0,0,0)},
			9:  {"prepared": 9,  "slots": (4,3,2,0,0)},
			10: {"prepared": 9,  "slots": (4,3,2,0,0)},
			11: {"prepared": 10, "slots": (4,3,3,0,0)},
			12: {"prepared": 10, "slots": (4,3,3,0,0)},
			13: {"prepared": 11, "slots": (4,3,3,1,0)},
			14: {"prepared": 11, "slots": (4,3,3,1,0)},
			15: {"prepared": 12, "slots": (4,3,3,2,0)},
			16: {"prepared": 12, "slots": (4,3,3,2,0)},
			17: {"prepared": 14, "slots": (4,3,3,3,1)},
			18: {"prepared": 14, "slots": (4,3,3,3,1)},
			19: {"prepared": 15, "slots": (4,3,3,3,2)},
			20: {"prepared": 15, "slots": (4,3,3,3,2)},
		}
		lvl = min(caster.level, 20)
		entry = table.get(lvl, {"prepared": 0, "slots": (0,0,0,0,0)})
		if key == "prepared":
			return entry["prepared"]
		if key == "slots":
			return {i + 1: val for i, val in enumerate(entry["slots"])}

	def get_spell_slots(caster):
		return caster.get_stats("slots")

	def prepare_spells(caster):
		n = caster.get_stats("prepared")
		available = [s for s in caster.available_spells() if s.level > 0]
		available = _shuffled_by_character(
			caster.character,
			available,
			)
		caster.spells_known = available[:n]

	def modifier(caster):
		return (getattr(caster.character.AS, caster.casting_stat) - 10) // 2

	def html(caster):
		return str(caster)

	def __str__(caster):
		n = caster.get_stats("prepared")

		prepared = caster.spells_known[:n]
		unprepared = caster.spells_known[n:]
		all_spells = sorted(prepared + unprepared, key=lambda s: (s.level, s.name))
		spells = "".join(
			f"<li>【{s.level}】{s.name}</li>" if s in prepared else f"<li>〖{s.level}〗{s.name}</li>"
			for s in all_spells
		)
		slots_html = "<br>".join(
			f"<b>Level {lvl}</b>: <i>{num}</i>"
			for lvl, num in caster.spell_slots.items()
			if num
		)
		spells_descriptions = "".join(f'<div class="spell">{spell:html}</div>' for spell in all_spells)

		return f"""
		<div class="npc-textbox--full">
			<h1 style="font-family: {title_font('Ranger')}; font-size: 3.1em;">Ranger Spellcasting</h1>
			<p>You prepare {n} spells each day, using your Wisdom as your spellcasting ability.</p>
		</div>
		<div class="npc-textbox">
			<h2>Spell Slots:</h2>
			{slots_html}
			<p>You regain all slots when you finish a long rest.</p>
		</div>
		<div class="npc-textbox">
			<h2>Spell Save DC:</h2> {caster.spell_save_dc()}<br>
			<h2>Spell Attack Bonus:</h2> +{caster.spell_attack_bonus()}
		</div>
		<div class="npc-textbox" style="grid-column: span 1;">
			<h3 style="font-family: var(--font-script); font-size: 3.1em;">Spell List</h3>
			<ul style="list-style-type: '🍀'; font-family: var(--font-script); text-align: left;">
				{spells}
			</ul>
		</div>
		{spells_descriptions}
		"""

class Sorcerer(Spellcaster):
	"""
	2024 PHB Sorcerer spellcasting (Charisma).

	  • Full-caster slot table, identical to the Wizard's
	  • Cantrips 4 → 5 at level 4 → 6 at level 10
	  • Prepared spells 2 → 22, changed only on gaining a level
	  • Origin spells and any spells the Character carries in
	    ``known_spells`` (an Origin feat, say) are always prepared and never
	    count against the number prepared

	Sorcery Points are read from SorcererKit's RESOURCES, which is where the
	Font of Magic lesson reads them too, so the two boxes on the sheet can't
	disagree.
	"""

	# ---------- tables ----------
	_TABLE = {
		# lvl : (cantrips, prepared, slot tuple L1-9)
		1:  (4, 2,  (2,0,0,0,0,0,0,0,0)),
		2:  (4, 4,  (3,0,0,0,0,0,0,0,0)),
		3:  (4, 6,  (4,2,0,0,0,0,0,0,0)),
		4:  (5, 7,  (4,3,0,0,0,0,0,0,0)),
		5:  (5, 9,  (4,3,2,0,0,0,0,0,0)),
		6:  (5,10,  (4,3,3,0,0,0,0,0,0)),
		7:  (5,11,  (4,3,3,1,0,0,0,0,0)),
		8:  (5,12,  (4,3,3,2,0,0,0,0,0)),
		9:  (5,14,  (4,3,3,3,1,0,0,0,0)),
		10: (6,15,  (4,3,3,3,2,0,0,0,0)),
		11: (6,16,  (4,3,3,3,2,1,0,0,0)),
		12: (6,16,  (4,3,3,3,2,1,0,0,0)),
		13: (6,17,  (4,3,3,3,2,1,1,0,0)),
		14: (6,17,  (4,3,3,3,2,1,1,0,0)),
		15: (6,18,  (4,3,3,3,2,1,1,1,0)),
		16: (6,18,  (4,3,3,3,2,1,1,1,0)),
		17: (6,19,  (4,3,3,3,2,1,1,1,1)),
		18: (6,20,  (4,3,3,3,3,1,1,1,1)),
		19: (6,21,  (4,3,3,3,3,2,1,1,1)),
		20: (6,22,  (4,3,3,3,3,2,2,1,1)),
	}

	# ---------- constructor ----------
	def __init__(self, character, known: list | None = None):
		from AtlasLusoris.AtlasOfGuilds.SorcererKit import Find_Sorcery_Points

		super().__init__(character, known or [])
		self.class_name        = "Sorcerer"
		self.sorcery_points    = Find_Sorcery_Points(
			character
			)

	# ---------- core helpers ----------
	def get_casting_stat(self):
		return "CHA"

	def get_stats(self, key):
		lvl = min(self.level, 20)
		can, prepared, slots = Sorcerer._TABLE[lvl]
		match key:
			case "cantrips": return can
			case "prepared": return prepared
			case "slots":   return {i + 1: n for i, n in enumerate(slots) if n}

	def get_spell_slots(self):
		return self.get_stats("slots")

	# ---------- spell selection ----------
	def _always_prepared(self):
		"""Origin spells, then whatever the Character already carries, once each."""
		from AtlasLusoris.AtlasOfGuilds.SorcererKit import Find_Always_Prepared

		carried = (
			list(
				Find_Always_Prepared(
					self.character
					)
				)
			+ list(
				getattr(
					self.character,
					"known_spells",
					None,
					) or []
				)
			)
		unique = {}
		for spell in carried:
			unique.setdefault(
				spell.name,
				spell,
				)
		return list(
			unique.values()
			)

	def prepare_spells(self):
		"""
		Keep the always-prepared spells, then draw the rest from the list.

		The drawn cantrips and spells fill the table's counts in full: an
		always-prepared spell is never one of them.
		"""
		self.always_prepared = self._always_prepared()
		held = {
			spell.name
			for spell in self.always_prepared
			}

		pool = [
			spell
			for spell in self.available_spells()
			if spell.name not in held
			]
		cantrip_pool   = [s for s in pool if s.level == 0]
		leveled_pool   = [s for s in pool if s.level > 0]

		self.spells_known = (
			self.always_prepared
			+ _pick_distinct(
				self.character,
				cantrip_pool,
				min(
					self.get_stats("cantrips"),
					len(
						cantrip_pool
						),
					),
				)
			+ _pick_distinct(
				self.character,
				leveled_pool,
				min(
					self.get_stats("prepared"),
					len(
						leveled_pool
						),
					),
				)
			)

	# ---------- modifiers ----------
	def modifier(self):
		return (getattr(self.character.AS, "CHA") - 10) // 2

	# ---------- fancy output ----------
	def html(self) -> str:
		return str(self)

	def __str__(self):
		# split cantrips vs others
		cantrips = [s for s in self.spells_known if s.level == 0]
		spells   = sorted([s for s in self.spells_known if s.level > 0],
						  key=lambda sp: (sp.level, sp.name))
		always   = {
			spell.name
			for spell in getattr(self, "always_prepared", [])
			}

		def _item(spell):
			if spell.name in always:
				return f"<li>{spell.name} <i>(always prepared)</i></li>"
			return f"<li>{spell.name}</li>"

		spell_li = "".join(_item(s) for s in cantrips + spells)

		# slot display
		slots_html = "<br>".join(
			f"<b>Level {lvl}</b>: <i>{n}</i>"
			for lvl, n in self.spell_slots.items()
			if n
		)

		# individual spell blurbs
		blurbs = "".join(f'<div class="spell">{s:html}</div>' for s in cantrips + spells)

		# Sorcery Points open at level 2, with Font of Magic.
		points_html = (
			f"<br>\n\t\t\t<h2>Sorcery Points</h2> {self.sorcery_points}"
			if self.sorcery_points
			else ""
			)

		return f"""
		<div class="npc-textbox--full" >
			<h1 style="font-family:{title_font('Sorcerer')}; font-size:3.1em;">Sorcerer Spellcasting</h1>
			<p>Your innate magic flows from within, allowing you to impose your Will through the Arcane. You cast spells using <b>Charisma</b>.
			   You know {self.get_stats('cantrips')} cantrips and prepare {self.get_stats('prepared')} spells.</p>
		</div>

		<div class="npc-textbox">
			<h2>Spell Slots</h2>
			{slots_html}
			<p>You regain all expended slots when you finish a long rest.</p>
		</div>

		<div class="npc-textbox">
			<h2>Spell Save DC</h2> {self.spell_save_dc()}<br>
			<h2>Spell Attack Bonus</h2> +{self.spell_attack_bonus()}{points_html}
		</div>

		<div class="npc-textbox" style="grid-column: span 1;">
			<h3 style="font-family:var(--font-script); font-size:3.1em;">Known Spells</h3>
			<ul style="list-style-type:'🔅'; font-family:var(--font-script); text-align:left;">
				{spell_li}
			</ul>
		</div>

		{blurbs}
		"""

MONK_TECHNIQUE_LEVELS = [
	(2, [FlurryofBlows, PatientDefense, StepOfTheWind]),    # Level 2: Focus starts
	(3, [DeflectAttacks]),                                 # Level 3: Improved Deflection
	(5, [StunningStrike]),                                 # Level 5: Stunning Strike
	# Subclass techniques: You can append dynamically based on subclass.
	]


class Monk(Spellcaster):
	def __init__(caster, character):
		caster.character = character
		caster.level = character.Level
		caster.casting_stat = caster.get_casting_stat()
		caster.focus_points = caster.get_focus_points()

	def get_casting_stat(caster):
		return "WIS"

	def get_focus_points(caster):
		if caster.level >= 2: return caster.level
		else: return 0

	@property
	def spells_known(self):
		"""Return all Focus Techniques available to this Monk."""
		techniques = []
		for lvl, feats in MONK_TECHNIQUE_LEVELS:
			if self.level >= lvl:
				techniques.extend(feats)
		# Deduplicate by name
		unique = {ft.name: ft for ft in techniques}
		return list(unique.values())

	def focus_save_dc(self):
		# Usual: 8 + prof + WIS modifier
		prof = getattr(self.character, "proficiency_bonus", 2)
		wis_mod = self.WIS_modifier()
		return 8 + prof + wis_mod

	def WIS_modifier(self):
		# WIS modifier
		return (getattr(self.character.AS, "WIS", 10) - 10) // 2

	def html(caster):
		return str(caster)

	def __str__(caster):
		features = caster.spells_known
		dice_bag = caster.character.Dice_Bag(
			"presentation.spellcaster.focus_symbol",
			version="1",
			namespace="GenLegendActor",
			)
		symb = caster.character.Pick(["☯","☯︎","࿊","࿋","࿌","࿅", "☮",
			"☥", "☣", "𓂀", "𖥂", "𖨢", "⧊", "⧋","⚳", "⚴", "⚸",
			"♆", "♅", "♄", "♃", "☿", "♁", "𖤓", "ᙏ", "ᙎ", "𒀭",
			"𒐊", "𒐉", "𒐋", "𒐏", "𒐖","𒐕", "𒐗", "𒐘", "𐫱", "🀄︎", "🜹",
			"᛭", "⧾", "⚚", "⚕", "✯", "⚝", "⛤", "⛥","⛦", "❄","𖣓",
			"֎", "֍", "𖣐", "۝", "۩", "🃟", "🜾", "🝋", "𝚿", "𝛀", "Ʊ", "𓇳",
			"𓉱", "𓉷", "𓉶", "𓉴", "𖧞", "𖥋", "𖥘", "𖧑", "𓍢", "𓍣", "꥟", "꧁꧂",
			"⏾", "❂", "🀀", "🏵️", "ॐ", "⚕︎", "𐁊", "☸︎", "⚔︎", "𖡨", "🜍", "🜎",
			"㊍", "㊐", "㊥", "㊉", "㊏", "☷", "☶", "☰", "☱", "☲", "☳", "☴",
			"☵",

						],
			dice=dice_bag,
			)
		features_list = "".join(
			f"""<div class="npc-textbox" style="grid-column: span 1;">
					<h2 style="font-family: 'Cinzel'; font-size: 1.5em;">
						{ft.name}</h2>
					{symb}
					{ft.action_type} <br>
					Cost: {ft.cost} Focus Point<br>
					<i>{ft.description}</i>
					</div>"""
			for ft in features
			)
		return f"""
		<div class="npc-textbox--full">
			<h1 style="font-family: 'Cinzel'; font-size:    2.5em; ">
				Monk's Focus
				</h1>
				<p>Your martial training grants you extraordinary inner
				strength known as Focus.
				</p>
				</div>
		<div class="npc-textbox" style="grid-column: span 1;">
			<h2 style="font-family: 'Cinzel Decorative'; font-size: 1.5em;">
				Focus Points: <b>{caster.focus_points}</b>
				</h2>
				You regain all expended Focus Points upon finishing a Short or Long Rest.
				</div>
		<div class="npc-textbox" style="font-size: 1.521em;">
			<h3 style="font-family: 'Cinzel Decorative'">
				Focus Save DC:</h3>
				{caster.focus_save_dc()}<br>
			<h3 style="font-family: 'Cinzel Decorative'">
				Focus Ability Modifier:</h3>
				+{caster.WIS_modifier()}
			</div>

		<div class="npc-textbox" style="grid-column: span 1;">
			<h2 style="font-family: 'Cinzel Decorative'; font-size: 1.3em;">
				Focus Techniques:</h2>
			You can channel Focus to perform special techniques.
			</div>

				{features_list}


		"""

def get_monk_focus_features(level, subclass=None):
	features = []
	for lvl, feats in MONK_TECHNIQUE_LEVELS:
		if level >= lvl:
			features.extend(feats)
	# Add subclass focus techniques here if needed (by subclass and level)
	return features


class EldritchKnight(Spellcaster):
	def get_casting_stat(caster):
		from AtlasLusoris.AtlasOfGuilds.FighterKit import EldritchKnight

		return EldritchKnight.MAGIC.ability

	def get_stats(caster, key):
		from AtlasLusoris.AtlasOfGuilds.FighterKit import EldritchKnight

		rank = EldritchKnight.MAGIC.at(
			caster.level
			)
		if key == "cantrips":
			return rank.cantrips
		if key == "spells":
			return rank.prepared
		if key == "slots":
			return {
				index + 1: count
				for index, count in enumerate(
						rank.slots
						)
				}
		raise KeyError(
			f"Unknown Eldritch Knight spellcasting statistic: {key!r}."
			)

	def get_spell_slots(caster):
		return caster.get_stats("slots")

	def available_spells(caster):
		"""Return all spells this character can *learn* at their current level."""
		table = _expanded_spell_table(
				caster.character,
				SPELL_LISTS.get(
						"Wizard",
						{},
						),
				)
		slots = caster.get_stats(
			"slots"
			)
		maximum_level = max(
			(
				level
				for level, count in slots.items()
				if count > 0
				),
			default=0,
			)
		return [
			spell
			for level, spells in table.items()
			if (
				level == 0
				or 0 < level <= maximum_level
				)
			for spell in spells
			]

	def prepare_spells(caster):
		def Unique(
				spells,
				):
			return list(
				{
					spell.name: spell
					for spell in spells
					}.values()
				)

		cantrip_pool = Unique(
			spell
			for spell in caster.spells_available
			if int(
					spell.level
					) == 0
			)
		leveled_pool = Unique(
			spell
			for spell in caster.spells_available
			if int(
					spell.level
					) > 0
			)
		cantrip_pool.sort(
			key=lambda spell: spell.name
			)
		leveled_pool.sort(
			key=lambda spell: (
					int(
							spell.level
							),
					spell.name,
					)
			)
		caster.character.Dice_Bag(
			"magic.eldritch_knight.cantrips",
			version="2024",
			namespace="GenLegendMagic",
			).shuffle(
				cantrip_pool
				)
		caster.character.Dice_Bag(
			"magic.eldritch_knight.prepared",
			version="2024",
			namespace="GenLegendMagic",
			).shuffle(
				leveled_pool
				)

		selected = [
			*cantrip_pool[
				:caster.get_stats(
						"cantrips"
						)
				],
			*leveled_pool[
				:caster.get_stats(
						"spells"
						)
				],
			]
		known_names = {
			spell.name
			for spell in selected
			}
		for spell in getattr(
				caster.character,
				"known_spells",
				(),
				):
			if spell.name in known_names:
				continue
			selected.append(
				spell
				)
			known_names.add(
				spell.name
				)
		caster.spells_known = selected


	def modifier(caster):
		return (getattr(caster.character.AS, caster.casting_stat) - 10) // 2

	def html(caster):
		return str(caster)

	def __str__(caster):
		ordered_spells = sorted(caster.spells_known, key=lambda s: int(s.level))
		spells_names = "".join(f"<li>〖{spell.level}〗{spell.name}</li>" for spell in ordered_spells)
		spells_html = "".join(f"""<div class="spell">{spell:html}</div>""" for spell in ordered_spells)
		slots_html = "<br>".join(f"<b>Level {lvl}</b>: <i>{num}</i> " for lvl, num in caster.spell_slots.items())
		return f"""
			<div class="npc-textbox" style="grid-column: span 1;">
			<h1 style="font-family: {title_font(caster.character.subclass)}; font-size:    3.1em; ">{caster.character.subclass} Spellcasting</h1>
			<p> Eldritch Knights combine the martial mastery common to all Fighters with a careful study of magic. Their spells both complement and extend their combat skills.<br> You have learned to cast spells. </p>
			<h2>Spell Slots:</h2> {slots_html} <br>  You regain all expended slots when you finish a Long Rest.</p>
			<ul style="list-style-type: '♟️'; text-align: left; font-family: var(--font-script) ">{spells_names}</ul>
			<h2>Arcane Focus</h2>
			<b>Intelligence</b> is your spellcasting ability for your Wizard spells. You can use an Arcane Focus (such as a wand or scepter) <b>or your Spellbook</b> as a Spellcasting Focus for them.
			</div>
			<div class="npc-textbox" style="margin-bottom: 1em;">
				<b>Spell Save DC:</b> {caster.spell_save_dc()}<br>
				<b>Spell Attack Bonus:</b> +{caster.spell_attack_bonus()}
				</div>
			{spells_html}
			"""

class ArcaneTrickster(Spellcaster):
	"""
	Arcane Trickster spellcasting rules, 2024 PHB.
	Handles cantrips, spell slots, prepared spells, and focus.
	"""
	ARCANE_TRICKSTER_TABLE = {
		1:  {"cantrips": 0, "prepared": 0,  "slots": (0,0,0,0)},
		2:  {"cantrips": 0, "prepared": 0,  "slots": (0,0,0,0)},
		3:  {"cantrips": 3, "prepared": 3,  "slots": (2,0,0,0)},
		4:  {"cantrips": 3, "prepared": 4,  "slots": (3,0,0,0)},
		5:  {"cantrips": 3, "prepared": 4,  "slots": (3,0,0,0)},
		6:  {"cantrips": 3, "prepared": 4,  "slots": (3,0,0,0)},
		7:  {"cantrips": 3, "prepared": 5,  "slots": (4,2,0,0)},
		8:  {"cantrips": 3, "prepared": 6,  "slots": (4,2,0,0)},
		9:  {"cantrips": 3, "prepared": 6,  "slots": (4,2,0,0)},
		10: {"cantrips": 4, "prepared": 7,  "slots": (4,3,0,0)},
		11: {"cantrips": 4, "prepared": 8,  "slots": (4,3,0,0)},
		12: {"cantrips": 4, "prepared": 8,  "slots": (4,3,0,0)},
		13: {"cantrips": 4, "prepared": 9,  "slots": (4,3,2,0)},
		14: {"cantrips": 4, "prepared":10,  "slots": (4,3,2,0)},
		15: {"cantrips": 4, "prepared":10,  "slots": (4,3,2,0)},
		16: {"cantrips": 4, "prepared":11,  "slots": (4,3,3,0)},
		17: {"cantrips": 4, "prepared":11,  "slots": (4,3,3,0)},
		18: {"cantrips": 4, "prepared":11,  "slots": (4,3,3,0)},
		19: {"cantrips": 4, "prepared":12,  "slots": (4,3,3,1)},
		20: {"cantrips": 4, "prepared":13,  "slots": (4,3,3,1)},
		}

	def get_casting_stat(trickster):
		return "INT"

	def get_stats(trickster, key):
		lvl = getattr(trickster.character, "level", getattr(trickster.character, "Level", 1))
		table = ArcaneTrickster.ARCANE_TRICKSTER_TABLE
		if lvl > 20: lvl = 20
		data = table.get(lvl, {"cantrips": 0, "prepared": 0, "slots": (0,0,0,0)})
		if key == "cantrips":
			return data["cantrips"]
		if key == "prepared":
			return data["prepared"]
		if key == "slots":
			return {i+1: v for i, v in enumerate(data["slots"])}

	def get_spell_slots(trickster):
		return trickster.get_stats("slots")

	def available_spells(trickster):
		"""Return all spells this Arcane Trickster can learn/cast at their current level."""
		# Prefer the tailored Arcane Trickster list
		base_source = (
			SPELL_LISTS.get("Arcane Trickster")
			or
			SPELL_LISTS.get("Wizard")
			)
		if not base_source:
			return []
		source = _expanded_spell_table(
				trickster.character,
				base_source,
				)
		# Unlock spells up to allowed level
		lvl = getattr(trickster.character, "level", getattr(trickster.character, "Level", 1))
		# Find max spell slot level available (0 below level 3 — cantrips only)
		max_slot = max(
			(i+1 for i, n in enumerate(trickster.get_stats("slots").values()) if n > 0),
			default=0,
			)
		unlocked_levels = [k for k in source if k <= max_slot]
		# Collate spells
		spells = [spell for lvl in unlocked_levels for spell in source[lvl]]
		return spells

	def prepare_spells(trickster):
		"""
		Select cantrips and prepared spells for Arcane Trickster.
		Mage Hand is always known and cannot be replaced.
		"""
		# Cantrips - always include Mage Hand if present
		available_cantrips = [s for s in trickster.spells_available if int(s.level) == 0]
		mage_hand = next((c for c in available_cantrips if c.name == "Mage Hand"), None)
		other_cantrips = [c for c in available_cantrips if c.name != "Mage Hand"]

		n_cantrips = trickster.get_stats("cantrips")
		trickster.spells_known = [mage_hand] if mage_hand else []
		needed = n_cantrips - len(trickster.spells_known)

		if needed > 0:
			suggested = [MindSliver, MinorIllusion]
			chosen = []
			for rec in suggested:
				found = next((c for c in other_cantrips if c.name == rec), None)
				if found and found not in chosen:
					chosen.append(found)
			remaining = [c for c in other_cantrips if c not in chosen]
			remaining = _shuffled_by_character(
				trickster.character,
				remaining,
				)
			chosen += remaining
			trickster.spells_known += chosen[:needed]
		# Now select leveled spells (prepared)
		n_prepared = trickster.get_stats("prepared")
		leveled_pool = [s for s in trickster.spells_available if int(s.level) > 0]

		# Optionally: Recommended spells for level 3
		recommended = ["Charm Person", "Disguise Self", "Fog Cloud"]
		chosen_prepared = []
		for rec in recommended:
			found = next((s for s in leveled_pool if s.name == rec), None)
			if found and found not in chosen_prepared:
				chosen_prepared.append(found)
		# Fill remaining randomly
		remaining = [s for s in leveled_pool if s not in chosen_prepared]
		remaining = _shuffled_by_character(
			trickster.character,
			remaining,
			)
		chosen_prepared += remaining[:max(0, n_prepared - len(chosen_prepared))]
		trickster.spells_known += chosen_prepared[:n_prepared]


	def modifier(trickster):
		int_val = getattr(trickster.character.AS, "INT", 10)
		return (int_val - 10) // 2

	def html(trickster):
		return str(trickster)

	def __str__(trickster):
		ordered_spells = sorted(trickster.spells_known, key=lambda s: int(s.level))
		spells_names = "".join(f"<li>〖{spell.level}〗{spell.name}</li>" for spell in ordered_spells)
		spells_html = "".join(f"""<div class="spell">{spell:html}</div>""" for spell in ordered_spells)
		slots = trickster.get_stats("slots")
		slots_html = "<br>".join(f"<b>Level {lvl}</b>: <i>{num}</i> " for lvl, num in slots.items() if num > 0)
		return f"""
			<div class="npc-textbox--full">
				<h1 style="font-family: {title_font('Arcane Trickster')}; font-size:    3.1em;">Arcane Trickster Spellcasting</h1>
				<p> As an Arcane Trickster, you've learned to weave subtle magic with your rogue's cunning. Your spells come from the Wizard list, cast using Intelligence. <br> You always know <b>Mage Hand</b>, and can select other cantrips and spells from the Wizard list. </p>
				</div>
			<div class="npc-textbox" style="grid-column: span 1;">
				<h2>Spell Slots:</h2> {slots_html} <br>  You regain all expended slots when you finish a Long Rest.
				<ul style="list-style-type: '🎩'; text-align: left; font-family: var(--font-script);">{spells_names}</ul>
				<h2>Arcane Focus</h2>
				You can use an Arcane Focus (such as a wand or scepter), as a Spellcasting Focus for your Wizard spells.
				</div>
			<div class="npc-textbox" style="margin-bottom: 1em;">
				<h2>Spell Save DC:</h2> {trickster.spell_save_dc()}<br>
				</div>
			<div class="npc-textbox" style="margin-bottom: 1em;">
				<h2 style="font-size:    1.35em;">Spell Attack Bonus:</h2> +{trickster.spell_attack_bonus()}
				</div>
			{spells_html}
			"""


# Warlock spellcasting progression for 2024 PHB
# What a pact can be cast with, and what the pact-holder is called for it.
# Charisma talked something into a deal, Intelligence found the deal written
# down, Wisdom noticed the deal was already being offered.  See
# Documenta/Canon for why each is a corruption of a different caster.
#
# The Occultist and the Covenantor are Tags now, declared in WarlockKit as
# Casting Variants over the Warlock Guild, and each crunches the Guild's own
# ``Casting_Ability``.  This table is kept because it reads as the design note
# it is, and because a caller that wants the three names together should not
# have to walk the Pin Field for them.
WARLOCK_ABILITIES = {
	"CHA": "Warlock",
	"INT": "Occultist",
	"WIS": "Covenantor",
	}


def warlock_casting_ability(
		character,
		) -> str:
	"""
	Which of Charisma, Intelligence or Wisdom this pact answers to.

	Settled by whichever Casting Variant the Character carries, or by the Guild
	itself for the ninety in a hundred that answer to Charisma.  Kept as a name
	because the Invocation ability gates read well through it, but it decides
	nothing: it asks.
	"""
	from AtlasLusoris.GuildKit import casting_ability

	return casting_ability( character ) or "CHA"


def warlock_title(
		character,
		) -> str:
	"""``Occultist (Warlock)`` on the sheet, or plain ``Warlock`` for Charisma."""
	from AtlasLusoris.GuildKit import casting_title

	return casting_title( character ) or "Warlock"


WARLOCK_SPELLCASTING_TABLE = {
		1:  {"cantrips": 2, "prepared": 2,  "slots": (1,),   "slot_level": 1},
		2:  {"cantrips": 2, "prepared": 3,  "slots": (2,),   "slot_level": 1},
		3:  {"cantrips": 2, "prepared": 4,  "slots": (2,),   "slot_level": 2},
		4:  {"cantrips": 3, "prepared": 5,  "slots": (2,),   "slot_level": 2},
		5:  {"cantrips": 3, "prepared": 6,  "slots": (2,),   "slot_level": 3},
		6:  {"cantrips": 3, "prepared": 7,  "slots": (2,),   "slot_level": 3},
		7:  {"cantrips": 3, "prepared": 8,  "slots": (2,),   "slot_level": 4},
		8:  {"cantrips": 3, "prepared": 9,  "slots": (2,),   "slot_level": 4},
		9:  {"cantrips": 3, "prepared": 10, "slots": (2,),   "slot_level": 5},
		10: {"cantrips": 4, "prepared": 10, "slots": (2,),   "slot_level": 5},
		11: {"cantrips": 4, "prepared": 11, "slots": (3,),   "slot_level": 5},
		12: {"cantrips": 4, "prepared": 11, "slots": (3,),   "slot_level": 5},
		13: {"cantrips": 4, "prepared": 12, "slots": (3,),   "slot_level": 5},
		14: {"cantrips": 4, "prepared": 12, "slots": (3,),   "slot_level": 5},
		15: {"cantrips": 4, "prepared": 13, "slots": (3,),   "slot_level": 5},
		16: {"cantrips": 4, "prepared": 13, "slots": (3,),   "slot_level": 5},
		17: {"cantrips": 4, "prepared": 14, "slots": (4,),   "slot_level": 5},
		18: {"cantrips": 4, "prepared": 14, "slots": (4,),   "slot_level": 5},
		19: {"cantrips": 4, "prepared": 15, "slots": (4,),   "slot_level": 5},
		20: {"cantrips": 4, "prepared": 15, "slots": (4,),   "slot_level": 5},
		}

class Warlock(Spellcaster):
	def __init__(caster, character,known=None):
		if known is None:     known = []
		caster.class_name     = "Warlock"
		caster.character     = character
		caster.level         = character.level
		caster.spell_slots     = caster.get_spell_slots()
		caster.spells_available = caster.available_spells()
		caster.spells_known = known
		caster.casting_stat = caster.get_casting_stat()
		caster.prepare_spells()
		# Optionally track invocations, pact, arcanum

	def get_casting_stat(caster):
		return warlock_casting_ability( caster.character )

	def get_stats(caster, key):
		lvl = min(caster.level, 20)
		value = WARLOCK_SPELLCASTING_TABLE.get(lvl, WARLOCK_SPELLCASTING_TABLE[20])
		if key == "cantrips":
			return value["cantrips"]
		if key == "prepared":
			return value["prepared"]
		if key == "slots":
			# Unlike wizards, Warlocks only ever have one slot level at a time
			return {value["slot_level"]: value["slots"][0]}
		if key == "slot_level":
			return value["slot_level"]

	def get_spell_slots(caster):
		return caster.get_stats("slots")

	def available_spells(caster):
		"""Returns all spells this character can *prepare* at their current level."""
		table = _expanded_spell_table(
				caster.character,
				SPELL_LISTS.get(
						caster.character.char_class,
						{},
						),
				)
		max_slot = caster.get_stats("slot_level")
		# Only show spells up to max_slot (warlock can never prepare 6+)
		unlocked = [lvl for lvl in table if lvl <= max_slot]
		spells = [s for lvl in unlocked for s in table[lvl]]
		return spells

	def prepare_spells(caster):
		# 1) Pact‐spells
		n = caster.get_stats("prepared")
		# Warlocks can change prepared spells on level-up/long rest
		available = caster.available_spells()
		# Random for demo; in-app, let user select!
		chosen = _pick_distinct(
			caster.character,
			available,
			min(
				n,
				len(
					available
					),
				),
			)

		# 2) Cantrips
		cantrip_pool = [s for s in available if int(s.level) == 0]
		cantrips = _pick_distinct(
			caster.character,
			cantrip_pool,
			min(
				len(
					cantrip_pool
					),
				caster.get_stats(
					"cantrips"
					),
				),
			)

		caster.spells_known = cantrips + [s for s in chosen if int(s.level) > 0]
		if caster.character.subclass == "Celestial":
			if caster.level >= 3: caster.spells_known += [Aid, CureWounds,    GuidingBolt, LesserRestoration, Light, SacredFlame]
			if caster.level >= 5: caster.spells_known += [Daylight, Revivify]
			if caster.level >= 7: caster.spells_known += [GuardianFaith, WallofFire]
			if caster.level >= 9: caster.spells_known += [GreaterRestoration, SummonCelestial]
		if caster.character.subclass == "Fiend":
			if caster.level >= 3: caster.spells_known += [BurningHands,    Command,    ScorchingRay,    Suggestion]
			if caster.level >= 5: caster.spells_known += [Fireball, StinkingCloud]
			if caster.level >= 7: caster.spells_known += [FireShield, WallofFire]
			if caster.level >= 9: caster.spells_known += [Geas,    InsectPlague]
		if caster.character.subclass == "Great Old One":
			if caster.level >= 3: caster.spells_known += [DetectThoughts,    DissonantWhispers,    PhantasmalForce,    HideousLaughter]
			if caster.level >= 5: caster.spells_known += [Clairvoyance, HungerHadar]
			if caster.level >= 7: caster.spells_known += [Confusion,    SummonAberration]
			if caster.level >= 10: caster.spells_known += [Hex]
			if caster.level >= 9: caster.spells_known += [ModifyMemory,    Telekinesis]
		if caster.character.subclass == "Genie":
			if caster.level >= 1: caster.spells_known += [DetectEvilandGood]
			if caster.level >= 3: caster.spells_known += [PhantasmalForce]
			if caster.level >= 5: caster.spells_known += [CreateFoodWater]
			if caster.level >= 7: caster.spells_known += [PhantasmalKiller]
			if caster.level >= 9: caster.spells_known += [Creation]
			if caster.level >= 17: caster.spells_known += [Wish]
			dice_bag = caster.character.Dice_Bag(
				"Warlock.Genie.Patron",
				version="1",
				)
			patron = caster.character.Pick(
				[
					"Dao",
					"Djinni",
					"Efreeti",
					"Marid",
					],
				dice=dice_bag,
				)
			if patron == "Dao":
				if caster.level >= 1: caster.spells_known += [sanctuary]
				if caster.level >= 3: caster.spells_known += [SpikeGrowth]
				if caster.level >= 5: caster.spells_known += [MeldIntoStone]
				if caster.level >= 7: caster.spells_known += [StoneShape]
				if caster.level >= 9: caster.spells_known += [WallStone]
			if patron == "Djinni":
				if caster.level >= 1: caster.spells_known += [Thunderwave]
				if caster.level >= 3: caster.spells_known += [GustOfWind]
				if caster.level >= 5: caster.spells_known += [WindWall]
				if caster.level >= 7: caster.spells_known += [GreaterInvisibility]
				if caster.level >= 9: caster.spells_known += [Seeming]
			if patron == "Efreeti":
				if caster.level >= 1: caster.spells_known += [BurningHands]
				if caster.level >= 3: caster.spells_known += [ScorchingRay]
				if caster.level >= 5: caster.spells_known += [Fireball]
				if caster.level >= 7: caster.spells_known += [FireShield]
				if caster.level >= 9: caster.spells_known += [FlameStrike]
			if patron == "Marid":
				if caster.level >= 1: caster.spells_known += [FogCloud]
				if caster.level >= 3: caster.spells_known += [Blur]
				if caster.level >= 5: caster.spells_known += [SleetStorm]
				if caster.level >= 7: caster.spells_known += [ControlWater]
				if caster.level >= 9: caster.spells_known += [ConeofCold]
		if caster.character.subclass == "Archfey":
			if caster.level >= 3: caster.spells_known += [CalmEmotions, FaerieFire, MistyStep, PhantasmalForce, Sleep]
			if caster.level >= 5: caster.spells_known += [Blink, PlantGrowth]
			if caster.level >= 7: caster.spells_known += [DominateBeast, GreaterInvisibility]
			if caster.level >= 9: caster.spells_known += [DominatePerson,    Seeming]
		if caster.level >= 9: caster.spells_known += [ContactOtherPlane]


		# 3) Mystic Arcanum — one per slot-level at these thresholds:
		caster.mystic_arcanum = []
		arcanum_requirements = {6: 11, 7: 13, 8: 15, 9: 17}
		warlock_table = SPELL_LISTS.get(caster.character.char_class, {})
		for lvl, req_level in arcanum_requirements.items():
			if caster.level >= req_level:
				pool = warlock_table.get(lvl, [])
				if pool:
					caster.mystic_arcanum.append(
						caster.character.Pick(
							pool
							)
						)

	def modifier(caster):
		# CHA-based, so use character abilities
		return (getattr(caster.character.AS, caster.casting_stat) - 10) // 2

	def html(caster):
		# simply delegate to __str__, which you’ve already written
		return str(caster)

	def __str__(caster):
		cantrips = [s for s in caster.spells_known if int(s.level) == 0]
		leveled = [s for s in caster.spells_known if int(s.level) > 0]
		n_prep = caster.get_stats("prepared")
		arcanums   = getattr(caster, "mystic_arcanum", [])

		spell_list = "".join(f"<li>【{s.level}】{s.name}</li>" for s in cantrips + leveled)
		spells_html = "".join(f"""<div class="spell">{s:html}</div>""" for s in cantrips + leveled)

		slots = caster.get_stats("slots")
		slot_level = caster.get_stats("slot_level")
		symb = "⚀"
		if slot_level == 2: symb = "⚁"
		if slot_level == 3: symb = "⚂"
		if slot_level == 4: symb = "⚃"
		if slot_level == 5: symb = "⛥"
		slot_str = f"""
			<h3>{slots[slot_level]} × Level {slot_level} Spell Slot(s)</h3>
			<br><h2 style="font-family: var(--font-script); font-size: 2.1em;">"""
		for j in range(slots[slot_level]):
			slot_str += f" {symb} "
		slot_str += "</h2>"

		if arcanums:
			lis = "".join(f"<li>【{s.level}】{s.name}</li>" for s in arcanums)
			arcanum = f"""
				<div class="npc-textbox" style="grid-column: span 1;">
					<h2 style="font-family: var(--font-script); font-size: 2.1em;">Mystic Arcanum</h2>
					<p>You know these special once‐per‐rest spells:</p>
					<ul style="list-style-type: '🀄'; text-align: left; font-family: var(--font-script)">
						{lis}
						</ul>
					<p><i>Each arcanum can be cast once per <i>Long Rest</i> without spending a slot.</i></p>
					</div>
				<div class="npc-textbox" style="grid-column: span 1;">
					<h1 style="font-family: var(--font-script);"">Spellcasting Focus.</h1>
					You can use an Arcane Focus (a wand, a cristal ball, or
					scepter are exmples or Foci) as a <i>Spellcasting Focus</i>
					for your Warlock spells.
					</div>
					"""
		else:
			arcanum = ""

		return f"""
		<div class="npc-textbox--full">
			<h1 style="font-family: {title_font('Warlock')}; font-size: 3.1em;">Warlock Pact Magic</h1>
			<p>As a warlock, your pact grants you spellcasting drawn from a supernatural patron. Pact Magic uses <b>Charisma</b> and works differently from other spellcasters.</p>
		</div>
		<div class="npc-textbox" style="grid-column: span 1;">
			<h2 style="font-family: var(--font-script); font-size: 2.1em;">Pact Magic Slots:</h2>
			{slot_str}
			<br><b>All slots are cast at highest slot level.<br>
			You regain all slots on a Short or Long Rest.</b>
		</div>
		<div class="npc-textbox" style="grid-column: span 1;">
			<h3 style="font-family: var(--font-script); font-size: 2.1em;">Prepared Spells</h3>
			You know {n_prep} warlock spells.<br>
			<ul style="list-style-type: '🔮'; text-align: left; font-family: var(--font-script)">
				{spell_list}
			</ul>
			<h3 style="font-family: var(--font-script); font-size: 2.1em;">Cantrips</h3>
			You always know {caster.get_stats("cantrips")} cantrips from the warlock list.<br>
		</div>

		{arcanum}
		{spells_html}
		"""

class Bard(Spellcaster):
	CANTRIPS_KNOWN_BY_LEVEL = {
		1:  2,  2:  2,  3: 2,
		4:  3,  5:  3,	6: 3,  7: 3,  	8: 3,  	9: 3,
		10: 4,	11:	4, 12: 4, 13: 4, 	14:4, 	15:4,
		16: 4, 	17: 4, 18: 4, 19: 4, 	20:4
		}

	SPELLS_KNOWN_BY_LEVEL = {
		1:  4,  2:  5,  3:  6,  4:  7,  5:  8,
		6:  9,  7: 10,  8: 11,  9: 12, 10: 14,
		11:15, 12:15, 13:16, 14:18, 15:18,
		16:19, 17:19, 18:20, 19:20, 20:22
		}

	def __init__(caster, character):
		caster.cantrips_known: list[Spell] = []
		super().__init__(character, known=[])

	def get_casting_stat(caster):
		return "CHA"

	def modifier(self):
		return (getattr(self.character.AS, "CHA", 10) - 10) // 2

	def get_spell_slots(caster):
		Bard_table = {
			1: {1: 2},
			2: {1: 3},
			3: {1: 4, 2: 2},
			4: {1: 4, 2: 3},
			5: {1: 4, 2: 3, 3: 2},
			6: {1: 4, 2: 3, 3: 3},
			7: {1: 4, 2: 3, 3: 3, 4: 1},
			8: {1: 4, 2: 3, 3: 3, 4: 2},
			9: {1: 4, 2: 3, 3: 3, 4: 3, 5: 1},
			10: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2},
			11: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1},
			12: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1},
			13: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1},
			14: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1},
			15: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1, 8: 1},
			16: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1, 8: 1},
			17: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2, 6: 1, 7: 1, 8: 1, 9: 1},
			18: {1: 4, 2: 3, 3: 3, 4: 3, 5: 3, 6: 1, 7: 1, 8: 1, 9: 1},
			19: {1: 4, 2: 3, 3: 3, 4: 3, 5: 3, 6: 2, 7: 1, 8: 1, 9: 1},
			20: {1: 4, 2: 3, 3: 3, 4: 3, 5: 3, 6:2 , 7: 2, 8: 1, 9: 1},
			}
		return Bard_table.get(caster.level, {})

	def get_casting_stat(caster):
		return "CHA"

	def prepare_spells(self):
		level = self.level
		lvl = level
		n_cantrips  = Bard.CANTRIPS_KNOWN_BY_LEVEL[lvl]
		n_spells   	= Bard.SPELLS_KNOWN_BY_LEVEL[lvl]
		n_can = n_cantrips
		n_sp = n_spells

		# Magical Secrets from other classes
		bard_pool = _expanded_spell_table(
				self.character,
				SPELL_LISTS.get(
						"Bard",
						{},
						),
				)
		wiz_pool = 		SPELL_LISTS.get("Wizard", {})
		druid_pool = 	SPELL_LISTS.get("Druid", {})
		cleric_pool = 	SPELL_LISTS.get("Cleric", {})

		# 1. choose cantrips – always Bard list only
		bard_cantrips = bard_pool.get(
				0,
				[],
				)
		self.cantrips_known = _pick_distinct(
			self.character,
			bard_cantrips,
			min(
				n_can,
				len(
					bard_cantrips
					),
				),
			)

		# 2. baseline: up to level‑10 cap (14) must be Bard spells
		baseline_cap = Bard.SPELLS_KNOWN_BY_LEVEL[10]  # 14
		bard_spell_pool = [
				spell
				for level, bank in bard_pool.items()
				if level > 0
				for spell in bank
				]
		bard_needed = min(n_sp, baseline_cap)
		chosen_bard = _pick_distinct(
			self.character,
			bard_spell_pool,
			min(
				bard_needed,
				len(
					bard_spell_pool
					),
				),
			)

		# 3. any extra slots (lvl >10) ⇒ may draw from *any* list
		extra_needed = n_sp - len(chosen_bard)
		if extra_needed > 0:
			any_pool = {
				s.name: s for cls, tbl in SPELL_LISTS.items()  # dict → dedupe by name
				for lv, bank in tbl.items() if lv > 0 for s in bank
				}
			# remove dupes already chosen
			for s in chosen_bard:
				any_pool.pop(s.name, None)
			extra_choices = _pick_distinct(
				self.character,
				list(
					any_pool.values()
					),
				min(
					extra_needed,
					len(
						any_pool
						),
					),
				)
		else:
			extra_choices = []

		self.spells_known = chosen_bard + extra_choices


	def html(self):
		return str(self)
	def __str__(self):

		cantrips = [s for s in self.cantrips_known]
		spells   = sorted([s for s in self.spells_known if s.level > 0], key=lambda s: (s.level, s.name))

		# Output formatting
		can_li = "".join(f"<li>【0】{s.name}</li>" for s in self.cantrips_known)
		list_items = "".join(f"<li>【{s.level}】{s.name}</li>" for s in spells)
		blurbs = "".join(f"<div class='spell'>{s:html}</div>" for s in cantrips + spells)

		slots_html = "<br>".join(
			f"<b>Level {lvl}</b>: <i>{n}</i>"
			for lvl, n in self.spell_slots.items() if n
			)

		return f"""
		<div class="npc-textbox--full">
			<h1 style="font-family:{title_font('Bard')}; font-size:3.1em;">Bard Spellcasting</h1>
			<p>You draw on the magic of your bardic arts, casting spells using <b>Charisma</b> as your spellcasting ability.</p>
			<p>You can use a Musical Instrument as a Spellcasting Focus for your Bard spells.</p>
		</div>

		<div class="npc-textbox">
			<h2>Spell Slots</h2>{slots_html}
			<p>All slots refresh after a long rest.</p>
		</div>

		<div class="npc-textbox">
			<h2>Spell Save DC:</h2> {self.spell_save_dc()}<br>
			<h2>Spell Attack Bonus:</h2> +{self.spell_attack_bonus()}
		</div>
		<div class="npc-textbox" style="grid-column: span 1;">
			<h3 style="font-family:var(--font-script); font-size:2.5em;">Cantrips</h3>
			<ul style="list-style-type:'📜'; font-family:var(--font-script); text-align:left;">{can_li}</ul>
		</div>
		<div class="npc-textbox" style="grid-column: span 1;">
			<h3 style="font-family:var(--font-script); font-size:2.5em;">Known Spells</h3>
			<ul style="list-style-type:'🎼'; font-family:var(--font-script); text-align:left;">{list_items}</ul>
		</div>
		{blurbs}
		"""
	def a__str__(self):
		slots_html = "<br>".join(
			f"<b>Level {lvl}</b>: <i>{n}</i>" for lvl, n in self.spell_slots.items() if n
		)
		can_li = "".join(f"<li>【0】{s.name}</li>" for s in self.cantrips_known)
		spell_li = "".join(
			f"<li>【{s.level}】{s.name}</li>" for s in sorted(self.spells_known, key=lambda sp:(sp.level, sp.name))
		)
		blurbs = "".join(f"<div class='spell'>{s:html}</div>" for s in self.cantrips_known + self.spells_known)
		return f"""
		<div class='npc-textbox--full'>
			<h1 style='font-family:{title_font("Bard")}; font-size:3.1em;'>Bard Spellcasting</h1>
			<p>From 11th level onward, every new spell you learn can come from <i>any</i> class list thanks to Magical Secrets.</p>
			</div>
		<div class='npc-textbox'><h2>Spell Slots</h2>{slots_html}<br>All slots refresh after a long rest.</div>
		<div class='npc-textbox'><h2>Spell Save DC</h2> {self.spell_save_dc()}<br><h2>Spell Attack Bonus</h2> +{self.spell_attack_bonus()}</div>
		<div class='npc-textbox' style='grid-column: span 1;'>
			<h3 style='font-family:var(--font-script); font-size:2.3em;'>Cantrips Known</h3>
			<ul style='list-style-type:"♪";'>{can_li}</ul>
			<h3 style='font-family:var(--font-script); font-size:2.3em;'>Spells Known</h3>
			<ul style='list-style-type:"🎼";'>{spell_li}</ul>
			</div>
		{blurbs}"""


# Factory to get the appropriate class
def _bears(character, label):
	"""Does the character carry this class/subclass label?

	Checks the explicit fields first (char_class, subclass), then falls
	back to `label in character`. The fallback alone is no longer enough:
	a CharactersKit character is a TagKit Agent, and Tagged.__contains__
	shadows the old Character.__contains__ in the runtime MRO — its string
	probe only sees Tag labels (Player, …), so "Wizard" in character is
	False even for a wizard. Found live: every caster lost its spells.
	"""
	for attr in ("char_class", "subclass"):
		if str(getattr(character, attr, "") or "") == label:
			return True
	try:
		return label in character
	except Exception:
		return False


def _include_character_spells(
	caster,
	character,
	):
	if caster is None:
		return None

	known_names = {
		getattr(
			spell,
			"name",
			None,
			)
		for spell in getattr(
			caster,
			"spells_known",
			(),
			) or ()
		}

	for spell in getattr(
		character,
		"known_spells",
		(),
		) or ():
		if spell.name in known_names:
			continue

		caster.spells_known.append( spell )
		known_names.add(
			spell.name
			)

	return caster


def spellcaster(character):
	#-- subclass casters first: an Eldritch Knight is a Fighter by class,
	#-- a caster only by subclass — the specific label must win
	from AtlasLusoris.AtlasOfGuilds.FighterKit import (
		EldritchKnight as Eldritch_Knight_Tag,
		)

	if character in Eldritch_Knight_Tag:
		selected = EldritchKnight(character)
	elif _bears(character, "Arcane Trickster"):
		selected = ArcaneTrickster(character)
	elif _bears(character, "Wizard"):
		selected = Wizard(character)
	elif _bears(character, "Sorcerer"):
		selected = Sorcerer(character)
	elif _bears(character, "Monk"):
		selected = Monk(character)
	elif _bears(character, "Warlock"):
		selected = Warlock(character)
	elif _bears(character, "Ranger"):
		selected = Ranger(character)
	elif _bears(character, "Druid"):
		selected = Druid(character)
	elif _bears(character, "Cleric"):
		selected = Cleric(character)
	elif _bears(character, "Bard"):
		selected = Bard(character)
	elif _bears(character, "Paladin"):
		selected = Paladin(character)
	elif _bears(character, "Artificer"):
		selected = Artificer(character)
	elif (
		getattr(
			character,
			"known_spells",
			None,
			)
		and getattr(
			character,
			"species_spellcasting_ability",
			None,
			)
		):
		selected = SpeciesSpellcaster(
			character
			)
	else:
		selected = None

	return _include_character_spells(
		selected,
		character,
		)


class Artificer(Spellcaster):
	"""
	2024 Artificer half-caster (Intelligence).
	Prepared spells + cantrips from the Artificer list; Specialty spells
	are always prepared and do not count against the prepared limit.
	"""

	_TABLE = {
			# lvl: (cantrips, prepared, slots L1-L5)
			1:  (2, 2,  (2, 0, 0, 0, 0)),
			2:  (2, 3,  (2, 0, 0, 0, 0)),
			3:  (2, 4,  (3, 0, 0, 0, 0)),
			4:  (2, 5,  (3, 0, 0, 0, 0)),
			5:  (2, 6,  (4, 2, 0, 0, 0)),
			6:  (2, 6,  (4, 2, 0, 0, 0)),
			7:  (2, 7,  (4, 3, 0, 0, 0)),
			8:  (2, 7,  (4, 3, 0, 0, 0)),
			9:  (2, 9,  (4, 3, 2, 0, 0)),
			10: (3, 9,  (4, 3, 2, 0, 0)),
			11: (3, 10, (4, 3, 3, 0, 0)),
			12: (3, 10, (4, 3, 3, 0, 0)),
			13: (3, 11, (4, 3, 3, 1, 0)),
			14: (4, 11, (4, 3, 3, 1, 0)),
			15: (4, 12, (4, 3, 3, 2, 0)),
			16: (4, 12, (4, 3, 3, 2, 0)),
			17: (4, 14, (4, 3, 3, 3, 1)),
			18: (4, 14, (4, 3, 3, 3, 1)),
			19: (4, 15, (4, 3, 3, 3, 2)),
			20: (4, 15, (4, 3, 3, 3, 2)),
			}

	_SPECIALTY_SPELLS = {
			"Alchemist": {
					3: (HealingWord, RayofSickness),
					5: (FlamingSphere, AcidArrow),
					9: (MassHealingWord, StinkingCloud),
					},
			"Armorer": {
					3: (MagicMissile, Thunderwave),
					5: (MirrorImage, Shatter),
					9: (HypnoticPattern, LightningBolt),
					},
			"Artillerist": {
					3: (Shield, Thunderwave),
					5: (ScorchingRay, Shatter),
					9: (Fireball, WindWall),
					},
			"Battle Smith": {
					3: (Heroism, Shield),
					5: (BrandingSmite, WardingBond),
					9: (AuraofVitality, ConjureBarrage),
					},
			}

	def __init__(
			self,
			character,
			known: list | None = None,
			):
		super().__init__(
				character,
				known or [],
				)
		self.class_name = "Artificer"

	def get_casting_stat(
			self,
			):
		return "INT"

	def get_stats(
			self,
			key,
			):
		lvl = min(
				self.level,
				20,
				)
		cantrips, prepared, slots = Artificer._TABLE[lvl]
		if key == "cantrips":
			return cantrips
		if key == "prepared":
			return prepared
		if key == "slots":
			return {
					i + 1: n
					for i, n in enumerate(
							slots
							)
					if n
					}
		raise KeyError(
				key
				)

	def get_spell_slots(
			self,
			):
		return self.get_stats(
				"slots"
				)

	def available_spells(
			self,
			):
		table = _expanded_spell_table(
				self.character,
				SPELL_LISTS.get(
						"Artificer",
						{},
						),
				)
		max_level = max(
				self.get_stats(
						"slots"
						),
				default=0,
				)
		unlocked = [
				lvl
				for lvl in table
				if lvl == 0 or lvl <= max_level
				]
		return [
				spell
				for lvl in unlocked
				for spell in table[lvl]
				]

	def _specialty_spells(
			self,
			):
		ladder = Artificer._SPECIALTY_SPELLS.get(
				getattr(
						self.character,
						"subclass",
						None,
						),
				{},
				)
		granted = []
		for need, spells in ladder.items():
			if self.level >= need:
				granted.extend(
						spells
						)
		return granted

	def prepare_spells(
			self,
			):
		pool = self.available_spells()
		cantrip_pool = [
				spell
				for spell in pool
				if int(
						spell.level
						) == 0
				]
		leveled_pool = [
				spell
				for spell in pool
				if int(
						spell.level
						) > 0
				]
		specialty = self._specialty_spells()
		specialty_names = {
				spell.name
				for spell in specialty
				}
		leveled_pool = [
				spell
				for spell in leveled_pool
				if spell.name not in specialty_names
				]
		n_cantrips = self.get_stats(
				"cantrips"
				)
		n_prepared = self.get_stats(
				"prepared"
				)
		cantrips = _pick_distinct(
				self.character,
				cantrip_pool,
				min(
						n_cantrips,
						len(
								cantrip_pool
								),
						),
				)
		leveled_pool = _shuffled_by_character(
				self.character,
				leveled_pool,
				)
		prepared = leveled_pool[
				:n_prepared
				]
		self.spells_known = cantrips + specialty + prepared
		self.cantrips_known = cantrips

	def modifier(
			self,
			):
		return (
				getattr(
						self.character.AS,
						self.casting_stat,
						10,
						) - 10
				) // 2

	def html(
			self,
			):
		return str(
				self
				)

	def __str__(
			self,
			):
		n = self.get_stats(
				"prepared"
				)
		cantrips = [
				spell
				for spell in self.spells_known
				if int(
						spell.level
						) == 0
				]
		specialty = self._specialty_spells()
		specialty_names = {
				spell.name
				for spell in specialty
				}
		prepared = [
				spell
				for spell in self.spells_known
				if int(
						spell.level
						) > 0 and spell.name not in specialty_names
				]
		slots_html = "<br>".join(
				f"<b>Level {lvl}</b>: <i>{num}</i>"
				for lvl, num in self.spell_slots.items()
				if num
				)
		lis = "".join(
				f"<li>【{spell.level}】{spell.name}</li>"
				for spell in sorted(
						cantrips + specialty + prepared,
						key=lambda spell: (
								int(
										spell.level
										),
								spell.name,
								),
						)
				)
		blurbs = "".join(
				f'<div class="spell">{spell.html()}</div>'
				for spell in cantrips + specialty + prepared
				)
		return f"""
		<div class="npc-textbox--full">
			<h1 style="font-family: {title_font('Artificer')}; font-size: 3.1em;">Artificer Spellcasting</h1>
			<p>You channel magic through tools. Intelligence is your spellcasting ability.
			You prepare {n} Artificer spells of level 1+, plus any Specialty spells.</p>
		</div>
		<div class="npc-textbox">
			<h2>Spell Slots:</h2>
			{slots_html}
			<p>You regain all slots when you finish a Long Rest.</p>
		</div>
		<div class="npc-textbox">
			<h2>Spell Save DC:</h2> {self.spell_save_dc()}<br>
			<h2>Spell Attack Bonus:</h2> +{self.spell_attack_bonus()}
		</div>
		<div class="npc-textbox" style="grid-column: span 1;">
			<h3 style="font-family: var(--font-script); font-size: 3.1em;">Spell List</h3>
			<ul style="list-style-type: '⚙️'; font-family: var(--font-script); text-align: left;">
				{lis}
			</ul>
			<p><i>Tools Required.</i> You must have Thieves' Tools, Tinker's Tools,
			or Artisan's Tools in hand as a Spellcasting Focus.</p>
		</div>
		{blurbs}
		"""


class Paladin(Spellcaster):
	"""Half-caster using Charisma; prepares CHA mod + half level spells."""

	SLOT_TABLE = {
		1: {1: 2},
		2: {1: 2},
		3: {1: 3},
		4: {1: 3, 2: 1},
		5: {1: 4, 2: 2},
		6: {1: 4, 2: 2},
		7: {1: 4, 2: 3},
		8: {1: 4, 2: 3},
		9: {1: 4, 2: 3, 3: 2},
		10:{1: 4, 2: 3, 3: 2},
		11:{1: 4, 2: 3, 3: 3},
		12:{1: 4, 2: 3, 3: 3},
		13:{1: 4, 2: 3, 3: 3, 4: 1},
		14:{1: 4, 2: 3, 3: 3, 4: 1},
		15:{1: 4, 2: 3, 3: 3, 4: 2},
		16:{1: 4, 2: 3, 3: 3, 4: 2},
		17:{1: 4, 2: 3, 3: 3, 4: 3, 5: 1},
		18:{1: 4, 2: 3, 3: 3, 4: 3, 5: 1},
		19:{1: 4, 2: 3, 3: 3, 4: 3, 5: 2},
		20:{1: 4, 2: 3, 3: 3, 4: 3, 5: 2},
      	}

	PREPARED_SPELLS = {
		1: 2,   2: 3,   3: 4,   4: 5,   5: 6,
		6: 6,   7: 7,   8: 7,   9: 9,  10: 9,
		11: 10, 12: 10, 13: 11, 14: 11, 15: 12,
		16: 12, 17: 14, 18: 14, 19: 15, 20: 15,
		}

	def __init__(self, character, known: list[Spell] | None = None):
		super().__init__(character, known or [])

	def get_stats(self, key: str):
		lvl = min(self.level, 20)
		entry = {
			"prepared": Paladin.PREPARED_SPELLS[lvl],
			"slots": Paladin.SLOT_TABLE[lvl],
			"cantrips": 0,  # Paladins don't naturally get cantrips, but can get them from features
			}
		if key == "prepared":
			return entry["prepared"]
		if key == "slots":
			return entry["slots"]
		if key == "cantrips":
			return entry["cantrips"]
		raise KeyError(key)

	def get_casting_stat(self):
		return "CHA"

	def modifier(self):
		return (getattr(self.character.AS, "CHA", 10) - 10) // 2

	def get_spell_slots(self):
		return self.get_stats("slots")

	def prepare_spells(self):
		prepared = self.get_stats("prepared")
		max_slot = max(
				self.get_stats("slots"),
				default=0,
				)
		always_prepared = [
				spell
				for spell in list(
						getattr(
								self,
								"spells_known",
								[],
								) or []
						)
				if getattr(
						spell,
						"level",
						0,
						) == 0 or int(
						spell.level
						) <= max_slot
				]
		auto_names = {
				spell.name
				for spell in always_prepared
				}

		pool = [
				spell
				for lvl, bank in _expanded_spell_table(
						self.character,
						SPELL_LISTS.get(
								"Paladin",
								{},
								),
						).items()
				if 0 < lvl <= max_slot
				for spell in bank
				if spell.name not in auto_names
				]
		pool = _shuffled_by_character(
				self.character,
				pool,
				)

		# merge always-prepared with randomly prepared spells
		chosen = always_prepared + pool[
				:max(
						0,
						prepared - len(
								[
										spell
										for spell in always_prepared
										if int(
												spell.level
												) > 0
										]
								),
						)
				]
		self.spells_known = chosen

		# Handle cantrips from features (like Blessed Warrior)
		self.cantrips_known = [
				spell
				for spell in self.spells_known
				if int(
						spell.level
						) == 0
				]
		self.spells_known = [
				spell
				for spell in self.spells_known
				if int(
						spell.level
						) > 0
				]

	def __str__(self):
		return html(self)

	def html(self):
		prepared = self.get_stats("prepared")
		spells = sorted(
			[s for s in self.spells_known if s.level > 0],
			key=lambda s: (s.level, s.name)
			)
		cantrips = sorted(
			[s for s in getattr(self, 'cantrips_known', [])],
			key=lambda s: s.name
			)

		cantrip_items = "".join(f"<li>【0】{s.name}</li>" for s in cantrips)
		list_items = "".join(f"<li>【{s.level}】{s.name}</li>" for s in spells)
		slots_html = "<br>".join(
			f"<b>Level {lvl}</b>: <i>{num}</i>"
			for lvl, num in self.spell_slots.items() if num
			)
		cantrip_cards = "".join(f'<div class="spell">{spell:html}</div>' for spell in cantrips)
		spell_cards = "".join(f'<div class="spell">{spell:html}</div>' for spell in spells)

		return f"""
          <div class="npc-textbox--full" >
              <h1 style="font-family:{title_font('Paladin')}; font-size:3.1em;">Paladin Spellcasting</h1>
              <p>You prepare {prepared} Paladin spells each day. Charisma is your spellcasting
  ability, and you can use a holy symbol as your focus.</p>
          </div>
          {f'<div class="npc-textbox"><h2>Cantrips</h2><ul style="list-style-type:"✠"; text-align:left; font-family:var(--font-script);">{cantrip_items}</ul></div>' if cantrips else ''}
          <div class="npc-textbox">
              <h2>Spell Slots</h2>
              {slots_html}
              <p>You regain all slots after a Long Rest.</p>
          </div>
          <div class="npc-textbox">
              <h2>Prepared Spells</h2>
              <ul style="list-style-type:'✠'; text-align:left; font-family:var(--font-script);">
                  {list_items or "<li>No prepared Paladin spells</li>"}
              </ul>
          </div>
          {cantrip_cards}
          {spell_cards}
          """
