from fastapi import APIRouter
from . import webhook, web_page

router = APIRouter()
router.include_router(web_page.router, prefix="/web")
router.include_router(webhook.router, prefix="/webhook")
