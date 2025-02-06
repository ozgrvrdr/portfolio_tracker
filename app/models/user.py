from app import db, bcrypt, login_manager  
from flask_login import UserMixin  

class User(UserMixin, db.Model):  
    __tablename__ = 'users'  
    
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(50), unique=True, nullable=False)  
    email = db.Column(db.String(120), unique=True, nullable=False)  
    password_hash = db.Column(db.String(255), nullable=False)  
    
    # İlişkiler  
    portfolyolar = db.relationship('Portfolyo', back_populates='user', cascade='all, delete-orphan')  
    
    def set_password(self, password):  
        # Şifreyi hash'le  
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')  
    
    def check_password(self, password):  
        # Şifre kontrolü  
        return bcrypt.check_password_hash(self.password_hash, password)  
    
    def __repr__(self):  
        return f'<User {self.username}>'  

@login_manager.user_loader  
def load_user(user_id):  
    return User.query.get(int(user_id))