from iotdriver import Driver
from selenium import webdriver
from exception import LmsError
from selenium.webdriver.chrome.webdriver import WebDriver
from settings import *
import os
import time


class LmsDriver(Driver):
	_link: object
	_browser: WebDriver
	_username = lms_user_login
	_password = lms_user_password
	_module_path = str(os.path.realpath(__file__)).split('\\')
	_driver_path = '/'.join(_module_path[:-1]) + '/' + 'driver.exe'
	_session_is_running = False
	_authorized = False
	_tabs_opened = 0

	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, '_inst'):
			cls._inst = super(LmsDriver, cls).__new__(cls)
		return cls._inst

	def set_session(self, params):
		if not LmsDriver._session_is_running:
			print(LmsDriver._driver_path)
			try:
				self._browser = webdriver.Chrome(LmsDriver._driver_path)
			except Exception:
				raise LmsError(DRIVER_NOT_FOUND_ERROR)
			self._browser.maximize_window()
			self._link = params['link']

	def turn_on(self):
		if LmsDriver._session_is_running:
			raise LmsError(ALREADY_RUNNING_ERROR)
		if LmsDriver._authorized:
			try:
				self._browser.get(LmsDriver._link)
				self._tabs_opened += 1
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
			self._press_join_conference_button()
			time.sleep(5)
			self._press_audio_only_button()
		LmsDriver._session_is_running = True

	def turn_off(self):
		if not LmsDriver._session_is_running:
			raise LmsError(ALREADY_CLOSED_ERROR)
		self.close_all_tabs()
		LmsDriver._session_is_running = False

	def _authorize(self, username, password):
		self._browser.get(start_page_lms)
		self._set_username(username)
		self._set_password(password)
		self._press_log_in_button()

	def _set_username(self, username):
		self._set_textbox_text("username", username)

	def _set_password(self, password):
		self._set_textbox_text("password", password)

	def _set_textbox_text(self, textboxName, text):
		textbox = self._browser.find_element_by_id(textboxName)
		if textbox is None:
			raise LmsError(ELEMENT_NOT_FOUND)
		textbox.send_keys(text)

	def _press_log_in_button(self):
		login_button = self._browser.find_element_by_id("loginbtn")
		if login_button is None:
			raise LmsError(ELEMENT_NOT_FOUND)
		login_button.click()

	def _press_join_conference_button(self):
		join_button = self._browser.find_element_by_id("join_button_input")
		if join_button is None:
			raise LmsError(ELEMENT_NOT_FOUND)
		join_button.click()
		self._tabs_opened += 1

	def _press_audio_only_button(self):
		self._switch_webdriver_tab(1)
		audio_button = self._browser.find_element_by_xpath('//button[@aria-label="Listen only"]')
		if audio_button is None:
			raise LmsError(ELEMENT_NOT_FOUND)
		audio_button.click()

	def _switch_webdriver_tab(self, id):
		window_after = self._browser.window_handles[id]
		self._browser.switch_to.window(window_after)

	def close_all_tabs(self):
		while self._tabs_opened >= 0:
			self._switch_webdriver_tab(0)
			self._browser.close()
			self._tabs_opened -= 1
