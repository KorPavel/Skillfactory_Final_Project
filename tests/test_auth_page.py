import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pages.auth_page import AuthPage
from pages.locators import AccountPageLocators
from settings import valid_user_data, valid_guest_data, various_accounts, \
    get_nums, letters_en, letters_ru, letters_cn, get_specsymbols


def rs_write(result_status, title, *args):
    with open('Notebook.txt', 'a', encoding='utf8') as file:
        file.write(f'>> Описание теста: {title}\n')
        if args:
            file.write('>> Тестовые данные:\n' + "\n".join(map(str, args)) + '\n')
        file.write(f'>> Результат теста: {result_status}\n')


class TestAuth:

    @pytest.mark.proba
    @pytest.mark.xfail(reason='Баги! 1. Элементы левого и правого полей поменяны местами. '
                              '2. Название таба "Телефон" по ТЗ должно быть "Номер"')
    def test_guest_should_see_login_form(self, browser, result_status='FAILED'):
        """ Тест-кейс гость проверяет наличие основных элементов на странице авторизации """
        page = AuthPage(browser)
        page.open()
        try:
            page.should_be_logo_on_header()
            elements_left_side = ['Авторизация', 'Номер', 'Почта', 'Логин', 'Лицевой счёт',
                                  'Пароль', 'Забыл пароль', 'Войти', 'Зарегистрироваться']
            page.should_be_basic_content('left', elements_left_side)
            elements_right_side = ['Ростелеком']
            page.should_be_basic_content('right', elements_right_side)
            page.should_be_footer()
            result_status = 'PASSED'
        finally:
            title = self.test_guest_should_see_login_form.__doc__
            rs_write(result_status, title)

    @pytest.mark.proba
    def test_guest_should_see_phone_auth(self, browser, result_status='FAILED'):
        """ Тест-кейс гость проверяет, что авторизация по умолчанию по номеру телефона и паролю """
        page = AuthPage(browser)
        page.open()
        try:
            page.should_be_phone_active()
            result_status = 'PASSED'
        finally:
            title = self.test_guest_should_see_phone_auth.__doc__
            rs_write(result_status, title)

    def test_guest_should_see_user_agreement(self, browser, result_status='FAILED'):
        """ Тест-кейс гость переходит на страницу пользовательского соглашения """
        page = AuthPage(browser)
        page.open()
        try:
            page.go_to_the_user_agreement_page()
            result_status = 'PASSED'
        finally:
            title = self.test_guest_should_see_user_agreement.__doc__
            rs_write(result_status, title)

    @pytest.mark.parametrize('account', various_accounts,
                             ids=["account VKontakte", "account OK", "account @mail", "account Google",
                                  "account Yandex", "go to the registration page"])
    def test_guest_should_see_various_forms_of_registration(self, browser, account, result_status='FAILED'):
        """ Тест-кейс гость проверяет возможность регистрации через различные аккаунты
        'ВКонтакте', Одноклассники, @Мой мир, Google, а также переход на страницу регистрации """
        page = AuthPage(browser)
        page.open()
        try:
            page.should_be_various_accounts_link(account)
            result_status = 'PASSED'
        finally:
            title = self.test_guest_should_see_various_forms_of_registration.__doc__
            rs_write(result_status, title)

    def test_guest_should_see_support_phone(self, browser, result_status='FAILED'):
        """ Тест-кейс гость проверяет возможность набора номера службы поддержки """
        page = AuthPage(browser)
        page.open()
        try:
            page.should_be_support_phone_link()
            result_status = 'PASSED'
        finally:
            title = self.test_guest_should_see_support_phone.__doc__
            rs_write(result_status, title)

    # Нет тестовых данных "Лицевой счёт" для входа в аккаунт пользователя
    @pytest.mark.proba
    @pytest.mark.positive
    @pytest.mark.parametrize('tab', ['phone', 'email', 'login'], ids='{}'.format)
    def test_auth_ok_by_tab(self, browser, tab, result_status='FAILED'):
        """ Базовая проверка авторизации "ТЕЛЕФОН + ПАРОЛЬ", "ПОЧТА + ПАРОЛЬ", "ЛОГИН + ПАРОЛЬ" """
        page = AuthPage(browser)
        page.open()
        args = [valid_user_data[tab], valid_user_data['password']]
        try:
            page.insert_user_data_to_fields(*args)
            assert WebDriverWait(browser, 10).until(
                EC.text_to_be_present_in_element(AccountPageLocators.PAGE_ACCOUNT,
                                                 'Учетные данные'))
            result_status = 'PASSED'
        finally:
            title = self.test_auth_ok_by_tab.__doc__
            rs_write(result_status, title, *args)

    @pytest.mark.negative   # , 'email', 'login', 'ls'
    @pytest.mark.parametrize('tab', ['phone', 'email', 'login', 'ls'], ids='{}'.format)
    def test_auth_any_tabs_bad(self, browser, tab, result_status='FAILED'):
        """ Негативные тест-кейсы. Проверка авторизации пользователя в различных сочетаниях
        PHONE + PASSWORD, EMAIL + PASSWORD, LOGIN + PASSWORD, LS + PASSWORD
        В тестах используется 'костыль', чтобы при прохождении негативных авторизаций не приходилось
        вводить капчу, перед каждым тестом запускается одна позитивная авторизация """
        page = AuthPage(browser)
        page.open()
        page.for_reset_bad_cases()
        args = [tab, valid_guest_data[tab], valid_guest_data['password']]
        try:
            page.check_auth_param_plus_pass(*args, exp=False)
            result_status = 'PASSED'
        finally:
            title = self.test_auth_any_tabs_bad.__doc__
            rs_write(result_status, title, *args)

    @pytest.mark.positive
    @pytest.mark.xfail(reason='Баг! При вводе 12-значного числа таб Лицевой счёт не активируется')
    @pytest.mark.parametrize('tab', ['phone', 'email', 'login', 'ls'], ids='{}'.format)
    def test_check_autochange_tabs(self, browser, tab, result_status='FAILED'):
        """ Позитивные тест-кейсы. Проверка, что при вводе номера телефона/почты/логина/лицевого счета -
        таб выбора аутентификации меняется автоматически """
        page = AuthPage(browser)
        page.open()
        args = [tab, valid_guest_data[tab]]
        try:
            page.check_autochange_tabs(*args)
            result_status = 'PASSED'
        finally:
            title = self.test_check_autochange_tabs.__doc__
            rs_write(result_status, title, *args)

    @pytest.mark.positive
    @pytest.mark.parametrize('count_digits', [10, 11, 20], ids='{} digits'.format)
    def test_check_valid_phone_good(self, browser, count_digits, result_status='FAILED'):
        """ Позитивные тест-кейсы. Граничные значения. Проверка корректности введённого номера телефона """
        page = AuthPage(browser)
        page.open()
        tab = 'phone'
        args = [tab, count_digits]
        val = ''
        try:
            val = page.check_phone_correct(*args)
            result_status = 'PASSED'
        finally:
            title = self.test_check_valid_phone_good.__doc__
            args[1] = val
            rs_write(result_status, title, *args)

    @pytest.mark.negative
    @pytest.mark.parametrize('count_digits', [1, 9], ids='{} digits'.format)
    def test_check_valid_phone_bad(self, browser, count_digits, result_status='FAILED'):
        """ Негативные тест-кейсы. Граничные значения. Проверка корректности введённого номера телефона """
        page = AuthPage(browser)
        page.open()
        tab = 'phone'
        args = [tab, count_digits]
        val = ''
        try:
            val = page.check_phone_correct(*args, False)
            result_status = 'PASSED'
        finally:
            title = self.test_check_valid_phone_bad.__doc__
            args[1] = val
            rs_write(result_status, title, *args)

    @pytest.mark.positive
    @pytest.mark.parametrize('mail_name', [1, 64], ids='mail_name: {} symb.'.format)
    @pytest.mark.parametrize('mail_domain', [1, 252], ids='mail_domain: {} symb.'.format)
    def test_check_valid_email_good(self, browser, mail_name, mail_domain, result_status='FAILED'):
        """ Позитивные тест-кейсы. Граничные значения. Проверка корректности введённого адреса электронной почты """
        page = AuthPage(browser)
        page.open()
        args = [mail_name, mail_domain]
        val = ''
        try:
            val = page.check_email_correct(*args)
            result_status = 'PASSED'
        finally:
            title = self.test_check_valid_email_good.__doc__
            args[0], args[1] = 'email', val
            rs_write(result_status, title, *args)

    @pytest.mark.negative
    @pytest.mark.xfail(reason='Баг! Поле принимает длину email более 320 символов')
    @pytest.mark.parametrize('mail_name', [0, 65], ids='mail_name: {} symb.'.format)
    @pytest.mark.parametrize('mail_domain', [0, 253], ids='mail_domain: {} symb.'.format)
    def test_check_valid_email_bad(self, browser, mail_name, mail_domain, result_status='FAILED'):
        """ Негативные тест-кейсы. Граничные значения. Проверка корректности введённого адреса электронной почты """
        page = AuthPage(browser)
        page.open()
        args = [mail_name, mail_domain]
        val = ''
        try:
            val = page.check_email_correct(*args, False)
            result_status = 'PASSED'
        finally:
            title = self.test_check_valid_email_bad.__doc__
            args[0], args[1] = 'email', val
            rs_write(result_status, title, *args)

    @pytest.mark.positive
    @pytest.mark.parametrize('count_digits', [12, 13, 20], ids='{} digits'.format)
    def test_check_valid_ls_good(self, browser, count_digits, result_status='FAILED'):
        """ Позитивные тест-кейсы. Граничные значения. Проверка корректности введённого лицевого счёта """
        page = AuthPage(browser)
        page.open()
        page.click_tab_ls()
        tab = 'ls'
        args = [tab, count_digits]
        val = ''
        try:
            val = page.check_phone_correct(*args)
            result_status = 'PASSED'
        finally:
            title = self.test_check_valid_ls_good.__doc__
            args[1] = val
            rs_write(result_status, title, *args)

    @pytest.mark.negative
    @pytest.mark.parametrize('count_digits', [1, 11], ids='{} digits'.format)
    def test_check_valid_ls_bad(self, browser, count_digits, result_status='FAILED'):
        """ Негативные тест-кейсы. Граничные значения. Проверка корректности введённого лицевого счёта """
        page = AuthPage(browser)
        page.open()
        tab = 'ls'
        args = [tab, count_digits]
        val = ''
        try:
            val = page.check_phone_correct(*args, False)
            result_status = 'PASSED'
        finally:
            title = self.test_check_valid_ls_bad.__doc__
            args[1] = val
            rs_write(result_status, title, *args)

    # ----------------------------------------------------------------
    # Не составлены тест-кейсы для проверки корректных значений логина,
    # т.к. в ТЗ нет требований для этого элемента
    # ----------------------------------------------------------------

    @pytest.mark.positive
    @pytest.mark.parametrize('length_value', [1, 19, 1000], ids='{} symbols'.format)
    @pytest.mark.parametrize('placeholder', [get_nums, letters_en, letters_ru, letters_cn, get_specsymbols],
                             ids='{0.__name__}'.format)
    def test_check_length_login_value_good(self, browser, placeholder, length_value, result_status='FAILED'):
        """ Позитивные тест-кейсы. Граничные значения. Проверка длины введённого логина """
        page = AuthPage(browser)
        page.open()
        page.for_reset_bad_cases()
        page.click_tab_login()
        args = [placeholder(length_value)]
        try:
            page.check_login_correct(*args)
            result_status = 'PASSED'
        finally:
            title = self.test_check_length_login_value_good.__doc__
            rs_write(result_status, title, *args)

    # Эти тесты вызывают ошибку 500 !!!
    @pytest.mark.negative
    @pytest.mark.parametrize('length_value', [1200], ids='{} symbols'.format)
    @pytest.mark.parametrize('placeholder', [get_nums, letters_en, letters_ru, letters_cn, get_specsymbols],
                             ids='{0.__name__}'.format)
    def test_check_length_login_value_bad(self, browser, placeholder, length_value, result_status='FAILED'):
        """ Негативные тест-кейсы. Граничные значения. Проверка длины введённого логина """
        page = AuthPage(browser)
        page.open()
        page.for_reset_bad_cases()
        page.click_tab_login()
        args = [f'rtkid_{placeholder(length_value - 6)}']
        try:
            page.check_login_correct(*args, False)
            result_status = 'PASSED'
        finally:
            title = self.test_check_length_login_value_bad.__doc__
            rs_write(result_status, title, *args)

    @pytest.mark.negative
    @pytest.mark.parametrize('symbols', [letters_en, letters_ru, get_specsymbols],
                             ids='digits+{0.__name__} symbols'.format)
    def test_check_valid_phone_symbols_bad(self, browser, symbols, result_status='FAILED'):
        """ Негативные тест-кейсы. Классы эквивалентности. Проверка корректности введённого номера телефона """
        page = AuthPage(browser)
        page.open()
        tab = 'phone'
        args = ("Телефон", get_nums(3) + symbols(7))
        try:
            page.check_phone_correct(tab, symbols, False)
            result_status = 'PASSED'
        finally:
            title = self.test_check_valid_phone_symbols_bad.__doc__
            rs_write(result_status, title, *args)

    @pytest.mark.negative
    @pytest.mark.parametrize('symbols', [letters_en, letters_ru, get_specsymbols],
                             ids='digits+{0.__name__} symbols'.format)
    def test_check_valid_ls_symbols_bad(self, browser, symbols, result_status='FAILED'):
        """ Негативные тест-кейсы. Классы эквивалентности. Проверка корректности введённого лицевого счёта """
        page = AuthPage(browser)
        page.open()
        tab = 'ls'
        args = ["Лицевой счёт", get_nums(3) + symbols(7)]
        try:
            page.check_phone_correct(tab, symbols, False)
            result_status = 'PASSED'
        finally:
            title = self.test_check_valid_ls_symbols_bad.__doc__
            rs_write(result_status, title, *args)
