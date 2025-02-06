from app import db  
from sqlalchemy.orm import relationship  
from datetime import datetime  

class Transaction(db.Model):  
    __tablename__ = 'transactions'  
    
    id = db.Column(db.Integer, primary_key=True)  
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)  
    portfolyo_id = db.Column(db.Integer, db.ForeignKey('portfolyolar.id'), nullable=False)  
    
    transaction_type = db.Column(db.String(10), nullable=False)  # 'buy' or 'sell'  
    quantity = db.Column(db.Float, nullable=False)  
    price = db.Column(db.Float, nullable=False)  
    date = db.Column(db.DateTime, default=datetime.utcnow)  
    
    # İlişkiler  
    asset = relationship('Asset')  
    portfolyo = relationship('Portfolyo')  
    
    def __repr__(self):  
        return f'<Transaction {self.transaction_type} {self.quantity} {self.asset.name}>'