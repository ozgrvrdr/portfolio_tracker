from flask import Blueprint, render_template, redirect, url_for, flash, request  
from flask_login import login_user, logout_user, login_required, current_user  
from app import db, bcrypt  
from app.models import User  

# Blueprint oluşturma  
bp = Blueprint('auth', __name__)  

@bp.route('/register', methods=['GET', 'POST'])  
def register():  
    # Kullanıcı zaten giriş yapmışsa ana sayfaya yönlendir  
    if current_user.is_authenticated:  
        return redirect(url_for('portfolio.dashboard'))  
    
    if request.method == 'POST':  
        username = request.form.get('username')  
        email = request.form.get('email')  
        password = request.form.get('password')  
        
        # Kullanıcı adı veya email zaten var mı?  
        user_exists = User.query.filter(  
            (User.username == username) | (User.email == email)  
        ).first()  
        
        if user_exists:  
            flash('Kullanıcı adı veya email zaten kullanımda.', 'danger')  
            return redirect(url_for('auth.register'))  
        
        # Yeni kullanıcı oluştur  
        new_user = User(username=username, email=email)  
        new_user.set_password(password)  
        
        try:  
            db.session.add(new_user)  
            db.session.commit()  
            flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success')  
            return redirect(url_for('auth.login'))  
        except Exception as e:  
            db.session.rollback()  
            flash('Kayıt sırasında bir hata oluştu.', 'danger')  
    
    return render_template('auth/register.html')  

@bp.route('/login', methods=['GET', 'POST'])  
def login():  
    # Kullanıcı zaten giriş yapmışsa ana sayfaya yönlendir  
    if current_user.is_authenticated:  
        return redirect(url_for('portfolio.dashboard'))  
    
    if request.method == 'POST':  
        username = request.form.get('username')  
        password = request.form.get('password')  
        
        # Kullanıcıyı bul  
        user = User.query.filter_by(username=username).first()  
        
        if user and user.check_password(password):  
            login_user(user)  
            flash('Giriş başarılı!', 'success')  
            return redirect(url_for('portfolio.dashboard'))  
        else:  
            flash('Geçersiz kullanıcı adı veya şifre.', 'danger')  
    
    return render_template('auth/login.html')  

@bp.route('/logout')  
@login_required  
def logout():  
    logout_user()  
    flash('Çıkış yapıldı.', 'success')  
    return redirect(url_for('auth.login'))