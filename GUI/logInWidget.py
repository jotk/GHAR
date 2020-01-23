from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit
from email_validator import validate_email, EmailNotValidError
import webbrowser
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFormLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import sys

# class clickSubmit(QObject):
# 	submitted = pyqtSignal()

class LogInWidget(QWidget):
	""" QWidget that takes in email, password, and allow user to submit.
	Parameters: Parent Window, Database connection
	Shows email input, password input, and a submit button. When submit is clicked,
	the Widget calls a validator function in parent window of type LogInWindow.
	"""
	def __init__(self, DBconnect,*args, **kwargs):
		""" Initializes object's database connection, email field, password field, and submit connection """
		super().__init__(*args, **kwargs)
		self.DBconnect = DBconnect
		# tried to make custom signal, uneccesary
		#self.submittedSignal = clickSubmit()
		#self.submittedSignal.submitted.connect(self.parentWindow.submitClicked(string, string))

		self.mainLayout = QVBoxLayout(self)
		self.formLayout = QFormLayout()
		self.emailLayout = QHBoxLayout()
		self.passwordLayout = QHBoxLayout()

		self.email = QLineEdit()
		self.password = QLineEdit()
		self.password.setEchoMode(QLineEdit.Password)

		self.submit = QPushButton("Log In")
		self.newuser = QPushButton("New User")
		# SHOULD BE? self.submit.clicked.connect(partial(self.parentWindow.submitClicked, self.email.text(), self.password.text()))

		self.formLayout.addRow("Email", self.email)
		self.formLayout.addRow("Password", self.password)

		widg_width = self.frameGeometry().width()
		pic_width = int((widg_width*.25))

		self.logo_pic = QPixmap('images/house_logo.png')
		self.logo_pic = self.logo_pic.scaled(pic_width, pic_width, Qt.KeepAspectRatio)
		self.logo = QLabel()
		self.logo.setPixmap(self.logo_pic)

		self.mainLayout.addWidget(self.logo, alignment=Qt.AlignHCenter)
		self.mainLayout.addLayout(self.formLayout)

		self.buttonLayout = QHBoxLayout() # alligns the buttons horizontally
		self.buttonLayout.addWidget(self.submit)
		self.buttonLayout.addWidget(self.newuser)

		self.mainLayout.addLayout(self.buttonLayout)
		# self.mainLayout.addWidget(self.newuser, alignment=Qt.AlignHCenter)


	def checkEmailValid(self, text):
		""" Checks if given email is valid (not related to DB) through checking
		domain and checking syntax
		Parameters: email (String)
		Output: (True if valid False if invalid (Bool), email if valid and error if not valid (String)) (Tuple)
		"""
		print("Email passed in checkEmailValid: ", text)
		try:
			v = validate_email(text)  # validate and get info
			return (True, v["email"])  # replace with normalized form
		except EmailNotValidError as e:
			# email is not valid, exception message is human-readable
			print(str(e))
			return (False, str(e))

	def logInValid(self, in_email, in_pwd):
		""" Checks with database through the db connection if the email and password exist
		Parameters: email (String) password (String)
		Output: (True if exists False if does not exist (Bool), userId (Int)) (Tuple)

		"""
		email = in_email.text()
		pwd = in_pwd.text()
		print("logInValid email:", email)
		emailValidity = self.checkEmailValid(email)
		if emailValidity[0] == True:
			checkUserInfo = self.DBconnect.checkUser(email, pwd)
			print("Does it exist: ", checkUserInfo)
			if checkUserInfo[0]:
				return(checkUserInfo)
			else:
				self.password.clear()
				self.email.clear()
				self.email.setPlaceholderText("No account found")
				self.password.setPlaceholderText("Try again")
				return((False, None))

		else:
			self.password.clear()
			self.email.clear()
			self.email.setPlaceholderText("Invalid email")
			print(emailValidity[1])
			return((False, None))
