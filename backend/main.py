from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="TravelPilot", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


from routes import router
app.include_router(router)

# --- Serve built React frontend in production ---
FRONTEND_BUILD = Path(__file__).parent.parent / "frontend" / "dist"

if FRONTEND_BUILD.is_dir():
    # Serve static assets (JS, CSS, images)
    app.mount("/assets", StaticFiles(directory=FRONTEND_BUILD / "assets"), name="static-assets")

    # Catch-all: serve index.html for client-side routing
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        index_file = FRONTEND_BUILD / "index.html"
        if index_file.is_file():
            return FileResponse(index_file)
        return {"error": "Frontend not built. Run: cd frontend && npm run build"}
