from unittest import TestCase

from app import app
from models import db, connect_db, BlogUser

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class BlogglyAppTestCase(TestCase):
    """Test flask app of Bloggly"""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def test_homepage(self):
        """Make sure homepage loads correctly"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h2>Users</h2>', html)

    def test_add_user(self):
        """tests adding of user"""
        
        with self.client as client:
            test_user = BlogUser(first_name='Ben', last_name='Hong', image_url=None)
            db.session.add(test_user)
            db.session.commit()
            user = BlogUser.query.filter_by(first_name='Ben').first()
            response = client.get(f'/{user.id}')
            html = response.get_data(as_text=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Ben Hong</h1>', html)


        