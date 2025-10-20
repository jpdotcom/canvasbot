from fastapi import FastAPI
import requests
from routers import users,assignments, llm
from dotenv import load_dotenv 
import os 
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()
CANVAS_BASE_URL = "https://canvas.case.edu/api/v1"
DATABASE_URL=os.getenv("DATABASE_URL")


app=FastAPI()
app.include_router(users.router);
app.include_router(assignments.router)
app.include_router(llm.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("REACT_DEV_SERVER", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message":"CanvasBot Backend Started Up!"}

