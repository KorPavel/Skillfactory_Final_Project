import pytest
from pages.auth_page import AuthPage
from pages.register_page import RegisterPage
from settings import letters_en, get_nums, get_specsymbols, letters_cn, \
    various_mail, various_phone, various_password, popular_password
from time import sleep


def rs_write(result_status, title, *args):
    with open('Notebook.txt', 'a', encoding='utf8') as file:
        file.write(f'>> Описание теста: {title}\n')
        if args:
            file.write('>> Тестовые данные:\n' + "\n".join(map(str, args)) + '\n')
        file.write(f'>> Результат теста: {result_status}\n')


def go_to_reg(browser):
    page = AuthPage(browser)
    page.open()
    page.click_to_register_link()


class TestRegistration:

    @pytest.mark.xfail(reason='Баги!!! 1.Слоган "Ростелекома" отсутствует в левой части страницы. '
                              '2. Кнопка "Зарегистрироваться" в ТЗ называется "Продолжить".')
    def test_guest_should_see_login_form(self, browser, result_status='FAILED'):
        """ Тест-кейс гость проверяет наличие основных элементов на странице регистрации """
        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        try:
            page.should_be_logo_on_header()
            elements_left_side = ['Ростелеком']
            page.should_be_basic_content('left', elements_left_side)
            elements_right_side = ['Регистрация', 'Имя', 'Фамилия', 'Регион', 'E-mail',
                                   'мобильный телефон', 'Пароль', 'Подтверждение пароля',
                                   'Продолжить', 'пользовательского соглашения']
            page.should_be_basic_content('right', elements_right_side)
            page.should_be_footer()
            page.browser.save_screenshot('register_page_elems.png')
            result_status = 'PASSED'
        finally:
            title = self.test_guest_should_see_login_form.__doc__
            rs_write(result_status, title)

    def test_register_default_region(self, browser, result_status='FAILED'):
        """ Проверка региона регистрации по умолчанию. """
        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        args = ("Москва",)

        try:
            page.should_be_default_region(*args)
            result_status = 'PASSED'
        finally:
            title = self.test_register_default_region.__doc__
            rs_write(result_status, title, *args)

    def test_register_select_some_region(self, browser, result_status='FAILED'):
        """ Проверка выбора любого региона регистрации пользователя """
        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        args = ("Липецк",)
        try:
            page.should_be_select_some_region(*args)
            result_status = 'PASSED'
        finally:
            title = self.test_register_select_some_region.__doc__
            rs_write(result_status, title, *args)

    @pytest.mark.positive
    @pytest.mark.parametrize("address", ['email', 'phone'], ids="{0}".format)
    def test_register_complete(self, browser, address, result_status='FAILED'):
        """ Позитивные тест-кейсы. Проверка полей регистрации по валидным значениям.
        Варианты регистрации по электронной почте или по телефону."""
        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        args = [address]
        val = {}
        try:
            val = page.choosing_registration_option(*args)
            result_status = 'PASSED'
        finally:
            [args.append(el) for el in val.values()]
            title = self.test_register_complete.__doc__
            rs_write(result_status, title, *args)

    @pytest.mark.negative
    def test_register_empty_fields(self, browser, result_status='FAILED'):
        """ Негативный тест-кейс. Проверка невозможной регистрации при незаполненных полях """
        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        try:
            page.send_all_fields_is_empty()
            result_status = 'PASSED'
        finally:
            title = self.test_register_empty_fields.__doc__
            rs_write(result_status, title)

    @pytest.mark.positive
    @pytest.mark.parametrize('type_name', ['first_name', 'last_name'], ids="{0}".format)
    @pytest.mark.parametrize("length_name", [2, 3, 30], ids="{0} symbols".format)
    def test_register_first_name_length_good(self, browser, type_name: str, length_name: int, result_status='FAILED'):
        """ Позитивные тест-кейсы. Проверка граничных значений длительности ИМЕНИ/ФАМИЛИИ
        пользователя, набранных кириллическими символами """
        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        args = [type_name, length_name]
        val = ''
        try:
            val = page.params_name_length(*args)
            result_status = 'PASSED'
        finally:
            title = self.test_register_first_name_length_good.__doc__
            args[1] = val
            rs_write(result_status, title, *args)

    @pytest.mark.negative
    @pytest.mark.parametrize('type_name', ['first_name', 'last_name'], ids="{0}".format)
    @pytest.mark.parametrize("length_name", [0, 1, 31], ids="{0} symbols".format)
    def test_register_first_name_length_bad(self, browser, type_name: str, length_name: int, result_status='FAILED'):
        """ Негативные тест-кейсы. Проверка граничных значений длительности ИМЕНИ/ФАМИЛИИ
        пользователя, набранных кириллическими символами """
        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        args = [type_name, length_name]
        val = ''
        try:
            val = page.params_name_length(*args, False)
            result_status = 'PASSED'
        finally:
            title = self.test_register_first_name_length_bad.__doc__
            args[1] = val
            rs_write(result_status, title, *args)

    @pytest.mark.positive
    @pytest.mark.parametrize("phone", [('+7', 10), ('7', 10), ('89', 9), ('+89', 9),
                                       ('+375', 9), ('375', 9)],
                             ids='prefix {0[0]} and {0[1]} digits'.format)
    def test_register_phone_length_good(self, browser, phone: tuple, result_status='FAILED'):
        """ Позитивные тест-кейсы. Проверка граничных значений длительности ТЕЛЕФОННЫХ НОМЕРОВ
         с валидными префиксами """
        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        args = ['phone', phone]
        val = ''
        try:
            val = page.params_address_length(*args)
            result_status = 'PASSED'
        finally:
            title = self.test_register_phone_length_good.__doc__
            args[1] = val
            rs_write(result_status, title, *args)

    @pytest.mark.negative
    @pytest.mark.parametrize("phone", [('+7', 9), ('+7', 11), ('+375', 8), ('+375', 10),
                                       ('+6', 10), ('+475', 9), ('', 0)],
                             ids='prefix {0[0]} and {0[1]} digits'.format)
    def test_register_phone_length_bad(self, browser, phone: tuple, result_status='FAILED'):
        """ Негативные тест-кейсы. Проверка граничных значений длительности ТЕЛЕФОННЫХ НОМЕРОВ
         с валидными префиксами, так же с валидными длительностями и невалидными префиксами """
        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        args = ['phone', phone]
        val = ''
        try:
            val = page.params_address_length(*args, exp=False)
            result_status = 'PASSED'
        finally:
            title = self.test_register_phone_length_bad.__doc__
            args[1] = val
            rs_write(result_status, title, *args)

    @pytest.mark.positive
    @pytest.mark.parametrize("user", [1, 64], ids="{0} symb. mail name".format)
    @pytest.mark.parametrize("server", [1, 252], ids="{0} symb.mail domain".format)
    def test_register_email_length_good(self, browser, user: int, server: int, result_status='FAILED'):
        """ Позитивные тест-кейсы. Проверка граничных значений длительности ИМЕНИ ПОЛЬЗОВАТЕЛЯ
         и ИМЕНИ СЕРВЕРА в адресе электронного письма """
        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        args = ["email", user, server]
        val = ''
        try:
            val = page.params_address_length(*args)
            result_status = 'PASSED'
        finally:
            del args[2]
            title = self.test_register_email_length_good.__doc__
            args[1] = val
            rs_write(result_status, title, *args)

    @pytest.mark.negative
    @pytest.mark.xfail(reason='Баг! Поле принимает email с количеством символов, '
                              'превышающих стандартные значения')
    @pytest.mark.parametrize("user", [0, 65], ids="{0} symb. mail name".format)
    @pytest.mark.parametrize("server", [0, 253], ids="{0} symb. mail domain".format)
    def test_register_email_length_bad(self, browser, user: int, server: int, result_status='FAILED'):
        """ Негативные тест-кейсы. Проверка граничных значений длительности ИМЕНИ ПОЛЬЗОВАТЕЛЯ
         с валидным именем сервера в адресе электронного письма, а также пустого поля регистрации """
        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        args = ["email", user, server]
        val = ''
        try:
            val = page.params_address_length(*args, exp=False)
            result_status = 'PASSED'
        finally:
            del args[2]
            title = self.test_register_email_length_bad.__doc__
            args[1] = val
            rs_write(result_status, title, *args)

    @pytest.mark.positive
    @pytest.mark.parametrize("password", ['password', 'password_confirm'], ids="{0}".format)
    @pytest.mark.parametrize("length_password", [8, 9, 20], ids="{0} symbols".format)
    def test_register_passwords_length_good(self, browser, password: str, length_password: int, result_status='FAILED'):
        """ Позитивные тест-кейсы. Проверка граничных значений длительности ПАРОЛЯ
        и ПАРОЛЯ ПОДТВЕРЖДЕНИЯ пользователя, набранных латиницей и спецсимволами """
        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        args = [password, length_password]
        val = ''
        try:
            val = page.params_password_length(*args)
            result_status = 'PASSED'
        finally:
            title = self.test_register_passwords_length_good.__doc__
            args[1] = val
            rs_write(result_status, title, *args)

    @pytest.mark.negative
    @pytest.mark.parametrize("password", ['password', 'password_confirm'], ids="{0}".format)
    @pytest.mark.parametrize("length_password", [0, 7, 21], ids="{0} symbols".format)
    def test_register_passwords_length_bad(self, browser, password: str, length_password: int, result_status='FAILED'):
        """ Негативные тест-кейсы. Проверка граничных значений длительности ПАРОЛЯ
        и ПАРОЛЯ ПОДТВЕРЖДЕНИЯ пользователя, набранных латиницей и спецсимволами """
        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        args = [password, length_password]
        val = ''
        try:
            val = page.params_password_length(*args, exp=False)
            result_status = 'PASSED'
        finally:
            title = self.test_register_passwords_length_bad.__doc__
            args[1] = val
            rs_write(result_status, title, *args)

    @pytest.mark.negative
    def test_register_passwords_not_equal_bad(self, browser, result_status='FAILED'):
        """ Негативный тест-кейс. Проверка граничных значений различия ПАРОЛЯ
        и ПАРОЛЯ ПОДТВЕРЖДЕНИЯ при их валидных значениях """
        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        args, pwd, pwd_conf = [], '', ''
        try:
            pwd, pwd_conf = page.valid_passwords_equal(False)
            result_status = 'PASSED'
        finally:
            args = [pwd, pwd_conf]
            title = self.test_register_passwords_not_equal_bad.__doc__
            rs_write(result_status, title, *args)

    @pytest.mark.negative
    @pytest.mark.parametrize('type_name', ['first_name', 'last_name'], ids="{0}".format)
    @pytest.mark.parametrize("name", [letters_en, get_nums, get_specsymbols, letters_cn],
                             ids="{0.__name__}".format)
    def test_register_name_equivalence(self, browser, type_name, name, result_status='FAILED'):
        """ Негативные тест-кейсы. Проверка ИМЕНИ/ФАМИЛИИ пользователя по классам эквивалентности
        при валидной длине имени """
        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        args = [type_name, name]
        val = ''
        try:
            val = page.params_name_length(*args, False)
            result_status = 'PASSED'
        finally:
            title = self.test_register_name_equivalence.__doc__
            args[1] = val
            rs_write(result_status, title, *args)

    @pytest.mark.positive
    @pytest.mark.parametrize("mail_name", [(10, 0), (0, 10), (5, 5)],
                             ids=['only english letters', 'only numbers', 'english letters + numbers'])
    def test_register_email_equivalence_good(self, browser, mail_name: tuple, result_status='FAILED'):
        """ Позитивные тест-кейсы. Проверка ИМЕНИ почтового ящика по классам эквивалентности
         при валидном ИМЕНИ домена в адресе электронной почты """
        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        args = ["email", mail_name]
        val = ''
        try:
            val = page.params_address_equal(*args)
            result_status = 'PASSED'
        finally:
            title = self.test_register_email_equivalence_good.__doc__
            args[1] = val
            rs_write(result_status, title, *args)

    @pytest.mark.negative
    @pytest.mark.parametrize("email", various_mail, ids="{0}".format)
    def test_register_email_equivalence_bad(self, browser, email, result_status='FAILED'):
        """ Негативные тест-кейсы. Проверка адреса электронной почты по классам эквивалентности при
        невалидных имени почтового ящика или имени домена """
        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        args = ["email", email]
        val = ''
        try:
            val = page.params_address_equal(*args, exp=False)
            result_status = 'PASSED'
        finally:
            title = self.test_register_email_equivalence_bad.__doc__
            args[1] = val
            rs_write(result_status, title, *args)

    @pytest.mark.negative
    @pytest.mark.parametrize("phone", various_phone, ids="{0}".format)
    def test_register_phone_equivalence_bad(self, browser, phone, result_status='FAILED'):
        """ Негативные тест-кейсы. Проверка ТЕЛЕФОННЫХ НОМЕРОВ по классам эквивалентности """
        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        args = ["phone", phone]
        val = ''
        try:
            val = page.params_address_equal(*args, exp=False)
            result_status = 'PASSED'
        finally:
            title = self.test_register_phone_equivalence_bad.__doc__
            args[1] = val
            rs_write(result_status, title, *args)

    @pytest.mark.positive
    @pytest.mark.parametrize("password", ['password', 'password_confirm'], ids="{0}".format)
    @pytest.mark.parametrize("text_password", various_password[2:], ids="\"{0}-Ok\" ".format)
    def test_register_passwords_good(self, browser, password: str, text_password: str, result_status='FAILED'):
        """ Позитивные тест-кейсы. Проверка ПАРОЛЯ и ПАРОЛЯ ПОДТВЕРЖДЕНИЯ по классам эквивалентности """
        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        args = [password, text_password + '-Ok']
        val = ''
        try:
            val = page.params_password_length(*args)
            result_status = 'PASSED'
        finally:
            title = self.test_register_passwords_good.__doc__
            args[1] = val
            rs_write(result_status, title, *args)

    @pytest.mark.xfail(reason='Баг! Проходит пароль с китайскими иероглифами')
    @pytest.mark.negative
    @pytest.mark.parametrize("password", ['password', 'password_confirm'], ids="{0}".format)
    @pytest.mark.parametrize("text_password", various_password, ids="\"{0}\" ".format)
    def test_register_passwords_bad(self, browser, password: str, text_password: str, result_status='FAILED'):
        """ Негативные тест-кейсы. Проверка ПАРОЛЯ и ПАРОЛЯ ПОДТВЕРЖДЕНИЯ по классам эквивалентности """
        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        args = [password, text_password]
        val = ''
        try:
            val = page.params_password_length(*args, exp=False)
            result_status = 'PASSED'
        finally:
            title = self.test_register_passwords_bad.__doc__
            args[1] = val
            rs_write(result_status, title, *args)

    @pytest.mark.negative
    @pytest.mark.parametrize("text_password", popular_password, ids="\"{0}\"".format)
    def test_register_passwords_popular(self, browser, text_password: str, result_status='FAILED'):
        """ Негативные тест-кейсы. Проверка ПАРОЛЯ и ПАРОЛЯ ПОДТВЕРЖДЕНИЯ по классам эквивалентности """
        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        args = [text_password]
        try:
            _ = page.params_password_equal(*args)
            result_status = 'PASSED'
        finally:
            title = self.test_register_passwords_popular.__doc__
            rs_write(result_status, title, *args)

    @pytest.mark.proba
    @pytest.mark.positive
    def test_successful_registration_from_a_virtual_email(self, browser, virtual_email=None,
                                                          sdi_code=None, result_status='FAILED'):
        """ Тест-кейс прохождения этапов регистрации на сайте в автоматическом режиме,
        используя рандомный почтовый ящик с сайта '1secmail.com'. Далее добавляем этот email
        в файл settings.
        !!! Тест запускать через командную строку !!! """

        go_to_reg(browser)
        page = RegisterPage(browser, browser.current_url)
        try:
            virtual_email = page.get_virtual_email()
            page.change_user_data('email', virtual_email)
            sleep(30)  # Время ожидания письма с кодом от Ростелекома ...
            sdi_code = page.read_last_mail_message(virtual_email)
            page.insert_reg_code_to_codes_area(sdi_code)
            page.checking_user_account()
            page.overwriting_settings(virtual_email)
            result_status = 'PASSED'
        finally:
            title = self.test_successful_registration_from_a_virtual_email.__doc__
            args = [f'Виртуальный email: {virtual_email}', f'SDI code: {sdi_code}']
            rs_write(result_status, title, *args)

