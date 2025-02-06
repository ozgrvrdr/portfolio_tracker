from flask import Blueprint, render_template, redirect, url_for, flash, request  
from flask_login import login_required, current_user  
from app import db  
from app.models import Portfolyo, Asset  # Portfolio -> Portfolyo  
from datetime import datetime  

# Blueprint oluşturma  
bp = Blueprint('assets', __name__)  

@bp.route('/add_asset/<int:portfolyo_id>', methods=['GET', 'POST'])  # portfolio_id -> portfolyo_id  
@login_required  
def add_asset(portfolyo_id):  # portfolio_id -> portfolyo_id  
    # Portföyü kontrol et  
    portfolyo = Portfolyo.query.get_or_404(portfolyo_id)  # Portfolio -> Portfolyo  
    
    # Kullanıcının kendi portföyü mü kontrol et  
    if portfolyo.user_id != current_user.id:  
        flash('Bu portföye varlık ekleme izniniz yok.', 'danger')  
        return redirect(url_for('portfolyo.dashboard'))  # portfolio -> portfolyo  
    
    if request.method == 'POST':  
        name = request.form.get('name')  
        asset_type = request.form.get('type')  
        quantity = float(request.form.get('quantity'))  
        purchase_price = float(request.form.get('purchase_price'))  
        purchase_date = request.form.get('purchase_date')  
        
        # Yeni varlık oluştur  
        new_asset = Asset(  
            portfolyo_id=portfolyo_id,  # portfolio_id -> portfolyo_id  
            name=name,  
            type=asset_type,  
            quantity=quantity,  
            purchase_price=purchase_price,  
            purchase_date=datetime.strptime(purchase_date, '%Y-%m-%d') if purchase_date else datetime.utcnow()  
        )  
        
        try:  
            db.session.add(new_asset)  
            db.session.commit()  
            flash('Varlık başarıyla eklendi!', 'success')  
            return redirect(url_for('portfolyo.portfolyo_details', portfolyo_id=portfolyo_id))  # portfolio -> portfolyo  
        except Exception as e:  
            db.session.rollback()  
            flash('Varlık eklenirken bir hata oluştu.', 'danger')  
    
    return render_template('portfolyo/add_asset.html', portfolyo=portfolyo)  # portfolio -> portfolyo  
    
@bp.route('/edit_asset/<int:asset_id>', methods=['GET', 'POST'])  
@login_required  
def edit_asset(asset_id):  
    # Varlığı ve bağlı olduğu portföyü getir  
    asset = Asset.query.get_or_404(asset_id)  
    portfolyo = asset.portfolyo  # portfolio -> portfolyo  
    
    # Kullanıcının kendi portföyü mü kontrol et  
    if portfolyo.user_id != current_user.id:  
        flash('Bu varlığı düzenleme izniniz yok.', 'danger')  
        return redirect(url_for('portfolyo.dashboard'))  # portfolio -> portfolyo  
    
    if request.method == 'POST':  
        # Güncelleme bilgileri  
        asset.name = request.form.get('name')  
        asset.type = request.form.get('type')  
        asset.quantity = float(request.form.get('quantity'))  
        asset.purchase_price = float(request.form.get('purchase_price'))  
        
        # Satış bilgileri (isteğe bağlı)  
        sold_price = request.form.get('sold_price')  
        sold_date = request.form.get('sold_date')  
        
        if sold_price:  
            asset.sold_price = float(sold_price)  
        if sold_date:  
            asset.sold_date = datetime.strptime(sold_date, '%Y-%m-%d')  
        
        try:  
            db.session.commit()  
            flash('Varlık başarıyla güncellendi!', 'success')  
            return redirect(url_for('portfolyo.portfolyo_details', portfolyo_id=portfolyo.id))  # portfolio -> portfolyo  
        except Exception as e:  
            db.session.rollback()  
            flash('Varlık güncellenirken bir hata oluştu.', 'danger')  
    
    return render_template('portfolyo/edit_asset.html', asset=asset, portfolyo=portfolyo)  # portfolio -> portfolyo  
    
@bp.route('/delete_asset/<int:asset_id>', methods=['POST'])  
@login_required  
def delete_asset(asset_id):  
    # Varlığı ve bağlı olduğu portföyü getir  
    asset = Asset.query.get_or_404(asset_id)  
    portfolyo = asset.portfolyo  # portfolio -> portfolyo  
    
    # Kullanıcının kendi portföyü mü kontrol et  
    if portfolyo.user_id != current_user.id:  
        flash('Bu varlığı silme izniniz yok.', 'danger')  
        return redirect(url_for('portfolyo.dashboard'))  # portfolio -> portfolyo  
    
    try:  
        db.session.delete(asset)  
        db.session.commit()  
        flash('Varlık başarıyla silindi!', 'success')  
    except Exception as e:  
        db.session.rollback()  
        flash('Varlık silinirken bir hata oluştu.', 'danger')  
    
    return redirect(url_for('portfolyo.portfolyo_details', portfolyo_id=portfolyo.id))  # portfolio -> portfolyo