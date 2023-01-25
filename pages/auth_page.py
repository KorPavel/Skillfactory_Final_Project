from .base_page import BasePage
from .locators import AuthPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..settings import *
from time import sleep
import uuid


class AuthPage(BasePage):

    def should_be_logo_on_header(self):
        """ Проверка наличия логотипа в хедере страницы """
        assert self.is_element_present(*AuthPageLocators.LOGO_HEADER)

    def should_be_basic_content(self, side: str, elements: list):
        """ Проверка наличия основного контента на странице авторизации """
        party = self.wait.until(EC.presence_of_all_elements_located(AuthPageLocators.RIGHT_SIDE)) \
            if side == 'right' else \
            self.wait.until(EC.presence_of_all_elements_located(AuthPageLocators.LEFT_SIDE))
        self.browser.save_screenshot(f'auth_page_elems{uuid.uuid4()}.png')
        self.checking_the_selected_elements_in_the_main_content(party, elements)

    def click_to_forgot_password_link(self):
        forgot_link = self.wait.until(EC.presence_of_element_located(AuthPageLocators.FORGOT_PASS))
        forgot_link.click()

    def should_be_phone_active(self):
        """ Проверка активности таба выбора авторизации по телефону"""
        phone = self.wait.until(EC.presence_of_element_located(
            AuthPageLocators.TAB_PHONE))
        cl_phone = phone.get_attribute('class')
        mail = self.wait.until(EC.presence_of_element_located(
            AuthPageLocators.TAB_MAIL))
        cl_mail = mail.get_attribute('class')
        login = self.wait.until(EC.presence_of_element_located(
            AuthPageLocators.TAB_LOGIN))
        cl_login = login.get_attribute('class')
        ls = self.wait.until(EC.presence_of_element_located(
            AuthPageLocators.TAB_LS))
        cl_ls = ls.get_attribute('class')
        assert 'active' in cl_phone
        for elem in [cl_mail, cl_login, cl_ls]:
            assert 'active' not in elem

    def go_to_the_user_agreement_page(self):
        """ Проверка перехода на страницу пользовательского соглашения """
        agree = self.wait.until(EC.presence_of_element_located(
            AuthPageLocators.USER_AGREE))
        text = agree.text
        assert 'соглашения' in text
        original_window = self.browser.current_window_handle
        agree.click()
        self.switch_to_new_window(
            original_window, 'https://b2c.passport.rt.ru/sso-static/agreement/agreement.html')

    def should_be_various_accounts_link(self, account):
        """ Проверка регистрации через различные аккаунты """
        acc_link = self.wait.until(EC.presence_of_element_located(account[0]))
        acc_link.click()
        sleep(2)
        assert account[1] in self.browser.current_url


    def click_tab_phone(self):
        """ Метод кликает по табу 'Телефон' и проверяет изменение его цвета """
        phone_tab = self.wait.until(EC.presence_of_element_located(AuthPageLocators.TAB_PHONE))
        phone_tab.click()
        tab_btn = phone_tab.get_attribute('class')
        assert 'active' in tab_btn

    def click_tab_email(self):
        """ Метод кликает по табу 'Почта' и проверяет изменение его цвета """
        email_tab = self.wait.until(EC.presence_of_element_located(AuthPageLocators.TAB_MAIL))
        email_tab.click()
        tab_btn = email_tab.get_attribute('class')
        assert 'active' in tab_btn

    def click_tab_login(self):
        """ Метод кликает по табу 'Логин' и проверяет изменение его цвета """
        login_tab = self.wait.until(EC.presence_of_element_located(AuthPageLocators.TAB_LOGIN))
        login_tab.click()
        tab_btn = login_tab.get_attribute('class')
        assert 'active' in tab_btn

    def click_tab_ls(self):
        """ Метод кликает по табу 'Лицевой счёт' и проверяет изменение его цвета """
        ls_tab = self.wait.until(EC.presence_of_element_located(AuthPageLocators.TAB_LS))
        ls_tab.click()
        tab_btn = ls_tab.get_attribute('class')
        assert 'active' in tab_btn

    def send_params_to_relevant_areas(self, login, pwd):
        """ Метод заполняет поля логина и пароля соответствующими данными и отправляет их на проверку """
        login_area = self.wait.until(EC.presence_of_element_located(AuthPageLocators.NAME_AREA))
        login_area.send_keys(login)
        pass_area = self.wait.until(EC.presence_of_element_located(AuthPageLocators.PASS_AREA))
        pass_area.send_keys(pwd)
        submit_button = self.wait.until(EC.presence_of_element_located(AuthPageLocators.LOGIN_BUTTON))
        submit_button.click()

    def insert_to_login_area(self, param):
        login_area = self.wait.until(EC.presence_of_element_located(AuthPageLocators.NAME_AREA))
        login_area.send_keys(param)
        pass_area = self.wait.until(EC.presence_of_element_located(AuthPageLocators.PASS_AREA))
        pass_area.click()

    def for_reset_bad_cases(self):
        """ Вспомогательный тест для проведения негативных тестов, чтобы не вводить
        цифро-буквенный код с картинки после ряда случаев неудачной авторизации пользователя """
        self.send_params_to_relevant_areas(valid_user_data['email'],
                                           valid_user_data['password'])
        WebDriverWait(self.browser, 15).until(EC.presence_of_element_located(AuthPageLocators.USER_ACCOUNT))
        logout_button = self.wait.until(EC.presence_of_element_located(AuthPageLocators.EXIT_ACCOUNT))
        logout_button.click()
        assert self.wait.until(EC.text_to_be_present_in_element(
            AuthPageLocators.PAGE_TITLE, 'Авторизация'))

    def check_auth_param_plus_pass(self, tab, param, password, exp=True):
        """ Проверка вариантов авторизации. При позитивном сценарии метод проверяет
        соответствие имени и фамилии пользователя на странице в личном кабинете.
        При негативном сценарии - появление надписи 'Неверный логин или пароль' и
        изменение цвета надписи 'Забыл пароль' """
        if tab == 'phone':
            self.click_tab_phone()
        elif tab == 'email':
            self.click_tab_email()
        elif tab == 'login':
            self.click_tab_login()
        else:
            self.click_tab_ls()
        self.send_params_to_relevant_areas(param, password)
        if exp:
            WebDriverWait(self.browser, 20).until(EC.presence_of_element_located(AuthPageLocators.USER_ACCOUNT))
            assert WebDriverWait(self.browser, 15).until(EC.text_to_be_present_in_element(
                AuthPageLocators.USER_FIRSTNAME, valid_user_data['first_name']))
            assert WebDriverWait(self.browser, 15).until(EC.text_to_be_present_in_element(
                AuthPageLocators.USER_LASTNAME, valid_user_data['last_name']))
            logout_button = self.wait.until(EC.presence_of_element_located(AuthPageLocators.EXIT_ACCOUNT))
            logout_button.click()
        else:
            self.check_change_color_forgot_password()
            assert self.wait.until(EC.text_to_be_present_in_element(
                AuthPageLocators.PAGE_TITLE, 'Авторизация'))
            assert self.wait.until(EC.text_to_be_present_in_element(
                AuthPageLocators.MESSAGE_ERR, 'Неверный логин или пароль'))

    def check_change_color_forgot_password(self):
        """ Проверка надписи 'Забыл пароль' на изменение цвета """
        forgot_pass = self.wait.until(EC.presence_of_element_located(AuthPageLocators.FORGOT_PASS))
        forgot_color = forgot_pass.get_attribute('class')
        assert 'animated' in forgot_color, 'Цвет надписи остался серым'

    def check_autochange_tabs(self, tab, param):
        """ Проверка автоматической смены таба """
        self.insert_to_login_area(param)
        print(f'\n{tab}: {param}')
        tab_type = self.wait.until(EC.presence_of_element_located(AuthPageLocators.TAB_TYPE))
        assert tab.upper() == tab_type.get_attribute('value'), 'Таб не соответствует типу введённого параметра'
        print(tab_type.get_attribute('value'))

    def check_phone_correct(self, tab, text, exp=True):
        ''' Проверка корректности номера телефона '''
        if isinstance(text, int):
            param = get_nums(text)
        else:
            param = get_nums(3) + text(7)
        if tab == 'phone':
            self.click_tab_phone()
        else:
            self.click_tab_ls()
        print(f'\n{param}')
        self.insert_to_login_area(param)
        if exp:
            assert self.is_not_element_present(*AuthPageLocators.MES_PHONE_ERR)
        else:
            if isinstance(text, int):
                text_err = self.wait.until(EC.presence_of_element_located(
                    AuthPageLocators.MES_PHONE_ERR)).text
                assert text_err in ['Неверный формат телефона',
                                    'Проверьте, пожалуйста, номер лицевого счета']
            else:
                assert self.wait.until(EC.text_to_be_present_in_element(
                    AuthPageLocators.LOG_AREA_NAME, 'Логин'))

    def check_email_correct(self, user, server, exp=True):
        """ Проверка корректности имени адреса электронной почты """
        param = f'{letters_en(user)}@{letters_en(server)}.ru'
        self.click_tab_email()
        self.insert_to_login_area(param)
        if exp:
            assert self.wait.until(EC.text_to_be_present_in_element(
                AuthPageLocators.LOG_AREA_NAME, 'Электронная почта'))
        else:
            assert self.wait.until(EC.text_to_be_present_in_element(
                AuthPageLocators.LOG_AREA_NAME, 'Логин'),
                'Поле приняло длину адреса электронной почты, большую, '
                'чем предусмотрено стандартом')

    def check_login_correct(self, param, exp=True):
        """ Проверка значений и длины логина"""
        self.send_params_to_relevant_areas(param, valid_user_data['password'])
        if exp:
            assert self.wait.until(EC.text_to_be_present_in_element(
                AuthPageLocators.MESSAGE_ERR, 'Неверный логин или пароль'))
        else:
            self.is_not_element_present(*AuthPageLocators.MESSAGE_ERR)
