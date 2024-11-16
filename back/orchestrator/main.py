from fastapi import FastAPI
from orchestrator.api import router
import uvicorn

app = FastAPI()

# Inclui as rotas do orquestrador
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8005, reload=True)
