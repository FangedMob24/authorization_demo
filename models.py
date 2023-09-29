from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    """User information"""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, unique=True)

    password = db.Column(db.Text, nullable=False)
    
    email = db.Column(db.String(50), nullable=False, unique=True)
    
    first_name = db.Column(db.String(30), nullable=False)
    
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship('Feedback', backref='users')

    @classmethod
    def register(cls,username,pwd,email,first_name,last_name):
        

        hashed = bcrypt.generate_password_hash(pwd)

        hased_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hased_utf8, email=email,
                   first_name=first_name, last_name=last_name)
    
    @classmethod
    def authenticate(cls,username,pwd):

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False
        

        
class Feedback(db.Model):
    """  """

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.Text, nullable=False)

    username = db.Column(db.Text, db.ForeignKey('users.username'))