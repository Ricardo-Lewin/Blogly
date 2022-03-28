"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "apple"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def root():
    """Show recent list of posts, most-recent first."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("homepage.html", posts=posts)


##### User Routes #####

@app.route('/users')
def list_users():
    """Show All Users and add user form"""
    users = User.query.all()
    return render_template('users_listing.html', users=users)


@app.route('/users/new')
def add_user_form():
    """Show form to add user"""
    return render_template('add_user.html')


@app.route('/users/new', methods=["POST"])
def add_user():
    """Submits Form Data and adds to database"""
    new_user = User(
        first_name=request.form['first-name'],
        last_name=request.form['last-name'],
        image_url=request.form['image'] or None)

    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_details(user_id):
    """Show User details"""
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Show Edit User Page"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Submits Form Data and adds to database"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['image']

    db.session.add(user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_delete(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


##### Posts Routes #####

@app.route('/posts/<int:post_id>')
def post_details(post_id):
    """Show User's Post details"""
    post = Post.query.get_or_404(post_id)
    return render_template('user_post.html', post=post)


@app.route('/users/<int:user_id>/posts/new')
def add_post_form(user_id):
    """Show form to add new post"""
    user = User.query.get_or_404(user_id)
    return render_template('post_form.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """Submits Form Data and adds to database"""
    user = User.query.get_or_404(user_id)
    new_post = Post(
        title=request.form['title'],
        content=request.form['content'],
        user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")
    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """Show Edit Post Form"""
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Submits Form Data and adds to database"""
    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    return redirect(f'/users/{post.user.id}')


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def post_delete(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")
