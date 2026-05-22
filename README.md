# Address Book API

A REST API for managing addresses with geospatial search built with FastAPI and SQLite.

## Requirements

- Python 3.11+

## Quick Start

**1. Clone the repository**

```bash
git clone <your-repo-url> #<> Code >> Local >> HTTPS >> Copy URL to clipboard
cd address-book-api
```

**2. Create and activate a virtual environment**

```bash
# Windows
python -m venv vnv
vnv\Scripts\activate

# Linux / Mac / WSL
python -m venv vnv
source vnv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment** _(optional — app runs with defaults without this step)_

```bash
# Windows
copy .env.example .env

# Linux / Mac / WSL
cp .env.example .env
```

**5. Run the app**

```bash
uvicorn main:app --reload
```

The API is now running at `http://127.0.0.1:8000`

Open `http://127.0.0.1:8000/docs` to explore and test all endpoints via Swagger UI.

---

## API Endpoints

| Method   | Endpoint                   | Description                          |
| -------- | -------------------------- | ------------------------------------ |
| `GET`    | `/`                        | Health check                         |
| `POST`   | `/api/v1/addresses/`       | Create a new address                 |
| `GET`    | `/api/v1/addresses/`       | List all addresses                   |
| `GET`    | `/api/v1/addresses/{id}`   | Get a single address                 |
| `PATCH`  | `/api/v1/addresses/{id}`   | Update an address                    |
| `DELETE` | `/api/v1/addresses/{id}`   | Delete an address                    |
| `GET`    | `/api/v1/addresses/nearby` | Find addresses within a given radius |

### Nearby Search

Returns all addresses within `distance_km` kilometres of the given coordinates.

```
GET /api/v1/addresses/nearby?latitude=48.8584&longitude=2.2945&distance_km=10
```

---

## Environment Variables

| Variable       | Default                      | Description                |
| -------------- | ---------------------------- | -------------------------- |
| `DATABASE_URL` | `sqlite:///./addressbook.db` | Database connection string |
| `APP_ENV`      | `development`                | Environment name           |
| `LOG_LEVEL`    | `INFO`                       | Logging level              |
| `API_VERSION`  | `v1`                         | API version prefix         |

Copy `.env.example` to `.env` and change values as needed. The app works out of the box without a `.env` file using the defaults above.

---

## Running with Docker

```bash
docker build -t address-book-api .
docker run -p 8000:8000 address-book-api
```

---

## Project Structure

```
address-book-api/
├── app/
│   ├── api/v1/         # Route handlers
│   ├── core/           # Config, logging, exception handlers
│   ├── db/             # Database engine and session
│   ├── models/         # SQLAlchemy ORM models
│   ├── schemas/        # Pydantic request/response schemas
│   └── services/       # Business logic
├── main.py             # App entry point
├── requirements.txt
├── Dockerfile
└── .env.example
```
