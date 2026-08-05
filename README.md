# Page Pulse API

A production-ready FastAPI service that audits web pages by fetching metadata, measuring response time, and returning structured results.

---

## Features

- FastAPI
- Async HTTP requests
- URL validation
- Configurable timeout
- HTML title extraction
- Response time measurement
- In-memory caching
- Rate limiting
- Request ID middleware
- Structured logging
- Unit testing
- GitHub Actions CI
- Ready for deployment

---

## Tech Stack

- FastAPI
- HTTPX
- BeautifulSoup4
- CacheTools
- SlowAPI
- Structlog
- Pytest
- GitHub Actions

---

## Installation

```bash
git clone <repository-url>

cd page-pulse

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

---

## Run

```bash
uvicorn app.main:app --reload
```

---

## API Documentation

Swagger:

```
http://127.0.0.1:8000/docs
```

---

## Example Request

```json
{
    "url":"https://google.com"
}
```

---

## Example Response

```json
{
  "success": true,
  "cached": false,
  "status_code": 200,
  "response_time_ms": 150.8,
  "title": "Google"
}
```

---

## Testing

```bash
pytest -v
```

---

## CI

GitHub Actions automatically runs tests on every push and pull request.

---

## Deployment

Hosted on Render.