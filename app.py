"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, BlogUser, Post

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

@app.route("/<int:BlogUser_id>")
def user_page(BlogUser_id):
    """Show info on a single user."""
    user = BlogUser.query.get_or_404(BlogUser_id)
    posts = user.posts
    return render_template("user_details.html", user=user, posts=posts)

@app.route("/user/<int:userID>/edit")
def user_edit(userID):
    """Edit a single user."""

    user = BlogUser.query.get_or_404(userID)
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

@app.route("/delete/<int:userID>")
def user_delete(userID):
    """Delete a single user."""

    user = BlogUser.query.get_or_404(userID)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")

@app.route("/users/<int:userID>/posts/new", methods=["GET", "POST"])
def user_add_post(userID):
    """Creates Form to add post"""
    user = BlogUser.query.get_or_404(userID)
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        new_post = Post(title=title, content=content, user_id=userID)
        db.session.add(new_post)
        db.session.commit()
        return redirect(f"/{userID}")
    else:
        return render_template("new_post_form.html", user=user)

# @app.route("/posts/<int:userID>")


