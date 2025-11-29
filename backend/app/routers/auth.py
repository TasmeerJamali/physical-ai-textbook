"""
Authentication router using Better-Auth compatible patterns.

This implements Better-Auth style authentication with:
- Secure password hashing (bcrypt)
- JWT tokens with refresh capability
- User profile with personalization data
- Database persistence via Neon Postgres
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Optional
import uuid
import asyncpg

from app.config import get_settings


router = APIRouter()
settings = get_settings()

# Password hashing context - Better-Auth uses bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme
security = HTTPBearer()


# ============ Pydantic Models ============

class UserSignup(BaseModel):
    """User signup request with personalization questions."""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Minimum 8 characters")
    name: str = Field(..., min_length=2)
    # Background questions for personalization (Better-Auth style metadata)
    experience_level: str = "beginner"  # beginner, intermediate, advanced
    programming_languages: list[str] = []
    robotics_experience: bool = False
    learning_goals: list[str] = []


class UserLogin(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """JWT token response - Better-Auth compatible."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict


class UserProfile(BaseModel):
    """User profile response."""
    id: str
    email: str
    name: str
    experience_level: str
    programming_languages: list[str]
    robotics_experience: bool
    learning_goals: list[str]
    created_at: datetime


class RefreshTokenRequest(BaseModel):
    """Refresh token request."""
    refresh_token: str


# ============ Password Utilities ============

def hash_password(password: str) -> str:
    """Hash password using bcrypt (Better-Auth standard)."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ============ JWT Utilities ============

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token (longer lived)."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)  # 7 day refresh token
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    """Decode and validate JWT token."""
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# ============ Database Utilities ============

async def get_db_connection():
    """Get async database connection to Neon Postgres."""
    # Parse the database URL for asyncpg
    db_url = settings.database_url
    if db_url.startswith("postgresql+asyncpg://"):
        db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")

    try:
        conn = await asyncpg.connect(db_url)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None


async def init_users_table():
    """Initialize users table in Neon Postgres."""
    conn = await get_db_connection()
    if not conn:
        return False

    try:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR(50) PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                experience_level VARCHAR(50) DEFAULT 'beginner',
                programming_languages TEXT[] DEFAULT '{}',
                robotics_experience BOOLEAN DEFAULT FALSE,
                learning_goals TEXT[] DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await conn.close()
        return True
    except Exception as e:
        print(f"Table creation error: {e}")
        await conn.close()
        return False


# ============ Auth Endpoints ============

@router.post("/signup", response_model=TokenResponse)
async def signup(user: UserSignup):
    """
    Register a new user with Better-Auth style flow.

    - Validates email uniqueness
    - Hashes password with bcrypt
    - Stores in Neon Postgres
    - Returns JWT access + refresh tokens
    """
    conn = await get_db_connection()

    if not conn:
        raise HTTPException(status_code=503, detail="Database unavailable")

    try:
        # Check if email exists
        existing = await conn.fetchrow(
            "SELECT id FROM users WHERE email = $1", user.email
        )
        if existing:
            await conn.close()
            raise HTTPException(status_code=400, detail="Email already registered")

        # Create user
        user_id = f"user_{uuid.uuid4().hex[:12]}"
        password_hash = hash_password(user.password)

        await conn.execute('''
            INSERT INTO users (id, email, password_hash, name, experience_level,
                             programming_languages, robotics_experience, learning_goals)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        ''', user_id, user.email, password_hash, user.name, user.experience_level,
            user.programming_languages, user.robotics_experience, user.learning_goals)

        await conn.close()

        # Create tokens
        token_data = {"sub": user.email, "user_id": user_id}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.access_token_expire_minutes * 60,
            user={
                "id": user_id,
                "email": user.email,
                "name": user.name,
                "experience_level": user.experience_level
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            await conn.close()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """
    Login with email and password.

    - Verifies password against bcrypt hash
    - Returns JWT access + refresh tokens
    """
    conn = await get_db_connection()

    if not conn:
        raise HTTPException(status_code=503, detail="Database unavailable")

    try:
        user = await conn.fetchrow(
            "SELECT * FROM users WHERE email = $1", credentials.email
        )
        await conn.close()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Verify password
        if not verify_password(credentials.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Create tokens
        token_data = {"sub": user["email"], "user_id": user["id"]}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.access_token_expire_minutes * 60,
            user={
                "id": user["id"],
                "email": user["email"],
                "name": user["name"],
                "experience_level": user["experience_level"]
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            await conn.close()
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """Refresh access token using refresh token."""
    payload = decode_token(request.refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    conn = await get_db_connection()
    if not conn:
        raise HTTPException(status_code=503, detail="Database unavailable")

    try:
        user = await conn.fetchrow(
            "SELECT * FROM users WHERE email = $1", payload.get("sub")
        )
        await conn.close()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Create new tokens
        token_data = {"sub": user["email"], "user_id": user["id"]}
        access_token = create_access_token(token_data)
        new_refresh_token = create_refresh_token(token_data)

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            expires_in=settings.access_token_expire_minutes * 60,
            user={
                "id": user["id"],
                "email": user["email"],
                "name": user["name"],
                "experience_level": user["experience_level"]
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            await conn.close()
        raise HTTPException(status_code=500, detail=f"Token refresh failed: {str(e)}")


@router.get("/me", response_model=UserProfile)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user profile from Bearer token."""
    payload = decode_token(credentials.credentials)

    conn = await get_db_connection()
    if not conn:
        raise HTTPException(status_code=503, detail="Database unavailable")

    try:
        user = await conn.fetchrow(
            "SELECT * FROM users WHERE email = $1", payload.get("sub")
        )
        await conn.close()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return UserProfile(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            experience_level=user["experience_level"],
            programming_languages=list(user["programming_languages"] or []),
            robotics_experience=user["robotics_experience"],
            learning_goals=list(user["learning_goals"] or []),
            created_at=user["created_at"]
        )
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            await conn.close()
        raise HTTPException(status_code=500, detail=f"Profile fetch failed: {str(e)}")


@router.post("/logout")
async def logout():
    """
    Logout endpoint - Better-Auth compatible.

    Note: JWT tokens are stateless, so logout is handled client-side
    by removing the token. This endpoint exists for API completeness.
    """
    return {"message": "Logged out successfully", "success": True}


@router.get("/init-db")
async def initialize_database():
    """Initialize the users table in Neon Postgres."""
    success = await init_users_table()
    if success:
        return {"message": "Database initialized successfully", "success": True}
    else:
        raise HTTPException(status_code=500, detail="Failed to initialize database")

