from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class BlogUser(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                        nullable=False)
    last_name = db.Column(db.String(50), 
                        nullable=False)
    image_url = db.Column(db.Text,
                        nullable=True,
                        default='https://ukdj.imgix.net/455a0284eb7a4194d11239e17b11ab2a_/generic-user-profile_354184.png')
    
    posts = db.relationship('Post')

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """Post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(300),
                        nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    # https://stackoverflow.com/questions/12154129/how-can-i-automatically-populate-sqlalchemy-database-fields-flask-sqlalchemy
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )
    
    author = db.relationship('BlogUser')