"""
FastAPI server with folder-based routing structure.
Routes are automatically discovered and registered based on folder structure.
"""
import os
import sys
import importlib.util
from pathlib import Path
from fastapi import FastAPI
from fastapi.routing import APIRouter

app = FastAPI(
    title="FastAPI with Folder-based Routing",
    description="API server where routes are organized by folder structure",
    version="1.0.0"
)

def load_router_from_file(file_path: Path) -> APIRouter:
    """Load a router from a Python file."""
    try:
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
    except Exception as e:
        print(f"Error loading router from {file_path}: {e}")
        return None

def register_routes():
    """Automatically discover and register routes from the api folder structure."""
    api_path = Path(__file__).parent / "api"
    
    if not api_path.exists():
        print("No 'api' folder found.")
        return
    
    print(f"🔍 Scanning for routes in: {api_path}")
    
    # Find all __init__.py files in the api directory
    for init_file in api_path.rglob("__init__.py"):
        try:
            # Calculate the route prefix based on folder structure
            relative_path = init_file.parent.relative_to(api_path)
            
            # Create the route prefix
            if str(relative_path) == ".":
                route_prefix = "/api"
                tag_name = "api"
            else:
                route_parts = relative_path.parts
                route_prefix = "/api/" + "/".join(route_parts)
                tag_name = route_parts[-1]
            
            print(f"📁 Loading router from: {init_file}")
            print(f"🔗 Route prefix: {route_prefix}")
            
            # Load and register the router
            router = load_router_from_file(init_file)
            if router:
                app.include_router(router, prefix=route_prefix, tags=[tag_name])
                print(f"✅ Successfully registered routes with prefix: {route_prefix}")
            else:
                print(f"❌ No router found in {init_file}")
                
        except Exception as e:
            print(f"❌ Error processing {init_file}: {e}")

# Register all routes on startup
print("🚀 Starting FastAPI server with folder-based routing...")
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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
