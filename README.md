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

### ADR 1 — Introduced a `users` table not mentioned in the spec

**Context**: The spec described reviewer and admin roles and a scoring workflow, but defined no mechanism for persisting user identities or credentials. Without a `users` table there is no safe way to verify who is submitting a score or enforce role-based access — any client could claim any role.

**Decision**: Added a `users` table (`id`, `email`, `hashed_password`, `role`, `created_at`) with a foreign key from `scores.reviewer_id → users.id`. Registration is the only way to create a user; the role is determined server-side by comparing the email against an `ADMIN_EMAIL` env var — the client never supplies it.

**Trade-off**: This goes beyond the literal spec, but omitting it would make the RBAC requirement impossible to enforce correctly. The added surface is minimal and contained to `models/user.py`, `repositories/users.py`, and `routers/auth.py`.

---

### ADR 2 — JWT delivered via HttpOnly cookies instead of response body

**Context**: The frontend needs to attach the JWT on every authenticated request. The common approach is to return the token in the response body and store it in `localStorage`, but `localStorage` is readable by any JavaScript on the page, making it vulnerable to XSS attacks.

**Decision**: The login endpoint sets the JWT as an `HttpOnly; SameSite=lax` cookie. The browser attaches it automatically on every same-origin request. The frontend never reads or stores the token — `credentials: 'include'` on `fetch` is all that is needed.

**Trade-off**: HttpOnly cookies cannot be read by JavaScript, which means the frontend cannot decode the token client-side to get the user's role or email. A separate `/auth/me` endpoint (or including user info in the login response body alongside the cookie) is needed to give the UI the current user's details.

---

## Learning Reflection

This was my first time working with FastAPI. Coming from opinionated frameworks like NestJS, FastAPI feels noticeably more barebones — there is no built-in module system, no enforced project structure, and no decorator-driven DI container. Instead, you wire everything together yourself using Python's type hints and FastAPI's `Depends()`. That freedom made it easy to adopt a clean layered architecture (routers → services → repositories), but it also meant the structure was entirely my own responsibility rather than something the framework guided me toward. Given more time, I'd explore the SSE stretch goal (`GET /candidates/{id}/stream`) using FastAPI's `StreamingResponse` paired with a lightweight pub/sub (e.g., Redis Streams or an in-process event bus) to push live score updates to connected clients without polling.
