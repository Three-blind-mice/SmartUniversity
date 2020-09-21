import pyautogui
import psutil
import time
from iotdriver import Driver
from exception import ZoomError
from subprocess import Popen
from settings import *


class ZoomDriver(Driver):
    _meeting_id: object
    _password: object
    _session_is_running = False

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(ZoomDriver, cls).__new__(cls)
        return cls._inst

    def set_session(self, params):
        if not ZoomDriver._session_is_running:
            try:
                self._zoom = Popen(('start', path_to_zoom), shell=True)
                self._zoom.wait()
                self._zoom.poll()
                time.sleep(3)
            except:
                raise ZoomError(WRONG_PATH_ERROR)
            self._meeting_id = params['meeting_id']
            self._password = params['password']

    def turn_on(self):
        if ZoomDriver._session_is_running:
            raise ZoomError(ALREADY_RUNNING_ERROR)
        ZoomDriver._session_is_running = True
        ZoomDriver._press_on_button('join_btn.png', confidence=0.9)
        time.sleep(3)
        ZoomDriver._press_on_button('meeting_id_button.png', confidence=0.5)
        ZoomDriver._write_on_fild(self._meeting_id)
        time.sleep(3)
        ZoomDriver._press_on_key('enter')
        #ZoomDriver._press_on_button('password_btn.png', confidence=0.5)
        #ZoomDriver._write_on_fild(self._password)
        time.sleep(2)

    @staticmethod
    def turn_off():
        if not ZoomDriver._session_is_running:
            raise ZoomError(ALREADY_CLOSED_ERROR)
        else:
            for proc in psutil.process_iter():
                if proc.name().lower().find('zoom') != -1:
                    pid = proc.pid
                    parent = psutil.Process(pid)
                    children = parent.children(recursive=True)
                    for child in children:
                        child.kill()
                    psutil.wait_procs(children, timeout=5)
                    parent.kill()
                    parent.wait(5)
            ZoomDriver._session_is_running = False

    @staticmethod
    def _press_on_button(img_button, confidence=0.):
        btn = pyautogui.locateCenterOnScreen(imgs_path + img_button, confidence=confidence)
        if btn is None:
            #ZoomDriver._session_is_running = True
            ZoomDriver.turn_off()
            raise ZoomError(BUTTON_ERROR.format(img_button))
        pyautogui.moveTo(btn)
        pyautogui.click()

    @staticmethod
    def _write_on_fild(text):
        pyautogui.write(text)

    @staticmethod
    def _press_on_key(button):
        pyautogui.press(button)
