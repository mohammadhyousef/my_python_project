from flask import request, render_template, url_for, flash, session, g, redirect, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from blog import get_db
import functools

bp = Blueprint('auth', __name__)



@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        error = None

        if not username:
            error = 'الرجاء ادخال اسم المستخدم'
        if not email:
            error = 'الرجاء ادخال البريد الإلكتروني'
        if not password:
            error = 'الرجاء ادخال كلمة المرور'

        if error == None:
            db = get_db()

            try:
                db.execute('INSERT INTO users (username, email, password) VALUES (?,?,?)', (username, email, generate_password_hash(password)))
                db.commit()
                db.close()
            except db.IntegrityError: # type: ignore
                error = f'{username} مسجل بالفعل'
            else:
                return redirect(url_for('auth.login'))
            
            flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None 
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone() 

        
        if not email:
            error = 'البريد الإلكتروني غير مسجل '
        elif not check_password_hash(user['password'], password):
            error = 'كلمة المرور خاطئة '

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('blog.index'))
    
        flash(error)

    if g.user:
        return redirect(url_for('index'))
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id == None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM users WHERE id = ?', (user_id, )).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.index'))

@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    # code to handle reset password request
    return render_template('auth.Reset_request.html')
 
            