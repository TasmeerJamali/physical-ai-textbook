"""Authentication router using Better-Auth compatible endpoints."""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from jose import jwt

from app.config import get_settings


router = APIRouter()
settings = get_settings()


class UserSignup(BaseModel):
    """User signup request."""
    email: EmailStr
    password: str
    name: str
    # Background questions for personalization
    experience_level: str = "beginner"  # beginner, intermediate, advanced
    programming_languages: list[str] = []
    robotics_experience: bool = False
    learning_goals: list[str] = []


class UserLogin(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserProfile(BaseModel):
    """User profile response."""
    id: str
    email: str
    name: str
    experience_level: str
    created_at: datetime


# In-memory user store (replace with database in production)
users_db: dict = {}


def create_access_token(data: dict) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)


@router.post("/signup", response_model=TokenResponse)
async def signup(user: UserSignup):
    """
    Register a new user with background questions.
    
    Background questions help personalize content delivery.
    """
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Store user (in production, hash password and use database)
    user_id = f"user_{len(users_db) + 1}"
    users_db[user.email] = {
        "id": user_id,
        "email": user.email,
        "password": user.password,  # Hash in production!
        "name": user.name,
        "experience_level": user.experience_level,
        "programming_languages": user.programming_languages,
        "robotics_experience": user.robotics_experience,
        "learning_goals": user.learning_goals,
        "created_at": datetime.utcnow()
    }
    
    # Create token
    token = create_access_token({"sub": user.email, "user_id": user_id})
    
    return TokenResponse(
        access_token=token,
        expires_in=settings.access_token_expire_minutes * 60
    )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """Login with email and password."""
    user = users_db.get(credentials.email)
    if not user or user["password"] != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": credentials.email, "user_id": user["id"]})
    
    return TokenResponse(
        access_token=token,
        expires_in=settings.access_token_expire_minutes * 60
    )


@router.get("/me", response_model=UserProfile)
async def get_current_user(token: str):
    """Get current user profile from token."""
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        email = payload.get("sub")
        user = users_db.get(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserProfile(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            experience_level=user["experience_level"],
            created_at=user["created_at"]
        )
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

