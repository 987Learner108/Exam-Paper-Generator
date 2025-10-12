import os
import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from mangum import Mangum

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.main import app

# Create Mangum handler for Vercel
handler = Mangum(app)

def main(event, context):
    """Vercel serverless function handler"""
    return handler(event, context)
