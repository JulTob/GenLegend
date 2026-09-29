"""Reusable Shiny rendering for spellcasting summaries and spell cards."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from typing import Any

from shiny import ui

from AtlasVenustas import Chip, ornament_for

from app.components.shared import safe_str


# The sheet spells abilities out; the caster objects speak in three-letter keys.
ABILITY_NAMES = {
    "STR": "Strength",
    "DEX": "Dexterity",
    "CON": "Constitution",
    "INT": "Intelligence",
    "WIS": "Wisdom",
    "CHA": "Charisma",
    }


# The sheet spells abilities out; the caster objects speak in three-letter keys.
ABILITY_NAMES = {
    "STR": "Strength",
    "DEX": "Dexterity",
    "CON": "Constitution",
    "INT": "Intelligence",
    "WIS": "Wisdom",
    "CHA": "Charisma",
    }


@dataclass(
        frozen=True,
        )
class _SpellcastingParameters:
    """One mechanically distinct spellcasting parameter set."""

    source: str
    ability: str
    save_dc: int


def _save_dc(
        character: Any,
        ability: str,
        ) -> int | None:
    scores = getattr(
            character,
            "AS",
            None,
            )

    if scores is None or not ability:
        return None

    try:
        score = int(
                getattr(
                        scores,
                        ability,
                        )
                )
        proficiency = int(
                getattr(
                        character,
                        "proficiency_bonus",
                        2,
                        )
                )
    except (AttributeError, TypeError, ValueError):
        return None

    return (
        8
        + proficiency
        + (
            score
            - 10
            ) // 2
        )


def _spellcasting_parameter_sets(
        caster: Any,
        ) -> tuple[_SpellcastingParameters, ...]:
    """Find unique parameter sets and retain the source of each difference."""
    character = getattr(
            caster,
            "character",
            None,
            )

    if character is None:
        return ()

    primary_ability = safe_str(
            getattr(
                    caster,
                    "casting_stat",
                    "",
                    ),
            "",
            ).upper()
    primary_dc = _save_dc(
            character,
            primary_ability,
            )
    primary_source = safe_str(
            getattr(
                    caster,
                    "class_name",
                    "Spellcasting",
                    ),
            "Spellcasting",
            ).strip()
    candidates: list[_SpellcastingParameters] = []

    if primary_ability and primary_dc is not None:
        candidates.append(
                _SpellcastingParameters(
                        primary_source,
                        primary_ability,
                        primary_dc,
                        )
                )

    species_ability = safe_str(
            getattr(
                    character,
                    "species_spellcasting_ability",
                    "",
                    ),
            "",
            ).upper()
    species_dc = _save_dc(
            character,
            species_ability,
            )

    if species_ability and species_dc is not None:
        heritage = safe_str(
                getattr(
                        character,
                        "heritage",
                        "",
                        ),
                "",
                ).replace(
                        "_",
                        " ",
                        ).strip()
        species = safe_str(
                getattr(
                        character,
                        "species",
                        "Species",
                        ),
                "Species",
                ).replace(
                        "_",
                        " ",
                        ).strip()
        species_source = f"{heritage or species} Lineage"
        candidates.append(
                _SpellcastingParameters(
                        species_source,
                        species_ability,
                        species_dc,
                        )
                )

    unique: list[_SpellcastingParameters] = []
    seen: set[tuple[str, int]] = set()

    for candidate in candidates:
        identity = (
            candidate.ability,
            candidate.save_dc,
            )

        if identity in seen:
            continue

        seen.add( identity )
        unique.append( candidate )

    return tuple( unique )


def _spell_slots_table_html(
        slots: Any,
        *,
        notes: list[str],
        ) -> str:
    """Compact level×count table for the Spell Slots rail chip."""
    rows: list[str] = []

    try:
        items = list(
                slots.items()
                )
    except Exception:
        return ""

    for level, number in items:
        if not number:
            continue
        rows.append(
                "<tr>"
                f"<td>Level {escape(str(level))}</td>"
                f'<td class="spell-slot-count">'
                f"{escape(str(number))}</td>"
                "</tr>"
                )

    if not rows:
        return ""

    note_html = "".join(
            f'<div class="spell-slots-note">{escape(note)}</div>'
            for note in notes
            if note
            )
    return (
        '<table class="spell-slots-table">'
        f"<tbody>{''.join(rows)}</tbody>"
        "</table>"
        f"{note_html}"
        )


def spellcasting_chips(
        caster: Any,
        ) -> list[Any]:
    """Return the ordered side-rail chips for one spellcaster."""
    chips: list[Any] = []

    def magic_chip(
            emoji: str,
            label: str,
            value: str,
            ) -> Chip:
        return Chip(
                emoji,
                label,
                value,
                kind="magic",
                )

    class_name = safe_str(
            getattr(
                    caster,
                    "class_name",
                    "",
                    ),
            "",
            ).strip()
    is_warlock = class_name == "Warlock"
    focus_points = getattr(
            caster,
            "focus_points",
            None,
            )
    is_monk = bool(
        focus_points is not None
        and int(focus_points or 0) > 0
        )

    slots = getattr(
            caster,
            "spell_slots",
            None,
            )

    if slots and not is_monk:
        try:
            if is_warlock:
                value = _spell_slots_table_html(
                        slots,
                        notes=[
                                "All slots at this level.",
                                "Regain on a short or long rest.",
                                ],
                        )
                if value:
                    chips.append(
                            magic_chip(
                                    "🪬",
                                    "Pact Magic Slots",
                                    value,
                                    )
                            )
            else:
                value = _spell_slots_table_html(
                        slots,
                        notes=[
                                "Regain all on a long rest.",
                                ],
                        )
                if value:
                    chips.append(
                            magic_chip(
                                    "✨",
                                    "Spell Slots",
                                    value,
                                    )
                            )
        except Exception:
            pass

    parameter_sets = (
        ()
        if is_monk
        else _spellcasting_parameter_sets(
                caster
                )
        )
    show_sources = len(parameter_sets) > 1

    for parameters in parameter_sets:
        prefix = (
            f"{parameters.source} "
            if show_sources
            else ""
            )
        chips.extend(
                (
                    magic_chip(
                            "🪄",
                            f"{prefix}Spellcasting Ability",
                            ABILITY_NAMES.get(
                                    parameters.ability,
                                    parameters.ability.capitalize(),
                                    ),
                            ),
                    magic_chip(
                            "🔮",
                            f"{prefix}Spell Save DC",
                            str(
                                    parameters.save_dc
                                    ),
                            ),
                    )
                )

    sorcery_points = getattr(
            caster,
            "sorcery_points",
            None,
            )

    if sorcery_points is not None:
        chips.append(
                magic_chip(
                        "💜",
                        "Sorcery Points",
                        str(sorcery_points),
                        )
                )

    if focus_points is not None and int(focus_points or 0) > 0:
        chips.append(
                magic_chip(
                        "☯",
                        "Focus Points",
                        (
                            f"{focus_points}\n"
                            "(Ki — regain on a short or long rest.)"
                            ),
                        )
                )

        if hasattr(
                caster,
                "focus_save_dc",
                ):
            try:
                chips.append(
                        magic_chip(
                                "🌀",
                                "Focus Save DC",
                                str(
                                        caster.focus_save_dc()
                                        ),
                                )
                        )
            except Exception:
                pass

    arcanums = getattr(
            caster,
            "mystic_arcanum",
            None,
            ) or []

    if arcanums:
        try:
            names = [
                (
                    f"L{getattr(spell, 'level', '?')}: "
                    f"{getattr(spell, 'name', spell)}"
                    )
                for spell in arcanums
                ]

            if names:
                chips.append(
                        magic_chip(
                                "🀄",
                                "Mystic Arcanum",
                                (
                                    "\n".join(names)
                                    + "\n(Once each per long rest.)"
                                    ),
                                )
                        )
        except Exception:
            pass

    return [
        ui.HTML(box)
        for box in chips
        ]


def _unique_spells(
        spells: Any,
        ) -> list[Any]:
    """Keep first occurrence of each spell name (feature grants win if first)."""
    unique: list[Any] = []
    seen: set[str] = set()

    for spell in spells or []:
        name = getattr(
                spell,
                "name",
                None,
                )
        if not name:
            unique.append(
                    spell
                    )
            continue
        key = str(
                name
                )
        if key in seen:
            continue
        seen.add(
                key
                )
        unique.append(
                spell
                )
    return unique


def known_spells_by_level(
        caster: Any,
        ) -> dict[int, list[str]]:
    """Group known or prepared spell names by spell level."""
    spells_known = _unique_spells(
            getattr(
                    caster,
                    "spells_known",
                    None,
                    ) or []
            )
    by_level: dict[int, list[str]] = {}

    try:
        ordered = sorted(
                spells_known,
                key=lambda spell: (
                    getattr(
                            spell,
                            "level",
                            0,
                            ),
                    getattr(
                            spell,
                            "name",
                            "",
                            ),
                    ),
                )

        for spell in ordered:
            name = getattr(
                    spell,
                    "name",
                    None,
                    )
            level = getattr(
                    spell,
                    "level",
                    0,
                    )

            if name:
                by_level.setdefault(
                        level,
                        [],
                        ).append(
                                str(name)
                                )
    except Exception:
        return {}

    return by_level


def known_spells_rail_box(
        caster: Any,
        ) -> Any | None:
    """Render the final side-rail list of known spell names."""
    by_level = known_spells_by_level(caster)

    if not by_level:
        return None

    title = (
        "Focus Techniques"
        if getattr(
                caster,
                "focus_points",
                None,
                )
        else "Known Spells"
        )
    sections: list[Any] = [
        ui.h2(title),
        ]

    for level, names in by_level.items():
        level_title = (
            "Cantrips"
            if level == 0
            else f"Level {level}"
            )
        sections.append(
                ui.h4(
                        level_title,
                        style=(
                            "margin-top: 0.8em; margin-bottom: 0.3em; "
                            "font-size: 0.85em; opacity: 0.7; "
                            "text-transform: uppercase; letter-spacing: 0.5px;"
                            ),
                        )
                )
        sections.append(
                ui.tags.ul(
                        *[
                            ui.tags.li(name)
                            for name in names
                            ],
                        )
                )

    return ui.div(
            {"class": "npc-textbox known-spells"},
            *sections,
            )


def _character_ornament(
        caster: Any,
        class_name: str,
        ) -> str:
    """One stable separator mark for this Character's spell list."""
    character = getattr(
            caster,
            "character",
            None,
            )
    guild = (
        safe_str(
                getattr(
                        character,
                        "char_class",
                        None,
                        ),
                "",
                ).strip()
        or class_name
        or None
        )
    species = safe_str(
            getattr(
                    character,
                    "species",
                    None,
                    ),
            "",
            ).strip() or None
    background = safe_str(
            getattr(
                    character,
                    "background",
                    None,
                    ),
            "",
            ).strip() or None
    seed = (
        getattr(
                character,
                "seed",
                None,
                )
        or getattr(
                character,
                "name",
                None,
                )
        or class_name
        or "spell"
        )
    return ornament_for(
            seed,
            guild=guild,
            species=species,
            background=background,
            )


def spellbook_html(
        caster: Any,
        ) -> str:
    """Render detailed spell cards; summary numbers remain in rail chips."""
    spells = _unique_spells(
            getattr(
                    caster,
                    "spells_known",
                    None,
                    ) or []
            )

    if not spells:
        return ""

    ordered = sorted(
            spells,
            key=lambda spell: (
                getattr(
                        spell,
                        "level",
                        0,
                        ),
                getattr(
                        spell,
                        "name",
                        "",
                        ),
                ),
            )
    parts: list[str] = []
    ability = safe_str(
            getattr(
                    caster,
                    "casting_stat",
                    "",
                    ),
            "",
            ).strip()
    class_name = safe_str(
            getattr(
                    caster,
                    "class_name",
                    "",
                    ),
            "",
            ).strip()
    separator = _character_ornament(
            caster,
            class_name,
            )

    if ability:
        class_phrase = (
            f" as a {escape(class_name)}"
            if class_name
            else ""
            )
        parts.append(
                (
                    "<p>You cast using "
                    f"<b>{escape(ability.capitalize())}</b>"
                    f"{class_phrase}.</p>"
                    )
                )

    last_index = len(
            ordered
            ) - 1

    for index, spell in enumerate(
            ordered
            ):
        try:
            card = f"{spell:html}"
        except Exception:
            try:
                card = spell.html()
            except Exception:
                spell_name = safe_str(
                        getattr(
                                spell,
                                "name",
                                "Spell",
                                )
                        )
                card = (
                    "<div class='spell'><b>"
                    f"{escape(spell_name)}"
                    "</b></div>"
                    )

        if ability and "⦔" in card:
            card = card.replace(
                    "⦔</i>",
                    (
                        "⦔</i><br><i>"
                        f"[{ability.capitalize()}]"
                        "</i>"
                        ),
                    1,
                    )

        parts.append(
                f'<div class="spell">{card}</div>'
                )

        if index < last_index:
            parts.append(
                    (
                        '<div class="spell-separator" aria-hidden="true">'
                        f"{escape(separator)}"
                        "</div>"
                        )
                    )

    return "\n".join(parts)


__all__ = [
    "known_spells_by_level",
    "known_spells_rail_box",
    "spellbook_html",
    "spellcasting_chips",
    ]


def _self_test() -> None:
    class Scores:
        INT = 16
        CHA = 14

    class Character:
        AS = Scores()
        proficiency_bonus = 3
        species = "Elf"
        heritage = "Dark_Elf"
        species_spellcasting_ability = "INT"

    class WizardCaster:
        character = Character()
        casting_stat = "INT"
        class_name = "Wizard"

    shared = _spellcasting_parameter_sets(
            WizardCaster()
            )
    assert shared == (
        _SpellcastingParameters(
                "Wizard",
                "INT",
                14,
                ),
        )

    WizardCaster.character.species_spellcasting_ability = "CHA"
    distinct = _spellcasting_parameter_sets(
            WizardCaster()
            )
    assert distinct == (
        _SpellcastingParameters(
                "Wizard",
                "INT",
                14,
                ),
        _SpellcastingParameters(
                "Dark Elf Lineage",
                "CHA",
                13,
                ),
        )

    print( "OK — spellcasting parameter self-test" )


if __name__ == "__main__":
    _self_test()
