# 🧪 Ecosystem QA Hub

This repository is the central integration testing "auditor" for the Nova Ecosystem.

Its purpose is **not** to run unit tests (which live inside each enabler/sector repo). Its sole purpose is to test the **"seams" *between* repositories** to ensure all our decoupled services work together as a unified system.[3, 4]

This repo acts as the "gate" that promotes "Pre-release" artifacts to "Stable."

## 🎯 What We Test

1.  **Intra-Enabler/Sector:** (`/tests/intra_...`)
      * **Purpose:** Tests the connection between a monorepo's core services and its own decoupled workers.
      * **Example:** Does the `balance` monorepo (API) correctly receive and process data from the `balance-worker-air` repo?
2.  **Inter-Enabler/Sector:** (`/tests/inter_...`)
      * **Purpose:** Tests the "user journeys" that cross multiple repositories.
      * **Example:** The "Coffee Shop" use case. Can the `hub` enabler create a project that successfully books logistics from the `mobility` enabler and triggers a payment in the `finance` enabler?

## ⚙️ How It Works: The QA Workflow

1.  A repository (e.g., `hub`) publishes a `hub-v1.5.0` pre-release.[5, 6, 7]
2.  Its workflow sends a `repository_dispatch` to this repo, specifying the `tag_name` and `test_suite` to run.[1]
3.  The `qa-run.yml` workflow starts.
4.  It downloads the `hub-v1.5.0` artifacts (`.tar.gz`) and the "latest stable" artifacts for other services.
5.  It uses Docker Compose to *assemble* test images by combining the **Private Runtime** (from `circular-engineering`) with the **Public Artifacts** (the `.tar.gz` files).
6.  It runs the specified tests (e.g., `pytest /tests/inter_sector/test_coffee_shop_journey.py`).
7.  If tests pass, it calls the `qa-promote.yml` workflow to promote the `hub-v1.5.0` release by setting `prerelease: false`.[8, 2]