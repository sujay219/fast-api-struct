"""
User Profile API endpoints.
This file will be accessible at /api/users/profile/*
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel

router = APIRouter()

class UserProfile(BaseModel):
    user_id: int
    bio: str
    avatar_url: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None

class ProfileUpdate(BaseModel):
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None

# In-memory storage for demo
profiles_db = [
    UserProfile(user_id=1, bio="Software engineer", location="San Francisco", website="https://johndoe.dev"),
    UserProfile(user_id=2, bio="Product manager", location="New York"),
    UserProfile(user_id=3, bio="Designer", location="Los Angeles", avatar_url="https://example.com/avatar3.jpg")
]

@router.get("/{user_id}", response_model=UserProfile)
async def get_user_profile(user_id: int):
    """Get user profile by user ID."""
    profile = next((p for p in profiles_db if p.user_id == user_id), None)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.post("/{user_id}", response_model=UserProfile)
async def create_user_profile(user_id: int, bio: str, avatar_url: Optional[str] = None, 
                             location: Optional[str] = None, website: Optional[str] = None):
    """Create a new user profile."""
    # Check if profile already exists
    existing_profile = next((p for p in profiles_db if p.user_id == user_id), None)
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists")
    
    new_profile = UserProfile(
        user_id=user_id,
        bio=bio,
        avatar_url=avatar_url,
        location=location,
        website=website
    )
    profiles_db.append(new_profile)
    return new_profile

@router.put("/{user_id}", response_model=UserProfile)
async def update_user_profile(user_id: int, profile_update: ProfileUpdate):
    """Update user profile."""
    profile = next((p for p in profiles_db if p.user_id == user_id), None)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    update_data = profile_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    return profile

@router.delete("/{user_id}")
async def delete_user_profile(user_id: int):
    """Delete user profile."""
    global profiles_db
    profile = next((p for p in profiles_db if p.user_id == user_id), None)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    profiles_db = [p for p in profiles_db if p.user_id != user_id]
    return {"message": f"Profile for user {user_id} deleted successfully"}
