# ESC Shipping — Django Backend

Production-ready Django REST Framework backend for the ESC Shipping management system.

## Project Structure

```
backend/
├── config/              # Project settings, URLs, WSGI/ASGI
│   ├── __init__.py
│   ├── settings.py      # Main settings (env-based)
│   ├── urls.py          # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── apps/                # Custom Django apps
│   └── __init__.py
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in git)
├── .env.example         # Template for environment variables
├── manage.py            # Django management script
└── README.md
```

## Quick Start

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
copy .env.example .env
# Edit .env with your database credentials and secret key
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /api/v1/auth/token/` | Obtain JWT access + refresh tokens |
| `POST /api/v1/auth/token/refresh/` | Refresh access token |
| `POST /api/v1/auth/token/verify/` | Verify token validity |
| `/api/docs/swagger/` | Swagger UI documentation |
| `/api/docs/redoc/` | ReDoc documentation |
| `/admin/` | Django admin panel |

## Tech Stack

- **Django 5.1** — Web framework
- **Django REST Framework** — API framework
- **SimpleJWT** — JWT authentication
- **django-cors-headers** — CORS handling
- **django-filter** — Query filtering
- **drf-spectacular** — OpenAPI 3 schema generation
- **PostgreSQL** — Primary database
- **python-decouple** — Environment variable management
