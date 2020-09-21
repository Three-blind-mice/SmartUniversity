from iotdriver import Driver
from selenium import webdriver
from exception import LmsError
from selenium.webdriver.chrome.webdriver import WebDriver
from settings import *
import os


class LmsDriver(Driver):
	"""Драйвер для работы с LMS MAI через браузер и установленный соответсвующий веб-драйвер."""
	_link: object
	_browser: WebDriver
	_username = 'st649687'
	_password = 'andrey123'
	_module_path = str(os.path.realpath(__file__)).split('\\')
	_driver_path = '/'.join(_module_path[:-1]) + '/' + 'driver.exe'
	_session_is_running = False
	_authorized = False

	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, '_inst'):
			cls._inst = super(LmsDriver, cls).__new__(cls)
		return cls._inst

	def set_session(self, params):
		if not LmsDriver._session_is_running:
			try:
				self._browser = webdriver.Chrome(LmsDriver._driver_path)
			except:
				raise LmsError(DRIVER_NOT_FOUND_ERROR)
			self._link = params['link']

	def turn_on(self):
		if LmsDriver._session_is_running:
			raise LmsError(ALREADY_RUNNING_ERROR)
		if LmsDriver._authorized:
			try:
				self._browser.get(LmsDriver._link)
			except:
				raise LmsError(WRONG_LINK_ERROR)
		else:
			self._authorize(LmsDriver._username, LmsDriver._password)
			try:
				self._browser.get(self._link)
			except Exception as err:
				print(err)
				raise LmsError(WRONG_LINK_ERROR)
			LmsDriver._authorized = True
		LmsDriver._session_is_running = True

	def turn_off(self):
		if not LmsDriver._session_is_running:
			raise LmsError(ALREADY_CLOSED_ERROR)
		self._browser.close()
		LmsDriver._session_is_running = False

	def _authorize(self, username, password):
		self._browser.get('https://lms.mai.ru/login/index.php')
		self._set_username(username)
		self._set_password(password)
		self._press_log_in_button()

	def _set_username(self, username):
		self._set_textbo_text("username", username)

	def _set_password(self, password):
		self._set_textbo_text("password", password)

	def _set_textbo_text(self, textboxName, text):
		textbox = self._browser.find_element_by_id(textboxName)
		if textbox is None:
			raise LmsError(ELEMENT_NOT_FOUND)
		textbox.send_keys(text)

	def _press_log_in_button(self):
		login_button = self._browser.find_element_by_id("loginbtn")
		if login_button is None:
			raise LmsError(ELEMENT_NOT_FOUND)
		login_button.click()




