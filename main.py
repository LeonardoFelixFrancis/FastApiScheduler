from fastapi import FastAPI
from src.controllers import (user_controller, 
                             auth_controller, 
                             lesson_controller, 
                             lesson_schedule_controller,
                             company_controller)
app = FastAPI()

app.include_router(user_controller.router)
app.include_router(auth_controller.router)
app.include_router(lesson_controller.router)
app.include_router(lesson_schedule_controller.router)
app.include_router(company_controller.router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

