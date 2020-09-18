from settings import *
from iotdriver import Driver
import subprocess
import pyautogui
import time
from exception import *
import psutil

class ZoomDriver(Driver):
	"""Класс, предоставляющий методы для работы 
	с приложением Zoom."""

	def __init__(self):
		ZoomDriver.zoom_is_running = False
		ZoomDriver.conference_is_running = False
		self._meeting_id = None
		self._password = None

	def set_params(self, params):
		if self._meeting_id is None or self._password is None:
			self._meeting_id = params['meeting_id']
			self._password = params['password']

	"""Пользователь уже должен быть авторизован в аккаунте при запуске этого метода."""
	def turn_on(self):
		if ZoomDriver.conference_is_running:
			return ALREADY_RUNNING_ERROR
		try:
			zoom = subprocess.Popen(('start', path_to_zoom), shell=True)
			zoom.wait()
			zoom.poll()
			time.sleep(3)
			ZoomDriver.zoom_is_running = True

			join_btn = pyautogui.locateCenterOnScreen(imgs_path+'join_btn.png', confidence=0.9)
			if join_btn is None:
				raise ZoomError(JOIN_BUTTON_ERROR)
			pyautogui.moveTo(join_btn)
			pyautogui.click()
			time.sleep(3)
			meeting_id_btn = pyautogui.locateCenterOnScreen(imgs_path+'meeting_id_button.png', confidence=0.5)
			if meeting_id_btn is None:
				raise ZoomError(MEETING_ID_BUTTON_ERROR)
			pyautogui.moveTo(meeting_id_btn)
			pyautogui.click()
			pyautogui.write(self._meeting_id)
			time.sleep(1)
			pyautogui.press('enter')
			# # password_btn = pyautogui.locateAllOnScreen(imgs_path+'password_btn.png', confidence=0.5)
			# # if password_btn is None:
			# # 	raise ZoomError(PASSWORD_BUTTON_ERROR)
			# # print(password_btn)
			# # pyautogui.moveTo(password_btn)
			# # pyautogui.click()
			# pyautogui.write(self._password)
			# time.sleep(2)
			return SUCCESS_CODE
		except ZoomError as err:
			print('Zoom error: {0}'.format(err.txt))
			return err.txt

	def turn_off(self):
		if not ZoomDriver.zoom_is_running:
			return ALREADY_CLOSED_ERROR
		else:
			for proc in psutil.process_iter():
				if proc.name().lower().find('zoom') != -1:
					pid = proc.pid
					parent = psutil.Process(pid)
					children = parent.children(recursive=True)
					for child in children:
						child.kill()
					gone, still_alive = psutil.wait_procs(children, timeout=5)
					parent.kill()
					parent.wait(5)
			ZoomDriver.zoom_is_running = False
			return SUCCESS_CODE

class DiscordDriver(Driver):

	def __init__(self):
		pass
	def turn_on(self):
		pass
	def turn_off(self):
		pass
	def set_params(self, params):
		pass