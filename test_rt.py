# python -m pytest -v --driver Chrome --driver-path chromedriver.exe tests/test_rt.py


from time import sleep
from base_data import *
from settings import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Сохраняем скриншот общей формы авторизации на сайте
def test_vision(selenium):
    form = AuthForm(selenium)
    form.driver.save_screenshot('screenshot_001.jpg')


# Проверяем, что по умолчанию выбрана форма авторизации по номеру телефона
def test_by_phone(selenium):
    form = AuthForm(selenium)

    assert form.placeholder.text == 'Мобильный телефон'


# Проверяем автосмену "таб ввода"
def test_change_placeholder(selenium):
    form = AuthForm(selenium)

    # вводим номер телефона
    form.username.send_keys('+79123456789')
    form.password.send_keys('_')
    sleep(10)

    assert form.placeholder.text == 'Мобильный телефон'

    # очищаем поля логина
    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)

    # вводим электронную почту
    form.username.send_keys('skill@gmail.ru')
    form.password.send_keys('_')
    sleep(10)

    assert form.placeholder.text == 'Электронная почта'

    # очищаем поля логина
    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)

    # вводим логин
    form.username.send_keys('MyLogin')
    form.password.send_keys('_')
    sleep(10)

    assert form.placeholder.text == 'Логин'


# Позитивный сценарий авторизации по номеру телефона
def test_positive_by_phone(selenium):
    form = AuthForm(selenium)

    # вводим номер телефон
    form.username.send_keys(valid_phone)
    form.password.send_keys(valid_pass)
    sleep(10)
    form.btn_click()

    assert form.get_current_url() == '/account_b2c/page'


# Негативный сценарий авторизации по номеру телефона
def test_negative_by_phone(selenium):
    form = AuthForm(selenium)

    # вводим номер телефона
    form.username.send_keys('+77777777777')
    form.password.send_keys('12345678Ll')
    sleep(10)
    form.btn_click()

    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


# Позитивный сценарий авторизации по электронной почте
def test_positive_by_email(selenium):
    form = AuthForm(selenium)

    # вводим почту
    form.username.send_keys(valid_email)
    form.password.send_keys(valid_pass)
    sleep(10)
    form.btn_click()

    assert form.get_current_url() == '/account_b2c/page'


# Негативный сценарий авторизации по почте
def test_negative_by_email(selenium):
    form = AuthForm(selenium)

    # вводим почту
    form.username.send_keys('skill@ya.com')
    form.password.send_keys('1234567Ll')
    sleep(10)
    form.btn_click()

    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


# Проверяем получение временного кода на телефон и открытие формы для ввода кода
def test_get_code(selenium):
    form = CodeForm(selenium)

    # вводим номер телефона
    form.address.send_keys(valid_phone)

    # длительная пауза предназначена для ручного ввода капчи при необходимости
    sleep(40)
    form.get_click()

    rt_code = form.driver.find_element(By.ID, 'rt-code-0')

    assert rt_code


# Проверяем переход в форму восстановления пароля и её открытия
def test_forgot_pass(selenium):
    form = AuthForm(selenium)

    # кликаем по надписи "Забыл пароль"
    form.forgot.click()
    sleep(10)

    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')

    assert reset_pass.text == 'Восстановление пароля'


# Проверяем переход в форму регистрации и её открытие
def test_register(selenium):
    form = AuthForm(selenium)

    # кликаем по надписи "Зарегистрироваться"
    form.register.click()
    sleep(10)

    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')

    assert reset_pass.text == 'Регистрация'


# Проверяяем открытие пользовательского соглашения
def test_agreement(selenium):
    form = AuthForm(selenium)

    original_window = form.driver.current_window_handle
    # кликаем по надписи "Пользовательским соглашением" в подвале страницы
    form.agree.click()
    sleep(10)
    WebDriverWait(form.driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in form.driver.window_handles:
        if window_handle != original_window:
            form.driver.switch_to.window(window_handle)
            break
    win_title = form.driver.execute_script("return window.document.title")

    assert win_title == 'User agreement'


# Проверяем переход по ссылке авторизации пользователя через "ВКонтакте"
def test_auth_vk(selenium):
    form = AuthForm(selenium)
    form.vk_btn.click()
    sleep(10)

    assert form.get_base_url() == 'oauth.vk.com'


# Проверяем переход по ссылке авторизации пользователя через "Одноклассники"
def test_auth_ok(selenium):
    form = AuthForm(selenium)
    form.ok_btn.click()
    sleep(10)

    assert form.get_base_url() == 'connect.ok.ru'


# Проверяем переход по ссылке авторизации пользователя через "mail.ru"
def test_auth_mailru(selenium):
    form = AuthForm(selenium)
    form.mailru_btn.click()
    sleep(10)

    assert form.get_base_url() == 'connect.mail.ru'


# Проверяем переход по ссылке авторизации пользователя через "Google"
def test_auth_google(selenium):
    form = AuthForm(selenium)
    form.google_btn.click()
    sleep(10)

    assert form.get_base_url() == 'accounts.google.com'


# Проверяем переход по ссылке авторизации пользователя через "Yandex"
def test_auth_ya(selenium):
    form = AuthForm(selenium)
    form.ya_btn.click()
    sleep(10)

    assert form.get_base_url() != 'passport.yandex.ru'