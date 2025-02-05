import os  

class Config:  
    # Güvenlik için gizli anahtar  
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'portfolio_tracker_secret_key_2024'  
    
    # Veritabanı bağlantısı (SQLite kullanılacak)  
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///portfolio.db'  
    
    # Veritabanı izleme kapalı  
    SQLALCHEMY_TRACK_MODIFICATIONS = False  

class DevelopmentConfig(Config):  
    DEBUG = True  

class ProductionConfig(Config):  
    DEBUG = False  

class TestingConfig(Config):  
    TESTING = True  
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'