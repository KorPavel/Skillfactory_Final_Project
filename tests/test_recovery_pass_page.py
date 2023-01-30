import pytest
from pages.auth_page import AuthPage
from pages.recovery_page import RecoveryPage
from settings import *
from time import sleep


def go_to_recovery_password(browser):
    page = AuthPage(browser)
    page.open()
    page.click_to_forgot_password_link()

class TestRecoveryPassword:

    @pytest.mark.xfail(reason='Баги!!! 1.Название таба "Телефон" по ТЗ называется "Номер". '
                              '2. Кнопка "Продолжить" в ТЗ называется "Далее".')
    def test_user_should_see_reset_password_form(self, browser):
        """ Тест-кейс. Проверка наличия основных элементов на странице восстановления пароля """
        go_to_recovery_password(browser)
        page = RecoveryPage(browser, browser.current_url)
        page.should_be_logo_on_header()
        elements_right_side = ["Восстановление пароля", "Телефон", "Почта", "Логин", "Лицевой счёт",
                               "Далее", "Вернуться назад"]
        page.should_be_basic_content('right', elements_right_side)
        page.should_be_footer()

    def test_user_should_see_recover_phone_default(self, browser):
        """ Тест-кейс. Проверка, что по умолчанию выбрана форма восстановления пароля по телефону """
        go_to_recovery_password(browser)
        page = RecoveryPage(browser, browser.current_url)
        tab = 'phone'
        page.should_be_tab_active(tab)

    def test_checking_tab_switching(self, browser):
        """ Тест-кейс. Проверка переключения табов и активности выбранного таба """
        go_to_recovery_password(browser)
        page = RecoveryPage(browser, browser.current_url)
        page.click_tab_ls()
        page.click_tab_login()
        page.click_tab_email()
        page.click_tab_phone()

    @pytest.mark.positive
    @pytest.mark.xfail(reason='При начальной активности таба "Телефон" нет автоматического '
                              'переключения таба на "Лицевой счёт".')
    @pytest.mark.parametrize('value', ['phone', 'email', 'login', 'ls'], ids='{}'.format)
    def test_checking_tab_switching_to_valid_values(self, browser, value):
        """ Тест-кейс. Проверка автоматического переключения табов при вводе
        в поле логина информации соответствующего типа """
        go_to_recovery_password(browser)
        page = RecoveryPage(browser, browser.current_url)
        # page.click_tab_email()  # Всё будет работать, если начальный таб будет, к примеру, "Почта"
        page.checking_tab_switching_to_insert_valid_values(value, valid_guest_data[value])

    @pytest.mark.negative
    def test_checking_messages_with_an_empty_field(self, browser):
        """ Тест-кейс. Проверка сообщений об ошибке при незаполненных полях ввода логина и кода
        и нажатии кнопки "Продолжить" """
        go_to_recovery_password(browser)
        page = RecoveryPage(browser, browser.current_url)
        page.checking_messages_with_an_empty_field()

    @pytest.mark.negative
    @pytest.mark.parametrize('value', ['phone', 'email', 'login', 'ls'], ids='{}'.format)
    def test_checking_message_with_an_incorrect_code(self, browser, value):
        """ Тест-кейс. Проверка сообщений об ошибке при вводе неправильного кода капчи """
        go_to_recovery_password(browser)
        page = RecoveryPage(browser, browser.current_url)
        page.checking_message_with_an_incorrect_code(valid_guest_data[value])

    @pytest.mark.positive
    @pytest.mark.skip(reason='Полуавтоматический метод, требуется участие человека')
    @pytest.mark.parametrize('value', ['phone', 'email', 'login'], ids='{}'.format)
    def test_successful_password_recovery_case(self, browser, value):
        """ Тест-кейсы. Прохождение этапов восстановления пароля к аккаунту пользователя
        с получением кода через сообщение по e-mail при условии, что у пользователя в
        аккаунте зарегистрирован телефон и адрес электронной почты """
        go_to_recovery_password(browser)
        page = RecoveryPage(browser, browser.current_url)
        page.successful_password_recovery_case(valid_user_data[value])

    @pytest.mark.manual
    def test_automatize_recovery_password(self, browser):
        """ Тест-кейс проходит процедуру восстановления пароля в автоматизированном режиме.
        В тесте требуется присутствие человека для набора кода с картинки капчи.
        Тест следует запускать с командной строки !!! """
        go_to_recovery_password(browser)
        page = RecoveryPage(browser, browser.current_url)
        page.checking_tab_switching_to_insert_valid_values('email', virtual_email)
        sleep(30)               # Время для ввода капчи с картинки
        page.click_to_continue()
        sleep(30)               # Время ожидания письма с кодом от Ростелекома
        reg_code = page.read_last_mail_message(virtual_email)
        page.insert_reg_code_to_codes_area(reg_code)
        new_password = page.insert_new_password_in_pass_area()
        page.checking_user_should_see_auth_page()
        page.overwriting_settings(virtual_email, new_password)






