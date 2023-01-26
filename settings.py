import os
from random import choice, randint
from string import punctuation, ascii_lowercase
from faker import Faker
from dotenv import load_dotenv
from .pages.locators import AuthPageLocators, BasePageLocators

__all__ = ['various_accounts', 'get_nums', 'letters_ru', 'letters_en', 'letters_cn',
           'get_specsymbols', 'valid_guest_data', 'valid_user_data', 'various_mail',
           'various_phone', 'text_errors', 'various_password', 'popular_password',
           'MAIN_URL']

load_dotenv()
faker = Faker('ru_RU')

MAIN_URL = 'https://b2c.passport.rt.ru'

various_accounts = [(AuthPageLocators.VK_LINK, 'vk.com'),
                    (AuthPageLocators.OK_LINK, 'ok.ru'),
                    (AuthPageLocators.MAIL_LINK, 'mail.ru'),
                    (AuthPageLocators.GOOGLE_LINK, 'google.com'),
                    (AuthPageLocators.YA_LINK, 'yandex.ru'),
                    (BasePageLocators.REGISTER_LINK, 'registration')]


def get_nums(count: int) -> str:
    """ Функция возвращает строку цифр длиной count символов """
    return ''.join([str(choice(range(10))) for _ in range(count)])


def letters_ru(count: int) -> str:
    """ Функция возвращает строку кириллицы длиной count символов """
    return ''.join(chr(randint(ord('а'), ord('я'))) for _ in range(count))


def letters_en(count: int) -> str:
    """ Функция возвращает строку латиницы длиной count символов """
    return ''.join(choice(ascii_lowercase) for _ in range(count))


def letters_cn(count: int) -> str:
    """ Функция возвращает строку китайских иероглифов длиной count символов """
    text_cn = '这些软软的法式包子多吃点喝点茶从架子上拿一个带钉子的馅饼好好享受你的饭吧别谢我'
    return ''.join(choice(text_cn) for _ in range(count))


def get_specsymbols(count: int) -> str:
    """ Функция возвращает строку спецсимволов длиной count знаков """
    return ''.join(choice(punctuation) for _ in range(count))


valid_user_data = {'first_name': os.getenv('valid_first_name'),
                   'last_name': os.getenv('valid_last_name'),
                   'login': os.getenv('valid_login'),
                   'email': os.getenv('valid_email'),
                   'phone': os.getenv('valid_phone'),
                   'password': os.getenv('valid_password'),
                   'password_confirm': os.getenv('valid_password')}

valid_guest_data = {'first_name': faker.first_name_male(),
                    'last_name': faker.last_name_male(),
                    'login': f'rtkid_{get_nums(13)}',
                    'email': faker.free_email(),
                    'phone': '+79' + get_nums(9),
                    'ls': get_nums(12),
                    'password': 'tEst1Ng%sIte_Rt',
                    'password_confirm': 'tEst1Ng%sIte_Rt'}

various_mail = [f'{letters_ru(10)}@email.com',
                f'email@{letters_ru(5)}.com',
                f'email@email.{letters_ru(3)}',
                f'{get_specsymbols(10)}@email.com',
                f'email@{get_specsymbols(5)}.com',
                f'email@email.{get_specsymbols(3)}',
                f'{letters_cn(10)}@email.com',
                f'email@{letters_cn(5)}.com',
                f'email@email.{letters_cn(3)}'
                ' @email.com',
                'email@ .com',
                'email@email com',
                'email@email. com',
                'email@e mail.com'
                'e mail@email.com',
                'email@email.c om']

various_phone = [letters_ru(11),
                 letters_en(11),
                 letters_cn(11),
                 get_specsymbols(11),
                 f'+7{letters_ru(10)}',
                 f'+7{letters_en(10)}',
                 f'+7{get_specsymbols(10)}',
                 f'+375{letters_ru(9)}',
                 f'+375{letters_en(9)}',
                 f'+375{get_specsymbols(9)}']

popular_password = ['Qwerty12345',
                    'Qwerty123',
                    'Asdfg12345',
                    'Asdfg123',
                    'Zxcvb12345']

# Пароль должен содержать только латинские буквы 'Qw1这些软软的法式包子' - Баг! Пароль проходит.
various_password = ['Qw1这些软软的法式包子',
                    'Qw1ПарольХорош',
                    'GoodPassword',
                    'GOODPASSWORD!',
                    'goodpassword?']

text_errors = ['Длина пароля должна быть не менее 8 символов',
               'Длина пароля должна быть не более 20 символов',
               'Пароль должен содержать только латинские буквы',
               'Пароль должен содержать хотя бы 1 спецсимвол или хотя бы одну цифру',
               'Пароль должен содержать хотя бы одну прописную букву',
               'Пароль должен содержать хотя бы одну заглавную букву']

