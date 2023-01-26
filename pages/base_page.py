import os.path
import os
from .locators import BasePageLocators
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, browser, url='https://b2c.passport.rt.ru', timeout=10):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)
        self.wait = WebDriverWait(browser, 5)

    def open(self):
        self.browser.get(self.url)

    def is_element_located(self, how, what) -> bool:
        ''' Метод ищет элемент с явным ожиданием '''
        try:
            self.wait.until(
                EC.presence_of_element_located((how, what)),
                f'CSS Selector "\x1B[1m{what}\x1B[0m" is not find')
        except NoSuchElementException:
            return False
        return True

    def is_element_present(self, how, what) -> bool:
        ''' Метод проверяет, что элемент присутствует на странице '''
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            print(f'Элемент с локатором {what} не найден')
            return False
        return True

    def is_elements_present(self, how, what) -> bool:
        ''' Метод ищет группу элементов на странице по локатору '''
        try:
            self.browser.find_elements(how, what)
        except NoSuchElementException:
            print(f'Элементы с локатором {what} не найдены')
            return False
        return True

    def is_not_element_present(self, how, what, timeout=4):
        ''' Метод проверяет, что элемент отсутствует на странице '''
        try:
            WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True
        return False

    def click_to_register_link(self):
        reg_link = self.wait.until(EC.presence_of_element_located(BasePageLocators.REGISTER_LINK))
        reg_link.click()

    def switch_to_new_window(self, first_window, new_url):
        """ Проверка URL новой страницы """
        self.wait.until(EC.number_of_windows_to_be(2))
        for window_handle in self.browser.window_handles:
            if window_handle != first_window:
                self.browser.switch_to.window(window_handle)
                break
        assert self.wait.until(EC.url_to_be(new_url), 'Incorrect URL')
        self.browser.close()
        self.browser.switch_to.window(first_window)

    def should_be_footer(self):
        """ Проверка наличия футера на странице авторизации """
        elem = self.wait.until(EC.presence_of_element_located(
            BasePageLocators.FOOTER_RT), 'Элемент не найден')
        assert 'Ростелеком' in elem.text

    def should_be_support_phone_link(self):
        """ Проверка соответствия ссылки и номера телефона службы поддержки """
        support = self.wait.until(EC.presence_of_element_located(BasePageLocators.SUPPORT_PHONE))
        phone = support.text.replace(' ', '')
        assert phone in support.get_attribute('href')

    # @staticmethod
    def checking_the_selected_elements_in_the_main_content(self, side, elements: list):
        """ Проверка выбранных элементов в основном контенте страницы """
        sp = []
        [sp.append(el.text) for el in side]
        content = ' '.join(''.join(sp).split('\n'))
        print('\n', content)
        for elem in elements:
            assert elem in content, f'Элемент «{elem}» отсутствует на странице'

    def make_screenshot(self, pict):
        scr_shots = 'screenshots'
        if not os.path.exists(scr_shots):
            os.mkdir(scr_shots)
        self.browser.save_screenshot(os.path.join(scr_shots, pict))

