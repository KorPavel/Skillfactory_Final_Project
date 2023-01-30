from selenium.webdriver.common.by import By


class BasePageLocators:
    FOOTER_RT = (By.CLASS_NAME, 'rt-footer-copyright')
    SUPPORT_PHONE = (By.CLASS_NAME, 'rt-footer-right__support-phone')
    REGISTER_LINK = (By.ID, 'kc-register')
    SDI_CODES_AREA = (By.CSS_SELECTOR, '[inputmode="numeric"]')   # .sdi-container .code-input__input


class AuthPageLocators:
    LOGO_HEADER = (By.CLASS_NAME, 'what-is-container__logo-container')
    LEFT_SIDE = (By.ID, 'page-left')
    RIGHT_SIDE = (By.ID, 'page-right')
    TAB_MAIL = (By.ID, 't-btn-tab-mail')
    TAB_PHONE = (By.ID, 't-btn-tab-phone')
    TAB_LOGIN = (By.ID, 't-btn-tab-login')
    TAB_LS = (By.ID, 't-btn-tab-ls')
    LOGIN_AREA = (By.ID, 'username')
    PASSWORD_AREA = (By.ID, 'password')
    PASSWORD_EYE = (By.CLASS_NAME, 'rt-input__eye')
    SUBMIT_BUTTON = (By.NAME, 'login')
    TAB_TYPE = (By.NAME, 'tab_type')
    FORGOT_PASS = (By.ID, 'forgot_password')
    LOGIN_BUTTON = (By.ID, 'kc-login')
    BACK_TO_OTP_BTN = (By.ID, 'back_to_otp_btn')  # Кнопка Войти по временному коду
    USER_AGREE = (By.CSS_SELECTOR, '.auth-policy .rt-link')
    VK_LINK = (By.ID, 'oidc_vk')
    OK_LINK = (By.ID, 'oidc_ok')
    MAIL_LINK = (By.ID, 'oidc_mail')
    GOOGLE_LINK = (By.ID, 'oidc_google')
    YA_LINK = (By.ID, 'oidc_ya')
    OAUTH_WRAP = (By.ID, 'oauth_wrap_content')
    USER_ACCOUNT = (By.CLASS_NAME, 'home-container')
    PAGE_TITLE = (By.CLASS_NAME, 'card-container__title')
    EXIT_ACCOUNT = (By.ID, 'logout-btn')  # Выход из аккаунта
    USER_LASTNAME = (By.CLASS_NAME, 'user-name__last-name')
    USER_FIRSTNAME = (By.CLASS_NAME, 'user-name__first-patronymic')
    MESSAGE_ERR = (By.ID, 'form-error-message')
    LOG_AREA_NAME = (By.CLASS_NAME, 'rt-input__placeholder--top')
    MES_PHONE_ERR = (By.CLASS_NAME, 'rt-input-container__meta--error')


class AccountPageLocators:
    PAGE_ACCOUNT = (By.CSS_SELECTOR, '.home h3:nth-child(2)')


class RegisterPageLocators:
    """ Локаторы элементов на странице регистрации """
    LOGO_HEADER = (By.CLASS_NAME, 'main-header__logo-container')
    LEFT_SIDE = (By.ID, 'page-left')
    RIGHT_SIDE = (By.ID, 'page-right')
    REGISTER_FORM = (By.CLASS_NAME, 'card-container')
    FIRST_NAME = (By.NAME, 'firstName')
    LAST_NAME = (By.NAME, 'lastName')
    ADDRESS = (By.ID, 'address')
    PASSWORD = (By.ID, 'password')
    PASSWORD_CONFIRM = (By.ID, 'password-confirm')
    REGION = (By.CSS_SELECTOR, '.rt-select .rt-input__mask-start')
    SELECT_REG1 = (By.XPATH, ".//div[contains(@class,'register-form__dropdown')]//div[@class='rt-input__action']")
    SELECT_REG2 = (By.XPATH, "//div[@class='rt-select__list-item' and text()[contains(.,'$')]]")
    REGISTER_BUTTON = (By.NAME, 'register')
    TEXT_ERROR = (By.CLASS_NAME, 'rt-input-container__meta--error')
    REGISTER_CONF_FORM = (By.CLASS_NAME, 'register-confirm-form')
    COUNT_SYMB_ERROR = (By.CSS_SELECTOR, '.new-password-container .rt-input-container__meta--error')
    POPULAR_PASSWORD = (By.ID, 'form-error-message')
    SDI_CODES_AREA = (By.CSS_SELECTOR, '.sdi-container .code-input__input')
    USER_LASTNAME = (By.CLASS_NAME, 'user-name__last-name')
    USER_FIRSTNAME = (By.CLASS_NAME, 'user-name__first-patronymic')


class RecoveryPageLocators:
    """ Локаторы элементов на странице восстановления пароля """
    LOGO_HEADER = (By.CLASS_NAME, 'main-header__logo-container')
    LEFT_SIDE = (By.ID, 'page-left')
    RIGHT_SIDE = (By.ID, 'page-right')
    PAGE_TITLE = (By.CLASS_NAME, 'card-container__title')
    PAGE_TEXT = (By.CLASS_NAME, 'card-container__desc')
    TAB_PHONE = (By.ID, 't-btn-tab-phone')
    TAB_MAIL = (By.ID, 't-btn-tab-mail')
    TAB_LOGIN = (By.ID, 't-btn-tab-login')
    TAB_LS = (By.ID, 't-btn-tab-ls')
    TAB_TYPE = (By.NAME, 'tab_type')
    NAME_AREA = (By.ID, 'username')
    CODE_AREA = (By.ID, 'captcha')
    CAPT_IMG = (By.ID, 'rt-captcha__image')     # Картинка с кодом
    CAPT_RELOAD = (By.ID, 'rt-captcha__reload') # Кнопка получить код повторно
    CONTINUE = (By.ID, 'reset')
    TO_BACK = (By.ID, 'reset-back')
    MESS_ERROR1 = (By.ID, 'form-error-message') # 'Неверный логин или текст с картинки'
    MESS_ERROR2 = (By.CLASS_NAME, 'rt-input-container__meta--error')
    ZURUCK = (By.NAME, 'cancel_reset')  # Кнопка назад при восстанов. пароля
    PASS_NEW = (By.ID, 'password-new')
    PASS_CONF = (By.ID, 'password-confirm')
    SAFE_BUTTON = (By.ID, 't-btn-reset-pass')
    RADIO_EMAIL = (By.CSS_SELECTOR, '.rt-radio:nth-child(2) input')  # '.rt-radio-group [value="email"]'
    RADIO_SMS = (By.CSS_SELECTOR, '.rt-radio:nth-child(1) input')  # '.rt-radio-group [value="sms"]'
    NEXT2 = (By.CLASS_NAME, 'reset-choice-form__reset-btn')
    BACK2 = (By.CLASS_NAME, 'rt-btn--transparent')
    USER_LASTNAME = (By.CLASS_NAME, 'user-name__last-name')
    USER_FIRSTNAME = (By.CLASS_NAME, 'user-name__first-patronymic')


