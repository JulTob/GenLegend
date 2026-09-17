#!/usr/bin/env python3
"""Prove that a change moved code without moving any Character.

The standing gate of the recovery plan (QST-0132): a refactor meant to change
nothing must leave every generated Character identical, field by field.  Record
a fingerprint before the change, compare after it.  When a questa *intends* a
difference, it says so first, and the diff this prints is the evidence.

Run:

    .venv/bin/python scripts/verify_fingerprint.py --save /tmp/before.json
    # ...make the change...
    .venv/bin/python scripts/verify_fingerprint.py --check /tmp/before.json

The default grid is every Guild at levels 1 and 5, seeds 1 and 2 — 52
Characters, about a minute.  Widen it before closing a questa:

    FINGERPRINT_LEVELS=1,3,5,9,13,17,20 FINGERPRINT_SEEDS=1,2,3,4,5 \\
        .venv/bin/python scripts/verify_fingerprint.py --check /tmp/before.json
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Iterator


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


# The bags a Loadout may keep its items in.  Named here rather than guessed,
# so a renamed bag fails loudly as a missing field instead of silently
# fingerprinting nothing.
ITEM_BAGS = (
        "bag",
        "carried",
        "worn",
        "held",
        "items",
        )


def Grid_Levels() -> tuple[int, ...]:
    """The levels under test, from the environment or the default pair."""
    setting = os.environ.get(
            "FINGERPRINT_LEVELS",
            "1,5",
            )
    return tuple(
            int(
                    piece
                    )
            for piece in setting.split(",")
            if piece.strip()
            )


def Grid_Seeds() -> tuple[int, ...]:
    """The seeds under test, from the environment or the default pair."""
    setting = os.environ.get(
            "FINGERPRINT_SEEDS",
            "1,2",
            )
    return tuple(
            int(
                    piece
                    )
            for piece in setting.split(",")
            if piece.strip()
            )


@contextlib.contextmanager
def hush() -> Iterator[None]:
    """Silence the generator's Minion trace at the file-descriptor level."""
    with open(
            os.devnull,
            "w",
            ) as devnull:
        # Flush at both boundaries: Python block-buffers a piped stdout, and
        # buffered text written inside the quiet stretch would otherwise be
        # flushed after the descriptors are restored, and surface anyway.
        sys.stdout.flush()
        sys.stderr.flush()
        out, err = os.dup(1), os.dup(2)
        os.dup2(
                devnull.fileno(),
                1,
                )
        os.dup2(
                devnull.fileno(),
                2,
                )
        try:
            yield
        finally:
            sys.stdout.flush()
            sys.stderr.flush()
            os.dup2(out, 1)
            os.dup2(err, 2)
            os.close(out)
            os.close(err)


def Named(value: Any) -> str:
    """The name a domain object answers to, for a stable comparison."""
    return str(
            getattr(
                    value,
                    "name",
                    value,
                    )
            )


def Skill_Ranks(character) -> list[list[Any]]:
    """Every Skill, its training rank, and its Jack of All Trades flag."""
    skills = getattr(
            character,
            "skills",
            None,
            )
    if skills is None:
        return []
    return [
            [
                    skill.name,
                    skill.proficiency_level,
                    bool(
                            getattr(
                                    skill,
                                    "jack",
                                    False,
                                    )
                            ),
                    ]
            for skill in skills.get_all_skills()
            ]


def Gear_Ranks(character) -> list[list[Any]]:
    """Every Weapon and Armour proficiency the sheet carries."""
    skills = getattr(
            character,
            "skills",
            None,
            )
    if skills is None:
        return []
    return [
            [
                    entry.name,
                    entry.proficiency_level,
                    ]
            for entry in (
                    skills.get_all_weapons()
                    + skills.get_all_armors()
                    )
            ]


def Carried_Items(character) -> list[str]:
    """Every item the Character carries, wears or holds, by name."""
    equipment = getattr(
            character,
            "equipment",
            None,
            )
    if equipment is None:
        return []
    carried = []
    for bag in ITEM_BAGS:
        contents = getattr(
                equipment,
                bag,
                None,
                )
        if not contents:
            continue
        for item in contents:
            carried.append(
                    f"{bag}:{Named(item)}"
                    )
    return sorted(carried)


def Training_Grants(character) -> list[str]:
    """Every recorded training batch: what was granted, and by whom."""
    training = getattr(
            character,
            "training",
            None,
            )
    if training is None:
        return []
    return sorted(
            f"{batch.grant_id}:{grant.capability.name}:{int(grant.rank)}"
            for batch in training.gains
            for grant in batch.grants
            )


def Fingerprint_Of(character) -> dict[str, Any]:
    """One Character reduced to the facts a refactor must not move."""
    return {
            "name": Named(character),
            "level": getattr(character, "level", None),
            "guild": getattr(character, "character_class", None),
            "specialization": getattr(character, "specialization", None),
            "background": Named(
                    getattr(
                            character,
                            "background",
                            "",
                            )
                    ),
            "race": getattr(character, "race", None),
            "subrace": getattr(character, "subrace", None),
            "AC": getattr(character, "AC", None),
            "HP": getattr(
                    character,
                    "HP",
                    getattr(
                            character,
                            "hp",
                            None,
                            ),
                    ),
            "skills": Skill_Ranks(character),
            "gear_training": Gear_Ranks(character),
            "other_proficiencies": sorted(
                    getattr(
                            character,
                            "other_proficiencies",
                            [],
                            )
                    or []
                    ),
            "features": sorted(
                    Named(feature)
                    for feature in getattr(
                            character,
                            "features",
                            [],
                            )
                    or []
                    ),
            "items": Carried_Items(character),
            "training": Training_Grants(character),
            }


def Fingerprint_Grid() -> dict[str, dict[str, Any]]:
    """The whole grid: every Guild, at every level, for every seed."""
    from AtlasActorLudi.Map_of_Character_Generation import summon_player
    from AtlasLusoris.GuildKit import GUILDS

    grid = {}
    for guild in sorted(
            GUILDS
            ):
        for level in Grid_Levels():
            for seed in Grid_Seeds():
                key = f"{guild}-L{level}-s{seed}"
                # Reading the fingerprint stays inside the quiet stretch:
                # race, subrace and character_class are Minion-decorated, so
                # the read itself reports to the log.
                with hush():
                    character = summon_player(
                            seed=seed,
                            level=level,
                            guild=guild,
                            )
                    fingerprint = json.loads(
                            json.dumps(
                                    Fingerprint_Of(
                                            character
                                            ),
                                    default=str,
                                    )
                            )
                grid[key] = fingerprint
    return grid


def Report_Difference(
        before: dict[str, Any],
        after: dict[str, Any],
        ) -> list[str]:
    """Name every Character, and every field, that moved."""
    complaints = []
    for key in sorted(
            set(before) | set(after)
            ):
        old = before.get(key)
        new = after.get(key)
        if old == new:
            continue
        if old is None:
            complaints.append(f"{key}: absent from the baseline")
            continue
        if new is None:
            complaints.append(f"{key}: no longer generated")
            continue
        for field in sorted(
                set(old) | set(new)
                ):
            if old.get(field) != new.get(field):
                complaints.append(
                        f"{key}.{field}:\n"
                        f"      was {old.get(field)}\n"
                        f"      now {new.get(field)}"
                        )
    return complaints


def Save(path: Path) -> int:
    """Record the baseline the next run compares against."""
    grid = Fingerprint_Grid()
    path.write_text(
            json.dumps(
                    grid,
                    indent=1,
                    sort_keys=True,
                    )
            )
    print(
            f"OK — {len(grid)} Characters fingerprinted to {path}"
            )
    return 0


def Check(path: Path) -> int:
    """Compare today's Characters against the recorded baseline."""
    if not path.exists():
        print(
                f"No baseline at {path}. Record one with --save before the change.",
                file=sys.stderr,
                )
        return 2

    before = json.loads(
            path.read_text()
            )
    after = Fingerprint_Grid()
    complaints = Report_Difference(
            before,
            after,
            )

    if not complaints:
        print(
                f"OK — {len(after)} Characters identical to {path}"
                )
        return 0

    print(
            f"{len(complaints)} DIFFERENCES against {path}:"
            )
    for complaint in complaints[:40]:
        print(f"  ! {complaint}")
    if len(complaints) > 40:
        print(f"  … and {len(complaints) - 40} more")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            )
    group = parser.add_mutually_exclusive_group(
            required=True,
            )
    group.add_argument(
            "--save",
            metavar="PATH",
            help="record the baseline before a change",
            )
    group.add_argument(
            "--check",
            metavar="PATH",
            help="compare against a baseline after a change",
            )
    arguments = parser.parse_args()

    if arguments.save:
        return Save(
                Path(
                        arguments.save
                        )
                )
    return Check(
            Path(
                    arguments.check
                    )
            )


if __name__ == "__main__":
    raise SystemExit(
            main()
            )
