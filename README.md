# AI News Briefing MVP

Production-style MVP for a personalized AI news briefing web app with a Next.js frontend, FastAPI backend, PostgreSQL storage, mock-first news ingestion, scheduled briefing generation, audio playback, and safe voice upload boundaries.

## Stack

- Frontend: Next.js, React, TypeScript, Tailwind CSS
- Backend: FastAPI, SQLAlchemy, Alembic, APScheduler
- Data: PostgreSQL
- Audio: `espeak` server-side WAV generation with browser speech fallback
- Voice cloning: guarded provider abstraction with mock implementation
- Local runtime: Docker Compose

## Project Tree

```text
.
|-- backend
|   |-- app
|   |   |-- api
|   |   |-- core
|   |   |-- data
|   |   |-- db
|   |   |-- models
|   |   |-- schemas
|   |   |-- services
|   |   |-- tasks
|   |   `-- main.py
|   |-- alembic
|   |-- Dockerfile
|   `-- requirements.txt
|-- frontend
|   |-- app
|   |-- components
|   |-- lib
|   `-- Dockerfile
|-- docker-compose.yml
`-- README.md
```

## Setup

1. Copy `backend/.env.example` to `backend/.env` if you want local overrides.
2. Copy `frontend/.env.example` to `frontend/.env.local` if you want frontend overrides.
3. Run `docker compose up --build`.
4. Open `http://localhost:3000`.
5. Create an account, choose topics, save a schedule, and click `Generate briefing now`.

## What The MVP Includes

- User sign up and sign in with JWT auth
- Topic selection and user preference storage
- Daily schedule configuration
- Mock news ingestion from multiple seeded stories
- Normalization, deduplication via normalized title hashing, event clustering, and weighted ranking
- Briefing generation with:
  - Opening summary
  - `Your Focus Topics`
  - `Major Headlines You Should Still Know`
  - Closing summary
- On-demand generation API and UI
- Briefing history
- Server-generated WAV playback when `espeak` is available
- Voice sample upload flow with safe, user-owned voice boundaries

## Ranking Formula

Configured in [backend/app/core/config.py](/d:/CODE/code/forfun/News/backend/app/core/config.py) and applied in [backend/app/services/news_pipeline.py](/d:/CODE/code/forfun/News/backend/app/services/news_pipeline.py).

```text
final_score =
  a * topic_relevance +
  b * global_importance +
  c * recency +
  d * source_diversity +
  e * novelty
```

Behavior:

- Selected topics are boosted through `topic_relevance`.
- Global events can override the usual ordering when `global_importance` is extremely high.
- Content budget targets about 70% focus topics and 30% important general headlines.

## API Surface

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET|PUT /api/preferences`
- `GET|PUT /api/preferences/topics`
- `GET|PUT /api/preferences/schedule`
- `POST /api/briefings/generate`
- `GET /api/briefings`
- `GET /api/briefings/{id}`
- `GET /api/briefings/{id}/audio`
- `POST /api/voice/sample`
- `GET /api/voice`
- `GET /api/status`

## Plug-In Points

- Real news APIs: [backend/app/services/providers/news/factory.py](/d:/CODE/code/forfun/News/backend/app/services/providers/news/factory.py)
- LLM summarization: extend [backend/app/services/briefing_service.py](/d:/CODE/code/forfun/News/backend/app/services/briefing_service.py)
- TTS provider: [backend/app/services/providers/tts](/d:/CODE/code/forfun/News/backend/app/services/providers/tts)
- Voice cloning provider: [backend/app/services/providers/voice_clone](/d:/CODE/code/forfun/News/backend/app/services/providers/voice_clone)

## Key Architecture Decisions

- Frontend and backend are separated cleanly so the frontend can later be wrapped in Electron without changing backend contracts.
- The backend uses mock-first ingestion so the product remains runnable before external API access exists.
- Voice cloning is intentionally abstracted and guarded to support only authorized user-owned voice usage.
- Scheduling uses APScheduler in-process for MVP simplicity; this can move to Redis/Celery or a cloud scheduler later.
- Standard TTS is always available through the default provider path, with browser fallback if server audio is unavailable.

## Known Limitations

- Clustering uses normalized-title hashing, which is simple and not semantic.
- Auth is JWT-only and does not include refresh tokens, email verification, or password reset.
- Scheduler runs in-process, so horizontal scaling would require an external scheduler or worker leader.
- Mock ingestion is seeded data until a real provider is connected.
- Voice cloning is a safe stub and does not produce cloned audio in the MVP.

## Next-Step Roadmap

1. Add a real news provider with source-level credibility scoring and more robust normalization.
2. Replace heuristic summaries with LLM-backed factual summaries and citation traces.
3. Upgrade clustering to embeddings or article similarity matching.
4. Move scheduled generation into a dedicated worker queue.
5. Add admin observability for ingestion, ranking, and provider health.
6. Add desktop packaging with Electron once the web flows stabilize.
