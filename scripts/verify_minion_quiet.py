#!/usr/bin/env python3
"""Verify that Minion logging is disabled by default.

This script ensures that:
1. Minion logging produces NO output by default
2. Setting MINION_ENABLED=1 enables logging
3. MINION_LOG=file.log alone still enables file logging (backward compatible)
4. An explicit MINION_ENABLED=no silences everything, even MINION_LOG
5. set_log_file(None) restores the quiet default (no console leak)
6. The quiet mode works correctly for CI/CD

Run:
    python scripts/verify_minion_quiet.py
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MINION_ENV_KEYS = ("MINION_ENABLED", "MINION_LOG")

# Minion decorators stamp every record with one of these bracket tags.
# Detection must key on the tags, not on the literal word "minion":
# a run that only exercises @watcher or @warden never prints "[minion]".
MINION_RECORD_TAGS = (
	"[minion]",
	"[warden]",
	"[watcher]",
	"[guardian]",
	"[changeling]",
	"[spy]",
	)


def _has_minion_records(text: str) -> bool:
	"""True when the text carries at least one Minion record tag."""
	return any(tag in text for tag in MINION_RECORD_TAGS)


def run_python_code(
	code: str,
	env: dict[str, str] | None = None,
	) -> tuple[str, str, int]:
	"""Run Python code and capture stdout, stderr, and return code.

	Minion-related environment variables from the outer environment are
	always removed first, so each test controls its own Minion settings.
	"""
	cmd = [sys.executable, "-c", code]
	clean_env = {
		key: value
		for key, value in os.environ.items()
		if key not in MINION_ENV_KEYS
		}
	result = subprocess.run(
		cmd,
		capture_output=True,
		text=True,
		cwd=PROJECT_ROOT,
		env={**clean_env, **(env or {})},
		)
	return result.stdout, result.stderr, result.returncode


_SUMMON_CODE = """
import io
import sys
from contextlib import redirect_stdout, redirect_stderr

# Capture all output
stdout_capture = io.StringIO()
stderr_capture = io.StringIO()

with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
    from AtlasActorLudi.Map_of_Character_Generation import summon_player
    p = summon_player(seed=42, level=1)

stdout_output = stdout_capture.getvalue()
stderr_output = stderr_capture.getvalue()

print(repr(stdout_output))
print("---STDERR---")
print(repr(stderr_output))
"""


def test_minion_disabled_by_default() -> tuple[bool, str]:
	"""Test that Minion logging is silent by default."""
	stdout, stderr, returncode = run_python_code(_SUMMON_CODE)
	if returncode != 0:
		return False, f"summon_player failed with rc={returncode}. stderr: {stderr[:200]}"

	combined = stdout
	if _has_minion_records(combined):
		return False, (
			"Minion records were printed although Minion logging should be "
			f"disabled by default. Output began with: {combined[:200]}"
			)
	return True, "Minion logging is silent by default"


def test_minion_enabled_explicitly() -> tuple[bool, str]:
	"""Test that MINION_ENABLED=1 enables logging."""
	env = {"MINION_ENABLED": "1"}
	stdout, stderr, returncode = run_python_code(_SUMMON_CODE, env)
	if returncode != 0:
		return False, f"summon_player failed under MINION_ENABLED=1 (rc={returncode}). stderr: {stderr[:200]}"

	combined = stdout
	if not _has_minion_records(combined):
		return False, (
			"MINION_ENABLED=1 did not produce any Minion record "
			f"([minion]/[warden]/[watcher]/...). Output began with: {combined[:200]}"
			)
	return True, "MINION_ENABLED=1 enables logging"


def test_minion_log_file() -> tuple[bool, str]:
	"""Test that MINION_LOG=file.log alone writes to the file (backward compatible)."""
	import tempfile
	with tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False) as f:
		log_path = f.name

	try:
		code = """
from AtlasActorLudi.Map_of_Character_Generation import summon_player
p = summon_player(seed=42, level=1)
"""
		env = {"MINION_LOG": log_path}
		stdout, stderr, returncode = run_python_code(code, env)
		if returncode != 0:
			return False, (
				f"summon_player failed under MINION_LOG (rc={returncode}). "
				f"stderr: {stderr[:200]}"
				)

		# Check that the log file was created and received records
		if os.path.exists(log_path):
			with open(log_path, "r", encoding="utf-8") as f:
				content = f.read()
			if content.strip():
				if _has_minion_records(content):
					return True, "MINION_LOG alone writes Minion records to file correctly"
				return True, (
					"MINION_LOG alone writes records to file correctly "
					"(no tagged record in this run, but the file is not empty)"
					)
			return False, f"MINION_LOG file exists but is empty at {log_path}"
		return False, f"MINION_LOG file was not created at {log_path}"
	finally:
		if os.path.exists(log_path):
			os.unlink(log_path)


def test_minion_explicit_disable_wins() -> tuple[bool, str]:
	"""Test that MINION_ENABLED=no silences the run even when MINION_LOG is set."""
	env = {"MINION_ENABLED": "no", "MINION_LOG": "minion_should_stay_silent.log"}
	stdout, stderr, returncode = run_python_code(_SUMMON_CODE, env)
	if os.path.exists("minion_should_stay_silent.log"):
		size = os.path.getsize("minion_should_stay_silent.log")
		os.unlink("minion_should_stay_silent.log")
		if size > 0:
			return False, (
				"MINION_ENABLED=no did not silence file logging; "
				f"the log file received {size} bytes."
				)
	if returncode != 0:
		return False, (
			f"summon_player failed under explicit disable (rc={returncode}). "
			f"stderr: {stderr[:200]}"
			)
	if _has_minion_records(stdout):
		return False, (
			"MINION_ENABLED=no did not silence console output. "
			f"Output began with: {stdout[:200]}"
			)
	return True, "MINION_ENABLED=no silences everything, even MINION_LOG"


def test_set_log_file_none_restores_silence() -> tuple[bool, str]:
	"""Test that set_log_file(None) restores the default quiet state.

	Regression test: choosing a log file enables Minion logging, but clearing
	it again used to leave logging enabled, so records fell through to the
	console even though the caller asked for silence.
	"""
	code = """
import io
from contextlib import redirect_stdout
from Minion import set_log_file, _emit

# A caller enabled logging by choosing a log file, then cleared it again.
set_log_file("should_not_be_written.log")
set_log_file(None)

buf = io.StringIO()
with redirect_stdout(buf):
	_emit("[minion] this record must stay silent")

if buf.getvalue().strip():
	raise SystemExit("console output leaked: " + repr(buf.getvalue()))
print("silent after set_log_file(None)")
"""
	stdout, stderr, returncode = run_python_code(code)
	if returncode != 0:
		return False, (
			f"set_log_file(None) check failed (rc={returncode}). "
			f"stderr: {stderr[:200]}"
			)
	if "silent after set_log_file(None)" not in stdout:
		return False, f"unexpected output: {stdout[:200]}"
	return True, "set_log_file(None) restores the quiet default"


def main() -> int:
	"""Run all verification checks."""
	print("=" * 70)
	print("Minion Quiet Mode Validation")
	print("=" * 70)
	print()

	all_passed = True

	# Test 1: Minion disabled by default
	print("[Check 1] Verifying Minion logging is disabled by default...")
	passed, message = test_minion_disabled_by_default()
	if passed:
		print(f"✅ {message}")
	else:
		print(f"❌ {message}")
		all_passed = False
	print()

	# Test 2: Minion can be enabled
	print("[Check 2] Verifying MINION_ENABLED=1 enables logging...")
	passed, message = test_minion_enabled_explicitly()
	if passed:
		print(f"✅ {message}")
	else:
		print(f"❌ {message}")
		all_passed = False
	print()

	# Test 3: Minion log file works without MINION_ENABLED
	print("[Check 3] Verifying MINION_LOG=file.log alone writes to file...")
	passed, message = test_minion_log_file()
	if passed:
		print(f"✅ {message}")
	else:
		print(f"❌ {message}")
		all_passed = False
	print()

	# Test 4: an explicit disable wins over MINION_LOG
	print("[Check 4] Verifying MINION_ENABLED=no silences even MINION_LOG...")
	passed, message = test_minion_explicit_disable_wins()
	if passed:
		print(f"✅ {message}")
	else:
		print(f"❌ {message}")
		all_passed = False
	print()

	# Test 5: clearing the log file restores the quiet default
	print("[Check 5] Verifying set_log_file(None) restores the quiet default...")
	passed, message = test_set_log_file_none_restores_silence()
	if passed:
		print(f"✅ {message}")
	else:
		print(f"❌ {message}")
		all_passed = False
	print()

	print("=" * 70)
	if all_passed:
		print("✅ All Minion quiet mode checks PASSED.")
		return 0
	else:
		print("❌ Some Minion quiet mode checks FAILED.")
		return 1


if __name__ == "__main__":
	sys.exit(main())
