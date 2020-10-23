from iotdriver import Driver
from selenium import webdriver
from exception import LmsError
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
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

	def set_session(self):
		if LmsDriver._session_is_running:
			raise LmsError(ALREADY_RUNNING_ERROR)
		try:
			self._browser = webdriver.Chrome(LmsDriver._driver_path)
		except Exception:
			raise LmsError(DRIVER_NOT_FOUND_ERROR)
		self._browser.get(start_page_lms)
		self._tabs_opened += 1
		self._browser.maximize_window()
		LmsDriver._session_is_running = True

	def turn_on(self, params):
		link = params['link']
		if LmsDriver._authorized:
			try:
				self._browser.get(link)
				self._tabs_opened += 1
			except Exception:
				raise LmsError(WRONG_LINK_ERROR)
		else:
			self._authorize(LmsDriver._username, LmsDriver._password)
			LmsDriver._authorized = True
			try:
				self._browser.get(link)
				self._press_join_conference_button()
				time.sleep(5)
				self._press_audio_only_button()
			except Exception as err:
				print(err)
				raise LmsError(WRONG_LINK_ERROR)

	def turn_off(self):
		if not LmsDriver._session_is_running:
			raise LmsError(ALREADY_CLOSED_ERROR)
		self.close_all_tabs()
		LmsDriver._session_is_running = False

	def _authorize(self, username, password):
		self._set_username(username)
		self._set_password(password)
		self._press_log_in_button()

	def _set_username(self, username):
		self._set_textbox_text("username", username)

	def _set_password(self, password):
		self._set_textbox_text("password", password)

	def _set_textbox_text(self, textboxName, text):
		try:
			textbox = self._browser.find_element_by_id(textboxName)
			textbox.send_keys(text)
		except NoSuchElementException:
			raise LmsError(ELEMENT_NOT_FOUND_ERROR)

	def _press_log_in_button(self):
		try:
			login_button = self._browser.find_element_by_id("loginbtn")
			login_button.click()
		except NoSuchElementException:
			raise LmsError(ELEMENT_NOT_FOUND_ERROR)

	def _press_join_conference_button(self):
		try:
			join_button = self._browser.find_element_by_id("join_button_input")
			join_button.click()
			self._tabs_opened += 1
		except NoSuchElementException:
			raise LmsError(ELEMENT_NOT_FOUND_ERROR)

	def _press_audio_only_button(self):
		try:
			self._switch_webdriver_tab(1)
			audio_button = self._browser.find_element_by_xpath('//button[@aria-label="Активный участник"]')
			audio_button.click()
		except NoSuchElementException:
			raise LmsError(ELEMENT_NOT_FOUND_ERROR)

	def _switch_webdriver_tab(self, id):
		window_after = self._browser.window_handles[id]
		self._browser.switch_to.window(window_after)

	def close_all_tabs(self):
		while self._tabs_opened >= 0:
			self._switch_webdriver_tab(0)
			self._browser.close()
			self._tabs_opened -= 1
