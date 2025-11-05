from sqlalchemy.orm import Session
import crud, schemas, database

# --- Connexion à la base ---

def fill_data():

    db: Session = database.SessionLocal()

    UserToscane = schemas.UserCreate(first_name="Toscane" , last_name="Yoro" , email= "toscane@gmail.com")
    UserKouma = schemas.UserCreate(first_name="Cyrille" , last_name="Kouma" , email= "cyrille@gmail.com")
    UserAkpro = schemas.UserCreate(first_name="Joseph" , last_name="Akpro" , email= "joseph@gmail.com")

    crud.create_user( db , UserToscane)
    crud.create_user( db , UserKouma)
    crud.create_user( db , UserAkpro)

    db.close()
    print("Données insérées avec succès !")
