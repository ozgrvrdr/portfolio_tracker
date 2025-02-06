from flask import Flask  
from flask_sqlalchemy import SQLAlchemy  
from flask_login import LoginManager  
from flask_migrate import Migrate  
from flask_bcrypt import Bcrypt  
from config import Config  

# Global nesneleri oluştur  
db = SQLAlchemy()  
login_manager = LoginManager()  
migrate = Migrate()  
bcrypt = Bcrypt()  

def create_app(config_class=Config):  
    # Flask uygulamasını oluştur  
    app = Flask(__name__)  
    
    # Konfigürasyonları yükle  
    app.config.from_object(config_class)  
    
    # Eklentileri başlat  
    db.init_app(app)  
    login_manager.init_app(app)  
    migrate.init_app(app, db)  
    bcrypt.init_app(app)  
    
    # Login yöneticisi ayarları  
    login_manager.login_view = 'auth.login'  
    
    # Modelleri import et  
    from .models import User, Portfolyo, Asset  
    
    # Route'ları import et  
    from .routes import auth, portfolyo, assets, main  
    
    # Blueprint'leri kaydet  
    app.register_blueprint(auth.bp)  
    app.register_blueprint(portfolyo.bp)  
    app.register_blueprint(assets.bp)  
    app.register_blueprint(main.bp)  
    
    return app