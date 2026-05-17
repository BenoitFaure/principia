# src/principia/backend/api/router.py
from fastapi import APIRouter

from .constitution import router as constitution_router
from .dev import router as dev_router
from .examples import router as examples_router

# Create the router instance
router = APIRouter()
router.include_router(constitution_router)
router.include_router(examples_router)
router.include_router(dev_router)
