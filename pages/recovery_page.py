from .base_page import BasePage
from .locators import RecoveryPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from time import sleep
from ..settings import *


class RecoveryPage(BasePage):

    def should_be_logo_on_header(self):
        """ Проверка наличия логотипа в хедере страницы """
        assert self.is_element_present(*RecoveryPageLocators.LOGO_HEADER)

    def should_be_basic_content(self, side: str, elements: list):
        """ Проверка наличия основного контента на странице регистрации """
        party = self.wait.until(EC.presence_of_all_elements_located(RecoveryPageLocators.RIGHT_SIDE)) \
            if side == 'right' else \
            self.wait.until(EC.presence_of_all_elements_located(RecoveryPageLocators.LEFT_SIDE))
        self.make_screenshot(f'recovery_page_elems{datetime.now().strftime("%m%d%H%M%S")}.png')
        self.checking_the_selected_elements_in_the_main_content(party, elements)

    def should_be_tab_active(self, tab):
        """ Проверка активности таба выбора восстановления пароля по телефону"""
        elem = self.wait.until(EC.presence_of_element_located(
            RecoveryPageLocators.TAB_TYPE))
        cl_elem = elem.get_attribute('value').lower()
        assert cl_elem == tab

    def click_tab_phone(self):
        """ Метод кликает по табу 'Телефон' и проверяет его активность """
        phone_tab = self.wait.until(EC.presence_of_element_located(RecoveryPageLocators.TAB_PHONE))
        phone_tab.click()
        tab_btn = phone_tab.get_attribute('class')
        assert 'active' in tab_btn

    def click_tab_email(self):
        """ Метод кликает по табу 'Почта' и проверяет его активность """
        email_tab = self.wait.until(EC.presence_of_element_located(RecoveryPageLocators.TAB_MAIL))
        email_tab.click()
        tab_btn = email_tab.get_attribute('class')
        assert 'active' in tab_btn

    def click_tab_login(self):
        """ Метод кликает по табу 'Логин' и проверяет его активность """
        login_tab = self.wait.until(EC.presence_of_element_located(RecoveryPageLocators.TAB_LOGIN))
        login_tab.click()
        tab_btn = login_tab.get_attribute('class')
        assert 'active' in tab_btn

    def click_tab_ls(self):
        """ Метод кликает по табу 'Лицевой счёт' и проверяет его активность """
        ls_tab = self.wait.until(EC.presence_of_element_located(RecoveryPageLocators.TAB_LS))
        ls_tab.click()
        tab_btn = ls_tab.get_attribute('class')
        assert 'active' in tab_btn

    def checking_tab_switching(self):
        """ Проверка переключения табов """
        self.click_tab_ls()
        self.click_tab_login()
        self.click_tab_email()
        self.click_tab_phone()

    def checking_tab_switching_to_insert_valid_values(self, tab, param):
        """ Проверка переключения табов с определением типа введенной информации """
        login_area = self.wait.until(EC.presence_of_element_located(RecoveryPageLocators.NAME_AREA))
        login_area.send_keys(param)
        code_area = self.wait.until(EC.presence_of_element_located(RecoveryPageLocators.CODE_AREA))
        code_area.click()
        self.should_be_tab_active(tab)

    def successful_password_recovery_case(self, param):
        """ Полуавтоматический метод проходит этапы восстановления пароля по коду
        через email сообщение """
        login_area = self.wait.until(EC.presence_of_element_located(RecoveryPageLocators.NAME_AREA))
        login_area.send_keys(param)
        code_area = self.wait.until(EC.presence_of_element_located(RecoveryPageLocators.CODE_AREA))
        code_area.click()
        sleep(40)  # Ожидание для заполнения капчи
        further = self.wait.until(EC.presence_of_element_located(RecoveryPageLocators.CONTINUE))
        further.click()
        # ---- Следующее окно: выбираем СМС или email ------
        WebDriverWait(self.browser, 15).until(EC.text_to_be_present_in_element(
            RecoveryPageLocators.PAGE_TITLE, 'Восстановление пароля'))
        assert self.is_element_present(*RecoveryPageLocators.RADIO_EMAIL)
        radio_email = self.wait.until(EC.presence_of_element_located(RecoveryPageLocators.RADIO_EMAIL))
        radio_email.click()
        next2 = self.wait.until(EC.presence_of_element_located(RecoveryPageLocators.NEXT2))
        next2.click()
        # ---- Следующее окно: вводим 6-значный код ------
        WebDriverWait(self.browser, 15).until(EC.text_to_be_present_in_element(
            RecoveryPageLocators.PAGE_TITLE, 'Восстановление пароля'))
        sleep(120)  # Ожидание для ввода кода
        # ---- Следующее окно: вводим новый пароль и подтверждения пароля ------
        WebDriverWait(self.browser, 15).until(EC.text_to_be_present_in_element(
            RecoveryPageLocators.PAGE_TEXT, 'Новый пароль должен содержать от 8 до 20 знаков, '
                                          'включать латинские, заглавные и строчные буквы, цифры '
                                          'или специальные символы'))
        new_pwd = f"{valid_user_data['password']}+{get_nums(2)}"
        print('\n', new_pwd)
        new_password = self.wait.until(EC.presence_of_element_located(RecoveryPageLocators.PASS_NEW))
        new_password.send_keys(new_pwd)
        new_password_conf = self.wait.until(EC.presence_of_element_located(RecoveryPageLocators.PASS_CONF))
        new_password_conf.send_keys(new_pwd)
        safe_button = self.wait.until(EC.presence_of_element_located(RecoveryPageLocators.SAFE_BUTTON))
        safe_button.click()
        sleep(10)
        assert WebDriverWait(self.browser, 15).until(EC.text_to_be_present_in_element(
            RecoveryPageLocators.PAGE_TITLE, 'Авторизация'))

    def checking_messages_with_an_empty_field(self):
        """ Проверка сообщений при незаполненных полях """
        method = [self.click_tab_phone, self.click_tab_email, self.click_tab_login, self.click_tab_ls]
        message = ['Введите номер телефона',
                   'Введите адрес, указанный при регистрации',
                   'Введите логин, указанный при регистрации',
                   'Введите номер вашего лицевого счета']
        for tab, msg in zip(method, message):
            tab()
            farther = self.wait.until(EC.presence_of_element_located(RecoveryPageLocators.CONTINUE))
            farther.click()
            assert self.wait.until(EC.text_to_be_present_in_element(RecoveryPageLocators.MESS_ERROR2, msg),
                                   'Сообщение не соответствует выбранному табу')

    def checking_message_with_an_incorrect_code(self, param: str):
        """ Проверка сообщения об ошибке при неверном коде капчи """
        login_area = self.wait.until(EC.presence_of_element_located(RecoveryPageLocators.NAME_AREA))
        login_area.send_keys(param)
        code_area = self.wait.until(EC.presence_of_element_located(RecoveryPageLocators.CODE_AREA))
        code_area.send_keys(get_nums(3) + letters_en(4))
        further = self.wait.until(EC.presence_of_element_located(RecoveryPageLocators.CONTINUE))
        further.click()
        assert self.wait.until(EC.text_to_be_present_in_element(
            RecoveryPageLocators.MESS_ERROR1, 'Неверный логин или текст с картинки'))


