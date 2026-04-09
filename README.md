# Formalator 🔄

**Bidirectional Text Translator** — A web app and Telegram bot that transforms text between formal and informal styles using LLM.

## Features

-  **Web Interface** — Clean React UI with side-by-side comparison
- 🔄 **Bidirectional Translation** — Switch between Formal → Informal and Informal → Formal
- 🤖 **Telegram Bot** — Translate text on the go via Telegram with `/mode` command
- 🔌 **LLM-Powered** — Uses OpenAI-compatible API for high-quality translations
- 🐳 **Docker-Ready** — One-command deployment with docker-compose

## Version 2 — What's New

- **Bidirectional translation**: Translate both ways (formal↔informal)
- **Web UI**: Direction toggle button group with dynamic labels and examples
- **API**: New `direction` parameter in `/api/translate` endpoint
- **Telegram Bot**: New `/mode` command to switch translation direction

## Architecture

```
┌──────────────┐     ┌──────────────────────┐
│  Website     │────▶│  FastAPI Backend       │
│  (React)     │◀────│  (translation logic)   │
└──────────────┘     └──────┬───────────────┘
                            │
┌──────────────┐     ┌──────┴───────────────┐
│  Telegram    │────▶│  Telegram Bot          │
│  User        │◀────│  (aiogram)             │
└──────────────┘     └──────────────────────┘
                            │
                     ┌──────┴───────┐
                     │  LLM API     │
                     │  (OpenAI-    │
                     │  compatible) │
                     └──────────────┘
```

## Tech Stack

- **Backend**: FastAPI + httpx (LLM client)
- **Frontend**: React 18 + Vite + TypeScript + Bootstrap 5
- **Telegram Bot**: aiogram 3.x
- **LLM**: OpenAI-compatible API (same pattern as se-toolkit-lab-7)

## Quick Start

### Prerequisites

- [uv](https://docs.astral.sh/uv/) for Python package management
- Node.js 20+ and pnpm for frontend
- Access to an OpenAI-compatible LLM API

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Formalator
```

### 2. Configure Environment

```bash
# Copy example env files
cp .env.example .env
cp .env.bot.example .env.bot.secret

# Edit .env and .env.bot.secret with your LLM API credentials
```

Edit the files and set:
- `LLM_API_KEY` — Your LLM API key
- `LLM_API_BASE_URL` — Base URL of your LLM API (e.g., `http://localhost:42005/v1`)
- `LLM_API_MODEL` — Model name (e.g., `coder-model`)
- `BOT_TOKEN` — Telegram bot token from @BotFather (for bot only)

### 3. Run Locally (Development)

#### Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

Backend runs at `http://localhost:8000`. API docs at `http://localhost:8000/docs`.

#### Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

Frontend runs at `http://localhost:5173`.

#### Telegram Bot

```bash
cd bot
uv sync
uv run bot.py --test "/start"  # Test mode
uv run bot.py                   # Normal mode (connects to Telegram)
```

### 4. Deploy with Docker

```bash
# Build and start all services
docker compose --env-file .env.bot.secret up --build -d

# Check services
docker compose ps

# View logs
docker compose logs backend --tail 20
docker compose logs bot --tail 20
```

Services:
- **Frontend**: `http://localhost:80`
- **Backend API**: `http://localhost:8000`
- **Telegram Bot**: Running and polling for messages

### Stop Services

```bash
docker compose down
```

## API Endpoints

### POST `/api/translate`

Translate text between formal and informal styles.

**Request:**
```json
{
  "text": "I would like to inquire about the status of my order.",
  "direction": "formal_to_informal"
}
```

**Direction options:**
- `formal_to_informal` (default): Makes text casual and conversational
- `informal_to_formal`: Makes text professional and formal

**Response:**
```json
{
  "original": "I would like to inquire about the status of my order.",
  "translated": "Hey, can you check what's up with my order?",
  "direction": "formal_to_informal"
}
```

### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "service": "formalator-api"
}
```

## Telegram Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message |
| `/help` | Show help and examples for current mode |
| `/mode <direction>` | Switch translation direction (formal→informal or informal→formal) |
| `/translate <text>` | Translate specific text |

You can also just send any text message and the bot will translate it using the current mode.

### Telegram Bot Modes

Use `/mode` to switch directions:

```
/mode formal→informal   # Make text casual
/mode informal→formal   # Make text formal
```

## Project Structure

```
Formalator/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py       # FastAPI app entry point
│   │   ├── translate.py  # Translation endpoint
│   │   └── llm_client.py # LLM API client
│   ├── tests/
│   │   └── test_translate.py
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/             # React web interface
│   ├── src/
│   │   ├── main.tsx      # React entry point
│   │   └── App.tsx       # Main component
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── bot/                  # Telegram bot
│   ├── bot.py            # Bot entry point
│   ├── config.py         # Config loader
│   ├── handlers/
│   │   └── commands.py   # Command handlers
│   ├── services/
│   │   └── llm_client.py # LLM API client
│   ├── pyproject.toml
│   └── Dockerfile
├── docker-compose.yml    # Docker orchestration
├── .env.example          # Example backend env
├── .env.bot.example      # Example bot env
└── README.md
```

## Development

### Running Tests

```bash
# Backend tests
cd backend
uv run pytest

# With coverage
uv run pytest --cov=app
```

### Code Quality

```bash
# Format and lint
uv run ruff format
uv run ruff check

# Type checking
uv run pyright
```

## Troubleshooting

| Symptom | Likely Cause |
|---------|--------------|
| Translation returns API key error | Check `LLM_API_KEY` in `.env` or `.env.bot.secret` |
| Bot container keeps restarting | Missing `BOT_TOKEN` or import error — check logs |
| LLM queries fail | `LLM_API_BASE_URL` must use `host.docker.internal` in Docker |
| Frontend can't connect to backend | Ensure backend is running on port 8000 |
| Build fails at `uv sync --frozen` | `uv.lock` must exist — run `uv sync` first |

## License

MIT
