# FastAPI Folder-Based Routing

This FastAPI server implements automatic folder-based routing where API endpoints are organized and discovered based on the folder structure.

## Project Structure

```
fast-api-struct/
├── main.py                 # Main FastAPI application with auto-discovery
├── requirements.txt        # Python dependencies
├── api/                   # API routes folder
│   ├── users/             # User-related endpoints
│   │   ├── __init__.py    # Routes: /api/users/*
│   │   └── profile/       # User profile endpoints
│   │       └── __init__.py # Routes: /api/users/profile/*
│   └── products/          # Product-related endpoints
│       └── __init__.py    # Routes: /api/products/*
```

## How It Works

1. **Automatic Route Discovery**: The server automatically scans the `api/` folder and its subdirectories
2. **Folder-to-Route Mapping**: Each folder becomes a route prefix
3. **File-to-Endpoint Mapping**: Python files in folders define the actual endpoints

### Route Mapping Examples

| File Path | Route Prefix | Example Endpoints |
|-----------|--------------|-------------------|
| `api/users/__init__.py` | `/api/users` | GET `/api/users/`, POST `/api/users/` |
| `api/products/__init__.py` | `/api/products` | GET `/api/products/`, GET `/api/products/{id}` |
| `api/users/profile/__init__.py` | `/api/users/profile` | GET `/api/users/profile/{user_id}` |

## Installation

1. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will be available at:
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Available API Endpoints

### Users API (`/api/users`)
- `GET /api/users/` - Get all users
- `GET /api/users/{user_id}` - Get specific user
- `POST /api/users/` - Create new user
- `PUT /api/users/{user_id}` - Update user
- `DELETE /api/users/{user_id}` - Delete user
- `GET /api/users/search/by-email?email=example` - Search users by email

### Products API (`/api/products`)
- `GET /api/products/` - Get all products
- `GET /api/products/{product_id}` - Get specific product
- `POST /api/products/` - Create new product
- `PUT /api/products/{product_id}` - Update product
- `DELETE /api/products/{product_id}` - Delete product
- `GET /api/products/category/{category_name}` - Get products by category

### User Profile API (`/api/users/profile`)
- `GET /api/users/profile/{user_id}` - Get user profile
- `POST /api/users/profile/{user_id}` - Create user profile
- `PUT /api/users/profile/{user_id}` - Update user profile
- `DELETE /api/users/profile/{user_id}` - Delete user profile

## Adding New APIs

To add new API endpoints:

1. **Create a new folder** under `api/` (e.g., `api/orders/`)
2. **Create `__init__.py`** in the folder
3. **Define your router**:
   ```python
   from fastapi import APIRouter
   
   router = APIRouter()
   
   @router.get("/")
   async def get_orders():
       return {"orders": []}
   ```
4. **Restart the server** - routes are auto-discovered on startup

### Nested Routes

For nested routes like `/api/users/orders/`, create:
```
api/
└── users/
    └── orders/
        └── __init__.py
```

The router in `api/users/orders/__init__.py` will be accessible at `/api/users/orders/*`.

## Route File Requirements

Each route file must:
1. Define a `router` variable as `APIRouter()`
2. Use FastAPI decorators to define endpoints
3. Include proper error handling and response models

## Features

- ✅ Automatic route discovery
- ✅ Folder-based organization
- ✅ Nested route support
- ✅ Pydantic models for validation
- ✅ Comprehensive error handling
- ✅ Interactive API documentation
- ✅ Hot reload during development

## Development

The server runs with hot reload enabled, so changes to route files will automatically restart the server.
