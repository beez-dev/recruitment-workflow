# TechKraft Candidate Dashboard

Internal candidate scoring and review dashboard for TechKraft's recruitment workflow.

## Stack

- **Frontend**: Next.js 16 (App Router, TypeScript, Tailwind CSS)
- **Backend**: FastAPI (Python 3.12, SQLAlchemy async, SQLite)
- **Auth**: JWT (email + password)
- **Container**: Docker Compose

---

## Setup & Run

### Prerequisites

- Docker + Docker Compose, **or**
- Node.js 22+ and Python 3.12+

### Option A — Docker Compose

```bash
cp .env.example .env
# Edit .env and set a real SECRET_KEY
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs

### Option B — Local Development

**Backend**

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env
uvicorn app.main:app --reload --port 8000
```

**Frontend**

```bash
cd frontend
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

---

## Example API Calls

```bash
# Register a reviewer
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"reviewer@example.com","password":"password123"}'

# Login
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"reviewer@example.com","password":"password123"}' | jq -r .access_token)

# List candidates (paginated)
curl http://localhost:8000/candidates?limit=20&offset=0 \
  -H "Authorization: Bearer $TOKEN"

# Filter candidates
curl "http://localhost:8000/candidates?status=new&role_applied=engineer&keyword=alice" \
  -H "Authorization: Bearer $TOKEN"

# Submit a score
curl -X POST http://localhost:8000/candidates/{id}/scores \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"category":"technical","score":4,"note":"Strong problem solver"}'

# Trigger AI summary
curl -X POST http://localhost:8000/candidates/{id}/summary \
  -H "Authorization: Bearer $TOKEN"
```

---

## Running Tests

```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v
```

---

## Debugging Signal — Bug Analysis

The following pattern has a critical bug:

```python
def search_candidates(status, keyword, page, page_size):
    all_candidates = db.execute("SELECT * FROM candidates").fetchall()
    filtered = [c for c in all_candidates if c["status"] == status]
    # ... also filter by keyword in Python ...
    offset = (page - 1) * page_size
    return filtered[offset : offset + page_size]
```

**Issue**: The query fetches every row in the table into memory before filtering. At scale (10k+ candidates) this:

1. **OOM risk** — entire table loaded per request, unbounded memory use
2. **Slow** — transfers all rows over the DB connection regardless of filters
3. **Pagination is wrong** — `filtered[offset:offset+page_size]` slices the *in-memory* filtered list, not the full dataset, so total count is unavailable and page numbers are incoherent if filters are applied
4. **No index use** — the DB index on `status` is bypassed because filtering is done in Python

**Correct approach**: push filters, ordering, `OFFSET`, and `LIMIT` into SQL so the database engine uses indexes and the application never loads more rows than the page size.

```python
# All filtering and pagination in SQL
SELECT * FROM candidates
WHERE status = :status AND name ILIKE :keyword AND deleted_at IS NULL
ORDER BY created_at DESC
LIMIT :limit OFFSET :offset;
```

---

## Architecture Decision Record

### ADR 1 — SQLite over DynamoDB for local development

**Context**: Assignment allowed DynamoDB-style or SQLite. A full DynamoDB setup requires either AWS credentials or LocalStack, which adds non-trivial onboarding friction.

**Decision**: SQLite with SQLAlchemy async (`aiosqlite`). The schema uses the same relational model that would translate directly to Postgres in production.

**Trade-off**: SQLite does not support native JSON indexing or concurrent writes at scale. The `skills` column is stored as JSON, which limits query-ability. Switching to Postgres later requires only changing `DATABASE_URL`.

---

### ADR 2 — FastAPI with async SQLAlchemy

**Context**: Needed a Python API that handles concurrent requests without blocking (especially the mock 2s LLM call).

**Decision**: FastAPI with `asyncio` + SQLAlchemy 2.0 async session. The `await asyncio.sleep(2)` in the summary endpoint is non-blocking — other requests are served during the delay.

**Trade-off**: Async SQLAlchemy requires `aiosqlite` driver and slightly more boilerplate than sync SQLAlchemy. Synchronous libraries (e.g., bcrypt via passlib) are wrapped in thread executors automatically by FastAPI.

---

### ADR 3 — JWT role baked into token, registration hardcodes reviewer

**Context**: RBAC must be enforced server-side. A naive implementation might accept `role` from the registration payload.

**Decision**: Registration endpoint ignores any `role` field from the client and always writes `role="reviewer"` to the database. Admins must be seeded directly in the DB. The JWT payload includes `role` for convenience but the database record is the source of truth (the token is re-verified against the DB on each request).

**Trade-off**: No self-service admin promotion. Admins require a manual DB seed step — acceptable for an internal tool, unacceptable for a public SaaS.

---

## Learning Reflection

I implemented SQLAlchemy's async session pattern with `selectinload` for eager relationship loading — something I'd previously only done synchronously. Given more time, I'd explore the SSE stretch goal (`GET /candidates/{id}/stream`) using FastAPI's `StreamingResponse` paired with a lightweight pub/sub (e.g., Redis Streams or an in-process event bus) to push live score updates to connected clients without polling.
