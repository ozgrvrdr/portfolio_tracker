from flask import Blueprint, render_template, redirect, url_for, flash, request  
from flask_login import login_required, current_user  
from app import db  
from app.models import Portfolio, Asset  

# Blueprint oluşturma  
bp = Blueprint('portfolio', __name__)  

@bp.route('/dashboard')  
@login_required  
def dashboard():  
    # Kullanıcının portföylerini getir  
    portfolios = Portfolio.query.filter_by(user_id=current_user.id).all()  
    return render_template('portfolio/dashboard.html', portfolios=portfolios)  

@bp.route('/create_portfolio', methods=['GET', 'POST'])  
@login_required  
def create_portfolio():  
    if request.method == 'POST':  
        portfolio_name = request.form.get('portfolio_name')  
        
        # Portföy adı kontrolü  
        existing_portfolio = Portfolio.query.filter_by(  
            name=portfolio_name,   
            user_id=current_user.id  
        ).first()  
        
        if existing_portfolio:  
            flash('Bu isimde bir portföyünüz zaten var.', 'danger')  
            return redirect(url_for('portfolio.create_portfolio'))  
        
        # Yeni portföy oluştur  
        new_portfolio = Portfolio(  
            name=portfolio_name,   
            user_id=current_user.id  
        )  
        
        try:  
            db.session.add(new_portfolio)  
            db.session.commit()  
            flash('Portföy başarıyla oluşturuldu!', 'success')  
            return redirect(url_for('portfolio.dashboard'))  
        except Exception as e:  
            db.session.rollback()  
            flash('Portföy oluşturulurken bir hata oluştu.', 'danger')  
    
    return render_template('portfolio/create_portfolio.html')  

@bp.route('/portfolio/<int:portfolio_id>')  
@login_required  
def portfolio_details(portfolio_id):  
    # Portföyü ve varlıklarını getir  
    portfolio = Portfolio.query.get_or_404(portfolio_id)  
    
    # Kullanıcının kendi portföyü mü kontrol et  
    if portfolio.user_id != current_user.id:  
        flash('Bu portföye erişim izniniz yok.', 'danger')  
        return redirect(url_for('portfolio.dashboard'))  
    
    # Portföydeki varlıkları getir  
    assets = Asset.query.filter_by(portfolio_id=portfolio_id).all()  
    
    return render_template('portfolio/portfolio_details.html',   
                           portfolio=portfolio,   
                           assets=assets)