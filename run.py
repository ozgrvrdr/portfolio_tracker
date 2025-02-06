from app import create_app, db  
from config import DevelopmentConfig  # Konfigürasyon import edildi  
import os  

# Ortam değişkenlerini yükle  
from dotenv import load_dotenv  
load_dotenv()  

# Uygulamayı geliştirme konfigürasyonu ile oluştur  
app = create_app(DevelopmentConfig)  

if __name__ == '__main__':  
    # Uygulama bağlamında veritabanı tablolarını oluştur  
    with app.app_context():  
        # Veritabanı tablolarını oluştur  
        db.create_all()  
        
        # İlk süper kullanıcı oluşturma (opsiyonel)  
        from app.models.user import User  
        
        # Eğer hiç kullanıcı yoksa bir admin kullanıcısı oluştur  
        if not User.query.first():  
            admin_user = User(  
                username='admin',   
                email='admin@portfoliotracker.com'  
            )  
            admin_user.set_password('admin123')  # Güçlü bir şifre kullan  
            db.session.add(admin_user)  
            db.session.commit()  
            print("İlk admin kullanıcısı oluşturuldu.")  
    
    # Sunucu ayarları  
    host = os.environ.get('HOST', '127.0.0.1')  
    port = int(os.environ.get('PORT', 5000))  
    
    # Uygulamayı geliştirme modunda çalıştır  
    app.run(  
        debug=True,   
        host=host,   
        port=port  
    )