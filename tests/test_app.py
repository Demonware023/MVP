# Unit tests for Github Profiler
import unittest
import sqlite3
import json
from flask import Flask
from app import app, init_sqlite_db, verify_user, check_if_user_is_verified, get_user_from_db

class TestApp(unittest.TestCase):

    # setUpClass(): This class method is now responsible for setting up the Flask test client (cls.app) and initializing the database (cls.init_db()). It runs once before any test methods in the class.
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True
        cls.init_db()

    @classmethod
    def init_db(cls):
        with app.app_context():
            init_sqlite_db()

    # tearDownClass(): This optional class method can be used to clean up after all tests in the class have run. Here, it drops the users table from the SQLite database.
    @classmethod
    def tearDownClass(cls):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("DROP TABLE IF EXISTS users")
            con.commit()

    # Test Home Page
    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Github Profiler', response.data)

    # Test Register Page
    def test_register_page(self):
        response = self.app.get('/register_page/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'GitHub Profiler Registration', response.data)

    # Test Login Page
    def test_login_page(self):
        response = self.app.get('/login_page/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login to GitHub Profiler', response.data)

    # Test Register Function
    def test_register(self):
        # Adjust the URL and data according to your application's registration form
        response = self.app.post('/register/', data=dict(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        ), follow_redirects=True)
    
        # Assuming the registration process redirects to a login page or dashboard
        self.assertEqual(response.status_code, 200)  # Check if the registration was successful
        self.assertIn(b'Congratulations!! You have successfully registered', response.data)
        # Adjust the message above based on the actual success message displayed after registration

    # Test Login Success
    def test_login_success(self):
        self.app.post('/register/', data=dict(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        ))
        response = self.app.post('/login/', data=dict(
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

    # Test Login Failure
    def test_login_failure(self):
        response = self.app.post('/login/', data=dict(
            username='wronguser',
            password='wrongpassword'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Incorrect username or password.', response.data)

    # Test Logout Success
    def test_logout(self):
        self.app.post('/register/', data=dict(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        ))
        self.app.post('/login/', data=dict(
            username='testuser',
            password='testpassword'
        ))
        response = self.app.post('/logout/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Github Profiler', response.data)

    # Test Profile Page
    def test_profile(self):
        self.app.post('/register/', data=dict(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        ))
        self.app.post('/login/', data=dict(
            username='testuser',
            password='testpassword'
        ))
        response = self.app.get('/profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testuser\'s Profile', response.data)

    # Test Save Profile Button
    def test_save_profile(self):
        self.app.post('/register/', data=dict(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        ))
        self.app.post('/login/', data=dict(
            username='testuser',
            password='testpassword'
        ))
        response = self.app.post('/save_profile', data=dict(
            email='newemail@example.com',
            contact_link='http://newcontactlink.com'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Save Profile', response.data)

    # Test user profile
    def test_user_profile(self):
        self.app.post('/register/', data=dict(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        ))
        response = self.app.get('/user/testuser')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Profile', response.data)

    # Test Verify User
    def test_verify_user(self):
        self.app.post('/register/', data=dict(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        ))
        with app.app_context():
            verify_user('testuser')
            self.assertTrue(check_if_user_is_verified('testuser'))

    # Test admin page
    def test_admin(self):
        self.app.post('/register/', data=dict(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        ))
        response = self.app.get('/admin/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Page', response.data)

    # Test verify user route
    def test_verify_user_route(self):
        self.app.post('/register/', data=dict(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        ))
        self.app.post('/login/', data=dict(
            username='testuser',
            password='testpassword'
        ))
        response = self.app.post('/verify_user/testuser', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Page', response.data)
        with app.app_context():
            self.assertTrue(check_if_user_is_verified('testuser'))

    # Test Dashboard Login
    def test_dashboard(self):
        self.app.post('/register/', data=dict(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        ))
        self.app.post('/login/', data=dict(
            username='testuser',
            password='testpassword'
        ))
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

    # Test Github search function using Octocat
    def test_github_search(self):
        # Mocking GitHub API responses would be necessary for a complete test
        data = {
            'github_username': 'octocat'
        }
        response = self.app.post('/github_search', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'avatar_url', response.data)

    # Test Get User from Database function
    def test_get_user_from_db(self):
        self.app.post('/register/', data=dict(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        ))
        user = get_user_from_db('testuser')
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], 'testuser')
        self.assertEqual(user['email'], 'test@example.com')

if __name__ == '__main__':
    unittest.main()
