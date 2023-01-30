import os.path
import os
from .locators import BasePageLocators
from .Api_RegMail import RegEmail
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

    def checking_the_selected_elements_in_the_main_content(self, side, elements: list):
        """ Проверка выбранных элементов в основном контенте страницы """
        sp = []
        [sp.append(el.text) for el in side]
        content = ' '.join(''.join(sp).split('\n'))
        # print('\n', content)
        for elem in elements:
            assert elem in content, f'Элемент «{elem}» отсутствует на странице'

    def make_screenshot(self, pict):
        scr_shots = 'screenshots'
        if not os.path.exists(scr_shots):
            os.mkdir(scr_shots)
        self.browser.save_screenshot(os.path.join(scr_shots, pict))

    @staticmethod
    def overwriting_settings(*args):
        """В случае успешной регистрации, перезаписываем созданные пару email/пароль в файл settings"""
        email_reg, new_pass = '', ''
        if len(args) == 1:
            email_reg = args[0]
        else:
            email_reg, new_pass = args
        with open("settings.py", 'r', encoding='utf8') as file:
            lines = []
            for line in file.readlines():
                if 'virtual_email = ' in line:
                    lines.append(f"virtual_email = '{str(email_reg)}'\n")
                elif 'password_reg = ' in line:
                    lines.append(f"password_reg = '{str(new_pass)}'\n")
                else:
                    lines.append(line)
        with open(r"settings.py", 'w', encoding='utf8') as file:
            file.writelines(lines)

    @staticmethod
    def get_virtual_email():
        """ Метод получает рандомный почтовый ящик с сайта '1secmail.com' """
        result_email, status_email = RegEmail().get_api_email()  # запрос на получение валидного почтового ящика
        email_reg = result_email[0]  # из запроса получаем валидный email
        assert status_email == 200, 'status_email error'
        assert len(result_email) > 0, 'results is empty'
        print('\n', f'Новый почтовый ящик: {email_reg}')
        return email_reg

    @staticmethod
    def read_last_mail_message(email_reg):
        """ Метод прочитывает последнее входящее письмо от Ростелекома,
        и извлекает из него временный код регистрации """
        # Разделяем email на имя и домен для использования в следующих запросах:
        sign_at = email_reg.find('@')
        mail_name = email_reg[:sign_at]
        mail_domain = email_reg[sign_at + 1:len(email_reg)]
        result_id, status_id = RegEmail().get_id_letter(mail_name, mail_domain)
        # Получаем id письма с кодом из почтового ящика:
        id_letter = result_id[0].get('id')
        # Сверяем полученные данные с нашими ожиданиями
        assert status_id == 200, "status_id error"
        assert id_letter > 0, "id_letter is empty"

        """Получаем код регистрации из письма от Ростелекома"""
        result_code, status_code = RegEmail().get_reg_code(mail_name, mail_domain, str(id_letter))
        # Получаем body из текста письма:
        text_body = result_code.get('body')
        # Извлекаем код из текста методом find:
        reg_code = text_body[text_body.find(': ') + len(': '):
                             text_body.find(': ') + len(': ') + 6]
        # Сверяем полученные данные с нашими ожиданиями
        assert status_code == 200, "status_code error"
        assert reg_code != '', "reg_code is empty"
        return reg_code

    def insert_reg_code_to_codes_area(self, code):
        """ Метод вставляет цифры кода в соответствующие поля и отправляемся на страницу аккаунта """
        reg_digit = list(code)
        digit_area = self.wait.until(EC.presence_of_all_elements_located(
            BasePageLocators.SDI_CODES_AREA))
        for fild, digit in zip(digit_area, reg_digit):
            fild.send_keys(digit)

