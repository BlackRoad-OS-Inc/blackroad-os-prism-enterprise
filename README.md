[![Build](https://github.com/BlackRoad-OS/blackroad-os-prism-enterprise/actions/workflows/monorepo-matrix.yml/badge.svg)](https://github.com/BlackRoad-OS/blackroad-os-prism-enterprise/actions/workflows/monorepo-matrix.yml)
[![E2E](https://github.com/BlackRoad-OS/blackroad-os-prism-enterprise/actions/workflows/playwright.yml/badge.svg)](https://github.com/BlackRoad-OS/blackroad-os-prism-enterprise/actions/workflows/playwright.yml)
[![Deploy](https://github.com/BlackRoad-OS/blackroad-os-prism-enterprise/actions/workflows/deploy-blackroad.yml/badge.svg)](https://github.com/BlackRoad-OS/blackroad-os-prism-enterprise/actions/workflows/deploy-blackroad.yml)
[![Node ≥ 20](https://img.shields.io/badge/node-%3E%3D20-brightgreen)](https://nodejs.org)
[![License](https://img.shields.io/badge/license-UNLICENSED-red)](LICENSE)

# 🖤 BlackRoad Prism Console — Enterprise

**BlackRoad Prism Console** is a production-grade, AI-powered enterprise operating platform combining a Node.js/Express API, React/Vite front-end, Stripe billing, Playwright E2E testing, and a multi-agent orchestration layer — all in one monorepo.

> **Current version:** `1.0.0` · **Node:** `>=20` · **API port:** `4000` · **Frontend port:** `5173`

---

## Table of Contents

1. [Repository Layout](#1-repository-layout)
2. [Quick Start](#2-quick-start)
3. [Environment Variables](#3-environment-variables)
4. [npm Scripts Reference](#4-npm-scripts-reference)
5. [Stripe Integration](#5-stripe-integration)
6. [E2E Testing (Playwright)](#6-e2e-testing-playwright)
7. [Module Index](#7-module-index)
   - [srv/ — Back-end Services](#srv--back-end-services)
   - [sites/ — Front-end Sites](#sites--front-end-sites)
   - [apps/ — Standalone Apps](#apps--standalone-apps)
   - [packages/ — Shared Libraries](#packages--shared-libraries)
   - [stripe-seed/ — Billing Seeder](#stripe-seed--billing-seeder)
   - [e2e/ — End-to-End Tests](#e2e--end-to-end-tests)
   - [ops/ — Operations & Tooling](#ops--operations--tooling)
   - [docs/ — Documentation](#docs--documentation)
8. [Production Deployment](#8-production-deployment)
9. [Contributing](#9-contributing)
10. [Security](#10-security)
11. [License](#11-license)

---

## 1. Repository Layout

```
blackroad-os-prism-enterprise/
├── srv/                        # Back-end services (Express, FastAPI, etc.)
│   ├── blackroad-api/          # ★ Primary API — entry: server_full.js (port 4000)
│   ├── lucidia-llm/            # LLM bridge stub (FastAPI, default port 8000)
│   └── …                       # Additional micro-services
├── sites/                      # Front-end sites
│   └── blackroad/              # ★ Marketing / console UI (Vite + React, port 5173)
├── apps/                       # Standalone applications
├── packages/                   # Shared npm libraries
├── stripe-seed/                # Stripe test-mode data seeder
├── e2e/                        # Playwright end-to-end tests
├── ops/                        # Ops scripts, install helpers
├── docs/                       # Extended documentation
├── server_full.js              # Root API entry point
├── package.json                # Root workspace manifest
├── .env.example                # ★ Canonical environment variable reference
├── docker-compose.yml          # Local orchestration (ports 4000 / 5173 / 8000)
├── docker-compose.prod.yml     # Production compose override
├── docker-compose.prism.yml    # Prism console stack
├── docker-compose.site.yml     # Front-end only stack
└── docker-compose.dashboard.yml# Observability / dashboard stack
```

---

## 2. Quick Start

### Prerequisites

- **Node.js** `>=20` ([nvm](https://github.com/nvm-sh/nvm) recommended — see `.nvmrc`)
- **npm** `>=10`
- A Stripe **test** secret key (`sk_test_…`) — only needed for billing features

### Bootstrap

```bash
# 1. Clone
git clone https://github.com/BlackRoad-OS/blackroad-os-prism-enterprise.git
cd blackroad-os-prism-enterprise

# 2. Install all workspace dependencies
bash ops/install.sh          # recommended — creates .env from .env.example too
# OR manually:
npm install

# 3. Copy and configure environment
cp .env.example .env
# Edit .env and fill in STRIPE_SECRET_KEY, JWT_SECRET, etc.

# 4. Seed the database (first run)
npm run seed

# 5. Start the API (development)
cd srv/blackroad-api && npm run dev
# API available at http://localhost:4000

# 6. Start the front-end (separate terminal, from repo root)
npm run dev:site
# UI available at http://localhost:5173
```

### Docker (all-in-one)

```bash
docker compose up --build
# API  → http://localhost:4000
# UI   → http://localhost:5173
# LLM  → http://localhost:8000
```

---

## 3. Environment Variables

All variables are documented in [`.env.example`](.env.example). Copy it to `.env` before starting:

```bash
cp .env.example .env
```

Key variables:

| Variable | Default | Description |
|---|---|---|
| `NODE_ENV` | `development` | Runtime environment |
| `PRISM_API_PORT` | `4000` | API listen port |
| `PORT` | `3000` | Next.js / frontend port |
| `BLACKROAD_API_URL` | `http://localhost:4000` | API base URL consumed by UI |
| `JWT_SECRET` | — | **Required** — JWT signing secret |
| `STRIPE_SECRET_KEY` | — | Stripe secret key (`sk_live_…` / `sk_test_…`) |
| `STRIPE_WEBHOOK_SECRET` | — | Stripe webhook signing secret (`whsec_…`) |
| `STRIPE_PUBLIC_KEY` | — | Stripe publishable key (`pk_live_…` / `pk_test_…`) |
| `STRIPE_PRICE_*` | — | Price IDs for each plan tier / billing period |
| `LLM_URL` | `http://127.0.0.1:8000` | LLM bridge base URL |
| `DB_PATH` | `./blackroad.db` | SQLite database path |
| `LOG_LEVEL` | `info` | Logging verbosity |

> See [`.env.example`](.env.example) for the full list including observability, auth, and feature-flag variables.

---

## 4. npm Scripts Reference

Run from the **repo root** unless otherwise noted.

| Script | Command | Description |
|---|---|---|
| Start API | `npm start` | Run `server_full.js` in production mode |
| Dev API | `cd srv/blackroad-api && npm run dev` | Nodemon-watched dev server |
| Dev site | `npm run dev:site` | Vite dev server for `sites/blackroad` |
| Build site | `npm run site:build` | Production build of the front-end |
| Seed DB | `npm run seed` | Create admin user and base data |
| Health | `npm run health` | Quick health-check against running API |
| Lint | `npm run lint` | ESLint across `*.js / *.jsx / *.mjs` |
| Format | `npm run format` | Prettier write |
| Format check | `npm run format:check` | Prettier diff (CI) |
| Unit tests | `npm test` | Jest |
| API smoke | `npm run test:api` | Smoke test against running API |
| Compliance | `npm run test:compliance` | Vitest compliance suite |
| E2E | `cd e2e && npx playwright test` | Full Playwright E2E suite |
| Stripe seed | `cd stripe-seed && npm run seed` | Seed Stripe test account |

---

## 5. Stripe Integration

BlackRoad Prism Console uses **Stripe** for subscription billing.

### Plans

| Plan | Monthly Price ID | Yearly Price ID |
|---|---|---|
| Builder | `STRIPE_PRICE_BUILDER_MONTH` | `STRIPE_PRICE_BUILDER_YEAR` |
| Pro | `STRIPE_PRICE_PRO_MONTH` | `STRIPE_PRICE_PRO_YEAR` |
| Enterprise | `STRIPE_PRICE_ENTERPRISE_MONTH` | `STRIPE_PRICE_ENTERPRISE_YEAR` |

### Setup

```bash
# 1. Set your keys in .env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# 2. Seed test data (creates products, prices, customers, subscriptions)
cd stripe-seed
cp .env.example .env   # add your sk_test_ key
npm install
npm run seed

# 3. Forward webhooks locally (requires Stripe CLI)
stripe listen --forward-to localhost:4000/webhooks/stripe
```

### Webhook Security

All webhook events are validated against `STRIPE_WEBHOOK_SECRET` using Stripe's official signature verification. **Never** disable signature verification in production.

> See [`stripe-seed/README.md`](stripe-seed/README.md) for full seeder documentation.

---

## 6. E2E Testing (Playwright)

End-to-end tests live in [`e2e/`](e2e/) and run against a live API instance.

```bash
# Install Playwright browsers (first time)
cd e2e && npx playwright install --with-deps chromium

# Run all E2E tests (API must be running on port 4000)
npx playwright test

# Run with UI mode
npx playwright test --ui

# Run a single spec
npx playwright test specs/smoke.spec.ts

# View last report
npx playwright show-report
```

`BASE_URL` defaults to `http://localhost:4000`. Override for staging/production:

```bash
BASE_URL=https://staging.console.blackroad.io npx playwright test
```

> **CI:** E2E tests run automatically on every PR via the [Playwright workflow](https://github.com/BlackRoad-OS/blackroad-os-prism-enterprise/actions/workflows/playwright.yml).

---

## 7. Module Index

### `srv/` — Back-end Services

| Service | Entry Point | Port | Description |
|---|---|---|---|
| `blackroad-api` | `server_full.js` | `4000` | Primary REST + Socket.IO API, SQLite |
| `lucidia-llm` | FastAPI app | `8000` | LLM bridge (configurable via `LLM_URL`) |
| `blackroad-analytics` | — | — | Analytics aggregation service |
| `blackroad-backend` | — | — | Auxiliary background workers (data sync, queue consumers) |
| `lucidia-monitor` | — | — | System health monitor |

### `sites/` — Front-end Sites

| Site | Framework | Port | Description |
|---|---|---|---|
| `sites/blackroad` | Vite + React | `5173` | ★ Main marketing & console UI |
| `sites/blackroad-next` | Next.js | `3000` | Next.js variant |

### `apps/` — Standalone Apps

| App | Description |
|---|---|
| `blackroad-prism-console` | Prism console web app |
| `blackroad-landing` | Landing page |
| `blackroad-website` | Corporate website |

### `packages/` — Shared Libraries

Shared TypeScript/JavaScript utilities consumed across the monorepo via npm workspaces.

### `stripe-seed/` — Billing Seeder

Stripe test-mode data seeder. Creates products, prices, customers, and subscriptions.
See [`stripe-seed/README.md`](stripe-seed/README.md).

### `e2e/` — End-to-End Tests

Playwright test suite. Config: [`e2e/playwright.config.ts`](e2e/playwright.config.ts).

| File | Description |
|---|---|
| `e2e/specs/smoke.spec.ts` | API health smoke test |

### `ops/` — Operations & Tooling

| Script | Description |
|---|---|
| `ops/install.sh` | Bootstrap: install deps, create `.env` |
| `ops/README.md` | Ops documentation |

### `docs/` — Documentation

| Document | Description |
|---|---|
| [`docs/README_SELF_HOSTING.md`](docs/README_SELF_HOSTING.md) | Self-hosting guide |
| [`docs/README_SOVEREIGN.md`](docs/README_SOVEREIGN.md) | Sovereign deployment guide |
| [`PRODUCTION_DEPLOYMENT_CHECKLIST.md`](PRODUCTION_DEPLOYMENT_CHECKLIST.md) | Pre/post-deployment checklist |
| [`QUICKSTART.md`](QUICKSTART.md) | 5-minute quick-start |
| [`SECURITY.md`](SECURITY.md) | Security policy |
| [`CHANGELOG.md`](CHANGELOG.md) | Version history |
| [`RUNBOOK.md`](RUNBOOK.md) | Operational runbook |
| [`DEPLOYMENT.md`](DEPLOYMENT.md) | Deployment reference |

---

## 8. Production Deployment

See [`PRODUCTION_DEPLOYMENT_CHECKLIST.md`](PRODUCTION_DEPLOYMENT_CHECKLIST.md) for the complete pre/post-deployment checklist.

**Key requirements before going live:**

- All secrets set in `.env` (no placeholders)
- `STRIPE_WEBHOOK_SECRET` configured and signature validation active
- `JWT_SECRET` is a cryptographically random value (≥32 chars)
- `NODE_ENV=production`
- SSL/TLS terminated at the load balancer or reverse proxy
- Docker image built with `Dockerfile.prod`

```bash
# Production build and start
NODE_ENV=production npm start

# Or via Docker
docker compose -f docker-compose.prod.yml up -d
```

> CI/CD: the [deploy workflow](https://github.com/BlackRoad-OS/blackroad-os-prism-enterprise/actions/workflows/deploy-blackroad.yml) handles staging and production rollouts automatically.

---

## 9. Contributing

Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before submitting a pull request.

**Dependency hygiene:** do **not** manually edit `package.json` for packages.
Use the provided tooling:

```bash
node tools/dep-scan.js --dir srv/blackroad-api
# or
bash ops/install.sh
```

---

## 10. Security

- Report vulnerabilities via [`SECURITY.md`](SECURITY.md).
- Secrets must **never** be committed — `.env` is in `.gitignore`.
- Stripe webhook signatures are verified on every inbound event.
- See [`HARDENING.md`](HARDENING.md) for infrastructure hardening guidance.

---

## 11. License

`UNLICENSED` — Proprietary. All rights reserved. See [`LICENSE`](LICENSE).

---

> 🖤 **BlackRoad OS** — Built for production, engineered for scale.
