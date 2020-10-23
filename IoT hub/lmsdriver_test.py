import unittest
from lmsdriver import LmsDriver
from exception import LmsError
from settings import *
from selenium.common.exceptions import NoSuchWindowException


class LmsDriverTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = LmsDriver()

    def test_set_session_01(self):
        self.driver.set_session()
        element = self.driver._browser.find_element_by_id('page-login-index')
        assert element is not None

    def test_set_session_02(self):
        self.driver.set_session()
        element = self.driver._browser.find_element_by_id('page-login-index')
        if element is not None:
            login_field = self.driver._browser.find_element_by_id('username')
            assert login_field is not None

    def test_set_session_03(self):
        self.driver.set_session()
        element = self.driver._browser.find_element_by_id('page-login-index')
        if element is not None:
            password_field = self.driver._browser.find_element_by_id('password')
            assert password_field is not None

    def test_set_session_04(self):
        self.driver.set_session()
        try:
            self.driver.set_session()
        except LmsError as err:
            assert err.txt is ALREADY_RUNNING_ERROR

    def test_turn_on_01(self):
        self.driver.set_session()
        self.driver.turn_on(params={'link': 'https://lms.mai.ru/mod/bigbluebuttonbn/view.php?id=89830'})
        element = self.driver._browser.find_element_by_id('app')
        assert element is not None

    def test_turn_on_02(self):
        self.driver.set_session()
        try:
            self.driver.turn_on(params={'link': 'https://www.youtube.com'})
        except LmsError as err:
            assert err.txt is WRONG_LINK_ERROR

    def test_turn_of_01(self):
        self.driver.set_session()
        self.driver.turn_off()
        try:
            self.driver._browser.get('https://yandex.ru')
        except NoSuchWindowException:
            return True

    def test_turn_of_02(self):
        self.driver.set_session()
        self.driver.turn_on(params={'link': 'https://lms.mai.ru/mod/bigbluebuttonbn/view.php?id=89830'})
        self.driver.turn_off()
        try:
            self.driver._browser.get('https://yandex.ru')
        except NoSuchWindowException:
            return True

    def test_turn_of_03(self):
        self.driver.set_session()
        self.driver.turn_off()
        try:
            self.driver.turn_off()
        except LmsError as err:
            assert err.txt is ALREADY_CLOSED_ERROR

    def tearDown(self):
        self.driver._browser.quit()