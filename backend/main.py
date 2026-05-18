"""
Main FastAPI Application
========================
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.routes.solve import router as solve_router
from app.database.database import init_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifecycle"""
    logger.info("Starting application...")
    print("📄 API Documentation (Swagger UI): http://127.0.0.1:8000/docs")
    try:
        init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.warning(f"Database initialization warning: {e}")
    
    yield
    
    logger.info("Shutting down application...")


# Create FastAPI app
app = FastAPI(
    title="Travel Itinerary Optimization API",
    description="AI-powered travel planning using optimization algorithms",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(solve_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Travel Itinerary Optimization API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "algorithms": "/api/algorithms",
            "solve": "/api/solve (POST)"
        }
    }


@app.get("/docs")
async def docs_redirect():
    """Redirect to interactive API docs"""
    return {"message": "Visit /docs for interactive API documentation"}


if __name__ == "__main__":
    import uvicorn
    print("api docuementation in  http://127.0.0.1:8000/docs ")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
    
