"""Shared Shiny presentation helpers for character-shaped sheets."""

from __future__ import annotations

import re
from html import escape
from typing import Any

from AtlasVenustas import Chip

from shiny import ui


def safe_str(
        value: Any,
        fallback: str = "-",
        ) -> str:
    """Return a display string, replacing only ``None`` with the fallback."""
    if value is None:
        return fallback

    return str(value)


def safe_int(
        value: Any,
        fallback: int,
        ) -> int:
    """Return an integer display value or the supplied fallback."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def prose(
        text: Any,
        placeholder: str = "—",
        ) -> ui.Tag:
    """Render generator text as flowing Markdown prose."""
    body = safe_str(
            text,
            "",
            ).strip()

    if body:
        return ui.markdown(body)

    return ui.p(placeholder)


def html_prose(
        html: Any,
        placeholder: str = "—",
        ) -> ui.Tag:
    """Render trusted, code-authored HTML as flowing prose."""
    body = safe_str(
            html,
            "",
            ).strip()

    if body:
        return ui.HTML(body)

    return ui.p(placeholder)


def text_html(
        value: Any,
        placeholder: str = "-",
        ) -> ui.Tag:
    """Escape plain model text, then preserve its newlines as ``<br>``."""
    text = safe_str(
            value,
            placeholder,
            )

    return ui.HTML(
            escape(text).replace(
                    "\n",
                    "<br>",
                    )
            )


def attack_rolls_html(
        attack_rolls: Any,
        ) -> ui.Tag:
    """Render the ability, proficient, and base attack-roll table."""
    abilities = getattr(
            attack_rolls,
            "ABILITIES",
            (
                "STR",
                "DEX",
                "CON",
                "INT",
                "WIS",
                "CHA",
                ),
            )
    rows: list[Any] = []

    if attack_rolls is not None:
        for abbreviation in abilities:
            base = getattr(
                    attack_rolls,
                    f"{abbreviation}_base",
                    None,
                    )
            proficient = getattr(
                    attack_rolls,
                    f"{abbreviation}_prof",
                    None,
                    )

            if base is None or proficient is None:
                continue

            rows.append(
                    ui.tags.tr(
                            ui.tags.td(abbreviation),
                            ui.tags.td(
                                    {"class": "attack-roll-prof"},
                                    f"{proficient:+}⚜️",
                                    ),
                            ui.tags.td(
                                    {"class": "attack-roll-base"},
                                    f"{base:+}🔰",
                                    ),
                            )
                    )

    if rows:
        return ui.tags.table(
                {"class": "attack-rolls-table"},
                ui.tags.tbody(
                        *rows,
                        ),
                )

    value = (
        getattr(
                attack_rolls,
                "string",
                attack_rolls,
                )
        if attack_rolls is not None
        else ""
        )

    if callable(value):
        try:
            value = value()
        except Exception:
            value = ""

    return text_html(
            value,
            "-",
            )


def Feature_Chip_Triples(
        chips: Any,
        ) -> list[tuple[str, str, str]]:
    """
    Feature chips as ``(symbol, label, value)`` triples, for both sheets.

    Three shapes arrive here, each named:

    - a ``Chip`` (QST-0142: the one shape a Player feature declares);
    - the same three fields as a dictionary, after ``Feature.to_dict``;
    - an NPC ``Chip_Grant`` (label, value, icon), until the NonPlayer
      station of QST-0142 moves NonPlayer features to ``Chip`` too.

    Anything else is refused by name rather than skipped in silence.
    """
    from AtlasActorLudi.AtlasAlusoris.FeaturesKit import Chip_Grant

    if not chips:
        return []

    triples: list[tuple[str, str, str]] = []
    for item in chips:
        if isinstance(
                item,
                Chip,
                ):
            symbol, label, value = item.symbol, item.label, item.value
        elif isinstance(
                item,
                Chip_Grant,
                ):
            symbol, label, value = item.icon, item.label, item.value
        elif isinstance(
                item,
                dict,
                ):
            symbol = item.get(
                    "symbol",
                    "",
                    )
            label = item.get(
                    "label",
                    )
            value = item.get(
                    "value",
                    )
        else:
            raise TypeError(
                    f"{item!r} is not a Chip; write Chip( symbol, label, value )."
                    )
        if label is None or value is None:
            continue
        triples.append(
                (
                        safe_str(
                                symbol,
                                "",
                                ),
                        safe_str(
                                label
                                ),
                        safe_str(
                                value
                                ),
                        )
                )
    return triples


# A bolded run ending in a full stop is a sub-heading ("<b>Flurry of Blows.</b>",
# "<b>Level 3.</b>", "<b>Signature Magic.</b>"), and a feature that carries several
# of them runs them all into one block of text where nothing is separable.
# A bolded run WITHOUT the full stop is emphasis, not a heading: "<b>1d6</b>",
# "<b>4</b>", "<b>Charisma</b>". Across the whole catalogue that split is clean,
# which is why the break can be inserted here once instead of hand-editing every
# description in the ruleset.
_FEATURE_LABEL = re.compile(
        r"\s*(<b>[^<>]*?\.</b>)"
        )
_REPEATED_BREAK = re.compile(
        r"(?:<br\s*/?>\s*)+"
        )


def space_feature_labels(
        body: str,
        ) -> str:
    """Put each bolded sub-heading of a feature on its own line."""
    if "<b>" not in body:
        return body

    spaced = _FEATURE_LABEL.sub(
            r"<br>\1",
            body,
            )
    # Descriptions that already broke their own labels would otherwise gain a
    # second break, so collapse runs and drop one left at the very front.
    spaced = _REPEATED_BREAK.sub(
            "<br>",
            spaced,
            )

    return spaced.lstrip().removeprefix(
            "<br>"
            ).lstrip()


def feature_item(
        name: str,
        description: str,
        chips: Any = None,
        *,
        narrative: bool = False,
        ) -> ui.Tag:
    """Render one titled feature, optional chips, then Markdown description."""
    body = space_feature_labels(
            safe_str(
                    description,
                    "",
                    ).strip()
            )
    children: list[Any] = [
        ui.p(
                {"class": "feature-lead"},
                f"{safe_str(name)}.",
                ),
        ]

    chip_triples = Feature_Chip_Triples(
            chips
            )
    if chip_triples:
        children.append(
                ui.div(
                        {"class": "feature-chips"},
                        *[
                                ui.span(
                                        {"class": "feature-chip"},
                                        f"{symbol} " if symbol else "",
                                        ui.tags.strong(
                                                f"{label}"
                                                ),
                                        f" {value}",
                                        )
                                for symbol, label, value in chip_triples
                                ],
                        )
                )

    if body:
        children.append(
                ui.markdown(body)
                )

    return ui.div(
            {
                "class": (
                    "feature-entry is-narrative"
                    if narrative
                    else "feature-entry"
                    ),
                },
            *children,
            )


def sheet_branch(
        title: str,
        *content: Any,
        level: int = 2,
        ) -> ui.Tag:
    """One titled node in the character-sheet tree."""
    heading = {
        2: ui.h2,
        3: ui.h3,
        4: ui.h4,
        }.get(
                level,
                ui.h3,
                )

    return ui.div(
            {
                "class": (
                    f"sheet-branch sheet-branch--h{level}"
                    ),
                },
            heading(
                    title
                    ),
            ui.div(
                    {
                        "class": (
                            "sheet-branch-body prose-body"
                            )
                        },
                    *content,
                    ),
            )


def prose_section(
        title: str,
        *content: Any,
        level: int = 3,
        accent: bool = False,
        ) -> ui.Tag:
    """Render a titled section in a sheet's flowing main column."""
    heading = {
        1: ui.h1,
        2: ui.h2,
        3: ui.h3,
        }.get(
                level,
                ui.h3,
                )
    css_class = (
        "sheet-section is-fantasy"
        if accent
        else "sheet-section"
        )

    return ui.div(
            {"class": css_class},
            heading(title),
            ui.div(
                    {"class": "prose-body"},
                    *content,
                    ),
            )


def skill_rows(
        skills: Any,
        ) -> list[Any]:
    """Build ``<tr>`` rows for a skills table: mark, label, modifier.

    Shared by the Player and NonPlayer sheets so both render skills the same
    way (proficiency mark + skill name + modifier).
    """
    if not hasattr(
            skills,
            "list",
            ):
        return [
            ui.tags.tr(
                    ui.tags.td("⚪"),
                    ui.tags.td(
                            safe_str(skills)
                            ),
                    ui.tags.td(""),
                    ),
            ]

    try:
        rows: list[Any] = []

        for skill, label in skills.list:
            proficiency = getattr(
                    skill,
                    "proficiency_level",
                    0,
                    )
            mark = (
                "⭐️"
                if proficiency == 2
                else (
                    "⚫"
                    if proficiency == 1
                    else "⚪"
                    )
                )
            modifier = (
                skill.calculate_modifier()
                if hasattr(
                        skill,
                        "calculate_modifier",
                        )
                else ""
                )
            rows.append(
                    ui.tags.tr(
                            ui.tags.td(mark),
                            ui.tags.td(
                                    safe_str(label)
                                    ),
                            ui.tags.td(
                                    safe_str(modifier)
                                    ),
                            )
                    )

        return rows
    except Exception:
        return [
            ui.tags.tr(
                    ui.tags.td("⚪"),
                    ui.tags.td(
                            safe_str(skills)
                            ),
                    ui.tags.td(""),
                    ),
            ]


__all__ = [
    "attack_rolls_html",
    "feature_item",
    "html_prose",
    "prose",
    "prose_section",
    "safe_int",
    "safe_str",
    "sheet_branch",
    "skill_rows",
    "space_feature_labels",
    "text_html",
    ]
