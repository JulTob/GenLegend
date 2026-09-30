# QST-0143 — Vercel support

- **Type:** infrastructure · deployment
- **Priority:** 🟡 medium
- **Status:** Done — deployed, `https://gen-legend.vercel.app` serves the generator (2026-09-30)
- **Owner:** unclaimed
- **Route to:** Infrastructure (Artificer) · Simplicity (Monk)
- **Related:** Decree 0009 · QST-0090 (one `main`) · `README.md` Deploy

---

## 🔍 Diagnosis (what & where)

The site was published in one place only: Cloud Run, from the `Dockerfile`,
deployed by `.github/workflows/prove-and-publish.yml` over Workload Identity
Federation. No key exists anywhere.

Vercel was asked for as a second publishing target. Nothing in the repository
mentioned it: no `vercel.json`, no `/api` directory, no Python entrypoint file
outside the package.

The obstacle worth naming: `app/main.py` is a Shiny application, and Shiny is
a plain ASGI callable, not FastAPI or Flask. Whether Vercel would find it at all
was the open question.

## ✅ What was checked (evidence, not assumption)

1. **Which files Vercel considers an entrypoint.**
   `@vercel/python@17.0.2`, `dist/index.js` around line 7512:

   ```js
   var PYTHON_ENTRYPOINT_FILENAMES = ["app", "index", "server", "main", "wsgi", "asgi"];
   var PYTHON_ENTRYPOINT_DIRS = ["", "src", "app", "api"];
   ```

   `app` is both a directory and a filename in that list, so `app/main.py` is a
   candidate with no shim, no re-export and no new file.

2. **Whether that file really exports an entrypoint.** The builder parses the
   source with `findAppOrHandler` from `@vercel/python-analysis`. Run against
   this checkout, replicating the builder's own candidate walk:

   ```
   candidate app/main.py -> app
   VERCEL ENTRYPOINT = { p: 'app/main.py', v: 'app' }
   ```

   So `app = Shareable_Path_Redirect(_shiny_app)` at module level is what
   Vercel loads. `Minion.py` is not a candidate at all.

3. **That all routes reach it.** Framework `python`, `packages/frameworks/src/frameworks.ts`
   line 4346: `defaultRoutes` are `filesystem` then `/(.*)` → `/`, and the
   builder emits a catch-all with `transforms: [{type: 'request.path', op: 'set',
   args: '/$1'}]`, so the app sees the original path, not `/`.

4. **That the paths that matter work.** Booted `app.main:app` under uvicorn,
   the same server Vercel uses (`vercel_runtime/vc_init.py` line 1236 runs ASGI
   through uvicorn with `lifespan="auto"`, so Shiny's lifespan is honoured):

   | Request | Result |
   | --- | --- |
   | `GET /` | 200, 68,940 bytes of generator HTML |
   | `GET /static/style.css` | 200, 54,923 bytes |
   | `GET /character?species=orc&guild=paladin` | 307 → `/` (the shareable redirect) |
   | `WS /websocket/` | connects, first frame `{"config": ...}` |

5. **That WebSockets are available.** Vercel shipped WebSocket support for
   Python Functions on 2026-07-23, public beta since 2026-06-22
   (<https://vercel.com/docs/functions/websockets>). It is a project setting,
   not a code change.

## 🎯 What landed

- `vercel.json` — `maxDuration` 300, and `excludeFiles` dropping the 30 MB the
  app never imports (`.recovery-vault`, `Curia`, `Documenta`, `Avatar`,
  `SpellsEffects`, `Enchantments`, the map SVGs).
- `.gitignore` — `.vercel/`, the per-machine project link.
- `README.md` — the Vercel section under Deploy.

The exclude list was checked against the code: no runtime module imports
`Curia`, `Documenta`, `Avatar`, `SpellsEffects`, `Enchantments` or
`AtlasWorldBuild`, and no module reads a `.md` at runtime. `scripts/verify_aasimar_page.py`
reads `Documenta/Canon/Mythos/Aasimar.md`, and it is a proof script, not the app.

## 🌍 Result

The project is connected and live: `https://gen-legend.vercel.app` serves the
generator (2026-09-30). The unproven parts of section 4 — that a real Vercel
project accepts the bundle, and that the WebSocket at `/websocket/` comes up —
are now answered by a live deployment, not by inference.

This checkout cannot reach the host to double-check it: DNS resolves
(`216.198.79.3`, `64.29.17.3`) but both edge IPs time out from here, so the
live check is the browser's, not this machine's.

**Nothing so far involves Julio.** The connection, the build and the report are
the repo owner's. Julio's one possible act here is adding a custom domain to
the Vercel project — Settings → Domains — if `genlegend.eu` is ever to be
served from Vercel instead of Cloud Run. He can do that whenever he wants; no
code waits on it.

## 🧭 Left open

- **Session survival across a Fluid Compute recycle.** The generator holds
  session state in memory and one WebSocket. Whether a recycled instance drops
  a live sheet mid-generation, or Shiny's reconnect covers it, was not tested
  and no evidence exists either way.
- Cloud Run is untouched: `Dockerfile`, `prove-and-publish.yml` and the
  `genlegend.eu` service still publish from `main`. Which host the domain
  should point at is a separate call, and no deploy files were deleted.