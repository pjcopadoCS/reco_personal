from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from models import Wine,Compras, db

purchases_bp = Blueprint('purchases', __name__)

@purchases_bp.route('/insert_delete_wines', methods=['GET', 'POST'])
@login_required
def insert_delete_wines():
    if request.method == 'GET':
        wines = current_user.wines
        return render_template('insert_delete_wines.html', wines=wines)
    elif request.method == 'POST':
        code = request.form.get('wine').strip()
        wine = Wine.query.filter_by(code=code).first()
        if 'add' in request.form:
            if not wine:
                flash(f'Wine with code {code} does not exist', 'danger')
            elif wine not in current_user.wines:
                user = current_user
                user.wines.append(wine)
                compra =Compras(user_id=user.id,
                        o_user_id=user.id,
                        code=wine.code,
                        wine_id=wine.id,
                        o_wine_id=wine.id,
                        username=user.username)
                db.session.add(compra)
                db.session.commit()
                flash(f'Wine {code} inserted correctly', 'success')
            else:
                flash(f"This wine {code} already inserted in purchases of user {current_user.username.capitalize()}", 'warning')
        else:
            current_user.wines.remove(wine)
            db.session.commit()
            flash(f'Wine {code} removed correctly', 'success')
        return redirect(url_for('purchases.insert_delete_wines'))