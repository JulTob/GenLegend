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

**Merging a pull request into `main` publishes the site.** That is the whole procedure. GitHub proves the code first, then deploys it. The change is live in about five minutes.

To republish without changing code: Actions → **Prove and Publish** → **Run workflow**, branch `main`.

### Reading the result

Two jobs run. **Prove** checks every pull request and every push to `main`. **Publish** deploys, and only from `main`, and only once Prove is green.

A green tick means the robot finished, not that the site changed. Open `genlegend.eu` and look at the thing you changed. Hard-refresh (`Ctrl+Shift+R`) before believing the page is unchanged.

Publish showing **`skipped`** in grey is not a failure. It skips on every pull request, by design, because only `main` publishes. If it skips on a push to `main`, the three variables below are missing.

### The three variables

Settings → Secrets and variables → Actions → **Variables**. Variables, not Secrets: none of them is a password, and hiding them only makes the next failure harder to read.

| Name | Value |
| --- | --- |
| `GCP_PROJECT_ID` | `gen-legend` |
| `GCP_SERVICE_ACCOUNT` | `github-deployer@gen-legend.iam.gserviceaccount.com` |
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | `projects/1068852386499/locations/global/workloadIdentityPools/github/providers/github` |

Set once, on 21 September 2026, by `scripts/setup-github-deploy.sh`. **No key exists anywhere.** GitHub proves who it is, and Google answers with a token good for minutes — so there is nothing long-lived to leak. If the variables are ever lost, re-run that script from Cloud Shell; it is safe to repeat and prints them again.

### Deploying by hand

Only when GitHub cannot, or to test a build before it is committed:

```bash
gcloud run deploy gen-legends --source . --region us-central1 --allow-unauthenticated
```

**The service is `gen-legends`, with an s.** `genlegend.eu` maps to it, and to nothing else. Deploying to `gen-legend` builds fine and changes nothing a visitor sees, because it quietly creates a second service the domain does not point at.

`gen-legend`, without the s, is the Google Cloud *project* — the box that holds the service, the billing and the permissions. Both names are correct, one layer apart. The service URL spells the nesting out: `gen-legends-1068852386499.us-central1.run.app` is the service, then the project's number. The `s` is a plural somebody typed in 2023, not an abbreviation for anything.

`--source .` uploads the working directory as it stands, not the last commit, so deploy from a clean checkout of `main` or you ship whatever you were editing. The GitHub route has no such trap: it always deploys the commit.

If the deploy stops on `Missing required argument [--clear-base-image]`, the service is still set to let Cloud Run manage a base image for it, which a Dockerfile build cannot do. Add `--clear-base-image` once; the setting stays cleared.

### Container

```bash
docker build --build-arg BUILD_SHA=$(git rev-parse --short HEAD) -t gen-legends .
docker run -p 8080:8080 gen-legends
```

Cloud Run builds this same Dockerfile.

### A pause button, if you ever want one

By default `main` publishes by itself. To make it wait for your word instead: Settings → Environments → New environment, named exactly `production`, then tick **Required reviewers** and add yourself. Publish then stops and emails you until you approve. Untick to go back to automatic.
