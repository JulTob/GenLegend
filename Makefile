# Gen Legend: one door.
#   make run            serve app.main:app on $(PORT)      make dev   the same, reloading on edits
#   make smoke-player   boot and generate seed 42           make replay-player   the seeded-replay rite
#   make sweep-player   every Guild at levels 1 and 5 (add WIDE=1 for every level, Species, Background, Specialization)
.PHONY: run dev setup smoke-player sweep-player replay-player verify-aasimar safepoint install-hooks loss-check

PORT ?= 8080
VENV := .venv
SHINY := $(VENV)/bin/shiny
PIP := $(VENV)/bin/pip
VENV_PYTHON := $(VENV)/bin/python
PYTHON := $(PYTHON_BIN)

ifeq ($(PYTHON),)
PYTHON := $(shell command -v python3.14 2>/dev/null || command -v python3.13 2>/dev/null || command -v python3.12 2>/dev/null || command -v python3.11 2>/dev/null || command -v python3.10 2>/dev/null || command -v python3 2>/dev/null)
endif

# Homebrew headers and libraries on Apple Silicon, for any dependency built from source.
ifneq ($(wildcard /opt/homebrew/include),)
export CPPFLAGS += -I/opt/homebrew/include
export LDFLAGS += -L/opt/homebrew/lib
endif

run: setup
	$(SHINY) run --port $(PORT) app.main:app

dev: setup
	$(SHINY) run --reload --port $(PORT) app.main:app

setup: $(SHINY)

$(SHINY):
	@test -n "$(PYTHON)" || (echo "Python 3.10+ not found (3.14 recommended: brew install python@3.14)." && exit 1)
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt

smoke-player: setup
	$(VENV_PYTHON) -c "import app.main; from AtlasActorLudi.Map_of_Character_Generation import summon_player; p = summon_player(seed=42, level=1); print('smoke-player OK', getattr(p, 'name', p))"
	$(VENV_PYTHON) -m AtlasVenustas.Charts_of_Printing
	$(VENV_PYTHON) -m AtlasActorLudi.Charts_of_Build

replay-player: setup
	$(VENV_PYTHON) scripts/verify_player_replay.py

# The Aasimar page is locked and owns its code.  This proves the code still
# agrees with it; if it fails, the page is right.
verify-aasimar: setup
	$(VENV_PYTHON) scripts/verify_aasimar_page.py

sweep-player: setup
	$(VENV_PYTHON) scripts/sweep_player.py $(if $(WIDE),--wide,)

safepoint:
	@chmod +x scripts/safepoint.sh
	@./scripts/safepoint.sh

install-hooks:
	@chmod +x scripts/install-git-hooks.sh scripts/git-hooks/pre-commit scripts/git-hooks/pre-push
	@./scripts/install-git-hooks.sh

loss-check:
	$(VENV_PYTHON) scripts/loss_detector.py --staged
