from fastapi import FastAPI
import uvicorn

from routers.editor_router import router as editor_router

app = FastAPI(title='joint_editor')
app.include_router(editor_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
