# AbonadoDTO

import sirope
import flask_login
import werkzeug.security as safe


class AbonadoDto(flask_login.UserMixin):
	def __init__(self, usuario, password):
		self.__usuario = usuario
		self.__password = safe.generate_password_hash(password)
		self.__rol = "ABONADO"


	@property
	def usuario(self):
		return self.__usuario

	def get_id(self):
		return self.usuario

	@property
	def rol(self):
		return self.__rol

	def check_password(self, password):
		return safe.check_password_hash(self.__password, password)

	@staticmethod
	def current_user():
		user = flask_login.current_user
		if user.is_anonymous:
			flask_login.logout_user()
			user = None
		return user

	@staticmethod
	def find(s: sirope.Sirope, usuario: str) -> "AbonadoDto":
		return s.find_first(AbonadoDto, lambda u: u.usuario == usuario)
