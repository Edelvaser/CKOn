import smtplib                                              # Импортируем библиотеку по работе с SMTP                       # Общий тип
from email.mime.text import MIMEText                        # Текст/HTML
from email.mime.multipart import MIMEMultipart              # Многокомпонентный объект
from modules.secret import *


def send_email(addr_to, text = ""):
    print(text)
    addr_from = login                         # Отправитель
    msg_subj = "Подтверждение регистрации"
    msg = MIMEMultipart()                                   # Создаем сообщение
    msg['From']    = addr_from                              # Адресат
    msg['To']      = addr_to                                # Получатель
    msg['Subject'] = msg_subj                               # Тема сообщения
    #msg_text = "Ваш электронный договор"
    body = text                                         # Текст сообщения
    msg.attach(MIMEText(body, 'plain'))                     # Добавляем в сообщение текст

    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(login, passw_app)
    mail.send_message(msg)
    mail.quit()
