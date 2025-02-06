from app import db  
from sqlalchemy.orm import relationship  

class Asset(db.Model):  
    __tablename__ = 'assets'  
    
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(100), nullable=False)  
    quantity = db.Column(db.Float, nullable=False)  
    price = db.Column(db.Float, nullable=False)  
    
    # İlişkiler  
    portfolyo_id = db.Column(db.Integer, db.ForeignKey('portfolyolar.id'), nullable=False)  
    portfolyo = relationship('Portfolyo', back_populates='assets')  
    
    def __repr__(self):  
        return f'<Asset {self.name}>'  
    
    @property  
    def total_value(self):  
        return self.quantity * self.price