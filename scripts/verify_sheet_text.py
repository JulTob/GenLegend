"""
The sheet snapshot: what a reader SEES on every Character's sheet, before and after.

The fingerprint (``verify_fingerprint.py``) guards what a Character IS: stats,
gear, training. It does not see the sheet's text. This gate does. It prints
every Character on the grid through the real sheet builder
(``app.components.character_sheet.build_character_sheet``), keeps only the
visible text, one line per block, and compares it with a saved copy.

Markup may change freely (a ``<b>`` becoming a ``<strong>``, a table becoming
a list); only a change a reader would notice shows up. That is what lets the
QST-0142 stations move text to Markdown and printers to new code while
proving the sheet reads the same.

Use
    PYTHONHASHSEED=0 FINGERPRINT_LEVELS=1,3,5,9,13,17,20 FINGERPRINT_SEEDS=1,2,3 \\
        .venv/bin/python scripts/verify_sheet_text.py --save /tmp/sheets.json
    ... change the code ...
    PYTHONHASHSEED=0 FINGERPRINT_LEVELS=1,3,5,9,13,17,20 FINGERPRINT_SEEDS=1,2,3 \\
        .venv/bin/python scripts/verify_sheet_text.py --check /tmp/sheets.json

The grid is the fingerprint's grid, read from the same two variables, plus
NonPlayer Characters at the same levels for ``SHEET_NONPLAYER_SEEDS``
(default 1 to 10), printed through ``build_npc_sheet``.
"""

from __future__ import annotations

import argparse
import difflib
import html
import json
import os
import random
import re
import sys
from pathlib import Path

from verify_fingerprint import Grid_Levels
from verify_fingerprint import Grid_Seeds
from verify_fingerprint import hush
from verify_fingerprint import PROJECT_ROOT


# Tags that start a new line for a reader: blocks, rows, list items, breaks.
BLOCK_TAGS = re.compile(
        r"<\s*/?\s*(div|p|li|tr|td|th|h[1-6]|br|ul|ol|table|section|details|summary)\b[^>]*>",
        re.IGNORECASE,
        )
ANY_TAG = re.compile(
        r"<[^>]+>",
        )
SCRIPT_OR_STYLE = re.compile(
        r"<(script|style)\b.*?</\1\s*>",
        re.IGNORECASE | re.DOTALL,
        )


def Visible_Lines(
        page: str,
        ) -> list[str]:
    """The text a reader sees, one line per block, spaces collapsed."""
    text = SCRIPT_OR_STYLE.sub(
            "",
            page,
            )
    text = BLOCK_TAGS.sub(
            "\n",
            text,
            )
    text = ANY_TAG.sub(
            "",
            text,
            )
    text = html.unescape(
            text
            )
    lines = []
    for raw in text.split("\n"):
        line = " ".join(
                raw.split()
                )
        if line:
            lines.append(
                    line
                    )
    return lines


def Sheet_Of(
        guild: str,
        level: int,
        seed: int,
        ) -> list[str]:
    """One Character's sheet, as visible lines."""
    from AtlasActorLudi.Map_of_Character_Generation import summon_player
    from app.components.character_sheet import build_character_sheet

    with hush():
        character = summon_player(
                seed=seed,
                level=level,
                guild=guild,
                )
        page = str(
                build_character_sheet(
                        character.to_dict()
                        )
                )
    return Visible_Lines(
            page
            )


def NonPlayer_Sheet_Of(
        level: int,
        seed: int,
        ) -> list[str]:
    """
    One NonPlayer Character's sheet, as visible lines.

    ``light=True``: a full NonPlayer cannot be summoned today (QST-0134
    finding 1, ``Grimoire_of_NPC.SetSize``), so the gate reads the light ones.
    """
    from AtlasActorLudi.AtlasAlusoris.Map_of_NonPlayer_Generation import (
            summon_nonplayer,
            )
    from app.components.npc_sheet import build_npc_sheet

    import app.random

    pin = f"nonplayer-{level}-{seed}"
    random.seed(
            pin
            )
    app.random.seed(
            pin
            )
        #-- Some NonPlayer text still draws from Python's shared generator or
        #-- from app.random's private one, instead of the Character's own
        #-- Dice.  Pin both so a sheet reads the same on every run.
    try:
        with hush():
            npc = summon_nonplayer(
                    level=level,
                    seed=seed,
                    light=True,
                    )
            page = str(
                    build_npc_sheet(
                            npc
                            )
                    )
    except Exception as error:
        return [
                f"SHEET FAILED: {type( error ).__name__}: {error}",
                ]
        #-- A failure is part of the picture: if it changes, the gate says so.
    return Visible_Lines(
            page
            )


def Sheet_Grid() -> dict[str, list[str]]:
    """Every Guild at every level for every seed, then NonPlayers on the same grid."""
    import app.main  # noqa: F401  (the sheet builder expects the app's setup)
    from AtlasLusoris.GuildKit import GUILDS

    grid = {}
    for guild in sorted(
            GUILDS
            ):
        for level in Grid_Levels():
            for seed in Grid_Seeds():
                key = f"{guild}-L{level}-s{seed}"
                grid[key] = Sheet_Of(
                        guild,
                        level,
                        seed,
                        )
    for level in Grid_Levels():
        for seed in NonPlayer_Seeds():
            key = f"NonPlayer-L{level}-s{seed}"
            grid[key] = NonPlayer_Sheet_Of(
                    level,
                    seed,
                    )
    return grid


def NonPlayer_Seeds() -> tuple[int, ...]:
    """NonPlayer seeds: more than for Players, since one seed picks everything."""
    setting = os.environ.get(
            "SHEET_NONPLAYER_SEEDS",
            "1,2,3,4,5,6,7,8,9,10",
            )
    return tuple(
            int(
                    piece
                    )
            for piece in setting.split(",")
            if piece.strip()
            )


def Save(
        path: Path,
        ) -> int:
    grid = Sheet_Grid()
    path.write_text(
            json.dumps(
                    grid,
                    indent=1,
                    ensure_ascii=False,
                    )
            )
    print(
            f"Saved {len(grid)} sheets to {path}"
            )
    return 0


def Check(
        path: Path,
        ) -> int:
    before = json.loads(
            path.read_text()
            )
    after = Sheet_Grid()
    changed = []
    for key in sorted(
            set(
                    before
                    ) | set(
                    after
                    )
            ):
        if before.get(key) != after.get(key):
            changed.append(
                    key
                    )
    if not changed:
        print(
                f"OK — {len(after)} sheets read the same as {path}"
                )
        return 0

    print(
            f"{len(changed)} SHEETS READ DIFFERENTLY against {path}:"
            )
    for key in changed[:12]:
        print(
                f"  ! {key}"
                )
        diff = difflib.unified_diff(
                before.get(key, []),
                after.get(key, []),
                lineterm="",
                n=0,
                )
        for line in list(diff)[2:14]:
            print(
                    f"      {line}"
                    )
    if len(changed) > 12:
        print(
                f"  … and {len(changed) - 12} more"
                )
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(
            description=__doc__.splitlines()[1],
            )
    mode = parser.add_mutually_exclusive_group(
            required=True,
            )
    mode.add_argument(
            "--save",
            type=Path,
            )
    mode.add_argument(
            "--check",
            type=Path,
            )
    arguments = parser.parse_args()
    if arguments.save is not None:
        return Save(
                arguments.save
                )
    return Check(
            arguments.check
            )


if __name__ == "__main__":
    sys.exit(
            main()
            )
