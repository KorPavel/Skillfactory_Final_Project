from .base_page import BasePage
from .locators import RegisterPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import *
from datetime import datetime


class RegisterPage(BasePage):

    def __init__(self, browser, url, timeout=10):
        super().__init__(browser, url, timeout)
        self.user_data = valid_guest_data
        self.first_name = self.wait.until(EC.presence_of_element_located(RegisterPageLocators.FIRST_NAME))
        self.last_name = self.wait.until(EC.presence_of_element_located(RegisterPageLocators.LAST_NAME))
        self.address = self.wait.until(EC.presence_of_element_located(RegisterPageLocators.ADDRESS))
        self.pwd = self.wait.until(EC.presence_of_element_located(RegisterPageLocators.PASSWORD))
        self.pwd_conf = self.wait.until(EC.presence_of_element_located(RegisterPageLocators.PASSWORD_CONFIRM))

    def filling_registration_fields(self):
        self.first_name.send_keys(self.user_data['first_name'])
        self.last_name.send_keys(self.user_data['last_name'])
        self.address.send_keys(self.user_data['email'])
        self.pwd.send_keys(self.user_data['password'])
        self.pwd_conf.send_keys(self.user_data['password_confirm'])

    def change_user_data(self, user_data_key, user_data_val):
        self.user_data[user_data_key] = user_data_val
        self.filling_registration_fields()
        reg_button = self.wait.until(EC.presence_of_element_located(RegisterPageLocators.REGISTER_BUTTON))
        reg_button.click()
        return self.user_data

    def reset_new_email(self, new_email):
        self.user_data['email'] = new_email
        self.address.click()
        self.address.clear()
        self.address.send_keys(self.user_data['email'])
        reg_button = self.wait.until(EC.presence_of_element_located(RegisterPageLocators.REGISTER_BUTTON))
        # reg_button.click()
        print(new_email)

    def change_user_passwords(self, user_pwd, user_pwd_conf):
        self.user_data['password'] = user_pwd
        self.user_data['password_confirm'] = user_pwd_conf
        self.filling_registration_fields()
        reg_button = self.wait.until(EC.presence_of_element_located(RegisterPageLocators.REGISTER_BUTTON))
        reg_button.click()

    def should_be_logo_on_header(self):
        """ Проверка наличия логотипа в хедере страницы """
        assert self.is_element_present(*RegisterPageLocators.LOGO_HEADER)

    def should_be_basic_content(self, side: str, elements: list):
        """ Проверка наличия основного контента на странице регистрации """
        party = self.wait.until(EC.presence_of_all_elements_located(RegisterPageLocators.RIGHT_SIDE)) \
            if side == 'right' else \
            self.wait.until(EC.presence_of_all_elements_located(RegisterPageLocators.LEFT_SIDE))
        self.make_screenshot(f'register_page_elems{datetime.now().strftime("%m%d%H%M%S")}.png')
        self.checking_the_selected_elements_in_the_main_content(party, elements)

    def should_be_registr_form(self):
        """ Проверка формы регистрации """
        sp = []
        right = self.wait.until(EC.presence_of_all_elements_located(RegisterPageLocators.RIGHT_SIDE))
        [sp.append(el.text) for el in right]
        assert 'Регистрация' in sp[0], 'Форма "Регистрация" отсутствует'

    def should_be_logo(self):
        """ Проверка слогана "Ростелеком" """
        sp = []
        left = self.wait.until(EC.presence_of_all_elements_located(RegisterPageLocators.LEFT_SIDE))
        [sp.append(el.text) for el in left]
        assert 'Ростелеком' in sp[0], 'Слоган "Ростелекома" отсутствует'

    def should_be_default_region(self, city):
        """ Проверка региона регистрации по умолчанию """
        default_region = self.wait.until(EC.presence_of_element_located(RegisterPageLocators.REGION))
        assert city in default_region.get_attribute('textContent'), "Регион регистрации не соответствует ТЗ"

    def should_be_select_some_region(self, city):
        """ Проверка выбора иного региона регистрации """
        how, what = RegisterPageLocators.SELECT_REG2
        what = what.replace('$', city)
        new_locator = (how, what)
        self.wait.until(EC.presence_of_element_located(RegisterPageLocators.SELECT_REG1)).click()
        self.wait.until(EC.presence_of_element_located(new_locator)).click()
        region = self.wait.until(EC.presence_of_element_located(RegisterPageLocators.REGION))
        assert city in region.get_attribute('textContent'), "Регион"

    def choosing_registration_option(self, address):
        """ Проверка валидных значений пользователя """
        user_data_key = 'email'
        user_data_val = self.user_data[address]
        user_data_dict = self.change_user_data(user_data_key, user_data_val)
        assert self.is_element_present(*RegisterPageLocators.REGISTER_CONF_FORM)
        return user_data_dict

    def send_all_fields_is_empty(self):
        for el in [self.first_name, self.last_name, self.address, self.pwd, self.pwd_conf]:
            el.send_keys('')
        self.wait.until(EC.presence_of_element_located(
            RegisterPageLocators.REGISTER_BUTTON)).click()
        assert self.is_element_present(*RegisterPageLocators.TEXT_ERROR)
        assert self.is_element_present(*RegisterPageLocators.REGISTER_FORM)

    def params_name_length(self, type_data, param, exp=True):
        """ Проверка длины имени пользователя """
        user_data_key = type_data
        if isinstance(param, int):
            user_data_val = letters_ru(param)
        else:
            user_data_val = param(10)
        self.change_user_data(user_data_key, user_data_val)
        self.user_data[user_data_key] = valid_user_data[user_data_key]
        # print('\n', user_data_key, user_data_val)
        if exp:
            assert self.is_element_present(*RegisterPageLocators.REGISTER_CONF_FORM)
        else:
            assert self.is_element_present(*RegisterPageLocators.TEXT_ERROR)
            assert self.is_element_present(*RegisterPageLocators.REGISTER_FORM)
        return user_data_val

    def params_address_length(self, type_data, *param, exp=True):
        """ Проверка длины телефонного номера пользователя """
        if type_data == 'phone':
            numbers = param[0]
            user_data_val = numbers[0] + get_nums(numbers[1])
            user_data_key = 'email'
        else:
            user, email = param
            user_data_key = 'email'
            user_data_val = letters_en(user) + '@' + letters_en(email) + '.ru'
        self.change_user_data(user_data_key, user_data_val)
        self.user_data[type_data] = valid_user_data[type_data]
        if exp:
            assert self.is_element_present(*RegisterPageLocators.REGISTER_CONF_FORM)
        else:
            assert self.is_element_present(*RegisterPageLocators.TEXT_ERROR)
            assert self.is_element_present(*RegisterPageLocators.REGISTER_FORM)
        return user_data_val

    def params_password_length(self, type_pass: str, param: int | str, exp=True):
        """ Проверка длины пароля """
        user_data_key = type_pass
        if isinstance(param, int):
            user_data_val = letters_en(param - 2).capitalize() + get_specsymbols(2) if param else ''
        else:
            user_data_val = param
        self.change_user_data(user_data_key, user_data_val)
        error_text = self.wait.until(EC.presence_of_element_located(RegisterPageLocators.COUNT_SYMB_ERROR))
        # print('\n', user_data_val, error_text.text)
        self.user_data[type_pass] = valid_user_data[type_pass]
        if exp:
            assert error_text.text == 'Пароли не совпадают'
        else:
            assert error_text.text in text_errors
        return user_data_val

    def valid_passwords_equal(self, exp=True):
        """ Проверка тождества ПАРОЛЯ и ПАРОЛЯ ПОДТВЕРЖДЕНИЯ при их валидных значениях """
        user_pwd_val = letters_en(10).capitalize() + get_specsymbols(2)
        user_pwd_conf_val = letters_en(10).capitalize() + get_specsymbols(2)
        # print('\n', user_pwd_val, user_pwd_conf_val, sep='\n')
        if exp:
            self.change_user_passwords(user_pwd_val, user_pwd_val)
            assert self.is_element_present(*RegisterPageLocators.REGISTER_CONF_FORM)
        else:
            self.change_user_passwords(user_pwd_val, user_pwd_conf_val)
            assert self.is_element_present(*RegisterPageLocators.COUNT_SYMB_ERROR)
            assert self.is_element_present(*RegisterPageLocators.REGISTER_FORM)
        return user_pwd_val, user_pwd_conf_val

    def params_address_equal(self, type_address, param, exp=True):
        """ Проверка валидности адреса """
        if type_address == 'email':
            user_data_key = type_address
            if isinstance(param, tuple):
                user_data_val = letters_en(param[0]) + get_nums(param[1]) + '@mail.ru'
            else:
                user_data_val = param
        else:
            user_data_key = 'email'
            user_data_val = param
        self.change_user_data(user_data_key, user_data_val)
        self.user_data['email'] = 'example@email.com'
        self.user_data['phone'] = '+77777777777'
        print('\n', user_data_key, user_data_val)
        if exp:
            assert self.is_element_present(*RegisterPageLocators.REGISTER_CONF_FORM)
        else:
            assert self.is_element_present(*RegisterPageLocators.TEXT_ERROR)
            assert self.is_element_present(*RegisterPageLocators.REGISTER_FORM)
        return user_data_val

    def params_password_equal(self, param: str):
        """ Проверка валидности пароля """
        self.change_user_passwords(param, param)
        assert self.is_element_present(*RegisterPageLocators.POPULAR_PASSWORD)
        assert self.is_element_present(*RegisterPageLocators.REGISTER_FORM)

    def checking_user_account(self):
        """ Метод проверяет вход в аккаунт пользователя """
        user_last_name = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located(
            RegisterPageLocators.USER_LASTNAME)).text
        user_first_name = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located(
            RegisterPageLocators.USER_FIRSTNAME)).text

        self.make_screenshot(f'account_page_{user_first_name}_{user_last_name}.png')
        assert '/account_b2c/page' in self.browser.current_url, 'Регистрация НЕ пройдена'
        print(user_first_name, user_last_name)

