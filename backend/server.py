from fastapi.middleware.cors import CORSMiddleware

# Reuse existing FastAPI app and routes without modifying them
from main import app

# Allow the Next.js dev server to call this API
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    # Run: python backend/server.py
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)


