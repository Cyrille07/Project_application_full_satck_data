from sqlalchemy.orm import Session
import crud, schemas, database

# --- Connexion à la base ---



def fill_data():
    UserToscane = schemas.UserCreate(first_name="Toscane" , last_name="Yoro" , email= "toscane@gmail.com")
    UserKouma = schemas.UserCreate(first_name="Cyrille" , last_name="Kouma" , email= "cyrille@gmail.com")
    UserAkpro = schemas.UserCreate(first_name="Joseph" , last_name="Akpro" , email= "joseph@gmail.com")
    
    Utilisateurs = [UserToscane, UserKouma, UserAkpro]

    ToscanePost = schemas.BlogPostCreate(title="l'art d'être sociable", content="Dsicuter avec des gens et avoir le smile")
    JosephPost = schemas.BlogPostCreate(title="la pilosophie", content="L'homme est un loup pour l'homme")
    CyrillePost = schemas.BlogPostCreate(title="Se démarquer", content="Savoir choisir ses personnages dans la vie de tous les jours")
    Posts =[ToscanePost, JosephPost, CyrillePost]

    db: Session = database.SessionLocal()

    for elt in Utilisateurs:
        crud.create_user( db , elt)

    for idx, post in enumerate(Posts, start=1):
        crud.create_blogpost(db, post, user_id=idx)


    db.close()
