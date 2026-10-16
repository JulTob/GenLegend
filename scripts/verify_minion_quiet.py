#!/usr/bin/env python3
"""Verify that Minion logging is disabled by default.

This script ensures that:
1. Minion logging produces NO output by default
2. Setting MINION_ENABLED=1 enables logging
3. The quiet mode works correctly for CI/CD

Run:
    python scripts/verify_minion_quiet.py
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run_python_code(code: str, env: dict[str, str] | None = None) -> tuple[str, str, int]:
    """Run Python code and capture stdout, stderr, and return code."""
    cmd = [sys.executable, "-c", code]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
        env={**os.environ, **(env or {})},
    )
    return result.stdout, result.stderr, result.returncode


def test_minion_disabled_by_default() -> tuple[bool, str]:
    """Test that Minion logging is silent by default."""
    code = """
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
combined = stdout_output + stderr_output

# Check that no Minion output appears
if "Minion" in combined or "minion" in combined:
    print("FAIL: Minion output detected when disabled")
    print(f"stdout: {stdout_output[:200]}")
    print(f"stderr: {stderr_output[:200]}")
    sys.exit(1)
else:
    print("PASS: No Minion output when disabled")
    sys.exit(0)
"""
    stdout, stderr, returncode = run_python_code(code)
    if returncode != 0:
        return False, f"Minion logging was NOT silent by default. Output: {stdout[:200]}"
    return True, "Minion logging is silent by default"


def test_minion_enabled_explicitly() -> tuple[bool, str]:
    """Test that MINION_ENABLED=1 enables logging."""
    code = """
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
combined = stdout_output + stderr_output

# Check that Minion output DOES appear
if "Minion" in combined or "minion" in combined:
    print("PASS: Minion output detected when enabled")
    sys.exit(0)
else:
    print("FAIL: No Minion output when enabled")
    sys.exit(1)
"""
    env = {"MINION_ENABLED": "1"}
    stdout, stderr, returncode = run_python_code(code, env)
    if returncode != 0:
        return False, f"MINION_ENABLED=1 did not enable logging. Output: {stdout[:200]}"
    return True, "MINION_ENABLED=1 enables logging"


def test_minion_log_file() -> tuple[bool, str]:
    """Test that MINION_LOG=file.log writes to file."""
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False) as f:
        log_path = f.name
    
    try:
        code = """
from AtlasActorLudi.Map_of_Character_Generation import summon_player
p = summon_player(seed=42, level=1)
"""
        env = {"MINION_LOG": log_path, "MINION_ENABLED": "1"}
        stdout, stderr, returncode = run_python_code(code, env)
        
        # Check that the log file was created and has content
        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                content = f.read()
            if "Minion" in content or "minion" in content:
                return True, "MINION_LOG writes to file correctly"
            else:
                return False, f"MINION_LOG file exists but has no Minion content: {content[:200]}"
        else:
            return False, f"MINION_LOG file was not created at {log_path}"
    finally:
        if os.path.exists(log_path):
            os.unlink(log_path)


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
    
    # Test 3: Minion log file works
    print("[Check 3] Verifying MINION_LOG=file.log writes to file...")
    passed, message = test_minion_log_file()
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
