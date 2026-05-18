# src/principia/backend/api/router.py
from fastapi import APIRouter

from .constitution import router as constitution_router
from .dev import router as dev_router
from .example_refinement_chat import router as example_refinement_chat_router
from .examples import router as examples_router
from .prompt_test_chat import router as prompt_test_chat_router

# Create the router instance
router = APIRouter()
router.include_router(constitution_router)
router.include_router(examples_router)
router.include_router(dev_router)
router.include_router(prompt_test_chat_router)
router.include_router(example_refinement_chat_router)
