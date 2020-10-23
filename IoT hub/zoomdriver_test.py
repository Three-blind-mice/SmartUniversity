import unittest
from zoomdriver import ZoomDriver
from exception import ZoomError
from settings import *
import psutil


class ZoomDriverTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = ZoomDriver()

    def test_set_session_01(self):
        self.driver.set_session()
        zoom_is_running = False
        for proc in psutil.process_iter():
            if proc.name().lower().find('zoom') != -1:
                zoom_is_running = True
        assert zoom_is_running is True

    def test_set_session_02(self):
        self.driver.set_session()
        zoom_is_running = False
        for proc in psutil.process_iter():
            if proc.name().lower().find('zoom') != -1:
                zoom_is_running = True
        try:
            self.driver.set_session()
        except ZoomError as err:
            assert err.txt is ALREADY_RUNNING_ERROR

    def test_turn_on_01(self):
        try:
            self.driver.set_session()
            self.driver.turn_on(params={'meeting_id': '8069715487', 'password': 'y1T2Mx'})
        except ZoomError as err:
            assert err.txt is BUTTON_ERROR.format('enter_with_sound_btn.jpg')

    def test_turn_on_02(self):
        self.driver.set_session()
        self.driver.turn_on(params={'meeting_id': '8069715487', 'password': 'y1T2Mx'})

    def test_turn_off_01(self):
        try:
            self.driver.turn_off()
        except ZoomError as err:
            assert err.txt is ALREADY_CLOSED_ERROR

    def test_turn_off_02(self):
        self.driver.set_session()
        self.driver.turn_on(params={'meeting_id': '8069715487', 'password': 'y1T2Mx'})
        self.driver.turn_off()

    def tearDown(self):
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