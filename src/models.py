# imports 
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from src.extensions import db,ma,login_manager
import secrets

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    
    cars = db.relationship('CarCollection', backref='user', lazy=True)

    def __init__(self, email, first_name='', last_name='', password='', token=''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.email}>'

class CarCollection(db.Model):
    id = db.Column(db.String, primary_key = True)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable = False)

    def __init__(self,brand,model,year,user_id, id = ''):
        self.id = self.set_id()
        self.brand = brand
        self.model = model
        self.year = year
        self.user_id = user_id


    def __repr__(self):
        return f'<CarCollection: {self.brand}-{self.model}-{self.year}'

    def set_id(self):
        return (secrets.token_urlsafe())


class CarCollectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CarCollection
        fields = ('id', 'brand', 'model','year')

car_schema = CarCollectionSchema()
cars_schema = CarCollectionSchema(many=True)