import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine, Base

# Register all models with SQLAlchemy before creating tables
import models.user      # noqa
import models.message   # noqa
import models.requests  # noqa

from routers import auth, messages, requests, ws

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TKR College Portal API",
    description="Backend for TKR College Portal — messaging, requests, and real-time notifications.",
    version="1.0.0",
)

# ─── CORS ─────────────────────────────────────────────────────────────────────
# FRONTEND_URL is set in Render environment variables to your Netlify URL.
# Multiple URLs can be separated by a comma, e.g.:
#   FRONTEND_URL=https://tkr-portal.netlify.app,https://custom-domain.com
frontend_url_env = os.environ.get("FRONTEND_URL", "")
extra_origins = [u.strip() for u in frontend_url_env.split(",") if u.strip()]

allowed_origins = [
    # Local development
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5500",
    "http://localhost:5501",
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5501",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
    # file:// origins appear as null in some browsers
    "null",
] + extra_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(messages.router)
app.include_router(requests.router)
app.include_router(ws.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "project": "TKR College Portal"}
