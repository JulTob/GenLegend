#!/usr/bin/env python3
"""Verify the public seeded Player replay contract.

This is intentionally a cross-module integration rite.  The public request
crosses the Player facade, legacy entropy quarantine, TagKit composition, and
sheet projection; no one module can prove that the resulting shared URL is a
faithful replay.

Run:

    .venv/bin/python scripts/verify_player_replay.py
"""

from __future__ import annotations

import contextlib
import difflib
import io
import json
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(
        __file__
        ).resolve().parent.parent
if str(
        PROJECT_ROOT
        ) not in sys.path:
    sys.path.insert(
            0,
            str(
                    PROJECT_ROOT
                    ),
            )


from AtlasActorLudi import Map_of_Character_Generation as player_generation
from AtlasActorLudi.SkillsKit import SKILLS


PLAYER_REQUEST = {
        "species": "Human",
        "guild": "Fighter",
        "specialization": "Battle Master",
        "background": "Soldier",
        "level": 1,
        "gender": "They",
        "seed": 42,
        }

_IDENTITY_FIELDS = (
        "name",
        "title",
        "Gender",
        "CreatureType",
        "Species",
        "Heritage",
        "Class",
        "Class_Title",
        "Subclass",
        "Specialization",
        "Background",
        "Level",
        "Seed",
        "Stats",
        "Alignment",
        "AC",
        "Health",
        "PB",
        "size",
        "passive_perception",
        "Speed",
        "HPD",
        "Story",
        )

_SAVING_THROW_ABILITIES = (
        "STR",
        "DEX",
        "CON",
        "INT",
        "WIS",
        "CHA",
        )


@contextlib.contextmanager
def quiet_generation() -> Iterator[None]:
    """Keep Minion trace output from obscuring an assertion failure."""
    with contextlib.redirect_stdout(
            io.StringIO()
            ), contextlib.redirect_stderr(
            io.StringIO()
            ):
        yield


def stable_value(
        value: Any,
        ) -> Any:
    """Project a sheet value to stable JSON-compatible data."""
    if value is None or isinstance(
            value,
            (
                    bool,
                    int,
                    float,
                    str,
                    ),
            ):
        return value

    if isinstance(
            value,
            dict,
            ):
        return {
                str(key): stable_value(
                        item
                        )
                for key, item in sorted(
                        value.items(),
                        key=lambda pair: str(
                                pair[0]
                                ),
                        )
                }

    if isinstance(
            value,
            (
                    list,
                    tuple,
                    ),
            ):
        return [
                stable_value(
                        item
                        )
                for item in value
                ]

    if isinstance(
            value,
            set,
            ):
        return sorted(
                stable_value(
                        item
                        )
                for item in value
                )

    return str(
            value
            )


def skill_projection(
        skills: Any,
        ) -> tuple[tuple[str, int, int], ...]:
    """Return every sheet Skill's name, rank, and calculated modifier."""
    projection = []

    for definition in SKILLS:
        skill = getattr(
                skills,
                definition.legacy_attribute,
                )
        projection.append(
                (
                        definition.key,
                        int(
                                skill.proficiency_level
                                ),
                        int(
                                skill.calculate_modifier()
                                ),
                        )
                )

    return tuple(
            projection
            )


def feature_projection(
        feature: Any,
        ) -> Any:
    """Project both legacy and current Feature entries semantically."""
    as_dict = getattr(
            feature,
            "to_dict",
            None,
            )
    if callable(
            as_dict
            ):
        return stable_value(
                as_dict()
                )

    return {
            "name": stable_value(
                    getattr(
                            feature,
                            "name",
                            "",
                            )
                    ),
            "description": stable_value(
                    getattr(
                            feature,
                            "description",
                            "",
                            )
                    ),
            }


def build_projection(
        character: Any,
        ) -> dict[str, Any]:
    """
    Project the Character's build: every Entry and Chip its Tags declare.

    Each is named by the Tag that declared it, so a moved or doubled
    declaration shows up as a difference, not only a changed text.
    """
    from AtlasActorLudi.Charts_of_Build import Find_Build

    build = Find_Build(
            character
            )
    return {
            "entries": [
                    {
                        "tag": built.tag.__name__,
                        "title": built.entry.title,
                        "flavor": built.entry.flavor,
                        "rules": built.entry.rules,
                        "section": built.entry.section.value,
                        "level": built.entry.level,
                        }
                    for built in build.entries
                    ],
            "chips": [
                    {
                        "tag": built.tag.__name__,
                        "symbol": built.chip.symbol,
                        "label": built.chip.label,
                        "value": stable_value(
                                built.chip.value
                                ),
                        }
                    for built in build.chips
                    ],
            }


def item_name(
        item: Any,
        ) -> str | None:
    """Return the sheet name of one carried or equipped Item."""
    if item is None:
        return None

    return str(
            getattr(
                    item,
                    "called",
                    getattr(
                            item,
                            "name",
                            item,
                            ),
                    )
            )


def loadout_projection(
        loadout: Any,
        ) -> dict[str, Any]:
    """Return Item identities and derived values visible on the sheet."""
    return {
            "wearing": item_name(
                    loadout.wearing
                    ),
            "offhand": item_name(
                    loadout.offhand
                    ),
            "melee": item_name(
                    loadout.melee
                    ),
            "ranged": item_name(
                    loadout.ranged
                    ),
            "bag": sorted(
                    item_name(
                            item
                            )
                    for item in loadout.bag
                    ),
            "purse": float(
                    loadout.purse
                    ),
            "armour_class": int(
                    loadout.armour_class
                    ),
            }


def player_sheet_projection(
        character: Any,
        ) -> dict[str, Any]:
    """Project all deterministic Player-sheet decisions for comparison."""
    data = character.to_dict()
    saving_throws = data["SavingThrow"]
    attack_rolls = data["AttackRolls"]

    return {
            "identity": {
                    key: stable_value(
                            data[key]
                            )
                    for key in _IDENTITY_FIELDS
                    },
            "skills": skill_projection(
                    data["Skills"]
                    ),
            "features": [
                    feature_projection(
                            feature
                            )
                    for feature in data["features"]
                    ],
            "build": build_projection(
                    character
                    ),
                #-- Ported Tags print from the build, not from features, so
                #-- the replay compares both (review of #97).
            "equipment": loadout_projection(
                    data["equipment"]
                    ),
            "saving_throws": {
                    "values": {
                            ability: int(
                                    getattr(
                                            saving_throws,
                                            ability,
                                            )
                                    )
                            for ability in _SAVING_THROW_ABILITIES
                            },
                    "proficiency": stable_value(
                            saving_throws.proficiency
                            ),
                    },
            "attack_rolls": {
                    ability: {
                            "base": int(
                                    getattr(
                                            attack_rolls,
                                            f"{ability}_base",
                                            )
                                    ),
                            "proficient": int(
                                    getattr(
                                            attack_rolls,
                                            f"{ability}_prof",
                                            )
                                    ),
                            }
                    for ability in _SAVING_THROW_ABILITIES
                    },
            "other_proficiencies": stable_value(
                    data["other_proficiencies"]
                    ),
            "practices": stable_value(
                    data["Practices"]
                    ),
            "weapon_masteries": stable_value(
                    getattr(
                            character,
                            "weapon_mastery_picks",
                            (),
                            )
                    ),
            "languages": stable_value(
                    data["Languages"]
                    ),
            }


def rendered_projection(
        projection: dict[str, Any],
        ) -> str:
    """Render a stable projection for an actionable assertion diff."""
    return json.dumps(
            projection,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
            )


def assert_same_projection(
        first: dict[str, Any],
        second: dict[str, Any],
        ) -> None:
    """Raise with a readable semantic diff when a replay diverges."""
    if first == second:
        return

    difference = "\n".join(
            difflib.unified_diff(
                    rendered_projection(
                            first
                            ).splitlines(),
                    rendered_projection(
                            second
                            ).splitlines(),
                    fromfile="first summon",
                    tofile="second summon",
                    lineterm="",
                    )
            )
    raise AssertionError(
            "A seeded Player request did not replay exactly:\n"
            f"{difference}"
            )


def summon_seeded_player(
        ) -> Any:
    """Build the fixed public request through the default public path."""
    with quiet_generation():
        return player_generation.summon_player(
                **PLAYER_REQUEST
                )


def assert_explicit_seed_is_not_retried(
        ) -> None:
    """Verify a public explicit seed reaches production exactly once."""
    original_attempt = player_generation._attempt_player
    attempted_seeds: list[int] = []

    def fail_once(
            **request: Any,
            ) -> None:
        attempted_seeds.append(
                request["seed"]
                )
        raise RuntimeError(
                "deliberate generation failure"
                )

    player_generation._attempt_player = fail_once

    try:
        with quiet_generation():
            try:
                player_generation.summon_player(
                        seed=314159
                        )
            except RuntimeError:
                pass
            else:
                raise AssertionError(
                        "A deliberate generation failure was hidden."
                        )
    finally:
        player_generation._attempt_player = original_attempt

    assert attempted_seeds == [314159], (
            "An explicit seed must be attempted once, without a hidden "
            f"replacement seed; got {attempted_seeds!r}."
            )


def main(
        ) -> None:
    """Run the public replay and entropy-isolation contracts."""
    assert_explicit_seed_is_not_retried()

    first_character = summon_seeded_player()
    second_character = summon_seeded_player()

    with quiet_generation():
        first = player_sheet_projection(
                first_character
                )
        second = player_sheet_projection(
                second_character
                )

    assert_same_projection(
            first,
            second,
            )

    print(
            "OK — seeded Player request replays exactly."
            )


if __name__ == "__main__":
    main()
