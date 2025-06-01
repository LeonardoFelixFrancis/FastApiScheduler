from fastapi import FastAPI
from src.controllers import user_controller, auth_controller, lesson_controller, lesson_schedule_controller
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://leofelixdev.com",
    "https://leofelixdev.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user_controller.router)
app.include_router(auth_controller.router)
app.include_router(lesson_controller.router)
app.include_router(lesson_schedule_controller.router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

