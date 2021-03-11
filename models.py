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
                        default='https://ukdj.imgix.net/455a0284eb7a4194d11239e17b11ab2a_/generic-user-profile_354184.png?auto=compress%2Cformat&ixlib=php-3.3.0&s=1eb3025fdb7932cd02c78b3d63348e3c')

