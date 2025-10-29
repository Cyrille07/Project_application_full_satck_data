from fastapi import FastAPI
from routers import users, blogposts
from . import models, database



models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(blogposts.router)