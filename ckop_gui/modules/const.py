import string
import random

letters_and_numbers = string.ascii_uppercase + string.ascii_lowercase + '1234567890'

# schoolSubjects2 = ["", "Math", "Physics", "Computer Science", "Russian"]

# laboratories2 = ["Not", "Electricity and magnetism", "Prototyping", "Mechanics and strength", "Thermal phenomena and molecular structures",
# "Microelectronics and circuit engineering", "Autonomous avionics", "Robotics", "Programming", "Mathematical modeling and analysis", "Astronomy and Aerospace Systems"]


# schoolSubjects = ["", "Математика", "Физика", "Информатика", "Русский язык"]
schoolSubjects = {0: 'Математика', 1: 'Физика', 2: 'Информатика', 3: 'Русский язык', 4: 'Астрономия', 5:'Физкультура', 6: 'Музыка'}
schoolSubjects2 = ['Математика', 'Физика', 'Информатика', 'Русский язык', 'Астрономия', 'Физкультура', 'Музыка']

# laboratories = ["Not", "Электричества и магнетизма", "Макетирования", "Механики и прочности", "Тепловых явлений и молекулярных структур",
# "Микроэлектроники и схемотехники", "Автономной авионики", "Робототехники", "Программирования", "Математического моделирования и анализа", "Астрономии и аэрокосмических систем"]

# laboratories = {i: name for i, name in zip([0, 1, 2, 3, 4, 5, 6], laboratories)}
# print(laboratories)

laboratories = {0: 'Not', 100:'Программирования', 101: 'Электричества и магнетизма', 102: 'Макетирования', 103: 'Механики и прочности', 104: 'Тепловых явлений и молекулярных структур', 105: 'Микроэлектроники и схемотехники', 106: 'Автономной авионики'}
laboratories2 = ["Not", "Программирования", "Электричества и магнетизма", "Макетирования", "Механики и прочности", "Тепловых явлений и молекулярных структур","Микроэлектроники и схемотехники", "Автономной авионики"]
alf = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ"
num = "0123456789"

tokens_str = "".join(random.choices(letters_and_numbers, k=10))

event_message = {
    "ERROR: short text" : "Слишком короткий текст",
    "ERROR: long text" : "Слишком длинный текст",
    "ERROR: you don't have an active project": "У Вас уже нет активного проекта",
    "ERROR: wrong number laboratory":"Неверная лаборатория",
    "ERROR: too long name project":"Слишком длинное имя проекта",
    "ERROR: short name project":"Слишком короткое имя проекта",
    "ERROR: address occupied":"Адрес уже есть в системе",
    "ERROR: login occupied":"Логин занят",
    "ERROR: empty password or login": "Пустой логин или пароль",
    "ERROR: only teacher":"Может выполнить только учитель",
    "ERROR: Not your project":"Это не Ваш проект",
    "Not your project":"Это не Ваш проект",
    "Teacher successfully registered":"Вы уже зарегистрированы",
    "ERROR: error data":"Ошибка в данных",
    "ERROR: wrong address":"Неверный адрес",
    "Address generated": "Адрес создан успешно",
    "ERROR: address already using":"Адрес уже используется",
    "Create project":"Проект созда",
    "ERROR: error create project":"Ошибка при создании проекта",
    "Already in the project": "Уже в проекте",
    "Project is full":"В проекте много учеников",
    "Add in project":"Ученик добавлен в проект",
    "ERROR: this address not belong student":"Это не студент",
    "Task change":"Задача изменена",
    "Task is ready":"Задача выполнена",
    "Delete out project":"Удален из проекта",
    "Not in project":"Ученик не в проекте",
    "Change goal":"Цель изменена",
    "Successfully change role":"Роль успешно изменена",
    "Response created":"Ответ на предложение отправлен",
    "Not your request": "Это запрос не к Вам",
    "ERROR: error status":"Ошибка в статусе",
    "Status change":"Статус проекта изменен",
    "ERROR: only student":"Может выполнить только ученик",
    "Student successfully registered":"Ученик успешно зарегистрирован",
    "ERROR: email occupied":"e-mail занят",
    "ERROR: wrong class":"Неверный класс",
    "Project create":"Проект создан",
    "ERROR: teacher not exist":"Учитель не доступен",
    "ERROR: you already have active project":"У Вас уже есть активный проект",
    "Request created":"Запрос создан",
    "Request has already been created":"Запрос уже был создан",
    "Change strong side":"Сильная сторона изменена",
    "ERROR: wrong number strong side":"Неверный номер сильной стороны",
    "Add task":"Задача добавлена",
    "ERROR: too much tasks":"Слишком много задач",
    "Change task": "Задача изменена",
    "ERROR: wrong number task":"Неверный номер задачи",
    

}



