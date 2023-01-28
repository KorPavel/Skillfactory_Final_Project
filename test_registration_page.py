import pytest
from .pages.auth_page import AuthPage
from .pages.registr_page import RegistrPage
from .settings import *
from time import sleep


def go_to_reg(browser):
    page = AuthPage(browser)
    page.open()
    page.click_to_register_link()


@pytest.mark.xfail(reason='Баги!!! 1.Слоган "Ростелекома" отсутствует в левой части страницы. '
                          '2. Кнопка "Зарегистрироваться" в ТЗ называется "Продолжить".')
def test_guest_should_see_login_form(browser):
    """ Тест-кейс гость проверяет наличие основных элементов на странице регистрации """
    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    page.should_be_logo_on_header()
    elements_left_side = ['Ростелеком']
    page.should_be_basic_content('left', elements_left_side)
    elements_right_side = ['Регистрация', 'Имя', 'Фамилия', 'Регион', 'E-mail',
                           'мобильный телефон', 'Пароль', 'Подтверждение пароля',
                           'Продолжить', 'пользовательского соглашения']
    page.should_be_basic_content('right', elements_right_side)
    page.should_be_footer()
    page.browser.save_screenshot('register_page_elems.png')


def test_register_default_region(browser):
    """ Проверка региона регистрации по умолчанию. """
    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    page.should_be_default_region("Москва")


def test_register_select_some_region(browser):
    """ Проверка выбора любого региона регистрации пользователя """
    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    page.should_be_select_some_region("Липецк")


@pytest.mark.positive
@pytest.mark.parametrize("address", ['email', 'phone'], ids="{0}".format)
def test_register_complete(browser, address):
    """ Позитивные тест-кейсы. Проверка полей регистрации по валидным значениям.
    Варианты регистрации по электронной почте или по телефону."""
    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    page.choosing_registration_option(address)


@pytest.mark.negative
def test_register_empty_fields(browser):
    """ Негативный тест-кейс. Проверка невозможной регистрации при незаполненных полях """
    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    page.send_all_fields_is_empty()


@pytest.mark.positive
@pytest.mark.parametrize('type_name', ['first_name', 'last_name'], ids="{0}".format)
@pytest.mark.parametrize("length_name", [2, 3, 30], ids="{0} symbols".format)
def test_register_first_name_length_good(browser, type_name: str, length_name: int):
    """ Позитивные тест-кейсы. Проверка граничных значений длительности ИМЕНИ/ФАМИЛИИ
    пользователя, набранных кириллическими символами """
    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    page.params_name_length(type_name, length_name)


@pytest.mark.negative
@pytest.mark.parametrize('type_name', ['first_name', 'last_name'], ids="{0}".format)
@pytest.mark.parametrize("length_name", [0, 1, 31], ids="{0} symbols".format)
def test_register_first_name_length_bad(browser, type_name: str, length_name: int):
    """ Негативные тест-кейсы. Проверка граничных значений длительности ИМЕНИ/ФАМИЛИИ
    пользователя, набранных кириллическими символами """
    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    page.params_name_length(type_name, length_name, False)


@pytest.mark.positive
@pytest.mark.parametrize("phone", [('+7', 10), ('7', 10), ('89', 9), ('+89', 9),
                                   ('+375', 9), ('375', 9)],
                         ids='prefix {0[0]} and {0[1]} digits'.format)
def test_register_phone_length_good(browser, phone: tuple):
    """ Позитивные тест-кейсы. Проверка граничных значений длительности ТЕЛЕФОННЫХ НОМЕРОВ
     с валидными префиксами """
    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    page.params_address_length('phone', phone)


@pytest.mark.negative
@pytest.mark.parametrize("phone", [('+7', 9), ('+7', 11), ('+375', 8), ('+375', 10),
                                   ('+6', 10), ('+475', 9), ('', 0)],
                         ids='prefix {0[0]} and {0[1]} digits'.format)
def test_register_phone_length_bad(browser, phone: tuple):
    """ Негативные тест-кейсы. Проверка граничных значений длительности ТЕЛЕФОННЫХ НОМЕРОВ
     с валидными префиксами, так же с валидными длительностями и невалидными префиксами """
    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    page.params_address_length('phone', phone, exp=False)


@pytest.mark.positive
@pytest.mark.parametrize("user", [1, 64], ids="{0} symb. mail name".format)
@pytest.mark.parametrize("server", [1, 252], ids="{0} symb.mail domain".format)
def test_register_email_length_good(browser, user: int, server: int):
    """ Позитивные тест-кейсы. Проверка граничных значений длительности ИМЕНИ ПОЛЬЗОВАТЕЛЯ
     и ИМЕНИ СЕРВЕРА в адресе электронного письма """
    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    page.params_address_length("email", user, server)


@pytest.mark.negative
@pytest.mark.xfail(reason='Баг! Поле принимает email с количеством символов, '
                          'превышающих стандартные значения')
@pytest.mark.parametrize("user", [0, 65], ids="{0} symb. mail name".format)
@pytest.mark.parametrize("server", [0, 253], ids="{0} symb. mail domain".format)
def test_register_email_length_bad(browser, user: int, server: int):
    """ Негативные тест-кейсы. Проверка граничных значений длительности ИМЕНИ ПОЛЬЗОВАТЕЛЯ
     с валидным именем сервера в адресе электронного письма, а также пустого поля регистрации """
    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    page.params_address_length("email", user, server, exp=False)


@pytest.mark.positive
@pytest.mark.parametrize("password", ['password', 'password_confirm'], ids="{0}".format)
@pytest.mark.parametrize("length_password", [8, 9, 20], ids="{0} symbols".format)
def test_register_passwords_length_good(browser, password: str, length_password: int):
    """ Позитивные тест-кейсы. Проверка граничных значений длительности ПАРОЛЯ
    и ПАРОЛЯ ПОДТВЕРЖДЕНИЯ пользователя, набранных латиницей и спецсимволами """
    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    page.params_password_length(password, length_password)


@pytest.mark.negative
@pytest.mark.parametrize("password", ['password', 'password_confirm'], ids="{0}".format)
@pytest.mark.parametrize("length_password", [0, 7, 21], ids="{0} symbols".format)
def test_register_passwords_length_bad(browser, password: str, length_password: int):
    """ Негативные тест-кейсы. Проверка граничных значений длительности ПАРОЛЯ
    и ПАРОЛЯ ПОДТВЕРЖДЕНИЯ пользователя, набранных латиницей и спецсимволами """
    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    page.params_password_length(password, length_password, False)


@pytest.mark.negative
def test_register_passwords_not_equal_bad(browser):
    """ Негативный тест-кейс. Проверка граничных значений различия ПАРОЛЯ
    и ПАРОЛЯ ПОДТВЕРЖДЕНИЯ при их валидных значениях """
    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    page.valid_passwords_equal(False)


@pytest.mark.negative
@pytest.mark.parametrize('type_name', ['first_name', 'last_name'], ids="{0}".format)
@pytest.mark.parametrize("name", [letters_en, get_nums, get_specsymbols, letters_cn],
                         ids="{0.__name__}".format)
def test_register_name_equivalence(browser, type_name, name):
    """ Негативные тест-кейсы. Проверка ИМЕНИ/ФАМИЛИИ пользователя по классам эквивалентности
    при валидной длине имени """
    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    page.params_name_length(type_name, name, False)


@pytest.mark.positive
@pytest.mark.parametrize("mail_name", [(10, 0), (0, 10), (5, 5)],
                         ids=['only english letters', 'only numbers', 'english letters + numbers'])
def test_register_email_equivalence_good(browser, mail_name: tuple):
    """ Позитивные тест-кейсы. Проверка ИМЕНИ почтового ящика по классам эквивалентности
     при валидном ИМЕНИ домена в адресе электронной почты """
    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    page.params_address_equal("email", mail_name)


@pytest.mark.negative
@pytest.mark.parametrize("email", various_mail, ids="{0}".format)
def test_register_email_equivalence_bad(browser, email):
    """ Негативные тест-кейсы. Проверка адреса электронной почты по классам эквивалентности при
    невалидных имени почтового ящика или имени домена """
    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    page.params_address_equal("email", email, exp=False)


@pytest.mark.proba
@pytest.mark.negative
@pytest.mark.parametrize("phone", various_phone, ids="{0}".format)
def test_register_phone_equivalence_bad(browser, phone):
    """ Негативные тест-кейсы. Проверка ТЕЛЕФОННЫХ НОМЕРОВ по классам эквивалентности """
    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    page.params_address_equal("phone", phone, exp=False)


@pytest.mark.positive
@pytest.mark.parametrize("password", ['password', 'password_confirm'], ids="{0}".format)
@pytest.mark.parametrize("text_password", various_password[2:], ids="\"{0}-Ok\" ".format)
def test_register_passwords_good(browser, password: str, text_password: str):
    """ Позитивные тест-кейсы. Проверка ПАРОЛЯ и ПАРОЛЯ ПОДТВЕРЖДЕНИЯ по классам эквивалентности """
    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    page.params_password_length(password, text_password + '-Ok')


@pytest.mark.xfail(reason='Баг! Проходит пароль с китайскими иероглифами')
@pytest.mark.negative
@pytest.mark.parametrize("password", ['password', 'password_confirm'], ids="{0}".format)
@pytest.mark.parametrize("text_password", various_password, ids="\"{0}\" ".format)
def test_register_passwords_bad(browser, password: str, text_password: str):
    """ Негативные тест-кейсы. Проверка ПАРОЛЯ и ПАРОЛЯ ПОДТВЕРЖДЕНИЯ по классам эквивалентности """
    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    page.params_password_length(password, text_password, False)


@pytest.mark.proba
@pytest.mark.negative
@pytest.mark.parametrize("text_password", popular_password, ids="\"{0}\"".format)
def test_register_passwords_popular(browser, text_password: str):
    """ Негативные тест-кейсы. Проверка ПАРОЛЯ и ПАРОЛЯ ПОДТВЕРЖДЕНИЯ по классам эквивалентности """
    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    page.params_password_equal(text_password)


@pytest.mark.positive
def test_successful_registration_from_a_virtual_email(browser):
    """ Тест-кейс прохождения этапов регистрации на сайте в автоматическом режиме,
    используя рандомный почтовый ящик с сайта '1secmail.com'. Далее добавляем этот email
    в файл settings.
    !!! Тест запускать через командную строку !!! """

    go_to_reg(browser)
    page = RegistrPage(browser, browser.current_url)
    virtual_email = page.get_virtual_email()
    page.change_user_data('email', virtual_email)
    sleep(30)                       # Время ожидания письма с кодом от Ростелекома ...
    sdi_code = page.read_last_mail_message(virtual_email)
    page.insert_reg_code_to_codes_area(sdi_code)
    page.checking_user_account()
    page.overwriting_settings(virtual_email)




