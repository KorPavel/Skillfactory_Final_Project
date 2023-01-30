#  Итоговый проект по автоматизации тестирования
#### *Testing a new authorization interface in the personal account from the customer Rostelecom Information Technologies*

-----------------
### Объект тестирования: *[ЕЛК Web](https://b2c.passport.rt.ru)*
#### [Здесь](https://lms.skillfactory.ru/assets/courseware/v1/f78e146f0eb3ace247a28b07e66467de/asset-v1:Skillfactory+QAP+18JUNE2020+type@asset+block/%D0%A2%D1%80%D0%B5%D0%B1%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F_SSO_%D0%B4%D0%BB%D1%8F_%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F_last.doc) представлены требования к проекту в файле (.doc)

#### Для тестирования сайта были использованы:
- ручное и автоматизированное тестирование
- позитивное и негативное тестирование (для проверки основного функционала интерфейса, а также выявления ошибок и проверки нестандартного поведения пользователя)
- нагрузочное тестирование (для проверки форм ввода данных и поведения системы на вводимые значения: пробелы, символы, иероглифы, слишком большое количество символов и т.п.)
- анализ граничных значений
- разбиение на классы эквивалентности (для тестирования полей ввода данных)
- тестирование состояний и переходов
- применялось кросс-брузерное тестирование (Google Chrome, Mozilla Firefox)

### [чек-лист | тест-кейсы | баг-репорт](https://docs.google.com/spreadsheets/d/1uK0ku4H61qHZAYwJI6w5TB_mHfZejBnzXnrLH2UobCg/edit?usp=sharing)

#### Окружение: 
- OC Windows 10 Version 21H2   
- Google Chrome  Версия 109.0.5414.75, (64 бита)  
- Firefox Browser Версия 100.0 (64 бита)   

---------------------
#### Тесты разбиты по группам: 
- `test_auth_page.py` - файл с тест-кейсами для страницы **авторизации**
- `test_registration_page.py` - файл с тест-кейсами для страницы **регистрации**
- `test_recovery_pass_page.py` - файл с тест-кейсами для страницы **восстановления пароля**

`conftest.py` - файл с фикстурами для подготовки браузеров и их запуска   
`settings.py` - файл с тестовыми данными  
В целях сокрытия конфиденциальной информации проекте используется файл `.env` (*не представлен*), для которого нужна библиотека "python-dotenv"
#### Пример содержания файла `.env`:
>valid_first_name = '`Сергей`'  
>valid_last_name = '`Собянин`'  
>valid_email = '`co6qnin@mail.ru`'  
>valid_phone = '`+77777777777`'  
>valid_login = '`rtkid_1234567890123`'  
>valid_password = '`Mep_C06qH1N`'  

Перед запуском тестов требуется установить необходимые библиотеки командой:
   ```bash
   pip install -r requirements.txt
   ```
Тесты подразделяются на позитивные и негативные.   Для запуска позитивных тестов через терминал следует набрать команду `-m positive`, к примеру:  
   ```bash
   pytest -v -s tests\test_auth_page.py -m positive
   ```
По умолчанию используется браузер Google Chrome. Чтобы запустить тесты в браузере Firefox следует добавить команду `--browser_name=firefox`:
   ```bash
   pytest -v -s tests\test_auth_page.py -m positive --browser_name=firefox
   ```
Для выбора режима тестирования без графического сопровождения добавляется команда `--headless=true`:  
   ```bash
   pytest -v -s tests\test_auth_page.py -m positive --headless=true
   ```
Для запуска какого-либо конкретного теста, следует указать путь до этого теста с разделителем "::", например:
   ```bash
   pytest -v -s tests\test_recovery_pass_page.py::TestRecoveryPassword::test_automatize_recovery_password
   ```
Внимание! В данном тесте код с картинки необходимо ввести самостоятельно.

