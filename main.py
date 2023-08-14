from fastapi import FastAPI
import uvicorn

from routers.editor_router import router as editor_router
from config import get_settings


settings = get_settings()

app = FastAPI(title=settings.app_name)
app.include_router(editor_router, tags=['editor'])

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=settings.app_port, reload=True)