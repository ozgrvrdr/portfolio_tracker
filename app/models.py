from app import db, login_manager  
from flask_login import UserMixin  
from datetime import datetime  
from werkzeug.security import generate_password_hash, check_password_hash  

@login_manager.user_loader  
def load_user(user_id):  
    return User.query.get(int(user_id))  

class User(UserMixin, db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(50), unique=True, nullable=False)  
    email = db.Column(db.String(120), unique=True, nullable=False)  
    password_hash = db.Column(db.String(255), nullable=False)  
    
    # Şifre için güvenli yöntemler  
    def set_password(self, password):  
        self.password_hash = generate_password_hash(password)  
    
    def check_password(self, password):  
        return check_password_hash(self.password_hash, password)  
    
    # Kullanıcının portföyleri  
    portfolios = db.relationship('Portfolio', backref='owner', lazy=True)  

class Portfolio(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(100), nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    
    # Portföydeki varlıklar  
    assets = db.relationship('Asset', backref='portfolio', lazy=True)  

class Asset(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)  
    
    name = db.Column(db.String(100), nullable=False)  
    type = db.Column(db.String(50), nullable=False)  # Hisse, kripto vs.  
    quantity = db.Column(db.Float, nullable=False)  
    purchase_price = db.Column(db.Float, nullable=False)  
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)  
    
    # İsteğe bağlı satış bilgileri  
    sold_price = db.Column(db.Float, nullable=True)  
    sold_date = db.Column(db.DateTime, nullable=True)