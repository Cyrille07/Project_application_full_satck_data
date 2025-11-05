from fastapi import FastAPI
from routers import users, blogposts
import models, database
import fill_database



models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# ✅ Crée les tables après que la base soit prête
@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=database.engine)

    # ✅ Remplit la base seulement si elle est vide
    db = database.SessionLocal()
    users_exist = db.query(models.User).first()
    if not users_exist:
        fill_database.fill_data()
    db.close()
    print("✅ Base initialisée avec succès !")


app.include_router(users.router)
app.include_router(blogposts.router)