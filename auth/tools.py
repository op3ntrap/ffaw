import os
import hashlib
import binascii



class UserDAO:
	def __init__(self):
		self.check = False

	def exist(self, user_id):
		from models import User
		user = User.query.get(user_id)
		if user is None:
			return False
		return True


def hash_pass(password):
	"""Hash a password for storing."""
	salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
	password_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
	password_hash = binascii.hexlify(password_hash)
	return salt + password_hash  # return bytes


def verify_pass(provided_password, stored_password):
	"""Verify a stored password against one provided by user"""
	stored_password = stored_password.decode('ascii')
	salt = stored_password[:64]
	stored_password = stored_password[64:]
	password_hash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
	password_hash = binascii.hexlify(password_hash).decode('ascii')
	return password_hash == stored_password
