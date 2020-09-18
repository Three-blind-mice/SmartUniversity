from iotdriver import Driver
from exception import *
import os
import json
from selenium import webdriver


class LmsDriver(Driver):
	"""Драйвер для работы с LMS MAI через браузер и установленный соответсвующий веб-драйвер."""
	def __init__(self):
		self.__params_initialized = False
		self.__running = False

	def turn_on(self):
		if self.__running == True:
			return ALREADY_RUNNING_ERROR
		try:
			if self.__params_initialized == False:
				raise LmsError(LOGGING_IN_WITHOUT_PARAMETERS)
			self.init_driver("driver")
			self.browser.get('https://lms.mai.ru/login/index.php')
			self.autorize(self.__username, self.__password)
			self.browser.get(self.__link)
			self.__running = True
			return SUCCESS_CODE
		except LmsError as err:
			print('LMS error: {0}'.format(err.txt))
			return err.txt

	def turn_off(self):
		if not self.__running:
			return ALREADY_CLOSED_ERROR
		self.browser.close()
		return SUCCESS_CODE

	def set_params(self, params):
		if self.__params_initialized == False:
			if params['username'] is None or params['password'] is None or params['link'] is None:
				raise LmsError(WRONG_PARAMETERS)
			self.__username = params['username']
			self.__password = params['password']
			self.__link = params['link']
			self.__params_initialized = True
		pass
		
	def init_driver(self, driverName):
		modulepath = os.path.realpath(__file__).split('/')
		driverpath = modulepath[:-1]
		driverpath = '/'.join(driverpath) + '/' + driverName
		self.browser = webdriver.Chrome(driverpath)
		if self.browser is None:
			raise LmsError(DRIVER_NOT_FOUND_ERROR)
		pass

	def autorize(self, username, password):
		self.set_username(username)
		self.set_password(password)
		self.press_log_in_button()
		pass
  
	def set_username(self, username):
		self.set_textbo_text("username", username)
		pass

	def set_password(self, password):
		self.set_textbo_text("password", password)
		pass

	def set_textbo_text(self, textboxName, text):
		textbox = self.browser.find_element_by_id(textboxName)
		if textbox is None:
			raise LmsError(ELEMENT_NOT_FOUND)
		textbox.send_keys(text)
		pass

	def press_log_in_button(self):
		login_button = self.browser.find_element_by_id("loginbtn")
		if login_button is None:
			raise LmsError(ELEMENT_NOT_FOUND)
		login_button.click()
		pass



