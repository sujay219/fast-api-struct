"""
Products API endpoints.
This file will be accessible at /api/products/*
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from decimal import Decimal

router = APIRouter()

# Pydantic models
class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str
    in_stock: bool = True

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    in_stock: Optional[bool] = None

# In-memory storage for demo
products_db = [
    Product(id=1, name="Laptop", description="High-performance laptop", price=999.99, category="Electronics"),
    Product(id=2, name="Coffee Mug", description="Ceramic coffee mug", price=15.99, category="Home"),
    Product(id=3, name="Book", description="Programming guide", price=29.99, category="Books")
]

@router.get("/", response_model=List[Product])
async def get_products():
    """Get all products."""
    return products_db

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int):
    """Get a specific product by ID."""
    product = next((p for p in products_db if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=Product)
async def create_product(product: ProductCreate):
    """Create a new product."""
    new_id = max((p.id for p in products_db), default=0) + 1
    new_product = Product(id=new_id, **product.dict())
    products_db.append(new_product)
    return new_product

@router.put("/{product_id}", response_model=Product)
async def update_product(product_id: int, product_update: ProductUpdate):
    """Update an existing product."""
    product = next((p for p in products_db if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    return product

@router.delete("/{product_id}")
async def delete_product(product_id: int):
    """Delete a product."""
    global products_db
    product = next((p for p in products_db if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    products_db = [p for p in products_db if p.id != product_id]
    return {"message": f"Product {product_id} deleted successfully"}

@router.get("/category/{category_name}")
async def get_products_by_category(category_name: str):
    """Get products by category."""
    category_products = [p for p in products_db if p.category.lower() == category_name.lower()]
    return category_products
