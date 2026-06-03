import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.adminpanel.auth import authentication_backend
from app.adminpanel.views import BookingsAdmin, CalendarAdmin, UserAdmin
from app.bookings.router import router as router_booking
from app.calendar.router import router as router_calendar
from app.wishes.router import router as router_wishe
from app.config import settings
from app.database import engine, Base
from app.images.router import router as router_images
from app.logger import logger
from app.pages.router import router as router_pages
from app.users.router import router as router_users


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    try:
        redis = aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            encoding="utf8",
            decode_responses=True,
        )
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"FAILED TO INIT CACHE: {e}")
    yield


app = FastAPI(
    lifespan=lifespan,
)

app.include_router(router_booking)
app.include_router(router_users)
app.include_router(router_calendar)
app.include_router(router_wishe)
app.include_router(router_pages)
app.include_router(router_images)


origins = [
    f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="app/static"), name="static")

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(CalendarAdmin)
admin.add_view(UserAdmin)
admin.add_view(BookingsAdmin)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info("Request handling time", extra={"process_time": round(process_time, 6)})
    return response
