from app import db  
from sqlalchemy.orm import relationship  

class Portfolyo(db.Model):  
    __tablename__ = 'portfolyolar'  
    
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(100), nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    
    # İlişkiler  
    user = relationship('User', back_populates='portfolyolar')  
    assets = relationship('Asset', back_populates='portfolyo', cascade='all, delete-orphan')  
    
    def __repr__(self):  
        return f'<Portfolyo {self.name}>'  
    
    @property  
    def total_value(self):  
        return sum(asset.total_value for asset in self.assets)