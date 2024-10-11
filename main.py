import uvicorn
from fastapi import FastAPI, APIRouter

from router import router

app = FastAPI()

main_router = APIRouter()
main_router.include_router(router, prefix="/music", tags=["Music"])
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
