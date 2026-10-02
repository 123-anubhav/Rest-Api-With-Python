from fastapi import FastAPI

from configuration.database import Base, engine

from models import User

from controllers.user_controller import router as user_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Agentic AI API"
)


app.include_router(user_router)
