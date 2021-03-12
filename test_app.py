from unittest import TestCase

from app import app
from models import db, connect_db, BlogUser, Post

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
            response = client.get(f'/user/{user.id}')
            html = response.get_data(as_text=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Ben Hong</h1>', html)


    def test_add_post(self):
        """ Tests adding a post. """

        with self.client as client:
            user = BlogUser.query.filter_by(first_name='Ben').first()
            test_post = Post(title='Test Title', content='Test content', user_id = user.id)
            db.session.add(test_post)
            db.session.commit()
            post = Post.query.filter_by(title='Test Title').first()
            response = client.get(f'/posts/{post.id}')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(f'<h1>{post.title}</h1>', html)


    def test_delete_post(self):
        """ Tests if deleting a single post removes it."""

        with self.client as client:
            post = Post.query.filter_by(title='Test Title').first()
            post_id = post.id
            self.assertIsNotNone(post)
            response = client.post(f'/posts/{post_id}/delete')
            html = response.get_data(as_text=True)

            post = Post.query.filter_by(title='Test Title').get(post_id)
            self.assertEqual(response.status_code, 302)
            self.assertIsNone(post)



    

        