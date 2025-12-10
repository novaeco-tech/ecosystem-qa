# 🧪 NovaEco QA

This repository is the central integration testing "auditor" for the NovaEco.

Its purpose is **not** to run unit tests (which live inside each enabler/sector repo). Its sole purpose is to test the **final artifacts** to ensure they are deployable before they are marked as "Stable".

This repo acts as the "gate" that promotes "Pre-release" artifacts to "Stable."

## 🎯 What We Test

Currently, we run a **Universal Smoke Test** on every release candidate:

1.  **Download:** Fetches the exact `.tar.gz` artifact from the source repo.
2.  **Build:** Wraps it in a standard Docker container (using `Dockerfile.template`).
3.  **Run:** Starts the service in isolation.
4.  **Verify:** Checks the `/health` endpoint (or root `/` for websites).

*Future Roadmap:* We will expand this to run "User Journeys" (Inter-sector tests) like the "Coffee Shop" scenario where `NovaHub` talks to `NovaFin`.

## ⚙️ How It Works: The QA Workflow

1.  A repository (e.g., `ecosystem-core`) publishes a `v1.2.1` pre-release.
2.  Its workflow sends a **Signal** (`repository_dispatch`) to this repo with the `repo`, `tag`, and `artifact_name`.
3.  The **`qa-run.yml`** workflow starts automatically.
4.  It downloads the specific artifact.
5.  It builds a temporary test container using `ghcr.io/novaeco-tech/dev-python` (or Node).
6.  It performs a `curl` health check.
7.  **If successful:** It calls the GitHub API to **Promote** the release (removes `prerelease: true`), marking it ready for production.