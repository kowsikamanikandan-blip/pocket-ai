from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import get_settings
from app.database import Base,engine
from app.routes.api import router as api_router
from app.routes.pages import router as page_router
s=get_settings()
@asynccontextmanager
async def lifespan(app): Base.metadata.create_all(bind=engine); yield
app=FastAPI(title=s.app_name,version='1.0.0',lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=s.origins,allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
app.mount('/static',StaticFiles(directory='static'),name='static'); app.include_router(page_router); app.include_router(api_router)
