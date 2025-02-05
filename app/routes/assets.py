from flask import Blueprint, render_template, redirect, url_for, flash, request  
from flask_login import login_required, current_user  
from app import db  
from app.models import Portfolio, Asset  
from datetime import datetime  

# Blueprint oluşturma  
bp = Blueprint('assets', __name__)  

@bp.route('/add_asset/<int:portfolio_id>', methods=['GET', 'POST'])  
@login_required  
def add_asset(portfolio_id):  
    # Portföyü kontrol et  
    portfolio = Portfolio.query.get_or_404(portfolio_id)  
    
    # Kullanıcının kendi portföyü mü kontrol et  
    if portfolio.user_id != current_user.id:  
        flash('Bu portföye varlık ekleme izniniz yok.', 'danger')  
        return redirect(url_for('portfolio.dashboard'))  
    
    if request.method == 'POST':  
        name = request.form.get('name')  
        asset_type = request.form.get('type')  
        quantity = float(request.form.get('quantity'))  
        purchase_price = float(request.form.get('purchase_price'))  
        purchase_date = request.form.get('purchase_date')  
        
        # Yeni varlık oluştur  
        new_asset = Asset(  
            portfolio_id=portfolio_id,  
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
            return redirect(url_for('portfolio.portfolio_details', portfolio_id=portfolio_id))  
        except Exception as e:  
            db.session.rollback()  
            flash('Varlık eklenirken bir hata oluştu.', 'danger')  
    
    return render_template('assets/add_asset.html', portfolio=portfolio)  

@bp.route('/edit_asset/<int:asset_id>', methods=['GET', 'POST'])  
@login_required  
def edit_asset(asset_id):  
    # Varlığı ve bağlı olduğu portföyü getir  
    asset = Asset.query.get_or_404(asset_id)  
    portfolio = asset.portfolio  
    
    # Kullanıcının kendi portföyü mü kontrol et  
    if portfolio.user_id != current_user.id:  
        flash('Bu varlığı düzenleme izniniz yok.', 'danger')  
        return redirect(url_for('portfolio.dashboard'))  
    
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
            return redirect(url_for('portfolio.portfolio_details', portfolio_id=portfolio.id))  
        except Exception as e:  
            db.session.rollback()  
            flash('Varlık güncellenirken bir hata oluştu.', 'danger')  
    
    return render_template('assets/edit_asset.html', asset=asset, portfolio=portfolio)  

@bp.route('/delete_asset/<int:asset_id>', methods=['POST'])  
@login_required  
def delete_asset(asset_id):  
    # Varlığı ve bağlı olduğu portföyü getir  
    asset = Asset.query.get_or_404(asset_id)  
    portfolio = asset.portfolio  
    
    # Kullanıcının kendi portföyü mü kontrol et  
    if portfolio.user_id != current_user.id:  
        flash('Bu varlığı silme izniniz yok.', 'danger')  
        return redirect(url_for('portfolio.dashboard'))  
    
    try:  
        db.session.delete(asset)  
        db.session.commit()  
        flash('Varlık başarıyla silindi!', 'success')  
    except Exception as e:  
        db.session.rollback()  
        flash('Varlık silinirken bir hata oluştu.', 'danger')  
    
    return redirect(url_for('portfolio.portfolio_details', portfolio_id=portfolio.id))