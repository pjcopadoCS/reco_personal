from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from models import Wine, db

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
                flash(f'El vi amb el codi {code} no existeix', 'danger')
            elif wine not in current_user.wines:
                current_user.wines.append(wine)
                db.session.commit()
                flash(f'Vi {code} insertit correctament', 'success')
            else:
                flash(f"El vi {code} ja figura a la llista de compres de l'usuari {current_user.username.capitalize()}", 'warning')
        else:
            current_user.wines.remove(wine)
            db.session.commit()
            flash(f'Vi {code} eliminat correctament', 'success')
        return redirect(url_for('purchases.insert_delete_wines'))