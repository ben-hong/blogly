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
        db.ForeignKey('users.id', ondelete='CASCADE')
    )

    author = db.relationship('BlogUser')
    # post_tag = db.relationship('PostTag')
    tags = db.relationship('Tag',
                            secondary='posts_tags')
    

class Tag(db.Model):
    """Tag"""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    name = db.Column(db.String(20),
                    nullable=False,
                    unique=True)
    
    post_tag = db.relationship('PostTag')

class PostTag(db.Model):
    """PostTag"""
    __tablename__ = "posts_tags"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    post_id = db.Column(db.Integer,
                       db.ForeignKey("posts.id"),
                       primary_key=True)
    tag_id = db.Column(db.Integer,
                          db.ForeignKey("tags.id"),
                          primary_key=True)
    