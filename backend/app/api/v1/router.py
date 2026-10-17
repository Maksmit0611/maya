from fastapi import APIRouter

from app.api.v1 import briefs, chat, jobs, projects, results, rooms

api_router = APIRouter()
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(rooms.router, tags=["rooms and assets"])
api_router.include_router(briefs.router, tags=["briefs"])
api_router.include_router(chat.router, prefix="/chat", tags=["agent chat"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["generation jobs"])
api_router.include_router(results.router, tags=["results"])
