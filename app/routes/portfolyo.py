from flask import Blueprint, render_template, redirect, url_for, flash, request  
from flask_login import login_required, current_user  
from app import db  
from app.models import Portfolyo, Asset  # Portfolio -> Portfolyo  

# Blueprint oluşturma  
bp = Blueprint('portfolyo', __name__)  # 'portfolio' -> 'portfolyo'  

@bp.route('/dashboard')  
@login_required  
def dashboard():  
    portfolyolar = Portfolyo.query.filter_by(user_id=current_user.id).all()  
    return render_template('portfolyo/dashboard.html', portfolyolar=portfolyolar)  

@bp.route('/create_portfolyo', methods=['GET', 'POST'])  
@login_required  
def create_portfolyo():  
    if request.method == 'POST':  
        name = request.form.get('name')  
        
        # Yeni portföy oluştur  
        new_portfolyo = Portfolyo(  
            name=name,  
            user_id=current_user.id  
        )  
        
        try:  
            db.session.add(new_portfolyo)  
            db.session.commit()  
            flash('Portföy başarıyla oluşturuldu!', 'success')  
            return redirect(url_for('portfolyo.dashboard'))  
        except Exception as e:  
            db.session.rollback()  
            flash('Portföy oluşturulurken bir hata oluştu.', 'danger')  
    
    return render_template('portfolyo/create_portfolyo.html')  

@bp.route('/portfolyo_details/<int:portfolyo_id>')  
@login_required  
def portfolyo_details(portfolyo_id):  
    portfolyo = Portfolyo.query.get_or_404(portfolyo_id)  
    
    # Kullanıcının kendi portföyü mü kontrol et  
    if portfolyo.user_id != current_user.id:  
        flash('Bu portföye erişim izniniz yok.', 'danger')  
        return redirect(url_for('portfolyo.dashboard'))  
    
    return render_template('portfolyo/portfolyo_details.html', portfolyo=portfolyo)  

# Diğer route fonksiyonları da benzer şekilde güncellenecek