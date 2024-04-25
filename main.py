from fastapi import FastAPI
from app.settings import settings
from app.endpoints.appointment_router import appointment_router

app = FastAPI(title='Appointment Service')

app.include_router(appointment_router, prefix='/api')