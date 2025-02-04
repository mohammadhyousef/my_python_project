import sqlite3
from flask import Flask, redirect, request, url_for, render_template

app = Flask(__name__)

DATABASE = 'blog.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

@app.route('/posts')
def index():
    connection = get_db()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)
  
@app.route('/posts/<int:post_id>')
def show(post_id):
    connection = get_db()
    post = connection.execute('SELECT * FROM posts WHERE id=?', (post_id,)).fetchone()
    return render_template('show.html', post=post)


@app.route('/posts/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        connection = get_db()
        title = request.form['title']
        body = request.form['body']
        connection.execute('INSERT INTO posts (title, body, author_id) VALUES (?,?,?)', (title, body, 1))
        connection.commit()
        connection.close()
        return redirect(url_for('index'))
    return render_template('create.html')