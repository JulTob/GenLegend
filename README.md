# D&D — Gen Legend

Tools for Players and Dungeon Masters: generate Player Characters, NPCs, maps, and in time a companion for building worlds. The first public product is the Player Character generator.

The living handbook is [the Wiki](https://github.com/JulTob/GenLegend/wiki). 

Tickets (questae) live in `Documenta/Questae/` (new) and `Curia/Questae/` (older, being merged into Documenta). Decisions live in the Agora.

## Run

```bash
make run
```

`make setup` builds `.venv` from `requirements.txt` the first time (Python 3.10+, 3.14 recommended). `make dev` reloads on edits. The server is `app.main:app`; there is no other entry point.

## Prove

```bash
make smoke-player
```

Boot and generate seed 42. `make replay-player` proves a seeded request replays exactly; `make sweep-player` builds every Guild at levels 1 and 5 (`WIDE=1` builds every level, Species, Background and Specialization and renders every sheet, about nine minutes). The pre-push hook runs the smoke.

## One line: `main`

`origin/main` on GitHub is the product. There is no other remote branch. Local `main` tracks it and is never force-moved (Decree 0008).

Every piece of work is a questa branch, fast-forwarded into `main` when its gate passes:

```bash
git fetch origin
git worktree add ~/Desktop/DnD-session-<short> origin/main
cd ~/Desktop/DnD-session-<short>
git checkout -b questa/QST-####-short-slug
```

`make install-hooks` once per clone. Older lines from the 2026 recovery are local archive tags (`archive/*`, `salvage/*`, `safepoint/*`); they are evidence, not product, and are not pushed.

## Deploy

One container, one command:

```bash
docker build --build-arg BUILD_SHA=$(git rev-parse --short HEAD) -t gen-legends .
```

`gcloud run deploy gen-legends --source . --region us-central1 --allow-unauthenticated` builds the same Dockerfile on Cloud Run.

**The service is `gen-legends`, with an s.** `genlegend.eu` maps to it, and to nothing else. Deploying to `gen-legend` builds fine and changes nothing a visitor sees, because it quietly creates a second service the domain does not point at.

`--source .` uploads the working directory as it stands, not the last commit, so deploy from a clean checkout of `main` or you ship whatever you were editing.

If the deploy stops on `Missing required argument [--clear-base-image]`, the service is still set to let Cloud Run manage a base image for it, which a Dockerfile build cannot do. Add `--clear-base-image` once; the setting stays cleared.

### Deploying from GitHub instead

`.github/workflows/prove-and-publish.yml` runs the two rites above. **Prove** checks every pull request and every push to `main`. **Publish** deploys, and runs only on `main`, only once Prove is green, and only once the Google side exists.

Set that up once, from Cloud Shell:

```bash
bash scripts/setup-github-deploy.sh
```

It creates a deployer account and a Workload Identity provider locked to this repository, then prints three values to paste into GitHub as **Variables** (not Secrets) under Settings → Secrets and variables → Actions. No key is created, so no key can leak. Until those variables exist, Publish skips and `main` stays green.

Two ways to deploy once it is wired: push to `main`, or press **Run workflow** on the Actions tab. Add a `production` Environment with yourself as a required reviewer if the deploy should wait for your word; without one, GitHub publishes without asking.
