
# College ERP

An integrated College Admission Management and Student Management system.

## Project Modules

- Admission Management
- Student Management

Both modules will be developed in separate folders and integrated using agreed interfaces.

## Technology Stack

- Frontend: React, TypeScript, Vite, Tailwind CSS
- Backend: Python, FastAPI
- ORM: SQLAlchemy
- Database: PostgreSQL
- Database migrations: Alembic
- Local database environment: Docker Compose

## Prerequisites

Install the following:

- Git
- Node.js LTS and npm
- Python 3.12
- Docker Desktop
- Visual Studio Code

## Repository Structure

```text
college-erp/
├── admission/
├── student/
├── shared/
├── backend/
│   ├── app/
│   └── tests/
├── docs/
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Local Database Setup

1. Install and start Docker Desktop.
2. Create a root-level `.env` file.
3. Generate a local database password:

   ```bash
   openssl rand -hex 24
   ```

4. Add the generated value to `.env`:

   ```dotenv
   POSTGRES_PASSWORD=YOUR_GENERATED_PASSWORD
   ```

5. Start PostgreSQL:

   ```bash
   docker compose up -d
   ```

6. Check the database container:

   ```bash
   docker compose ps
   ```

7. Verify PostgreSQL:

   ```bash
   docker compose exec db \
     psql -U erp_user -d college_erp \
     -c "SELECT current_database(), current_user;"
   ```

The expected database is `college_erp`, and the expected user is `erp_user`.

## Stop the Database

```bash
docker compose stop
```

Start it again with:

```bash
docker compose up -d
```

The named Docker volume preserves database data across container stops and restarts.

Do not remove the volume unless you intentionally want to delete the local database data.

## Security

- Never commit `.env`.
- Never commit credentials or real student data.
- Use synthetic data during development.
- Do not connect to the college's production systems without authorization.

## Documentation

- `docs/prd.md`: Requirements and project scope.
- `docs/architecture.md`: System architecture and technical decisions.
- `docs/rules.md`: Development and collaboration rules.
- `docs/phases.md`: Milestones and progress.
- `docs/memory.md`: Important project decisions.
- `docs/design.md`: To be created when frontend work begins.


## Backend Development

From the repository root:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

## Step 5 — Commit the milestone

After the endpoint works and the documentation reflects what you actually tested, return to the repository root:

```bash
cd ..
git status