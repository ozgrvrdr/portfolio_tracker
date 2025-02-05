from flask import Flask  
from flask_sqlalchemy import SQLAlchemy  
from flask_bcrypt import Bcrypt  
from flask_login import LoginManager  
from config import Config  

# Temel nesneleri oluştur  
db = SQLAlchemy()  
bcrypt = Bcrypt()  
login_manager = LoginManager()  

def create_app(config_class=Config):  
    # Flask uygulamasını başlat  
    app = Flask(__name__)  
    
    # Yapılandırma ayarlarını yükle  
    app.config.from_object(config_class)  
    
    # Eklentileri başlat  
    db.init_app(app)  
    bcrypt.init_app(app)  
    login_manager.init_app(app)  
    
    # Giriş sayfasını ayarla  
    login_manager.login_view = 'auth.login'  
    
    # Blueprint'leri içe aktar (sonra eklenecek)  
    from .routes import auth, portfolio, assets  
    
    # Blueprint'leri kaydet  
    app.register_blueprint(auth.bp)  
    app.register_blueprint(portfolio.bp)  
    app.register_blueprint(assets.bp)  
    
    return app