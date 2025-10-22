from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def test():
    return {"message": "API is working!", "status": "success"}

@app.post("/")
def test_post():
    return {"message": "POST endpoint is working!", "status": "success"}

handler = Mangum(app, lifespan="off")
