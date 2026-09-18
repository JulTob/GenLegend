# Current State of the TOP Migration

> Reviewed: 2026-08-31

**First publish (Decree 0004):** the public product is the Player Character
generator. NPC, NPC list, and DM chrome are parked behind
`PLAYER_ONLY_PUBLISH` in `app/publish_scope.py`. Live preview launches
`app.main:app` (`shiny_app.py` is a compatibility shim).

This ledger separates the approved model from the transitional code. The
destination is binding in `Canon/Project-Model.md`; this file records evidence,
remaining bridges, and the next safe cuts.

## Landed

### Shiny frontline

- `app.main:app` is the composition root.
- `app/` owns Shiny navigation, session state, pages, components, and assets.
- Flask routes and templates are retired from the supported path.
- NPC presentation renders resolved Chips and Entries.

### Character root

- `AtlasActorLudi/CharactersKit.py` provides the shared `Character` Target.
- `Player` and `NonPlayer` are mutually exclusive Role Tags.
- Public Player and NonPlayer summon Maps return Character-based results.

### Atlas boundaries

- NonPlayer-specific production is nested under
  `AtlasActorLudi/AtlasAlusoris/`.
- Shared Guild Tags live in `AtlasLusoris/GuildKit.py`.
- Shared Background Tags have one home:
  `AtlasLusoris/BackgroundKit.py`.
- Larger official catalogues are divided into source-specific Maps beneath
  `AtlasLusoris/AtlasOfBackgrounds/`; they register through `BackgroundKit`
  and do not create parallel registries.
- There is no Alusoris Background Kit.

### Current identity migration

- Guild and Background are independent axes.
- The old 42-value Archetype input is classified by exact name for legacy
  requests.
- The Profile axis and `ProfileKit` have been retired.
- Sixty-one full Backgrounds are shared by Player and NonPlayer: the sixteen
  core 2024 records and forty-five later official records.
- Twenty-six full Backgrounds are NonPlayer-only, including `Doctor`.
- `PC_Background` and `NPC_Background` MetaTOP Tags classify first-class
  Background declarations.
- Player, NonPlayer, shared, and NonPlayer-only registries are live read-only
  views derived from those Tag Fields.
- Every Background Tag owns Reports for its ability choices, skill training,
  tool, Origin Feature, available Feature identities, title, description,
  source metadata, and role contract.
- `Build_Background(...)` is the one extension point for project and homebrew
  Backgrounds; no parallel eligibility or ability lookup needs updating.
- The later official catalogue covers Eberron, Forgotten Realms, Astarion,
  Lorwyn, Ravenloft, and the complete Arcana Unleashed Play-Along preview
  Background available as of 2026-07-23.
- Thirty-one book-specific Origin Feature identities are source-aware Tags
  marked `catalogued`; their detailed mechanics are not represented as
  complete.
- Former Profiles now awaken ordinary Background Tags from
  `AtlasLusoris/BackgroundKit.py`.
- Generated Characters do not store `profile`, `archetype`, or
  `legacy_archetype`.
- Current Shiny forms and URLs expose Race, Guild, and Background only.
- Creature Type is recorded separately from generator Race/Species labels.

### Features

- NonPlayer tactical Features use typed immutable specifications.
- Selected grants are persisted once.
- A grant can provide an Entry and optional Chips.
- Selection reads canonical Tags and structured spell metadata.
- The starter catalogue is project-original and provenance-aware.

### Determinism

- NPC tactical selection uses a Character-derived named stream.
- Player and NonPlayer public generation are isolated from concurrent legacy
  RNG interference.
- Transitional sheet sections resolve once through a deterministic projection
  adapter.
- The legacy bridge restores both RNG modules after success and failure.

### Gear and equipment (2026-08-01)

- `AtlasInventarium` is the gear home, split by axis: `ItemKit` (the `Item` domain
  object and its Tag family), `Ledger_of_Weapons` / `_Armors` / `_Tools` / `_Gear` /
  `_Wonders` (records), `Map_of_Gear_Proficiency` (training → what may be used),
  `Map_of_Materials` and `Map_of_Gear_Titles` (flavour from Tags), `Grimoire_of_Crafts`
  (affixes as Tags), and `GearKit` (loadout policy).
- `Equipped` is a Tag, not a slot pointer, so an impossible loadout is a question that
  can be asked and repaired rather than a slot silently overwritten.
- Artifact bonuses are summed at read time; AC is derived, never stored, so natural
  defences (Unarmored Defence) are never overwritten.
- Player generation runs `Outfit_Player` once, before Guild training, so Weapon Mastery
  names weapons the Character actually carries.
- Each module carries its own `__main__` self-test; `GearKit.__main__` also sweeps
  12 guilds × 5 levels for the equipment invariants.
- `Grimoire_of_Objects` (legacy `Inventory`, `GenerateEquipment`) was deleted on
  2026-09-16 (QST-0046); `GearKit` is the only equipment path.
- NPCs remain on their own gear path by explicit decision.

### Gear and equipment (2026-08-01)

- `AtlasInventarium` is the gear home, split by axis: `ItemKit` (the `Item` domain
  object and its Tag family), `Ledger_of_Weapons` / `_Armors` / `_Tools` / `_Gear` /
  `_Wonders` (records), `Map_of_Gear_Proficiency` (training → what may be used),
  `Map_of_Materials` and `Map_of_Gear_Titles` (flavour from Tags), `Grimoire_of_Crafts`
  (affixes as Tags), and `GearKit` (loadout policy).
- `Equipped` is a Tag, not a slot pointer, so an impossible loadout is a question that
  can be asked and repaired rather than a slot silently overwritten.
- Artifact bonuses are summed at read time; AC is derived, never stored, so natural
  defences (Unarmored Defence) are never overwritten.
- Player generation runs `Outfit_Player` once, before Guild training, so Weapon Mastery
  names weapons the Character actually carries.
- Each module carries its own `__main__` self-test; `GearKit.__main__` also sweeps
  12 guilds × 5 levels for the equipment invariants.
- `Grimoire_of_Objects` (legacy `Inventory`, `GenerateEquipment`) was deleted on
  2026-09-16 (QST-0046); `GearKit` is the only equipment path.
- NPCs remain on their own gear path by explicit decision.

## Approved destination not yet complete

Background-specific production should be routed outward. `Merchant`, for
example, may contribute a wares request that `AtlasInventarium` resolves.

### Universal Chip and Entry grants

The tactical NPC catalogue already proves the projection shape. Shared
`FeaturesKit` and all sheet renderers still need the same universal grant
contract.

The first reference slice is Fighter's Second Wind:

- Chip: `2nd Wind Uses`;
- Entry: feature title, explanation, action, recovery, and healing details.

### Character-owned named streams

The process-global RNG modules still exist in legacy Maps. The shared bridge
makes supported paths deterministic but serializes legacy work.

Each domain must move to a Character-owned named stream. Delete `app.random`
only after no supported Character path imports it.

### Decompose transitional Grimoires

`Grimoire_of_Characters` and `Grimoire_of_NPC` still contain mixed legacy
responsibilities. Peel one cohesive Map or Tag family at a time while keeping
the public summon APIs stable.

### Complete page separation

The Shiny boundary is correct, but remaining large page/server sections should
continue moving into small `app/pages/` modules. Production concepts must not
move with them.

## Compatibility policy

Supported old URLs and keyword arguments may remain readable during migration.
They translate immediately into current Guild or Background requests.

New URLs, serializers, tests, and production Maps do not create Archetype or
Profile records. `archetype=` and `profile=` remain accepted only as historic
keyword or URL adapters.

For the transitional six-segment NPC URL, the former Profile segment becomes
the one canonical Background. The former Background segment is returned only
as `legacy_background` parser metadata and is not applied as a second
Background.

## Verification currently available

- focused Actor Ludi identity and feature boundary suite;
- Player and NonPlayer URL suite;
- full package compilation;
- all canonical Guild, Background, Race, and legacy request generation;
- repeated and concurrent sheet-render determinism;
- Shiny import and startup smoke checks.

The former `Noble.ORIGIN_FEAT` overwrite warning was removed by declaring
Tag-level Background metadata through TagKit Reports rather than allowing a
Feature Tag class to be interpreted as a Character Action.
