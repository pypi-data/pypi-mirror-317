# models.py

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any




class Token(BaseModel):
  access_token: str
  token_type: str


class TokenData(BaseModel):
  username: Optional[str] = None
  scopes: List[str] = []


class UserCredentials(BaseModel):
  username: str
  password: str
  email: Optional[EmailStr] = None
  full_name: Optional[str] = None
  phone_number: Optional[str] = None  # Include phone number during registration
  scopes: Optional[List[str]] = []  # Add this line


class User(BaseModel):
  username: str
  email: Optional[EmailStr] = None
  full_name: Optional[str] = None
  disabled: Optional[bool] = None
  scopes: List[str] = []
  phone_number: Optional[str] = None  # Include phone_number in User model
  credits: float = 0.0  # Added credits field


class CoreAttributes(BaseModel):
  name: str = Field(..., min_length=3, max_length=100)
  description: str = Field(..., min_length=10, max_length=1000)
  price: float = Field(..., gt=0)
  category: str = Field(..., min_length=2)
  seller_location: List[float]
  shop_name: str = Field(..., min_length=1)
  seller_phone: Optional[str] = Field(None, pattern=r'^\+\d{10,15}$')  # Changed from regex to pattern


class ExtendedAttributes(BaseModel):
    attributes: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    tags: Optional[List[str]] = Field(default_factory=list)

class ImageManifest(BaseModel):
    file_hash: str
    chunk_hashes: Optional[List[str]] = Field(default_factory=list)
    file_name: str



class ProductIn(BaseModel):
    core: CoreAttributes
    extended: ExtendedAttributes = Field(default_factory=ExtendedAttributes)
    image_refs: List[str] = Field(default_factory=list)


class ProductOut(BaseModel):
    product_id: str
    core: CoreAttributes  # Assuming you have this model defined
    extended: ExtendedAttributes  # Assuming you have this model defined
    image_refs: List[ImageManifest]  # Update from List[str] to List[ImageManifest]

class CategorySuggestion(BaseModel):
    category_name: str




