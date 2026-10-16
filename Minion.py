# Minion.py — fail-system decorators: @minion, @warden, @watcher, @spy, @guardian, @changeling
# None of them change the function's return value. They only inform the log system.
import functools
import inspect
import os
import re
from datetime import datetime

_STOP_FILES = frozenset({"Minion.py"})
_START_FILES = frozenset({"main.py"})

# Log system: when set, decorators append plain-text records here.
# ``MINION_LOG=minion_app.log python3 ...`` enables it for a whole run.
# By default, Minion logging is DISABLED in production to avoid noise.
# Set MINION_ENABLED=1 to enable console output, or MINION_LOG=file.log for file output.
_log_path = os.environ.get("MINION_LOG")
_minion_enabled = os.environ.get("MINION_ENABLED", "").lower() in ("1", "true", "yes")

# Minion emoji for code

MINION = "🧞"
FAIL_MINION = "🧟"
WARDEN_MINION = "🧌"
WATCHER_MINION = "🦉"
SPY_MINION = "🕷️"
LOG_MINION = "🐉"
ALERT_MINION = "🧜🏽‍♀️"
MESSAGE_MINION = "🕊️"
RECALL_MINION = "🐦‍🔥"
END_MINION = "🦉"
GUARDIAN_MINION = "🐺"
CHANGELING_MINION = "🧚"

# Per-minion colors (for console output). Names: black, red, green, yellow, blue, magenta, cyan, white, dim, bold
MINION_COLOR = "cyan"
FAIL_COLOR = "yellow"
WARDEN_COLOR = "green"
WATCHER_COLOR = "cyan"
SPY_COLOR = "blue"
LOG_COLOR = "dim"
ALERT_COLOR = "bold"
GUARDIAN_COLOR = "magenta"
CHANGELING_COLOR = "yellow"


def set_log_file(path="minion_app.log"):
	"""Set path for decorators to append records. Default 'minion_app.log'. Pass None to disable file logging."""
	global _log_path
	_log_path = path

def get_log_file():
	"""Current log file path, or None."""
	return _log_path

def set_minion_enabled(enabled: bool) -> None:
	"""Enable or disable Minion logging globally. Pass False to silence all Minion output."""
	global _minion_enabled
	_minion_enabled = enabled

def get_minion_enabled() -> bool:
	"""Check if Minion logging is currently enabled."""
	return _minion_enabled

def set_start_files(files):
	"""Set custom start files for get_call_tree."""
	global _START_FILES
	_START_FILES = frozenset(files)

def get_start_files():
	"""Current start files set for get_call_tree."""
	return _START_FILES

def _emit(plain_text, color=None):
	"""Low-level sink: file when _log_path is set (plain text), else console (optionally colored)."""
	# If Minion logging is disabled globally, do nothing
	if not _minion_enabled:
		return
	
	if _log_path is not None:
		try:
			with open(_log_path, "a", encoding="utf-8") as f:
				f.write(plain_text + "\n")
			return
		except OSError:
			print(Color(f"{ALERT_MINION} Error writing to log file: {_log_path}", ALERT_COLOR))
	
	# Fall back to console output
	print(Color(plain_text, color) if color else plain_text)

# ─────────────────────────────────────────────────────────────────────────────
#  The Chronicler — gathers one job's records into a single, tidy account
# ─────────────────────────────────────────────────────────────────────────────
# Normally each Minion reports the instant something happens. But summoning a
# character calls the same helpers hundreds of times, and the repeats drown the
# signal. Put @chronicler on the top-level job. While it runs, the little Minions
# report *into the Chronicler's account* instead of straight to the screen; when
# the job ends, the Chronicler reads the account aloud:
#     • each distinct line once, live, as it first happens;
#     • repeats collapsed into a quiet "  ×N" at the end;
#     • any errors gathered into a closing section, each under a separator.
# A nested @chronicler simply joins the outermost account (only it opens/closes).

SEPARATOR = "─" * 40
_TIMESTAMP = re.compile(r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d")

class _Account:
	"""What the Chronicler collects while it is open."""
	def __init__(self):
		self.seen = {}     # identity -> [text, times_seen, color]   (for the ×N summary)
		self.errors = []   # error texts, gathered to show together at the very end

# The account currently open, or None when no Chronicler is running.
_account = None

def _identity(text):
	"""A record's identity, ignoring its clock time — so two identical events match."""
	return _TIMESTAMP.sub("⏱", text)

def print_record(text, color=None):
	"""
	Report one line to the log.
	  	• No Chronicler open  → print it now (unchanged behaviour).
	  	• Chronicler open     → first sighting prints live; repeats are only tallied;
	                          	errors are held back for the closing section.
	"""
	if _account is None:
		_emit(text, color)
		return

	if color == FAIL_COLOR:              # an error (bug tree / locator) — save it for the end
		_account.errors.append(text)
		return

	identity = _identity(text)
	if identity in _account.seen:
		_account.seen[identity][1] += 1  # seen before in this account — just add to the tally
	else:
		_account.seen[identity] = [text, 1, color]
		_emit(text, color)               # first time — show it live

def _read_account_aloud(account):
	"""Print the closing summary: each repeated line as "×N", then the errors."""
	for text, times_seen, color in account.seen.values():
		if times_seen > 1:
			_emit(SEPARATOR)
			_emit(f"{_identity(text)}  ×{times_seen}", color)
	for error_text in account.errors:
		_emit(SEPARATOR)
		_emit(error_text, FAIL_COLOR)

def chronicler(job):
	"""
	Decorator for a top-level job (e.g. summon_character): open one account, let the
	Minions inside report into it, then read the account aloud when the job finishes.
	A nested @chronicler just joins the account already open.
	"""
	def wrapped(*args, **kwargs):
		global _account
		if _account is not None:             # already inside an account — just run
			return job(*args, **kwargs)

		_account = _Account()                # open a fresh account
		try:
			return job(*args, **kwargs)
		finally:
			account, _account = _account, None  # close it before reading, so the
			_read_account_aloud(account)        # summary itself prints normally
	return wrapped

# ANSI colors (compact lookup)
_RESET = "\033[0m"
_COLORS = {
	"black": "\033[90m", "red": "\033[91m", 
	"green": "\033[92m", "yellow": "\033[93m",
	"blue": "\033[94m", "magenta": "\033[95m", 
	"cyan": "\033[96m", "white": "\033[97m",
	"dim": "\033[2m", "bold": "\033[1m",
	}

def Color(text, color="white"):
	"""Wrap text in ANSI color for terminal. color: black, red, green, yellow, blue, magenta, cyan, white, dim, bold."""
	c = _COLORS.get(color.lower(), _COLORS["white"])
	return f"{c}{text}{_RESET}"




def get_call_tree(start_files=None, stop_files=None):
	"""
	Current call stack as a short tree. 
	Only builds when a start file is seen.
	"""
	start = start_files or _START_FILES
	stop = stop_files or _STOP_FILES
	if not isinstance(start, set):
		start = frozenset(start)
	if not isinstance(stop, set):
		stop = frozenset(stop)
	stack = inspect.stack()
	out = ["\n╞🔮 Call Stack:"]
	level = 0
	prev_file = None
	active = False
	for frame in reversed(stack[1:]):
		fname = os.path.basename(frame.filename)
		if fname in stop:
			continue
		if fname in start:
			active = True
		if not active or ".py" not in fname:
			continue
		ln, fn = frame.lineno, frame.function
		if fname != prev_file:
			cur = level
			level += 1
			ind = "│  " * cur
			out.append(f"│  {ind}╭📜 「{fname}」")
		else:
			cur = level - 1
			ind = "│  " * cur
		if "module" not in fn:
			out.append(f"│  {ind}╭🪄({ln}) ⟨{fn}⟩")
		else:
			out.append(f"│  {ind}╭🪶({ln})")
		prev_file = fname
	out.append("├" + "──╯" * level)
	return "\n".join(out)

def bugged_tree(exc):
	"""Exception traceback as a short tree."""
	tb = exc.__traceback__
	out = ["\n╞🐛 Bugs:"]
	level = 0
	cur = 0
	prev_file = None
	while tb:
		f = tb.tb_frame
		fname = f.f_code.co_filename.split("/")[-1]
		ln, fn = tb.tb_lineno, f.f_code.co_name
		if fname != prev_file:
			cur = level
			level += 1
			out.append(f"╷  {'╷  ' * cur}🐝 「{fname}」")
		else:
			cur = level - 1
		out.append(f"╷  {'╷  ' * cur}🐞 ({ln}): ⟨{fn}⟩")
		prev_file = fname
		tb = tb.tb_next
	out.append("├" + "╶╶╯" * level)
	out.append(f"┝🦋 Bug: {type(exc).__name__} - {exc}")
	return "\n".join(out)

def _bug_report(exc):
	ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	header = Color(f"{FAIL_MINION} Minion bug report", "magenta")
	time_line = Color(f"⏳ {ts}", "dim")
	stack = Color(get_call_tree(), "cyan")
	bugs = Color(bugged_tree(exc), "green")
	return "\n".join([header, time_line, stack, bugs, "┷"])

def report_bug(exc):
	"""Send one exception's bug tree to the log without re-raising."""
	print_record(
		_bug_report(
			exc
			),
		FAIL_COLOR,
		)

def _to_text_repr(value):
	if value is None:
		return "None"
	if isinstance(value, str):
		return value
	return repr(value)

def minion(f):
	"""
	failure: reports bug tree to log system, then re-raises.
	success: reports result to log system, then returns it.
	"""
	def wrapped(*args, **kwargs):
		try:
			result = f(*args, **kwargs)
			print_record(f"{MINION}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [minion] {f.__name__}: {_to_text_repr(result)}", MINION_COLOR)
			return result
		except Exception as exc:
			report_bug(exc)
			raise
	return wrapped

def warden(f):
	"""
	On failure: reports bug tree to log, retries once with same args, returns that result (or re-raises if retry fails).
	On success: reports result to log system, then returns it.
	"""
	def wrapped(*args, **kwargs):
		try:
			result = f(*args, **kwargs)
			print_record(f"{WARDEN_MINION}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [warden] {f.__name__}: {_to_text_repr(result)}", WARDEN_COLOR)
			return result
		except Exception as exc:
			report_bug(exc)
			return f(*args, **kwargs)
	return wrapped

GUARDIAN_IDENTICAL_LIMIT = 10
GUARDIAN_MAX_ATTEMPTS = 100


def _failure_signature(exc):
	"""Identify an exception by its type and innermost source location."""
	tb = exc.__traceback__

	while tb and tb.tb_next:
		tb = tb.tb_next

	where = (
		f"{tb.tb_frame.f_code.co_filename}:{tb.tb_lineno}"
		if tb
		else "?"
		)

	return f"{type(exc).__name__}@{where}"


def guardian(f):
	"""Retry random failures, stopping when one proves deterministic."""
	@functools.wraps(f)
	def wrapped(*args, **kwargs):
		attempts = 0
		identical = 0
		last_exc = None
		last_signature = None

		while attempts < GUARDIAN_MAX_ATTEMPTS:
			try:
				result = f(
					*args,
					**kwargs,
					)
				print_record(
					f"{GUARDIAN_MINION}: "
					f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
					f"[guardian] {f.__name__}: {_to_text_repr(result)}",
					GUARDIAN_COLOR,
					)

				return result
			except Exception as exc:
				signature = _failure_signature(
					exc
					)

				if signature != last_signature:
					report_bug(exc)
					identical = 1
				else:
					identical += 1

				last_signature = signature
				last_exc = exc
				attempts += 1

				if identical >= GUARDIAN_IDENTICAL_LIMIT:
					raise RuntimeError(
						f"{GUARDIAN_MINION} {f.__name__}: the same failure "
						f"{identical} times running, so it is not the dice. "
						f"{_enriched_error(exc)}"
						) from exc

		raise RuntimeError(
			f"{GUARDIAN_MINION} {f.__name__}: max attempts "
			f"({GUARDIAN_MAX_ATTEMPTS}) reached. "
			f"{_enriched_error(last_exc)}"
			) from last_exc

	return wrapped


def changeling(*successors):
	"""Try distinct stand-ins in order without replaying failed work."""
	def decorate(f):
		ladder = (
			f,
			*successors,
			)

		@functools.wraps(f)
		def wrapped(*args, **kwargs):
			last_exc = None

			for rung, stand_in in enumerate(
					ladder
					):
				try:
					result = stand_in(
						*args,
						**kwargs,
						)
				except Exception as exc:
					report_bug(exc)
					last_exc = exc
					heir = (
						ladder[
							rung + 1
							]
						if rung + 1 < len(ladder)
						else None
						)
					answer = (
						f"{heir.__name__} takes over. "
						f"{_enriched_error(exc)}"
						if heir
						else (
							"no stand-in left. "
							f"{_enriched_error(exc)}"
							)
						)
					print_record(
						f"{CHANGELING_MINION}: "
						f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
						f"[changeling] {stand_in.__name__} failed; "
						f"{answer}",
						CHANGELING_COLOR,
						)

					continue

				if rung:
					print_record(
						f"{CHANGELING_MINION}: "
						f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
						f"[changeling] {f.__name__} answered by "
						f"{stand_in.__name__}: {_to_text_repr(result)}",
						CHANGELING_COLOR,
						)

				return result

			raise RuntimeError(
				f"{CHANGELING_MINION} {f.__name__}: every stand-in failed "
				f"({len(ladder)} of them). {_enriched_error(last_exc)}"
				) from last_exc

		return wrapped

	return decorate


def _enriched_error(exc):
	"""One-line error with file locator for the log."""
	tb = exc.__traceback__
	if not tb:
		return f"{type(exc).__name__}: {exc}"
	while tb.tb_next:  # walk to the innermost frame — the real culprit, not the Minion wrapper
		tb = tb.tb_next
	filename = tb.tb_frame.f_code.co_filename
	file_display = os.path.basename(filename)
	ln = tb.tb_lineno
	return f"{FAIL_MINION} Error in {file_display}:{ln} {type(exc).__name__}: {exc}"

def watcher(f):
	"""
	On success: reports the output to log. 
	On failure: reports enriched error (file locator) to log, then re-raises."""
	def wrapped(*args, **kwargs):
		try:
			out = f(*args, **kwargs)
			print_record(f"{WATCHER_MINION}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [watcher] {f.__name__}: {_to_text_repr(out)}", WATCHER_COLOR)
			return out
		except Exception as exc:
			print_record(
				_enriched_error(
					exc
					),
				FAIL_COLOR,
				)
			raise
	return wrapped

def spy(f):
	"""
	On every call: reports the call tree (chain of command) to the log, then runs the function.
	On failure: reports bug tree to log, then re-raises.
	"""
	def wrapped(*args, **kwargs):
		try:
			ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			tree = get_call_tree()
			print_record(f"{SPY_MINION} [spy] {f.__name__} ({args}, {kwargs}) called at {ts}\n{tree}\n┷", SPY_COLOR)
			return f(*args, **kwargs)
		except Exception as exc:
			report_bug(exc)
			raise
	return wrapped




if __name__ == "__main__":
	# Self-test / usage demo. Run:  python Minion.py

	@watcher
	def name_step():
		return "Bramblefoot the Curious"

	@watcher
	def roll_step():
		return 15

	@minion
	def breaks():
		return 1 / 0

	# 1) Plain use (no Chronicler): every call reports immediately.
	print("— plain, no Chronicler —")
	name_step()
	roll_step()

	# 2) Under a Chronicler: repeats collapse to ×N, errors gather at the end.
	@chronicler
	def summon_demo():
		name_step()            # first time → live
		for _ in range(6):
			name_step()        # repeats → counted, not reprinted
		roll_step()            # a different line → live
		try:
			breaks()           # error → held for the closing section
		except ZeroDivisionError:
			pass

	print("\n— under a Chronicler —")
	summon_demo()

	# Expected: name_step + roll_step live, then a separator with "name_step … ×7",
	# then a separator and the bug tree for breaks().
