import pytest
from .pages.auth_page import AuthPage
from .settings import *


@pytest.mark.xfail(reason='Баги! 1. Элементы левого и правого полей поменяны местами. '
                          '2. Название таба "Телефон" по ТЗ должно быть "Номер"')
def test_guest_should_see_login_form(browser):
    """ Тест-кейс гость проверяет наличие основных элементов на странице авторизации """
    page = AuthPage(browser)
    page.open()
    page.should_be_logo_on_header()
    elements_left_side = ['Авторизация', 'Номер', 'Почта', 'Логин', 'Лицевой счёт',
                          'Пароль', 'Забыл пароль', 'Войти', 'Зарегистрироваться']
    page.should_be_basic_content('left', elements_left_side)
    elements_right_side = ['Ростелеком']
    page.should_be_basic_content('right', elements_right_side)
    page.should_be_footer()
    page.browser.save_screenshot('auth_page_elems.png')


def test_guest_should_see_phone_auth(browser):
    """ Тест-кейс гость проверяет, что авторизация по умолчанию по номеру телефона и паролю """
    page = AuthPage(browser)
    page.open()
    page.should_be_phone_active()


def test_guest_should_see_user_agreement(browser):
    """ Тест-кейс гость переходит на страницу пользовательского соглашения """
    page = AuthPage(browser)
    page.open()
    page.go_to_the_user_agreement_page()


@pytest.mark.parametrize('account', various_accounts,
                         ids=["account VKontakte", "account OK", "account @mail", "account Google",
                              "account Yandex", "go to the registration page"])
def test_guest_should_see_various_forms_of_registration(browser, account):
    """ Тест-кейс гость проверяет возможность регистрации через различные аккаунты
    'ВКонтакте', Одноклассники, @Мой мир, Google, а также переход на страницу регистрации """
    page = AuthPage(browser)
    page.open()
    page.should_be_various_accounts_link(account)


def test_guest_should_see_support_phone(browser):
    """ Тест-кейс гость проверяет возможность набора номера службы поддержки """
    page = AuthPage(browser)
    page.open()
    page.should_be_support_phone_link()


# Нет тестовых данных "Лицевой счёт" для входа в аккаунт пользователя
@pytest.mark.positive
@pytest.mark.parametrize('tab', ['phone', 'email', 'login'], ids='{}'.format)
def test_auth_any_tabs_good(browser, tab):
    """ Позитивные тест-кейсы. Проверка авторизации пользователя в различных сочетаниях
    PHONE + PASSWORD, EMAIL + PASSWORD, LOGIN + PASSWORD. """
    page = AuthPage(browser)
    page.open()
    page.check_auth_param_plus_pass(tab, valid_user_data[tab], valid_user_data['password'])


@pytest.mark.negative
@pytest.mark.parametrize('tab', ['phone', 'email', 'login', 'ls'], ids='{}'.format)
def test_auth_any_tabs_bad(browser, tab):
    """ Негативные тест-кейсы. Проверка авторизации пользователя в различных сочетаниях
    PHONE + PASSWORD, EMAIL + PASSWORD, LOGIN + PASSWORD, LS + PASSWORD
    В тестах используется 'костыль', чтобы при прохождении негативных авторизаций не приходилось
    вводить капчу, перед каждым тестом запускается одна позитивная авторизация """
    page = AuthPage(browser)
    page.open()
    page.for_reset_bad_cases()
    page.check_auth_param_plus_pass(tab, valid_guest_data[tab], valid_guest_data['password'], exp=False)


@pytest.mark.positive
# @pytest.mark.xfail(reason='Баг! При вводе 12-значного числа таб Лицевой счёт не активируется')
@pytest.mark.parametrize('tab', ['phone', 'email', 'login', 'ls'], ids='{}'.format)
def test_check_autochange_tabs(browser, tab):
    """ Позитивные тест-кейсы. Проверка, что при вводе номера телефона/почты/логина/лицевого счета -
    таб выбора аутентификации меняется автоматически """
    page = AuthPage(browser)
    page.open()
    page.click_tab_email()
    page.check_autochange_tabs(tab, valid_guest_data[tab])


@pytest.mark.positive
@pytest.mark.parametrize('count_digits', [10, 11, 20], ids='{} digits'.format)
def test_check_valid_phone_good(browser, count_digits):
    """ Позитивные тест-кейсы. Граничные значения. Проверка корректности введённого номера телефона """
    page = AuthPage(browser)
    page.open()
    tab = 'phone'
    page.check_phone_correct(tab, count_digits)


@pytest.mark.negative
@pytest.mark.parametrize('count_digits', [1, 9], ids='{} digits'.format)
def test_check_valid_phone_bad(browser, count_digits):
    """ Негативные тест-кейсы. Граничные значения. Проверка корректности введённого номера телефона """
    page = AuthPage(browser)
    page.open()
    tab = 'phone'
    page.check_phone_correct(tab, count_digits, False)


@pytest.mark.positive
@pytest.mark.parametrize('mail_name', [1, 64], ids='mail_name: {} symb.'.format)
@pytest.mark.parametrize('mail_domain', [1, 252], ids='mail_domain: {} symb.'.format)
def test_check_valid_email_good(browser, mail_name, mail_domain):
    """ Позитивные тест-кейсы. Граничные значения. Проверка корректности введённого адреса электронной почты """
    page = AuthPage(browser)
    page.open()
    page.check_email_correct(mail_name, mail_domain)


@pytest.mark.negative
@pytest.mark.xfail(reason='Баг! Поле принимает длину email более 320 символов')
@pytest.mark.parametrize('mail_name', [0, 65], ids='mail_name: {} symb.'.format)
@pytest.mark.parametrize('mail_domain', [0, 253], ids='mail_domain: {} symb.'.format)
def test_check_valid_email_bad(browser, mail_name, mail_domain):
    """ Негативные тест-кейсы. Граничные значения. Проверка корректности введённого адреса электронной почты """
    page = AuthPage(browser)
    page.open()
    page.check_email_correct(mail_name, mail_domain, False)


@pytest.mark.positive
@pytest.mark.parametrize('count_digits', [12, 13, 20], ids='{} digits'.format)
def test_check_valid_ls_good(browser, count_digits):
    """ Позитивные тест-кейсы. Граничные значения. Проверка корректности введённого лицевого счёта """
    page = AuthPage(browser)
    page.open()
    page.click_tab_ls()
    tab = 'ls'
    page.check_phone_correct(tab, count_digits)


@pytest.mark.negative
@pytest.mark.parametrize('count_digits', [1, 11], ids='{} digits'.format)
def test_check_valid_ls_bad(browser, count_digits):
    """ Негативные тест-кейсы. Граничные значения. Проверка корректности введённого лицевого счёта """
    page = AuthPage(browser)
    page.open()
    tab = 'ls'
    page.check_phone_correct(tab, count_digits, False)

# ----------------------------------------------------------------
# Не составлены тест-кейсы для проверки корректных значений логина,
# т.к. в ТЗ нет требований для этого элемента
# ----------------------------------------------------------------


@pytest.mark.negative
@pytest.mark.parametrize('symbols', [letters_en, letters_ru, get_specsymbols],
                         ids='digits+{0.__name__} symbols'.format)
def test_check_valid_phone_symbols_bad(browser, symbols):
    """ Негативные тест-кейсы. Классы эквивалентности. Проверка корректности введённого номера телефона """
    page = AuthPage(browser)
    page.open()
    tab = 'phone'
    page.check_phone_correct(tab, symbols, False)


@pytest.mark.negative
@pytest.mark.parametrize('symbols', [letters_en, letters_ru, get_specsymbols],
                         ids='digits+{0.__name__} symbols'.format)
def test_check_valid_ls_symbols_bad(browser, symbols):
    """ Негативные тест-кейсы. Классы эквивалентности. Проверка корректности введённого лицевого счёта """
    page = AuthPage(browser)
    page.open()
    tab = 'ls'
    page.check_phone_correct(tab, symbols, False)


