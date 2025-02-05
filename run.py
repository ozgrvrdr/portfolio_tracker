from app import create_app, db  

# Uygulamayı oluştur  
app = create_app()  

if __name__ == '__main__':  
    # Uygulama bağlamında veritabanı tablolarını oluştur  
    with app.app_context():  
        db.create_all()  
    
    # Uygulamayı geliştirme modunda çalıştır  
    app.run(debug=True)