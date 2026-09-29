import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from app.routes import router

load_dotenv()

# THIS LINE IS REQUIRED: Uvicorn looks specifically for "app"
app = FastAPI(title="ComicCraft - AI Comic Creator")

# Create output directories if they don't exist
os.makedirs("static/panels", exist_ok=True)
os.makedirs("static/exports", exist_ok=True)

# Mount static asset directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include Application Routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)