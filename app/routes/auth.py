from flask import Blueprint, render_template, redirect, url_for, flash, request  
from flask_login import login_user, logout_user, login_required, current_user  
from flask_wtf import FlaskForm  
from wtforms import StringField, PasswordField, SubmitField  
from wtforms.validators import DataRequired, Email, EqualTo  
from app.models.user import User  
from app import db, bcrypt  

bp = Blueprint('auth', __name__)  

class RegisterForm(FlaskForm):  
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])  
    email = StringField('E-posta', validators=[DataRequired(), Email()])  
    password = PasswordField('Şifre', validators=[DataRequired()])  
    confirm_password = PasswordField('Şifreyi Onayla', validators=[DataRequired(), EqualTo('password')])  
    submit = SubmitField('Kayıt Ol')  

class LoginForm(FlaskForm):  
    email = StringField('E-posta', validators=[DataRequired(), Email()])  
    password = PasswordField('Şifre', validators=[DataRequired()])  
    submit = SubmitField('Giriş Yap')  # Butondaki yazıyı değiştirin  

@bp.route('/register', methods=['GET', 'POST'])  
def register():  
    form = RegisterForm()  
    if form.validate_on_submit():  
        # Kullanıcı kayıt işlemi  
        existing_user = User.query.filter_by(email=form.email.data).first()  
        if existing_user:  
            flash('Bu e-posta zaten kayıtlı.')  
            return redirect(url_for('auth.register'))  
        
        new_user = User(  
            username=form.username.data,  
            email=form.email.data  
        )  
        new_user.set_password(form.password.data)  
        
        db.session.add(new_user)  
        db.session.commit()  
        
        flash('Kayıt başarılı! Giriş yapabilirsiniz.')  
        return redirect(url_for('auth.login'))  
    
    return render_template('auth/register.html', form=form)  

@bp.route('/login', methods=['GET', 'POST'])  
def login():  
    # Eğer kullanıcı zaten giriş yapmışsa dashboard'a yönlendir  
    if current_user.is_authenticated:  
        return redirect(url_for('main.dashboard'))  

    form = LoginForm()  
    if form.validate_on_submit():  
        user = User.query.filter_by(email=form.email.data).first()  
        if user and user.check_password(form.password.data):  
            login_user(user)  
            flash('Giriş başarılı!')  
            return redirect(url_for('main.dashboard'))  # Dashboard rotasına yönlendir  
        else:  
            flash('Geçersiz e-posta veya şifre')  
    
    return render_template('auth/login.html', form=form)  

@bp.route('/logout')  
@login_required  
def logout():  
    logout_user()  
    flash('Çıkış yapıldı.')  
    return redirect(url_for('auth.login'))  # İki nokta üst üste kaldırıldı