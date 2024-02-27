# Домашнее задание к лекции 7. «Подготовка к собеседованию»
# Задание 3

import email  # библиотека позволяет работать с сообщениями электронной почты как с отдельными объектами
import smtplib  # библиотека для отправки письма по электронной почте
import imaplib  # Клиент протокола IMAP4

# Пакет содержит также подклассы, описывающие различные MIME-типы. Для работы понадобятся 2 из них — MIMEMultipart и MIMEText
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


GMAIL_SMTP = "smtp.gmail.com"  # это сервер исходящей почты. Он проверяет корректность настроек, содержимое письма, доставляет его по заданному адресу, а также выдаёт подтверждение доставки или уведомляет об ошибках.
YAMAIL_IMAP = "imap.yandex.ru"  # IMAP (Internet Message Access Protocol) – это протокол электронной почты, который позволяет пользователям получать доступ к своим почтовым ящикам и управлять ими


class MailWork:
    
    def __init__(self, s_adr_from, s_adr_from_pswd, l_adr_to, s_text_subj, s_text_msg, s_adr_rd_from, s_adr_rd_from_pswd, s_header=None) -> None:
        '''
        Процедура получения пароля для приложения. Актуальна для Googe Mail, Yandex Mail
        Для начала, нужно включить двухфакторную аутентификацию в аккаунте, с которого вы
        собираетесь отправлять письма. Это важно. После этого, в Chrome нажимаем на
        “Manage your Accounts” →Безопасность. Ищем блок “Вход в аккаунт” и нажимаем на “Пароли приложений”.
        В выпадашке “Приложение” выбираем “Другое”, вводим имя и, наконец, “Создать”.
        В появившемся окне, на желтом фоне будет пароль.
        '''
        # Формирование переменных
        self.s_adr_from = s_adr_from  # почта, с которой будет производится отправка писем
        self.s_adr_from_pswd = s_adr_from_pswd  # Для получения пароля смотри описание выше
        
        self.s_adr_rd_from = s_adr_rd_from # почта, с которой будем читать писма
        self.s_adr_rd_from_pswd = s_adr_rd_from_pswd  # пароль для почты чтения писем
        
        self.l_adr_to = l_adr_to   # Адрес или список адресов куда шлём сообщения
        self.s_text_subj = s_text_subj  # Тема письма, желательна чтобы не ушло в папку спам почты
        self.s_text_msg = s_text_msg  # Текст письма
        self.s_header = s_header  # Заголовок по которому будем искать письма
        
    def send_msg(self) -> None:
        
        # Создание сообщения
        cl_msg = MIMEMultipart()  # Создаём экземпляр класса для формирования письма
        
        # Заполняем форму письма
        cl_msg['From'] = self.s_adr_from  # От кого
        cl_msg['To'] = ', '.join(self.l_adr_to)  # Кому, если нужно сделать несколько адресатов, то цикл не нужен, используем ', '.join()
        cl_msg['Subject'] = self.s_text_subj  # Тема письма
        cl_msg.attach(MIMEText(self.s_text_msg, 'plain', 'utf-8'))  # Добавляем в сообщение текст

        # Создаем объект SMTP
        cl_msg_server = smtplib.SMTP(GMAIL_SMTP, 587)

        cl_msg_server.ehlo()  # identify ourselves to smtp gmail client
        cl_msg_server.starttls()  # Начинаем шифрованный обмен по TLS
        cl_msg_server.ehlo()  # re-identify ourselves as an encrypted connection

        cl_msg_server.login(self.s_adr_from, self.s_adr_from_pswd)  # Получаем доступ
        #cl_msg_server.sendmail(s_adr_from, cl_msg_server, cl_msg.as_string())  # Вариант 1, отправки письма
        cl_msg_server.send_message(cl_msg)  # Вариант 2, отправки письма

        cl_msg_server.quit()  # Закрываем отправку
        #send end

    def read_msg(self, ) -> None:
        '''
        Разрешить доступ к почтовому ящику с помощью почтовых клиентов для чтения(IMAP)
        Войдите в вашу Yandex почту.
        Нажмите кнопку в правом верхнем углу и выберите пункт Все настройки.
        Выберите пункт Почтовые программы.
        Установите флаг С сервера imap.yandex.ru по протоколу IMAP.
        Выберите тип подключения: ...
        Нажмите кнопку Сохранить изменения.
        '''
        # Соединение и аутентификация 
        cl_mail_rd = imaplib.IMAP4_SSL(YAMAIL_IMAP, 993)  # Класс протокола соединения с почтой для чтения
        cl_mail_rd.login(self.s_adr_rd_from, self.s_adr_rd_from_pswd)
        
        # Получение писем
        #cl_mail_rd.list()
        cl_mail_rd.select('inbox')  # Письма по умолчанию лежат в папке: 'inbox'
        
        criterion = '(HEADER Subject "%s")' % self.s_header if self.s_header else 'ALL'  # Критерий поиска писем, если не задать, то выведет все письма
        
        # Получаем кортеж по критерию, вид кортежа: ('OK', [b'14 24 28']) писма в списке по порядку номеров 14 - первое полученное
        # UID, неизменяемый номер писем, получаем его, так как обычным способом номера писем, при удалении смещаются
        result, t_data = cl_mail_rd.uid('search', None, criterion)  
        
        # Проверка есть ли писма в почтовом ящике
        assert t_data[0], 'There are no letters with current header'
        
        # Получаем последнее пришедшее письмо [-1], [0] - первое письмо в почте(старое)
        latest_email_uid = t_data[0].split()[-1]
        result, t_data = cl_mail_rd.uid('fetch', latest_email_uid, '(RFC822)')  # Зная номер письма теперь его можно наконец-то получить
        
        '''
        result = OK - статус операции
        data = кортеж байтов, в первом будет содержаться порядковый номер, стандарт и ещё какое-то число.
               Во втором слоте кортежа, будет наш будущий объект email
        '''
        
        raw_email = t_data[0][1]
        email_message = email.message_from_bytes(raw_email)  # Извлекаем письмо при помощи метода message_from_bytes библиотеки email
        print(email_message)
        cl_mail_rd.logout()
        #end recieve


if __name__=='__main__':
    
    # Данные хардкодера
    # s_adr_from = 'login@gmail.com'  # почта, с которой будет производится отправка
    # s_adr_from_pswd = 'qwerty'  # Для получения пароля смотри описание выше
    # s_adr_rd_from = 'login@gmail.com'  # почта, с которой будем читать писма
    # s_adr_rd_from_pswd = 'qwerty'  # пароль для почты чтения писем
    
    # l_adr_to = ['vasya@email.com', 'petya@email.com']  # Адрес или список адресов куда шлём сообщения

    # s_text_subj = 'Subject'  # Тема письма, желательна чтобы не ушло в папку спам почты
    # s_text_msg = 'Message'  # Текст письма
    
    # Проба пера на своей почте
    s_adr_from = 'brutaltruth87@gmail.com'  # почта, с которой будет производится отправка
    s_adr_from_pswd = '**PASSWORD**'  # Для получения пароля смотри описание выше
    s_adr_rd_from = 'snapalm@yandex.ru'  # почта, с которой будем читать писма
    s_adr_rd_from_pswd = '**PASSWORD**'  # пароль для почты чтения писем
    
    l_adr_to = ['snapalm@ya.ru']  # Адрес или список адресов куда шлём сообщения

    s_text_subj = 'Subject'  # Тема письма, желательна чтобы не ушло в папку спам почты
    s_text_msg = 'Message'  # Текст письма
    
    ml_wrk = MailWork(s_adr_from=s_adr_from,
                      s_adr_from_pswd=s_adr_from_pswd,
                      l_adr_to=l_adr_to,
                      s_text_subj=s_text_subj,
                      s_text_msg=s_text_msg,
                      s_adr_rd_from=s_adr_rd_from,
                      s_adr_rd_from_pswd=s_adr_rd_from_pswd
                      #s_header='UNSEEN'
                      )

    #ml_wrk.send_msg()
    ml_wrk.read_msg()
    












