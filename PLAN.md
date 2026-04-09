# Formalator — Implementation Plan

## Project Overview

**Goal:** Build a formal-to-informal text translation system with three interfaces:
1. **FastAPI Backend** — REST API for text translation
2. **React Website** — Web UI with side-by-side comparison
3. **Telegram Bot** — Chat-based translation on the go

All three components use the same LLM backend (OpenAI-compatible API) for translation.

---

## Architecture

```
┌──────────────┐     ┌──────────────────────┐
│  Website     │────▶│  FastAPI Backend     │
│  (React)     │◀────│  (translation logic) │
└──────────────┘     └──────┬───────────────┘
                            │
┌──────────────┐     ┌──────┴───────────────┐
│  Telegram    │────▶│  Telegram Bot        │
│  User        │◀────│  (aiogram)           │
└──────────────┘     └──────────────────────┘
                            │
                     ┌──────┴───────┐
                     │  LLM API     │
                     │  (OpenAI-    │
                     │  compatible) │
                     └──────────────┘
```

### Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI + httpx + python-dotenv |
| Frontend | React 18 + Vite + TypeScript + Bootstrap 5 |
| Telegram Bot | aiogram 3.x + httpx + python-dotenv |
| LLM | OpenAI-compatible API (same as se-toolkit-lab-7) |
| Deployment | Docker + docker-compose |

---
## Version 1
- User enters formal text and bot translates it into informal

## Version 2
- **Bidirectional translation**: User may choose to translate formal text to informal or backwards
- **Web UI**: Added direction toggle button group (Formal → Informal / Informal → Formal)
- **API**: `POST /api/translate` now accepts optional `direction` parameter (defaults to `formal_to_informal`)
- **Telegram Bot**: Added `/mode` command to switch between translation directions
- **System prompts**: Two separate prompts — one for formal→informal, one for informal→formal
- **Examples**: Different example sets shown based on current direction

## Step 1: Scaffold Project Structure

### What to create

- **Root files**: `pyproject.toml`, `docker-compose.yml`, `.env.example`, `.env.bot.example`, `.gitignore`, `README.md`
- **`backend/`**: FastAPI app with translation endpoint
- **`frontend/`**: React + Vite project
- **`bot/`**: aiogram Telegram bot

### Key decisions

- Use `uv` for Python package management (same as Lab 7)
- Each component has its own `pyproject.toml` / `package.json`
- All services orchestrated via `docker-compose.yml`

---

## Step 2: Implement FastAPI Backend

### Files created

| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI app entry point, CORS middleware, `/health` endpoint |
| `backend/app/translate.py` | `POST /api/translate` endpoint with request/response models |
| `backend/app/llm_client.py` | LLM API client with translation system prompt |

### How it works

1. Client sends `POST /api/translate` with `{"text": "formal text here", "direction": "formal_to_informal"}`
2. Backend selects the appropriate system prompt based on `direction`
3. Backend constructs messages with the selected **system prompt** that instructs the LLM to translate in the chosen direction
4. LLM API is called via OpenAI-compatible `/chat/completions` endpoint
5. Response is returned as `{"original": "...", "translated": "...", "direction": "..."}`

### System prompts

The LLM is instructed with specific rules depending on direction:

**Formal → Informal:**
- Keep original meaning intact
- Use contractions (don't, can't, it's)
- Use casual vocabulary
- Be friendly and conversational
- Use simpler sentence structures

**Informal → Formal:**
- Keep original meaning intact
- Use proper grammar and complete sentences
- Avoid contractions
- Use formal vocabulary and professional tone
- Suitable for business emails, official documents

### Tests

- `test_health` — verifies `/health` returns `{"status": "ok"}`
- `test_translate_empty` — empty text returns empty response
- `test_translate_whitespace` — whitespace-only text is handled

---

## Step 3: Build React Frontend

### Files created

| File | Purpose |
|------|---------|
| `frontend/package.json` | Dependencies: React, Bootstrap |
| `frontend/vite.config.ts` | Vite config with `/api` proxy to backend |
| `frontend/tsconfig.json` | TypeScript strict mode |
| `frontend/index.html` | HTML entry point |
| `frontend/src/main.tsx` | React entry point, imports Bootstrap CSS |
| `frontend/src/App.tsx` | Main component with translation UI |

### UI Design

- **Header**: "Formalator" with tagline
- **Direction Toggle**: Button group to switch between "Formal → Informal" and "Informal → Formal"
- **Input panel** (left): Textarea for text + Translate/Clear buttons (labels change based on direction)
- **Output panel** (right): Displays translation result
- **Examples section**: Clickable example sentences that fill the input (examples change based on direction)
- **Footer**: Tech stack attribution

### How it works

1. User selects translation direction using the toggle buttons
2. User types text in the left panel
3. Clicks "Make Informal →" or "Make Formal →"
4. Frontend calls `POST /api/translate` with `{text, direction}`
5. Response appears in the right panel
6. User can click examples to try them instantly

---

## Step 4: Create Telegram Bot

### Files created

| File | Purpose |
|------|---------|
| `bot/bot.py` | Entry point with `--test` mode and Telegram polling |
| `bot/config.py` | Loads `.env.bot.secret` with BOT_TOKEN, LLM settings |
| `bot/handlers/commands.py` | `/start`, `/help`, `/translate` handlers |
| `bot/services/llm_client.py` | LLM API client (same system prompt as backend) |
| `bot/pyproject.toml` | Dependencies: aiogram, httpx, python-dotenv |

### Commands

| Command | Behavior |
|---------|----------|
| `/start` | Welcome message with instructions |
| `/help` | Help text with examples for current mode |
| `/mode <direction>` | Switch translation direction (formal→informal or informal→formal) |
| `/translate <text>` | Translates the provided text using current mode |
| *(any text)* | Automatically translates any plain text message using current mode |

### `--test` mode

The bot can be tested without connecting to Telegram:

```bash
uv run bot.py --test "/start"
uv run bot.py --test "/translate I would like to inquire about my order."
```

This prints the response directly to stdout — useful for development and debugging.

---

## Step 5: Dockerize All Services

### Dockerfiles

| Service | Base Image | Key Steps |
|---------|-----------|-----------|
| Backend | `python:3.12-slim` | `uv sync`, copy source, run uvicorn |
| Frontend | `node:20-alpine` → `nginx:alpine` | Multi-stage build: pnpm install → build → nginx |
| Bot | `python:3.12-slim` | `uv sync`, copy source, run bot.py |

### docker-compose.yml

Three services:

```yaml
services:
  backend:   # Port 8000, reads LLM_API_KEY from .env
  frontend:  # Port 80, depends on backend
  bot:       # No ports (polling mode), reads .env.bot.secret
```

### Environment files

| File | Used by | Contains |
|------|---------|----------|
| `.env` | backend, frontend | `LLM_API_KEY`, `LLM_API_BASE_URL`, `LLM_API_MODEL` |
| `.env.bot.secret` | bot | `BOT_TOKEN`, `LLM_API_KEY`, `LLM_API_BASE_URL`, `LLM_API_MODEL` |

> **Important**: In Docker mode, `LLM_API_BASE_URL` should use `host.docker.internal` instead of `localhost`.

---

## Step 6: How to Run

### Development mode

```bash
# Backend
cd backend && uv sync && uv run uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend && npm install && npm run dev

# Bot (test mode)
cd bot && uv sync && uv run bot.py --test "/start"

# Bot (live mode)
cd bot && uv run bot.py
```

### Docker deployment

```bash
# Configure environment
cp .env.example .env
cp .env.bot.example .env.bot.secret
# Edit both files with your API keys

# Deploy
docker compose --env-file .env.bot.secret up --build -d

# Check services
docker compose ps

# View logs
docker compose logs backend --tail 20
docker compose logs bot --tail 20

# Stop
docker compose down
```

---

## Step 7: Project Structure Summary

```
Formalator/
├── backend/                    # FastAPI translation API
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI app, CORS, /health
│   │   ├── translate.py        # POST /api/translate
│   │   └── llm_client.py       # LLM client + system prompt
│   ├── tests/
│   │   └── test_translate.py   # 3 unit tests
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/                   # React web interface
│   ├── src/
│   │   ├── main.tsx            # Entry point + Bootstrap import
│   │   └── App.tsx             # Main UI component
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
├── bot/                        # Telegram bot
│   ├── handlers/
│   │   ├── __init__.py
│   │   └── commands.py         # /start, /help, /translate
│   ├── services/
│   │   ├── __init__.py
│   │   └── llm_client.py       # LLM client (same prompt as backend)
│   ├── bot.py                  # Entry point + --test mode
│   ├── config.py               # .env loader
│   ├── pyproject.toml
│   └── Dockerfile
├── docker-compose.yml          # All 3 services
├── pyproject.toml              # Root workspace config
├── .env.example                # Backend env template
├── .env.bot.example            # Bot env template
├── .gitignore
└── README.md                   # Full documentation
```

---

## Key Design Patterns (from se-toolkit-lab-7)

1. **`--test` mode** — Bot can be tested without Telegram connection
2. **Handler layer** — Pure functions that return strings, no Telegram dependency
3. **Config loader** — Centralized env variable loading with fallback paths
4. **Shared LLM client** — Same system prompt in backend and bot
5. **OpenAI-compatible API** — Works with any LLM that supports the `/chat/completions` endpoint
