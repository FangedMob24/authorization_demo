from models import db, User, Feedback
from app import app

with app.app_context():
    db.drop_all()
    db.create_all()

u1 = User.register(
    "Fred",
    "Fred!",
    "fred@gmail.com",
    "Fred",
    "Baxter",
    )

u2 = User.register(
    "Maddox",
    "Maddox!",
    "Maddox@gmail.com",
    "Maddox",
    "Baxter",
    )

with app.app_context():
    db.session.add_all([u1,u2])
    db.session.commit()

f1 = Feedback(
    title = "Fred post",
    content = "This is a red dog",
    username = "Fred",
)

f2 = Feedback(
    title = "Maddox post",
    content = "This is a white dog",
    username = "Maddox",
)

with app.app_context():
    db.session.add_all([f1,f2])
    db.session.commit()