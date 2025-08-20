"""
Users API endpoints.
This file will be accessible at /api/users/*
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

# Pydantic models for request/response
class User(BaseModel):
    id: int
    name: str
    email: str
    active: bool = True

class UserCreate(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    active: Optional[bool] = None

# In-memory storage for demo purposes
users_db = [
    User(id=1, name="John Doe", email="john@example.com"),
    User(id=2, name="Jane Smith", email="jane@example.com"),
    User(id=3, name="Bob Johnson", email="bob@example.com")
]

@router.get("/", response_model=List[User])
async def get_users():
    """Get all users."""
    return users_db

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Get a specific user by ID."""
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    """Create a new user."""
    new_id = max((u.id for u in users_db), default=0) + 1
    new_user = User(id=new_id, **user.dict())
    users_db.append(new_user)
    return new_user

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate):
    """Update an existing user."""
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update only provided fields
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """Delete a user."""
    global users_db
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    users_db = [u for u in users_db if u.id != user_id]
    return {"message": f"User {user_id} deleted successfully"}

@router.get("/search/by-email")
async def search_users_by_email(email: str):
    """Search users by email."""
    matching_users = [u for u in users_db if email.lower() in u.email.lower()]
    return matching_users
