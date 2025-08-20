"""
FastAPI server with folder-based routing structure.
Routes are automatically discovered and registered based on folder structure.
"""
import os
import importlib.util
from pathlib import Path
from fastapi import FastAPI
from fastapi.routing import APIRouter

app = FastAPI(
    title="FastAPI with Folder-based Routing",
    description="API server where routes are organized by folder structure",
    version="1.0.0"
)

def load_router_from_file(file_path: Path, route_prefix: str) -> APIRouter:
    """Load a router from a Python file."""
    spec = importlib.util.spec_from_file_location("router_module", file_path)
    if spec is None or spec.loader is None:
        return None
    
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Look for a router object in the module
    if hasattr(module, 'router'):
        return module.router
    elif hasattr(module, 'app'):
        return module.app
    return None

def register_routes():
    """Automatically discover and register routes from the api folder structure."""
    api_path = Path(__file__).parent / "api"
    
    if not api_path.exists():
        print("No 'api' folder found. Creating example structure...")
        return
    
    # Walk through the api directory
    for root, dirs, files in os.walk(api_path):
        # Skip __pycache__ directories
        if "__pycache__" in root:
            continue
            
        # Look for Python files that could contain routes
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                file_path = Path(root) / file
                
                # Calculate the route prefix based on folder structure
                # Remove the api folder from the path and convert to route format
                relative_path = file_path.relative_to(api_path)
                route_parts = list(relative_path.parts[:-1])  # Remove the filename
                
                # If the file is named something other than __init__.py, include the filename (without .py)
                if file != "__init__.py":
                    route_parts.append(file[:-3])  # Remove .py extension
                
                # Create the route prefix
                route_prefix = "/api/" + "/".join(route_parts) if route_parts else "/api"
                
                # Load and register the router
                router = load_router_from_file(file_path, route_prefix)
                if router:
                    app.include_router(router, prefix=route_prefix, tags=[route_parts[-1] if route_parts else "api"])
                    print(f"Registered routes from {file_path} with prefix: {route_prefix}")

# Register all routes on startup
register_routes()

@app.get("/")
async def root():
    """Root endpoint to check if the server is running."""
    return {
        "message": "FastAPI server with folder-based routing is running!",
        "docs": "/docs",
        "api_structure": "Routes are organized under /api/* based on folder structure"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
