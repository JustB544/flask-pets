from models import db, connect_db, Pet
from app import app

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        pet1 = Pet(name="Woofly", species="Dog", age=6, notes="Likes to be called a good boy",
                   photo_url="https://media.npr.org/assets/img/2022/08/26/img_9911-751a5efa015240804a553b880ae7a537c413d28a-s1100-c50.jpg")
        pet2 = Pet(name="Porchetta", species="Porcupine",
                   photo_url="https://d18lev1ok5leia.cloudfront.net/chesapeakebay/field-guide/north-american-porcupine/_700x600_fit_center-center_none/porcupinefieldguide_thumb-01.jpg")
        pet3 = Pet(name="Snargle", species="Cat", 
                   photo_url="https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_2x3.jpg",
                   available=False)
        
        db.session.add_all([pet1, pet2, pet3])
        db.session.commit()
seed()