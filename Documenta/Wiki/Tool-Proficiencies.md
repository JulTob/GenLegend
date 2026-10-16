# Tool Proficiencies

*Last updated: 2026-10-16*
*Status: **In-House Development** (GenLegend custom implementation on top of D&D 5e rules)
*Related Questa: QST-0116, QST-0116.1, QST-0116.2, QST-0116.3

---

## Overview

This document describes **GenLegend's Tool Proficiency system**, which extends D&D 5e rules with **custom in-house developments** for tool proficiencies, their mechanical effects, and their integration with the Character generation system.

### What is a Tool Proficiency?

In D&D 5e, **Tool Proficiencies** represent a character's training with specific equipment that grants mechanical benefits beyond simple usage. Unlike Skills (which are tied to abilities like Dexterity or Intelligence), Tool Proficiencies:

- Are **granted by Backgrounds, Guilds (Classes), or other features**
- Provide **specific actions** the character can perform with the tool
- Use the **character's Proficiency Bonus** when relevant checks are made
- May allow **Advantage** when combined with relevant Skill proficiencies
- Enable **Works of Wonder** — extraordinary creations possible with time, tools, and materials

### GenLegend's Implementation

GenLegend implements Tool Proficiencies as **Tag-Oriented Programming (TOP) entities** in the `AtlasInventarium.ToolsKit` module. Each Tool is defined as:

```python
@dataclass(frozen=True, slots=True)
class Tool_Definition(Capability_Definition):
    ability: str          # Governing ability (STR, DEX, INT, WIS, CHA, ANY)
    category: str        # Artisan, Kit, Gaming Set, Musical Instrument
    variant: str         # Optional variant identifier
    practice: Practice_Definition | None  # The proficiency rules
```

Each `Practice_Definition` contains:
- **title**: The proficiency name (e.g., "Alchemy Proficiency")
- **flavour**: Narrative description of the tool's essence
- **sections**: Tuple of `Practice_Section` objects, each with:
  - `title`: Section name (e.g., "Principles of Transformation")
  - `guidance`: Rules text for that section
- **subject_title**: Optional title for dynamic subject insertion

---

## Tool Categories

GenLegend organizes tools into **four primary categories**, each with distinct mechanical behavior:

### 1. Artisan's Tools (16 tools)

Artisan's Tools represent **crafting and trade proficiencies**. They are typically granted by **Backgrounds** and enable characters to create, modify, and appraise items related to their craft.

| Tool Name | Governing Ability | Key | Legacy Attribute |
|-----------|------------------|-----|------------------|
| Alchemist's Supplies | Intelligence | `Alchemist_Supplies` | `Alchemist_Supplies` |
| Brewer's Supplies | Intelligence | `Brewer_Supplies` | `Brewer_Supplies` |
| Calligrapher's Supplies | Dexterity | `Calligrapher_Supplies` | `Calligrapher_Supplies` |
| **Cartographer's Tools** | Wisdom | `Cartographer_Tools` | `Cartographer_Tools` |
| Cobbler's Tools | Dexterity | `Cobbler_Tools` | `Cobbler_Tools` |
| **Cook's Utensils** | Wisdom | `Cook_Utensils` | `Cook_Utensils` |
| Glassblower's Tools | Intelligence | `Glassblower_Tools` | `Glassblower_Tools` |
| Jeweler's Tools | Intelligence | `Jeweler_Tools` | `Jeweler_Tools` |
| Leatherworker's Tools | Dexterity | `Leatherworker_Tools` | `Leatherworker_Tools` |
| **Mason's Tools** | Strength | `Mason_Tools` | `Mason_Tools` |
| Painter's Supplies | Wisdom | `Painter_Supplies` | `Painter_Supplies` |
| Potter's Tools | Intelligence | `Potter_Tools` | `Potter_Tools` |
| **Smith's Tools** | Strength | `Smith_Tools` | `Smith_Tools` |
| Tinker's Tools | Dexterity | `Tinker_Tools` | `Tinker_Tools` |
| Weaver's Tools | Dexterity | `Weaver_Tools` | `Weaver_Tools` |
| **Woodworker's Tools** | Any | `Woodworker_Tools` | `Woodworker_Tools` |

**Note on Woodworker's Tools**: This is the **only Artisan's Tool** that uses `ANY` as its governing ability, meaning the character can use any ability score for checks involving this tool. This is a **GenLegend custom rule** that differs from standard D&D 5e (where Woodworker's Tools would typically use Strength or Dexterity).

#### Artisan's Tools Mechanical Benefits

All Artisan's Tools share a common structure with **three guidance sections**:

1. **Core Competency**: What the character can *do* with the tool (identify, create, modify, repair, etc.)
2. **Expertise**: What the character can *recognize* or *determine* (materials, workmanship, purpose, alterations, etc.)
3. **Works of Wonder**: Extraordinary creations possible with suitable tools, time, and materials (DM's discretion)

**Example: Alchemist's Supplies**
- **Flavour**: "Matter can change. Poison can become medicine, stone can flow, and fire can be tamed. By the law of equivalence, every transformation demands something in return. You have learned how to invite the change without becoming the price."
- **Principles of Transformation**: You can identify, separate, concentrate, preserve, neutralize, or combine substances and their properties. You usually recognize common materials, reactions, dangers, and potential uses.
- **Works of Wonder**: With suitable tools, time, and materials, you might prepare acids, alchemist's fire, oils, perfumes, pigments, paper, spell components, medicines, poisons, potions, or elixirs.

---

### 2. Kits (5 tools)

Kits are **specialized tool sets** that don't fit into the other categories. They often have unique mechanical effects.

| Tool Name | Governing Ability | Key | Legacy Attribute |
|-----------|------------------|-----|------------------|
| **Disguise Kit** | Charisma | `Disguise_Kit` | `Disguise_Kit` |
| **Forgery Kit** | Dexterity | `Forgery_Kit` | `Forgery_Kit` |
| **Herbalism Kit** | Intelligence | `Herbalism_Kit` | `Herbalism_Kit` |
| **Poisoner's Kit** | Intelligence | `Poisoners_Kit` | `Poisoners_Kit` |
| **Thieves' Tools** | Dexterity | `Thieves_Tools` | `Thieves_Tools` |

#### Kit Mechanical Benefits

Each Kit has **unique mechanical sections** tailored to its purpose:

**Disguise Kit**:
- **Play the Part**: Apply makeup, dress/dye hair, fit false features, alter silhouettes, create/adapt costumes
- **Works of Wonder**: Your work can let someone pass as a different profession, rank, age, origin, or plausible individual

**Forgery Kit**:
- **Borrowed Authority**: Imitate handwriting, reproduce seals, alter text, match inks and parchments
- **Works of Wonder**: Create convincing forgeries that can pass scrutiny

**Herbalism Kit**:
- **The Living Apothecary**: Identify, gather, cultivate, preserve, and prepare plants, fungi, roots, seeds, sap, pollen, and other organic materials
- **Works of Wonder**: Prepare antitoxins, salves, or other herbal remedies

**Poisoner's Kit**:
- **The Dose Makes the Poison**: Detect, identify, extract, preserve, combine, neutralize, or safely apply poisons, venoms, and toxins
- **Works of Wonder**: Prepare weapon coatings, poisoned food/drink, or other toxic substances

**Thieves' Tools**:
- **The Quiet Answer**: Pick locks, open manacles, disarm, bypass, reset, or safely spring traps
- **Read Before You Reach**: Finding a trap and disarming it are separate tasks; Perception may reveal something is wrong, Investigation may reveal the mechanism

---

### 3. Gaming Sets (4 tools)

Gaming Sets represent **games of chance and strategy**. All Gaming Sets share the **same Practice Definition** (Gambling Proficiency), but are treated as separate tools for inventory purposes.

| Tool Name | Governing Ability | Key | Legacy Attribute |
|-----------|------------------|-----|------------------|
| Dice Set | Wisdom | `Dice_Set` | `Gaming_Set` |
| Dragonchess Set | Wisdom | `Dragonchess_Set` | `Gaming_Set` |
| Playing Card Set | Wisdom | `Playing_Card_Set` | `Gaming_Set` |
| Three-Dragon Ante Set | Wisdom | `Three_Dragon_Ante_Set` | `Gaming_Set` |

#### Gaming Set Mechanical Benefits

All Gaming Sets use the **Gambling Proficiency** practice:

- **Flavour**: "Every game is a world in miniature. Pieces become armies, cards become fortunes, and dice become judgement. Across the table, people wager more than gold: pride, secrets, promises, and maps they should never have possessed. You have learned that the game begins before the first throw and rarely ends when the winnings are counted."

- **Read the Table**: With a Gaming Set you are trained to use, you can calculate odds, manage wagers, and recognize familiar forms of cheating.

- **One Match Per Rest**: You can play one match as part of a Long Rest, making only one roll to determine its final outcome. Before rolling, determine the Difficulty Class, wager, and possible prize with the DM. You may wager gold or items you own for a proportional reward.

  - Make a **Luck check** and add your Proficiency Bonus
  - On a **success**, you win the agreed prize
  - On a **failure**, you lose your wager
  - A **natural 20** may reveal an exceptional prize (possibly a Wondrous Item chosen by the DM, if available)

- **Advantage**: If another uncertainty requires a check, the DM chooses the Ability and Difficulty Class. A relevant Skill proficiency can grant Advantage.

---

### 4. Musical Instruments (10 tools)

Musical Instruments are **both tools and potential spellcasting focuses**. All Musical Instruments share the **same Practice Definition** (Musicianship Proficiency).

| Tool Name | Governing Ability | Key | Legacy Attribute | Variant |
|-----------|------------------|-----|------------------|---------|
| Bagpipes | Charisma | `Bagpipes` | `Musical_Instrument` | Bagpipes |
| Drum | Charisma | `Drum` | `Musical_Instrument` | Drum |
| Dulcimer | Charisma | `Dulcimer` | `Musical_Instrument` | Dulcimer |
| Flute | Charisma | `Flute` | `Musical_Instrument` | Flute |
| Horn | Charisma | `Horn` | `Musical_Instrument` | Horn |
| Lute | Charisma | `Lute` | `Musical_Instrument` | Lute |
| Lyre | Charisma | `Lyre` | `Musical_Instrument` | Lyre |
| Pan Flute | Charisma | `Pan_Flute` | `Musical_Instrument` | Pan Flute |
| Shawm | Charisma | `Shawm` | `Musical_Instrument` | Shawm |
| Viol | Charisma | `Viol` | `Musical_Instrument` | Viol |

#### Musical Instrument Mechanical Benefits

All Musical Instruments use the **Musicianship Proficiency** practice:

- **Flavour**: "A pipe may empty a city of vermin, a lyre may soften the rulers of death, a horn may call across worlds, and a flute may guide its bearer through fire. Fairy roads open to familiar tunes, armies remember the drum, and even monsters sometimes stop to listen. You have learned how to make the world lean closer."

- **Move the World**: You can perform known music, improvise, reproduce a melody after hearing it, maintain your instruments, and recognize musical traditions. You might use music to:
  - Attract a crowd
  - Signal across a distance
  - Conceal a message
  - Accompany a ritual
  - Guide a dance
  - Influence the mood of creatures willing to listen
  - *Note: Music cannot compel creatures without magic*

- **Music as Magic**: 
  - Any Musical Instrument you are trained to use can serve as a **Spellcasting Focus** for spells you cast
  - Playing it satisfies a spell's **Verbal component**, provided the music can be heard
  - An enchantment may ride upon a melody, an illusion rise from the strings, a summoned creature answer a horn, or thunder follow a drumbeat
  - This changes *how* the magic manifests, but not its other components or effects

- **Known Instruments**: The practice includes a dynamic "Known Instruments" section that lists the specific instruments the character is proficient with.

---

## Tool Proficiency Mechanics

### Granting Tool Proficiencies

Tool Proficiencies are granted through:

1. **Backgrounds**: Each Background grants 1-2 Tool Proficiencies (or equivalent)
2. **Guilds (Classes)**: Some Guilds grant Tool Proficiencies at specific levels
3. **Feats**: Certain Feats may grant additional Tool Proficiencies
4. **Species/Heritage**: Rare cases where a Species grants a Tool Proficiency

### Using Tool Proficiencies

When a character attempts an action that could be aided by a Tool Proficiency:

1. **Check if the character has the relevant Tool Proficiency**
   ```python
   from AtlasActorLudi.ProficiencyKit import Is_Trained
   from AtlasInventarium.ToolsKit import TOOLS_BY_KEY
   
   tool = TOOLS_BY_KEY.get("Alchemist_Supplies")
   if tool and Is_Trained(character, tool):
       # Character is proficient
   ```

2. **Determine the governing Ability**
   - Most tools use a specific ability (INT, DEX, WIS, CHA, STR)
   - Woodworker's Tools uses ANY (GenLegend custom rule)

3. **Apply Proficiency Bonus**
   - Add the character's Proficiency Bonus to ability checks made with the tool

4. **Check for Advantage**
   - If a relevant Skill proficiency supports the approach, the character has Advantage
   - Example: A character with Alchemist's Supplies and Medicine proficiency might have Advantage on a check to identify a poison

5. **Works of Wonder**
   - These are **narrative permissions** that allow extraordinary creations
   - Require: suitable tools, time, materials (as determined by the DM)
   - Examples: creating potions, forging masterwork items, composing epic music

### Sheet Integration

Tool Proficiencies appear on the Character Sheet in several ways:

1. **Tool Proficiencies List**: All proficiencies the character possesses
2. **Equipment**: Physical tool items the character carries
3. **Tool Attributes**: For legacy sheet compatibility, tools are organized by their `legacy_attribute`

The `Sheet_Tool_Attributes()` function in `ToolsKit.py` generates the list of tool attributes for the sheet:

```python
def Sheet_Tool_Attributes() -> tuple[tuple[str, str], ...]:
    """Each tool attribute of the old mutable sheet, once, with the name it prints."""
```

This ensures that:
- Each tool category (Musical Instrument, Gaming Set) appears as a single attribute
- Variants (specific instruments, specific gaming sets) are grouped under their category
- Legacy names are preserved for backward compatibility

### Aliases

To handle **legacy naming conventions** and **common aliases**, GenLegend maintains a mapping of alternate names to canonical tools:

```python
TOOLS_BY_KEY.update({
    "Carpenter_Tools": Woodworker_Tools,
    "Woodcarver_Tools": Woodworker_Tools,
    "Navigator_Tools": Cartographer_Tools,
})
```

This means:
- "Carpenter's Tools" → resolves to **Woodworker's Tools**
- "Woodcarver's Tools" → resolves to **Woodworker's Tools**
- "Navigator's Tools" → resolves to **Cartographer's Tools**

---

## Data Model

### Tool Definition Structure

```python
@dataclass(frozen=True, slots=True)
class Tool_Definition(Capability_Definition):
    key: str              # Unique identifier (e.g., "Alchemist_Supplies")
    name: str            # Display name (e.g., "Alchemist's Supplies")
    legacy_attribute: str # For backward compatibility (e.g., "Alchemist_Supplies")
    ability: str         # Governing ability (STR, DEX, INT, WIS, CHA, ANY)
    category: str        # Artisan, Kit, Gaming Set, Musical Instrument
    variant: str         # Optional variant identifier
    practice: Practice_Definition | None  # The proficiency rules
```

### Practice Definition Structure

```python
@dataclass(frozen=True, slots=True)
class Practice_Definition:
    title: str                    # Proficiency name
    flavour: str                  # Narrative description
    sections: tuple[Practice_Section, ...]  # Rules sections
    subject_title: str = ""      # Optional dynamic subject title

@dataclass(frozen=True, slots=True)
class Practice_Section:
    title: str                    # Section name
    guidance: str                 # Rules text
```

---

## Implementation Details

### Module Organization

| Module | Purpose |
|--------|---------|
| `AtlasInventarium.ToolsKit.py` | Core Tool definitions and Practice definitions |
| `AtlasInventarium.Ledger_of_Tools.py` | Physical item representations of tools (weight, cost) |
| `AtlasInventarium.Map_of_Gear_Proficiency.py` | Gear proficiency mapping and resolution |
| `AtlasInventarium.GearKit.py` | Equipment generation and tool assignment |

### Tool Creation Flow

1. **Define the Tool** in `ToolsKit.py`:
   ```python
   Alchemist_Supplies = _Tool(
       "Alchemist_Supplies",
       "Alchemist's Supplies",
       "INT",
       "Artisan",
       practice=_Practice(
           "Alchemy Proficiency",
           "Matter can change...",
           ("Principles of Transformation", "You can identify..."),
           ("Works of Wonder", "With suitable tools..."),
       ),
   )
   ```

2. **Register in Collections**:
   ```python
   ARTISAN_TOOLS: tuple[Tool_Definition, ...] = (
       Alchemist_Supplies,
       Brewer_Supplies,
       # ...
   )
   ```

3. **Create Physical Item** in `Ledger_of_Tools.py`:
   ```python
   _KITS: dict[str, tuple[float, float]] = {
       "Alchemist_Supplies": (8, 50),  # (weight_lb, cost_gp)
       # ...
   }
   ```

4. **Link Tool to Item**:
   ```python
   def _kit(tool: Tool_Definition) -> Item:
       weight, value = _KITS[tool.key]
       ability = _ABILITY_NAMES[tool.ability]
       item = Make_Item(
           name=tool.name,
           value=value,
           weight=weight,
           description=f"{tool.practice.flavour} (Ability: {ability}).",
       )
       item.ability = ability
       item.tool = tool
       return item
   ```

---

## Custom Developments (GenLegend-Specific)

### 1. Woodworker's Tools Uses ANY Ability

**Standard D&D 5e**: Woodworker's Tools would use either Strength (for heavy work) or Dexterity (for fine work).

**GenLegend Custom Rule**: Woodworker's Tools uses **ANY** ability, allowing the character to choose which ability to use based on the specific task:
- **Strength**: For heavy carpentry, construction, or forceful shaping
- **Dexterity**: For fine woodworking, detailed carving, or precision joinery
- **Intelligence**: For complex designs, planning, or understanding wood properties
- **Wisdom**: For intuitive understanding of wood grain, structural integrity
- **Constitution**: For endurance in prolonged woodworking
- **Charisma**: For artistic woodworking or persuading others of the quality

This provides **greater flexibility** and reflects that woodworking can encompass many different types of work.

### 2. Works of Wonder System

GenLegend's **Works of Wonder** system is a **narrative framework** that:

- **Standardizes** what characters can create with their tool proficiencies
- **Encourages** creative problem-solving and world-building
- **Provides** DMs with clear guidance on what's possible
- **Supports** the "downtime activities" system

Each Works of Wonder entry follows the pattern:
> "With suitable tools, time, and materials, as determined by your DM, you might create [examples]."

This **delegates final authority to the DM** while providing **concrete examples** of what's possible.

### 3. Dynamic Subject Insertion

Some Practices include a **`subject_title`** field that enables dynamic content:

```python
MUSICIANSHIP_PRACTICE = _Practice(
    "Musicianship Proficiency",
    "A pipe may empty a city...",
    # ... sections ...
    subject_title="Known Instruments",
)
```

When resolved for a character, this creates a **"Known Instruments"** section that lists the specific instruments the character is proficient with.

### 4. Legacy Attribute System

To maintain **backward compatibility** with existing character sheets and save files, GenLegend maintains:

- **`legacy_attribute`**: A standardized attribute name for each tool category
- **`Sheet_Tool_Attributes()`**: Generates the list of tool attributes for the sheet
- **`Sheet_Tool_Aliases()`**: Maps old/alternate names to current tools

This ensures that:
- Old character sheets can be loaded without breaking
- Tool proficiencies are displayed consistently
- Aliases (like "Carpenter's Tools" → "Woodworker's Tools") work seamlessly

---

## Known Issues and Questa References

| Questa | Issue | Status | Notes |
|--------|-------|--------|-------|
| QST-0116 | Tools have no single identity | Solved | Resolved by `TOOLS_BY_KEY` mapping |
| QST-0116.1 | Woodworker's tools missing from sheet | Solved | Fixed in `Ledger_of_Tools.py` |
| QST-0116.2 | Artisan tool list kept in three places | Solved | Consolidated in `ToolsKit.py` |
| QST-0116.3 | Instruments invisible to training check | Solved | Fixed in training validation |

### Current State

All identified issues have been **resolved**, but the system continues to evolve:

- **New tools** can be added by extending the `_Tool()` definitions
- **New practices** can be created for unique tool categories
- **Custom rules** (like ANY ability for Woodworker's Tools) can be added per-tool

---

## Testing and Validation

### Self-Test

The `ToolsKit.py` module includes a self-test that verifies:

```python
def _self_test():
    # Every tool has a unique name
    assert len(names) == len(set(names)), "duplicate tool names in the ledger"
    
    # Every ToolsKit tool has a corresponding kit
    assert set(_KITS) == {tool.key for tool in DEFINITIONS}, (
        "every ToolsKit tool needs one kit, and no kit may outlive its tool"
    )
    
    # Artisan tools count
    assert len(ARTISAN_TOOLS) == 16
    
    # Aliases work correctly
    assert TOOLS_BY_NAME["Carpenter's Tools"] is TOOLS_BY_NAME["Woodworker's Tools"]
    
    # Every tool has a governing ability
    for tool in TOOLS:
        assert tool.ability, f"{tool.name} has no governing ability"
```

Run with:
```bash
python3 -m AtlasInventarium.ToolsKit
```

### Validation Script

A dedicated validation script (`scripts/verify_equipment.py`) exists to verify:
- All tools have proper definitions
- All tools have associated physical items
- All tools have valid governing abilities
- No duplicate tool names exist

---

## Future Enhancements

### 1. Additional Tool Categories

Potential new categories to consider:
- **Vehicle Tools** (e.g., Saddle, Shipwright's Tools, Vehicle (Land/Water))
- **Alchemical Apparatus** (separate from Alchemist's Supplies)
- **Arcane Focus** (as a tool category)
- **Holy Symbol** (as a tool category)

### 2. Tool Quality System

Add a **quality tier** to tools:
- **Crude**: -2 to checks, may break
- **Standard**: No modifier
- **Masterwork**: +1 to checks
- **Magical**: +2 to checks, may have additional effects

### 3. Tool Specialization

Allow characters to **specialize** within a tool category:
- Example: A character with Smith's Tools could specialize in "Bladesmithing" or "Armorsmithing"
- Grants **Advantage** on checks related to the specialization
- Enables **more specific Works of Wonder**

### 4. Tool Mastery Feats

Create **Feats** that enhance tool usage:
- **Tool Mastery**: +1 to checks with a chosen tool, can grant Advantage in certain situations
- **Polyglot Artisan**: Gain proficiency with additional Artisan's Tools
- **Master Craftsman**: Create masterwork items without a DM's approval (within limits)

### 5. Downtime Activities Integration

Integrate with a **downtime activities system**:
- Characters can spend downtime **crafting** using their tool proficiencies
- Track **materials consumed** and **items created**
- Generate **random crafting results** (success, exceptional success, failure, catastrophe)

---

## References

### Code References

- [`AtlasInventarium.ToolsKit.py`](https://github.com/JulTob/GenLegend/blob/main/AtlasInventarium/ToolsKit.py) - Core tool definitions
- [`AtlasInventarium.Ledger_of_Tools.py`](https://github.com/JulTob/GenLegend/blob/main/AtlasInventarium/Ledger_of_Tools.py) - Physical tool items
- [`AtlasInventarium.GearKit.py`](https://github.com/JulTob/GenLegend/blob/main/AtlasInventarium/GearKit.py) - Equipment generation
- [`scripts/verify_equipment.py`](https://github.com/JulTob/GenLegend/blob/main/scripts/verify_equipment.py) - Validation script

### D&D 5e References

- Player's Handbook, Chapter 5: Equipment
- Player's Handbook, Chapter 4: Personality and Background (Tool Proficiencies)
- Xanathar's Guide to Everything: Additional Tool Proficiencies
- Tasha's Cauldron of Everything: Expanded tool rules

### GenLegend References

- [Wiki Home](https://github.com/JulTob/GenLegend/wiki)
- [Documenta/Questae](https://github.com/JulTob/GenLegend/tree/main/Documenta/Questae) - Issue tracking
- [STRATEGY.md](https://github.com/JulTob/GenLegend/blob/main/STRATEGY.md) - Project strategy

---

## Appendix: Complete Tool List

### Artisan's Tools (16)

| # | Name | Ability | Key |
|---|------|---------|-----|
| 1 | Alchemist's Supplies | INT | `Alchemist_Supplies` |
| 2 | Brewer's Supplies | INT | `Brewer_Supplies` |
| 3 | Calligrapher's Supplies | DEX | `Calligrapher_Supplies` |
| 4 | Cartographer's Tools | WIS | `Cartographer_Tools` |
| 5 | Cobbler's Tools | DEX | `Cobbler_Tools` |
| 6 | Cook's Utensils | WIS | `Cook_Utensils` |
| 7 | Glassblower's Tools | INT | `Glassblower_Tools` |
| 8 | Jeweler's Tools | INT | `Jeweler_Tools` |
| 9 | Leatherworker's Tools | DEX | `Leatherworker_Tools` |
| 10 | Mason's Tools | STR | `Mason_Tools` |
| 11 | Painter's Supplies | WIS | `Painter_Supplies` |
| 12 | Potter's Tools | INT | `Potter_Tools` |
| 13 | Smith's Tools | STR | `Smith_Tools` |
| 14 | Tinker's Tools | DEX | `Tinker_Tools` |
| 15 | Weaver's Tools | DEX | `Weaver_Tools` |
| 16 | Woodworker's Tools | ANY | `Woodworker_Tools` |

### Kits (5)

| # | Name | Ability | Key |
|---|------|---------|-----|
| 1 | Disguise Kit | CHA | `Disguise_Kit` |
| 2 | Forgery Kit | DEX | `Forgery_Kit` |
| 3 | Herbalism Kit | INT | `Herbalism_Kit` |
| 4 | Poisoner's Kit | INT | `Poisoners_Kit` |
| 5 | Thieves' Tools | DEX | `Thieves_Tools` |

### Gaming Sets (4)

| # | Name | Ability | Key |
|---|------|---------|-----|
| 1 | Dice Set | WIS | `Dice_Set` |
| 2 | Dragonchess Set | WIS | `Dragonchess_Set` |
| 3 | Playing Card Set | WIS | `Playing_Card_Set` |
| 4 | Three-Dragon Ante Set | WIS | `Three_Dragon_Ante_Set` |

### Musical Instruments (10)

| # | Name | Ability | Key |
|---|------|---------|-----|
| 1 | Bagpipes | CHA | `Bagpipes` |
| 2 | Drum | CHA | `Drum` |
| 3 | Dulcimer | CHA | `Dulcimer` |
| 4 | Flute | CHA | `Flute` |
| 5 | Horn | CHA | `Horn` |
| 6 | Lute | CHA | `Lute` |
| 7 | Lyre | CHA | `Lyre` |
| 8 | Pan Flute | CHA | `Pan_Flute` |
| 9 | Shawm | CHA | `Shawm` |
| 10 | Viol | CHA | `Viol` |

**Total: 35 Tools**

---

*This document is maintained as part of the GenLegend project. For questions or contributions, please refer to the [project repository](https://github.com/JulTob/GenLegend).*
