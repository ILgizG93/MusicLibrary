import uvicorn
from fastapi import FastAPI, APIRouter

from router.artist import router as artist_router
from router.release import router as release_router

app = FastAPI()

main_router = APIRouter()
main_router.include_router(artist_router, prefix="/artist", tags=["Artist"])
main_router.include_router(release_router, prefix="/release", tags=["Release"])
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
