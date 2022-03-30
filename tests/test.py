from unittest import TestCase

from app import app
from models import User, db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTests(TestCase):
    def setUp(self):
        User.query.delete()
    
    def tearDown(self):
        db.session.rollback()
    
    def test_db_submit(self):
        user = User(first_name='Testy', last_name="Testerson")
        db.session.add(user)
        db.session.commit()

        test_user = User.query.get(1)
        self.assertEqual(user, test_user)

class FlaskTests(TestCase):
    def setUp(self):
        User.query.delete()

        user = User(first_name='Testy', last_name="Testerson")
        db.session.add(user)
        db.session.commit()
    
    def tearDown(self):
        db.session.rollback()
    
    def test_users(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Testy', html)
    
    def test_show_details(self):
        with app.test_client() as client:
            res = client.get('/users/1')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Details for Testy Testerson</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name":"Testy2", "last_name":"Testerson2", "img_url":""}
            res = client.post('/users/new', data=d, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<li><a href="/users/2">Testy2 Testerson2</a></li>', html)
    
    def test_edit_user(self):
        with app.test_client() as client:
            d = {"first_name":"Testamus", "last_name":"Testersonton", "img_url":""}
            res = client.post('/users/1/edit', data=d, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<li><a href="/users/1">Testamus Testersonton</a></li>', html)
    
    def test_delete_user(self):
        with app.test_client() as client:
            res = client.post('/users/1/delete', follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertNotIn('<h1>Details for Testy Testerson</h1>', html)