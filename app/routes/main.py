from flask import Blueprint, render_template, redirect, url_for  
from flask_login import login_required, current_user  

bp = Blueprint('main', __name__)  

@bp.route('/')  
def index():  
    if current_user.is_authenticated:  
        return render_template('main/dashboard.html')  
    return render_template('main/welcome.html')