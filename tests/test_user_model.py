from datetime import datetime
import time
import unittest
from app import create_app, db
from app.models import User, AnonymousUser, Role, Permission

class UserModelTestCase(unittest.TestCase):
	def test_password_setter(self):
		u = User(password='cat')
		self.assertTrue(u.password_hash is not None)

	def test_no_password_getter(self):
		u = User(password='cat')
		with self.assertRaises(AttributeError):
			u.password

	def test_password_verification(self):
		u = User(password='cat')
		self.assertTrue(u.verify_password('cat'))
		self.assertFalse(u.verify_password('dog'))

	def test_password_salts_are_randon(self):
		u1 = User(password='cat')
		u2 = User(password='cat')
		self.assertTrue(u1.password_hash != u2.password_hash)

	def test_valid_confirmation_token(self):
		u = User(password='dog')
		db.session.add(u)
		db.session.commit()
		token = u.generate_confirmation_token()
		self.assertTrue(u.confirm(token))

	def test_invalid_confirmation_token(self):
		u1 = User(password='cat')
		u2 = User(password='dog')
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()
		token = u1.generate_confirmation_token()
		self.assertFalse(u2.confirm(token))

	def test_expired_confirmation_token(self):
		u = User(password='cat')
		db.session.add(u)
		db.session.commit()
		token = u.generate_confirmation_token(1)
		time.sleep(2)
		self.assertFalse(u.confirm(token))

	def test_roles_and_permissions(self):
		u = User(email='john@example.com', password='cat')
		self.assertTrue(u.can(Permission.WRITE_ARTICLES))
		self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

	def test_anonymous_user(self):
		u = AnonymousUser()
		self.assertFalse(u.can(Permission.FOLLOW))

	def test_timestamps(self):
		u = User(password='cat')
		db.session.add(u)
		db.session.commit()
		self.assertTrue((datetime.utcnow() - u.last_seen).total_seconds() < 3)  
		self.assertTrue((datetime.utcnow() - u.member_since).total_seconds() < 3)

	def test_ping(self):
		u = User(password='cat')
		db.session.add(u)
		db.session.commit()
		last_seen_before = u.last_seen
		time.sleep(2)
		u.ping()
		self.assertTrue(u.last_seen > last_seen_before)

	def test_gravatar(self):
		u = User.query.filter_by(email='testone1757@yahoo.com').first()
		with self.app.test_request_context('/'):
			gravatar = u.gravatar()
		self.assertTrue('http://www.gravatar.com/avatar/' + 'f493ce7cb6e93255e2f27d92ffdb1c20' in avatar)