"""
User Address API endpoints.
This file will be accessible at /api/users/address/*
Note: This approach gives you routes like /api/users/address/{user_id}
If you want /api/users/{user_id}/address, use Option 1 instead.
"""
from fastapi import APIRouter, HTTPException, Path
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

# Address models
class Address(BaseModel):
    id: int
    user_id: int
    street: str
    city: str
    state: str
    zip_code: str
    country: str
    is_primary: bool = False

class AddressCreate(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str
    is_primary: bool = False

class AddressUpdate(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    is_primary: Optional[bool] = None

# In-memory storage for demo
addresses_db = [
    Address(id=1, user_id=1, street="123 Main St", city="San Francisco", state="CA", zip_code="94102", country="USA", is_primary=True),
    Address(id=2, user_id=1, street="456 Work Ave", city="San Francisco", state="CA", zip_code="94105", country="USA", is_primary=False),
    Address(id=3, user_id=2, street="789 Oak St", city="New York", state="NY", zip_code="10001", country="USA", is_primary=True),
]

# Helper function to check if user exists (you'd normally check your users database)
def user_exists(user_id: int) -> bool:
    # In a real app, you'd check your users database
    # For demo, assume users 1, 2, 3 exist
    return user_id in [1, 2, 3]

@router.get("/{user_id}", response_model=List[Address])
async def get_user_addresses(user_id: int = Path(..., description="The ID of the user")):
    """Get all addresses for a specific user."""
    if not user_exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    
    user_addresses = [addr for addr in addresses_db if addr.user_id == user_id]
    return user_addresses

@router.get("/{user_id}/{address_id}", response_model=Address)
async def get_user_address(
    user_id: int = Path(..., description="The ID of the user"),
    address_id: int = Path(..., description="The ID of the address")
):
    """Get a specific address for a user."""
    if not user_exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    
    address = next((addr for addr in addresses_db if addr.id == address_id and addr.user_id == user_id), None)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    return address

@router.post("/{user_id}", response_model=Address)
async def create_user_address(
    address: AddressCreate,
    user_id: int = Path(..., description="The ID of the user")
):
    """Create a new address for a user."""
    if not user_exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    
    # If this is set as primary, make all other addresses for this user non-primary
    if address.is_primary:
        for addr in addresses_db:
            if addr.user_id == user_id:
                addr.is_primary = False
    
    new_id = max((addr.id for addr in addresses_db), default=0) + 1
    new_address = Address(id=new_id, user_id=user_id, **address.dict())
    addresses_db.append(new_address)
    
    return new_address

@router.put("/{user_id}/{address_id}", response_model=Address)
async def update_user_address(
    address_update: AddressUpdate,
    user_id: int = Path(..., description="The ID of the user"),
    address_id: int = Path(..., description="The ID of the address")
):
    """Update a specific address for a user."""
    if not user_exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    
    address = next((addr for addr in addresses_db if addr.id == address_id and addr.user_id == user_id), None)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    # Update only provided fields
    update_data = address_update.dict(exclude_unset=True)
    
    # If setting as primary, make all other addresses for this user non-primary
    if update_data.get('is_primary'):
        for addr in addresses_db:
            if addr.user_id == user_id and addr.id != address_id:
                addr.is_primary = False
    
    for field, value in update_data.items():
        setattr(address, field, value)
    
    return address

@router.delete("/{user_id}/{address_id}")
async def delete_user_address(
    user_id: int = Path(..., description="The ID of the user"),
    address_id: int = Path(..., description="The ID of the address")
):
    """Delete a specific address for a user."""
    global addresses_db
    
    if not user_exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    
    address = next((addr for addr in addresses_db if addr.id == address_id and addr.user_id == user_id), None)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    addresses_db = [addr for addr in addresses_db if not (addr.id == address_id and addr.user_id == user_id)]
    return {"message": f"Address {address_id} for user {user_id} deleted successfully"}

@router.get("/{user_id}/primary", response_model=Address)
async def get_user_primary_address(user_id: int = Path(..., description="The ID of the user")):
    """Get the primary address for a user."""
    if not user_exists(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    
    primary_address = next((addr for addr in addresses_db if addr.user_id == user_id and addr.is_primary), None)
    if not primary_address:
        raise HTTPException(status_code=404, detail="No primary address found for user")
    
    return primary_address
