"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, BlogUser, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route("/")
def index():
    """ Loads Home Page """
    users = BlogUser.query.all()
    return render_template("users.html", users = users)

@app.route("/users/new")
def user_form():

     return render_template("user_form.html")



@app.route("/users/new", methods=["POST"])
def make_user():
    """ Post request to create new user """
    first_name = request.form["fname"]
    last_name = request.form["lname"]
    pic = request.form["imgURL"] or None

    blog_user = BlogUser(first_name=first_name, last_name=last_name, image_url=pic)
    db.session.add(blog_user)
    db.session.commit()

    return redirect("/")

@app.route("/user/<int:BlogUser_id>")
def user_page(BlogUser_id):
    """Show info on a single user."""
    user = BlogUser.query.get_or_404(BlogUser_id)
    posts = user.posts
    return render_template("user_details.html", user=user, posts=posts)

@app.route("/user/<int:user_id>/edit")
def user_edit(user_id):
    """Edit a single user."""

    user = BlogUser.query.get_or_404(user_id)
    return render_template("user_edit.html", user=user)


@app.route("/user/", methods=["POST"])
def save_edit():
    """Save single user edit."""
    first_name = request.form["fname"]
    last_name = request.form["lname"]
    pic = request.form["imgURL"] or None
    user_id = request.form["id"]
    
    user = BlogUser.query.get_or_404(user_id)

    user.first_name = first_name 
    user.last_name = last_name
    user.image_url = pic

    db.session.commit()

    return redirect("/")

@app.route("/delete/<int:user_id>")
def user_delete(user_id):
    """Delete a single user."""

    user = BlogUser.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")

@app.route("/users/<int:user_id>/posts/new", methods=["GET", "POST"])
def user_add_post(user_id):
    """Creates Form to add post"""
    user = BlogUser.query.get_or_404(user_id)
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(f"/user/{user_id}")
    else:
        return render_template("new_post_form.html", user=user)

@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    """Display details of a single post. """
    post = Post.query.get_or_404(post_id)
    user = post.author
    return render_template("post_detail.html", post = post, user = user)


@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    """ Edit a single post. """

    post = Post.query.get_or_404(post_id)

    if request.method == "POST":
            post.title = request.form["title"]
            post.content = request.form["content"]

            db.session.commit()
            return redirect(f"/posts/{post_id}")    
    else:
        return render_template("post_edit.html", post = post)


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete a single post. """

    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/user/{user_id}")

