# Data Engineering Basic

Python 3.12 workspace with PostgreSQL 16 and JupyterLab for SQL and batch-pipeline projects.

This is a **ProjLabs Local Lab** template (template version 1). Everything runs on your own
machine or in your own GitHub Codespace, using free and open-source software. No ProjLabs account,
cloud bill or vendor lock-in is involved.

## What's inside

| Service | Image | Purpose | Port |
|---------|-------|---------|------|
| workspace | `mcr.microsoft.com/devcontainers/python:1-3.12-bookworm` | Python 3.12, JupyterLab, your code | 8888 (JupyterLab) |
| postgres | `postgres:16.15-bookworm` | PostgreSQL 16 with the `sample` schema | internal only |

Python 3.12 with the pinned packages in `requirements.txt`. Your code goes in `src/` (it is on
`PYTHONPATH`, so notebooks and scripts can import it), tests in `tests/`, local data files in `data/` (git-ignored).

Recommended machine: **2 CPUs and 4 GB of memory** available to Docker.

## Start the lab

Pick **one** of these. All three use the same `compose.yaml`, so the environment is identical.

### 1. GitHub Codespaces (nothing to install)

1. On this repository's GitHub page choose **Code → Codespaces → Create codespace on main**
   (or **⋯ → New with options** to pick a machine with at least 2 cores).
2. Wait for the first build (a few minutes; later starts are faster). VS Code opens in the browser.
3. Forwarded ports appear in the **Ports** tab. They are private to you by default; keep them that way.

Codespaces includes a free monthly allowance for personal accounts; stop the codespace when you are
done (**Codespaces: Stop Current Codespace**) so it does not use your quota.

### 2. VS Code with Dev Containers (local)

1. Install Docker (Docker Desktop, or Docker Engine + Compose v2 on Linux), VS Code, and the
   **Dev Containers** extension (`ms-vscode-remote.remote-containers`).
2. Clone this repository and open the folder in VS Code.
3. Run **Dev Containers: Reopen in Container**. The first build downloads images and installs packages.

### 3. Docker Compose only (any editor)

```sh
cp .env.example .env            # optional: only if you want to change a default
docker compose up -d --build --wait
docker compose exec workspace bash
```

Open JupyterLab at <http://127.0.0.1:8888> (token: `projlab`, or your `JUPYTER_TOKEN`).
Stop with `docker compose stop`; your data is kept in Docker volumes.

## Verify the environment

Run this in the workspace terminal (VS Code/Codespaces terminal, or after `docker compose exec workspace bash`):

```sh
python -m pytest -q tests/test_environment.py
```

Every test should pass. A failure names the service that is not reachable; see *Reset* below.
From outside the container you can run `docker compose exec workspace python -m pytest -q tests/test_environment.py`.

## Working in this lab

- The sample data lives in the `sample` schema (`sample.customers`, `sample.orders`). It is loaded from
  `db/init/01-sample.sql` the first time the database volume is created.
- Connect from Python in the workspace:

  ```python
  import os, psycopg
  conn = psycopg.connect(host="postgres", user=os.environ["POSTGRES_USER"],
                         password=os.environ["POSTGRES_PASSWORD"], dbname=os.environ["POSTGRES_DB"])
  conn.execute("SELECT * FROM sample.orders").fetchall()
  ```

- In VS Code, the SQLTools extension can connect with host `postgres`, port `5432`, and the credentials above.


## Reset

| What | How |
|------|-----|
| Restart one service | `docker compose restart <service>` (e.g. `postgres`) |
| Restart everything | `docker compose restart`, or in VS Code **Dev Containers: Rebuild Container** / in Codespaces **Codespaces: Rebuild Container** |
| Rebuild the workspace after changing `requirements.txt` | Rebuild the container (as above), or `docker compose up -d --build workspace` |
| Reset the sample database and all lab data | `docker compose down -v && docker compose up -d --wait` from a terminal on your machine. In Codespaces use **Codespaces: Full Rebuild Container** (it removes the codespace's Docker volumes). |

Resetting deletes data stored in the lab's Docker volumes only. Files in this repository (your code,
notebooks, `data/`) are never touched.

## Save your work to GitHub

- Create your own copy with **Use this template → Create a new repository** on GitHub (or fork it), then
  open *your* repository in Codespaces or clone it locally.
- Commit and push as usual: `git add -A && git commit -m "Finish milestone 1" && git push`.
  The GitHub CLI (`gh`) is installed in the dev container (`gh auth status`).
- `data/` and `.env` are git-ignored on purpose. Commit small sample files with `git add -f data/<file>`.
- The included `.github/workflows/ci.yml` runs your unit tests on every push (service tests are skipped there).

## Secrets

- Never commit passwords or API keys. `.env` is git-ignored; `.env.example` holds placeholders only.
- The database passwords in this lab are local-only development defaults. Nothing is exposed to the
  internet: published ports bind to `127.0.0.1`, and Codespaces ports are private unless you change them.
- In Codespaces, store real keys as **Codespaces secrets** (GitHub → Settings → Codespaces → Secrets,
  scoped to this repository); they appear as environment variables in the workspace.
- Locally, put them in `.env`; compose passes `.env` into the workspace container.

## Known limitations

- No GPU.
- PostgreSQL is not published to your machine by default; connect from the workspace (host `postgres`).
- Sample data is small and synthetic.

## Troubleshooting

- **Port already in use**: another program uses that port on your machine. Stop it, or set a different
  host port in `.env` (see `.env.example`), then `docker compose up -d`.
- **Docker is not running**: start Docker Desktop (or `sudo systemctl start docker`) and retry.
- **Permission denied writing files (Linux, plain Docker Compose)**: the workspace runs as user `vscode`
  (uid 1000). If your Linux user has a different uid, use the Dev Containers path (it remaps the uid), or
  run `sudo chown -R 1000:1000 .` on a disposable clone.
- **Services unhealthy**: `docker compose ps` shows health; `docker compose logs <service>` shows why.
