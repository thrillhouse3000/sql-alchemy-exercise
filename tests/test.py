from unittest import TestCase
from app import app
from models import Post, User, Tag, PostTag, db

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
    
    def test_fullname(self):
        user = User(first_name='Testy', last_name="Testerson")
        self.assertEqual(user.fullname, 'Testy Testerson')

class PostModelTests(TestCase):
    def setUp(self):
        Post.query.delete()
    
    def tearDown(self):
        db.session.rollback()
    
    def test_db_submit(self):
        post = Post(title='Test', content="Testing")
        db.session.add(post)
        db.session.commit()

        test_post = Post.query.get(1)
        self.assertEqual(post, test_post)

class TagModelTests(TestCase):
    def setUp(self):
        Post.query.delete()
    
    def tearDown(self):
        db.session.rollback()
    
    def test_db_submit(self):
        tag = Tag(name='Test')
        db.session.add(tag)
        db.session.commit()

        test_tag = Tag.query.get(1)
        self.assertEqual(tag, test_tag)

class PostTagModelTests(TestCase):
    def setUp(self):
        Post.query.delete()
    
    def tearDown(self):
        db.session.rollback()
    
    def test_append(self):
        post = Post(title='TestPost', content="Testing")
        tag = Tag(name='TestTag')
        post.categories.append(PostTag(post_id=1, tag_id=1))
        db.session.add_all([tag, post])
        db.session.commit()
        self.assertEqual(post.tag[0].name, 'TestTag')

class UserRouteTests(TestCase):
    def setUp(self):

        user = User(first_name='Testy', last_name="Testerson")
        db.session.add(user)
        db.session.commit()
    
    def tearDown(self):
        
        db.session.rollback()
        db.drop_all()
        db.create_all()
    
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
            self.assertIn('Testerson2', html)
    
    def test_edit_user(self):
        with app.test_client() as client:
            d = {"first_name":"Testamus", "last_name":"Testersonton", "img_url":""}
            res = client.post('/users/1/edit', data=d, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Testersonton', html)
    
    def test_delete_user(self):
        with app.test_client() as client:
            res = client.post('/users/1/delete', follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertNotIn('<h1>Details for Testy Testerson</h1>', html)

class PostRouteTests(TestCase):
    def setUp(self):
        user = User(first_name='Testy', last_name="Testerson")
        post = Post(title='Test', content="Testing", user_id=1)
        db.session.add_all([user, post])
        db.session.commit()
    
    def tearDown(self):
        
        db.session.rollback()
        db.drop_all()
        db.create_all()
    
    def test_show_post(self):
        with app.test_client() as client:
            res = client.get('/posts/1')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Test', html)

    def test_add_post(self):
        with app.test_client() as client:
            d = {"title":"Test2", "content":"Testing2"}
            res = client.post('/users/1/posts/new', data=d, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Test2', html)
    
    def test_edit_post(self):
        with app.test_client() as client:
            d = {"title":"Test2", "content":"Testing2"}
            res = client.post('/posts/1/edit', data=d, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Test2', html)

    def test_delete_post(self):
        with app.test_client() as client:
            res = client.post('/posts/1/delete', follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertNotIn('Testing', html)

class TagRouteTests(TestCase):
    def setUp(self):
        tag = Tag(name="TestTag")
        db.session.add(tag)
        db.session.commit()
    
    def tearDown(self):
        
        db.session.rollback()
        db.drop_all()
        db.create_all()
    
    def test_show_tag(self):
        with app.test_client() as client:
            res = client.get('/tags/1')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('TestTag', html)
    
    def test_add_tag(self):
        with app.test_client() as client:
            d = {"name":"TestTag2"}
            res = client.post('/tags/new', data=d, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('TestTag2', html)
    
    def test_edit_tag(self):
        with app.test_client() as client:
            d = {"name":"TestTag2Updated"}
            res = client.post('/tags/1/edit', data=d, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('TestTag2Updated', html)
    
    def test_delete_tag(self):
        with app.test_client() as client:
            res = client.post('/tags/1/delete', follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertNotIn('TestTag', html)


