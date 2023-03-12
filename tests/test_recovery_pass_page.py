import pytest
from pages.auth_page import AuthPage
from pages.recovery_page import RecoveryPage
from settings import *
from time import sleep


def rs_write(result_status, title, *args):
    with open('Notebook.txt', 'a', encoding='utf8') as file:
        file.write(f'>> Описание теста: {title}\n')
        if args:
            file.write('>> Тестовые данные:\n' + "\n".join(map(str, args)) + '\n')
        file.write(f'>> Результат теста: {result_status}\n')


def go_to_recovery_password(browser):
    page = AuthPage(browser)
    page.open()
    page.click_to_forgot_password_link()


class TestRecoveryPassword:

    @pytest.mark.xfail(reason='Баги!!! 1.Название таба "Телефон" по ТЗ называется "Номер". '
                              '2. Кнопка "Продолжить" в ТЗ называется "Далее".')
    def test_user_should_see_reset_password_form(self, browser, result_status='FAILED'):
        """ Тест-кейс. Проверка наличия основных элементов на странице восстановления пароля """
        go_to_recovery_password(browser)
        page = RecoveryPage(browser, browser.current_url)
        try:
            page.should_be_logo_on_header()
            elements_right_side = ["Восстановление пароля", "Телефон", "Почта", "Логин", "Лицевой счёт",
                                   "Далее", "Вернуться назад"]
            page.should_be_basic_content('right', elements_right_side)
            page.should_be_footer()
            result_status = 'PASSED'
        finally:
            title = self.test_user_should_see_reset_password_form.__doc__
            rs_write(result_status, title)

    def test_user_should_see_recover_phone_default(self, browser, result_status='FAILED'):
        """ Тест-кейс. Проверка, что по умолчанию выбрана форма восстановления пароля по телефону """
        go_to_recovery_password(browser)
        page = RecoveryPage(browser, browser.current_url)
        args = ['phone']
        try:
            page.should_be_tab_active(*args)
            result_status = 'PASSED'
        finally:
            title = self.test_user_should_see_recover_phone_default.__doc__
            rs_write(result_status, title, *args)

    def test_checking_tab_switching(self, browser, result_status='FAILED'):
        """ Тест-кейс. Проверка переключения табов и активности выбранного таба """
        go_to_recovery_password(browser)
        page = RecoveryPage(browser, browser.current_url)
        try:
            page.click_tab_ls()
            page.click_tab_login()
            page.click_tab_email()
            page.click_tab_phone()
            result_status = 'PASSED'
        finally:
            title = self.test_checking_tab_switching.__doc__
            rs_write(result_status, title)

    @pytest.mark.positive
    @pytest.mark.xfail(reason='При начальной активности таба "Телефон" нет автоматического '
                              'переключения таба на "Лицевой счёт".')
    @pytest.mark.parametrize('value', ['phone', 'email', 'login', 'ls'], ids='{}'.format)
    def test_checking_tab_switching_to_valid_values(self, browser, value, result_status='FAILED'):
        """ Тест-кейс. Проверка автоматического переключения табов при вводе
        в поле логина информации соответствующего типа """
        go_to_recovery_password(browser)
        page = RecoveryPage(browser, browser.current_url)
        args = [value, valid_guest_data[value]]
        try:
            # page.click_tab_email()  # Всё будет работать, если начальный таб будет, к примеру, "Почта"
            page.checking_tab_switching_to_insert_valid_values(*args)
            result_status = 'PASSED'
        finally:
            title = self.test_checking_tab_switching_to_valid_values.__doc__
            rs_write(result_status, title, *args)

    @pytest.mark.negative
    def test_checking_messages_with_an_empty_field(self, browser, result_status='FAILED'):
        """ Тест-кейс. Проверка сообщений об ошибке при незаполненных полях ввода логина и кода
        и нажатии кнопки "Продолжить" """
        go_to_recovery_password(browser)
        page = RecoveryPage(browser, browser.current_url)
        try:
            page.checking_messages_with_an_empty_field()
            result_status = 'PASSED'
        finally:
            title = self.test_checking_messages_with_an_empty_field.__doc__
            rs_write(result_status, title)

    @pytest.mark.negative
    @pytest.mark.parametrize('value', ['phone', 'email', 'login', 'ls'], ids='{}'.format)
    def test_checking_message_with_an_incorrect_code(self, browser, value, result_status='FAILED'):
        """ Тест-кейс. Проверка сообщений об ошибке при вводе неправильного кода капчи """
        go_to_recovery_password(browser)
        page = RecoveryPage(browser, browser.current_url)
        args = [valid_guest_data[value]]
        try:
            page.checking_message_with_an_incorrect_code(*args)
            result_status = 'PASSED'
        finally:
            title = self.test_checking_message_with_an_incorrect_code.__doc__
            rs_write(result_status, title, *args)

    @pytest.mark.positive
    @pytest.mark.skip(reason='Полуавтоматический метод, требуется участие человека')
    @pytest.mark.parametrize('value', ['phone', 'email', 'login'], ids='{}'.format)
    def test_successful_password_recovery_case(self, browser, value, result_status='FAILED'):
        """ Тест-кейсы. Прохождение этапов восстановления пароля к аккаунту пользователя
        с получением кода через сообщение по e-mail при условии, что у пользователя в
        аккаунте зарегистрирован телефон и адрес электронной почты """
        go_to_recovery_password(browser)
        page = RecoveryPage(browser, browser.current_url)

        args = [valid_user_data[value]]
        try:
            page.successful_password_recovery_case(*args)
            result_status = 'PASSED'
        finally:
            title = self.test_successful_password_recovery_case.__doc__
            rs_write(result_status, title, *args)

    @pytest.mark.manual
    def test_automatize_recovery_password(self, browser, reg_code=None, new_password=None, result_status='FAILED'):
        """ Тест-кейс проходит процедуру восстановления пароля в автоматизированном режиме.
        В тесте требуется присутствие человека для набора кода с картинки капчи.
        Тест следует запускать с командной строки !!! """
        go_to_recovery_password(browser)
        page = RecoveryPage(browser, browser.current_url)
        try:
            page.checking_tab_switching_to_insert_valid_values('email', virtual_email)
            sleep(30)  # Время для ввода капчи с картинки
            page.click_to_continue()
            sleep(30)  # Время ожидания письма с кодом от Ростелекома
            reg_code = page.read_last_mail_message(virtual_email)
            page.insert_reg_code_to_codes_area(reg_code)
            new_password = page.insert_new_password_in_pass_area()
            page.checking_user_should_see_auth_page()
            page.overwriting_settings(virtual_email, new_password)
            result_status = 'PASSED'
        finally:
            title = self.test_automatize_recovery_password.__doc__
            args = [f'Виртуальный email: {virtual_email}',
                    f'SDI code: {reg_code}',
                    f'Новый пароль: {new_password}']
            rs_write(result_status, title, *args)





