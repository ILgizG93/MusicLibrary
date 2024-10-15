import uvicorn
from fastapi import FastAPI, APIRouter

from router.artist import router as artist_router

app = FastAPI()

main_router = APIRouter()
main_router.include_router(artist_router, prefix="/artist", tags=["Artist"])
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
