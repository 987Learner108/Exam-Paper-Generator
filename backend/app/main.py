from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import connect_to_mongo, close_mongo_connection
from app.core.config import settings
from app.routes import auth, admin, teacher

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Intelligent Exam Paper Generator with Multi-Agent AI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    await connect_to_mongo()
    print(f"🚀 {settings.APP_NAME} started successfully!")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    await close_mongo_connection()

# Health check
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Intelligent Exam Paper Generator API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "api": "operational"
    }

# Include routers
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(teacher.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
