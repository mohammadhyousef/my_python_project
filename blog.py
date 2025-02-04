from os import abort
from flask import current_app as app, request, session, redirect, url_for, render_template, flash, g, Blueprint, flash, Flask
import sqlite3
import functools





DATABASE = 'blog.db'

bp= Blueprint('blog', __name__, url_prefix='/posts')

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def login_required(func):
    @functools.wraps(func)
    def wrapped_func(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return func(**kwargs)
    
    return wrapped_func

def get_post(post_id, check_author = True):
    post = get_db().execute('SELECT * FROM posts WHERE id = ?', (post_id, )).fetchone()

    if post is None:
        abort(404, f'المقالة ذات المعرف {post_id}غير موجودة') # type: ignore
    
    if check_author and post['author_id'] != g.user['id']:
        abort(403) # type: ignore
    
    return post 

@bp.route('/')
def index():
    connection = get_db()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)


@bp.route('/<int:post_id>')
def show(post_id):
    post = get_post(post_id, check_author = False)
    return render_template('show.html', post=post)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        connection = get_db()
        title = request.form['title']
        body = request.form['body']
        connection.execute('INSERT INTO posts (title, body, author_id) VALUES(?,?,?)', (title, body, g.user['id']))
        connection.commit()
        connection.close()
        return redirect(url_for('blog.index'))
    return render_template('create.html')

@bp.route('/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = get_post(post_id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None 

        if not title:
            error = 'ادخل العنوان'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute('UPDATE posts SET title = ?, body = ? WHERE id = ?', (title, body, post_id))
            db.commit()
            db.close()
            return redirect(url_for('blog.index'))
        
    return render_template('create.html', post=post)
    

@bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete(post_id):
    post = get_post(post_id)
    db = get_db()
    db.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    db.commit()
    db.close()
    return redirect(url_for('blog.index'))

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'youremail@gmail.com'
app.config['MAIL_PASSWORD'] = 'yourpassword'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True



@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        # code to check if email exists in the database
        # code to generate a unique reset password token
        # code to store reset password token in the database
        # code to send reset password email
        #token =