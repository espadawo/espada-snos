import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import random

senders = {
    "mail": "IMAP application password" #тут вводите свои почты в формате "почта" "пароль IMAP" / enter your emails in the format "email" "IMAP password"
}

receivers = ["sms@telegram.org", "dmca@telegram.org", "abuse@telegram.org", "sticker@telegram.org", "support@telegram.org", "stopCA@telegram.org"] #получатели письма / email receivers 

def get_smtp_config(email):
    """Определяем SMTP-сервер в зависимости от домена почты""" #smpt server definition
    if "@yandex." in email:
        return {
            'host': 'smtp.yandex.ru',
            'port': 465,
            'ssl': True,
            'starttls': False
        }
    elif "@mail.ru" in email:
        return {
            'host': 'smtp.mail.ru',
            'port': 465,
            'ssl': True,
            'starttls': False
        }

    else:
        raise ValueError("Неизвестный почтовый сервис")

def logo():
    print("""
▓█████   ██████  ██▓███   ▄▄▄      ▓█████▄  ▄▄▄      
▓█   ▀ ▒██    ▒ ▓██░  ██▒▒████▄    ▒██▀ ██▌▒████▄    
▒███   ░ ▓██▄   ▓██░ ██▓▒▒██  ▀█▄  ░██   █▌▒██  ▀█▄  
▒▓█  ▄   ▒   ██▒▒██▄█▓▒ ▒░██▄▄▄▄██ ░▓█▄   ▌░██▄▄▄▄██ 
░▒████▒▒██████▒▒▒██▒ ░  ░ ▓█   ▓██▒░▒████▓  ▓█   ▓██▒
░░ ▒░ ░▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░ ▒▒   ▓▒█░ ▒▒▓  ▒  ▒▒   ▓▒█░
 ░ ░  ░░ ░▒  ░ ░░▒ ░       ▒   ▒▒ ░ ░ ▒  ▒   ▒   ▒▒ ░
   ░   ░  ░  ░  ░░         ░   ▒    ░ ░  ░   ░   ▒   
   ░  ░      ░                 ░  ░   ░          ░  ░
""")


def send_email(receiver, sender_email, sender_password, subject, body):
    try:

        smtp_config = get_smtp_config(sender_email) #настройки smpt для почты / smpt settings for mail

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        if smtp_config['ssl']:  #подключение к smpt серверу, а также включаем шифрование / connect to the smpt server and enable encryption
            server = smtplib.SMTP_SSL(host=smtp_config['host'], port=smtp_config['port'])
        else:
            server = smtplib.SMTP(host=smtp_config['host'], port=smtp_config['port'])
            if smtp_config['starttls']:
                server.starttls()

        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver, msg.as_string())
        time.sleep(3) #пауза после отправки / pause after sending
        server.quit()
        return True
    except Exception as e:
        print(f"Ошибка при отправке письма с {sender_email}: {e}")
        return False

def print_menu():
    
    account_email_subjects = [  #список тем указанное в письме / the list of topics specified in the email
        "Важное уведомление о нарушении",
        "Сообщение о проблемном аккаунте",
        "Жалоба на пользователя Telegram",
        "Сообщение о нарушении правил"
    ]

    channel_email_subjects = [
        "Срочное сообщение о нарушении в канале",
        "Нарушение правил платформы в канале",
        "Требуется срочная модерация канала"
    ]
    
    while True:
        logo()
        sent_email = 0
        print("\nМеню")
        print("1. Снос аккаунта.")
        print("2. Снос канала.")
        print("3. Информация о софте.")
        print("4. Инструкиця по использованию софта (Обязательно к прочтению).")
        print("5. Выход.")
        
        snosCh = input("Ваш выбор: ")
        
        if snosCh == "1":
            print("\nВыберите тип жалобы:")
            print("1.1 Обычный.")
            print("1.2 Снос сессий.")
            print("1.3 Виртуальный номер.")
            complaint_choice = input("Ваш выбор: ")
           
            if complaint_choice == "1.1":
                print("\nВведите причину, юзернейм, telegram id, затем ссылки на канал/чат и на нарушение")
                reason = input("Причина: ")
                username = input("Юз: ")
                telegegram_ID = input("Телеграм ID: ")
                chat_link = input("Ссылка на чат: ")
                violation_chat_link = input("Ссылка на нарушение: ")

                complaint_texts = {
                    "1.1": f"Здравствуйте, используя месенджер телеграм я нашел аккаунт который нарушает правила данной социальной сети, а именно {reason}. Его юзернейм - {username}, его id - {telegegram_ID}. Вот ссылка на чат с нарушением - {chat_link}, также предоставляю ссылку на само сообщение содержащее нарушение - {violation_chat_link}. Прошу вас проверить данного пользователя на наличие нарушений, спасибо за понимание."
                }

                for sender_email, sender_password in senders.items():   #отправка писем со всех почт на почту получателя / sending emails from all mailboxes to the recipient's mailbox
                    for receiver_email in receivers:
                        complaint_text = complaint_texts[complaint_choice]
                        complaint_body = complaint_text.format(
                            reason=reason.strip(),
                            username=username.strip(),
                            telegegram_ID=telegegram_ID.strip(),
                            chat_link=chat_link.strip(),
                            violation_chat_link=violation_chat_link.strip()
                        )
                        
                        email_subject = random.choice(account_email_subjects)
                        if send_email(receiver_email, sender_email, sender_password, email_subject, complaint_body):
                            print(f"\nОтправлено на {receiver_email} от {sender_email} (Тема: {email_subject})")
                            sent_email += 1
                            delay = random.randint(5, 10)
                            for i in range(delay, 0, -1):
                                print(f"\rОжидание: {i//60} мин {i%60} сек ", end='')
                                time.sleep(1)
                            print("\r" + " " * 30, end='')  
                        
            elif complaint_choice in ["1.2", "1.3"]:
                account_username = input("Юзернейм: ")
                Telegram_account_ID = input("Telegram ID: ")
                violation_chat_link = input("Ссылка на нарушение: ")

                complaint_texts = {
                    "1.2": f"Здравствуйте, помогите пожалуйста, я попался на фишинговую ссылку, после чего мой телеграм аккаунт был взломан, на аккаунте теперь установлен облачный пароль который я не устанавливал когда аккаунтом владел я, из-за этого я не могу зайти на свой аккаунт. Мой юзернейм - {account_username}, мой id в случае смены юзернейма злоумышлеником - {Telegram_account_ID}. Пожалуйста, сбросьте сессии аккаунта или удалите его, мне очень важны данные которые хранятся на этом аккаунте и мне не хотелось бы чтоб личные переписки попали в руки злоумышленику.",
                    "1.3": f"Здравствуйте, данный пользователь - {account_username}, использует виртуальный номер для рекламной спам рассылки, а также угрозы другим пользователям, вот ссылка на сообщение с нарушением - {violation_chat_link}."
                }

                for sender_email, sender_password in senders.items():
                    for receiver_email in receivers:
                        complaint_text = complaint_texts[complaint_choice]
                        complaint_body = complaint_text.format(
                            account_username=account_username.strip(),
                            Telegram_account_ID=Telegram_account_ID.strip(),
                            violation_chat_link=violation_chat_link.strip()
                        )
                        
                        email_subject = random.choice(account_email_subjects)
                        if send_email(receiver_email, sender_email, sender_password, email_subject, complaint_body):
                            print(f"\nОтправлено на {receiver_email} от {sender_email} (Тема: {email_subject})")
                            sent_email += 1
                            delay = random.randint(5, 10)
                            for i in range(delay, 0, -1):
                                print(f"\rОжидание: {i//60} мин {i%60} сек ", end='')
                                time.sleep(1)
                            print("\r" + " " * 30, end='')  
                        
        elif snosCh == "2":
            print("\nВыберите тип жалобы:")
            print("8. Личные данные.")
            print("9. Прайс листы по продаже услуг деанона и тд.")
            print("10. Детское порно")
            print("11. Расчлененка.")
            print("12. Живодерство.")
            print("13. Накрут просмотров.")
            print("14. Накрута подписчиков.")
            complaint_choice = input("Выбор: ")
            
            if complaint_choice == "8":
                print("\nВведите ссылку на канал, после на нарушение")
                channel_link = input("Ссылка на канал: ")
                violation_chat_link = input("Ссылка на нарушение: ")
                
                complaint_texts = {
                    "8": f"Здравствуйте, на вашей платформе я нашел канал который распостраняет личные данные невинных людей, вполне возможно что владелец данного канала угрожал данным людям в личные сообщения, так как юзернейма владельца канала у меня нет, прикрепляю только ссылку на канал, а также ссылку на сообщение с личными данными. Ссылка на канал - {channel_link}, ссылка на нарушение - {violation_chat_link}"
                }
                
                for sender_email, sender_password in senders.items():
                    for receiver_email in receivers:
                        complaint_text = complaint_texts[complaint_choice]
                        complaint_body = complaint_text.format(
                            channel_link=channel_link.strip(),
                            violation_chat_link=violation_chat_link.strip()
                        )
                        
                        email_subject = random.choice(channel_email_subjects)
                        if send_email(receiver_email, sender_email, sender_password, email_subject, complaint_body):
                            print(f"\nОтправлено на {receiver_email} от {sender_email} (Тема: {email_subject})")
                            sent_email += 1
                            delay = random.randint(5, 10)
                            for i in range(delay, 0, -1):
                                print(f"\rОжидание: {i//60} мин {i%60} сек ", end='')
                                time.sleep(1)
                            print("\r" + " " * 30, end='')  
            
            elif complaint_choice in ["9", "10", "11", "12", "13", "14"]:
                channel_link = input("Ссылка на канал: ")
                violation_chat_link = input("Ссылка на нарушение: ")
                manysub = input("Количество подписчиков:")
                manyviews = input("Колечество просмотров (вводить от минимального к максимальному, если не понял в каком плане, смотри инструкцию в начальном меню под пунктом 4):")
                
                complaint_texts = {
                    "9": f"Приветствую, прошу вас обратить внимание на канал который продает услуги доксинга, деанона и тому подобное на вашей платформе, данные действия нарушают УК РФ ст. 137 - нарушение неприкосновенности частной жизни. Прикрепляю ссылку на канал, а также ссылку на нарушение. Ссылка на канал - {channel_link}, ссылка на нарушение - {violation_chat_link}",
                    "10": f"Здравствуйте, хочу обратить ваше внимание на канал который занимается распространением детской порнографии. Лично мне не хотелось бы, чтоб мои дети, или любой другой пользователь с неустойчивой психикой попались на данный канал, просьба заблокировать данный канал - {channel_link}. Ссылки на запрещенный контент - {violation_chat_link}",
                    "11": f"Добрый день, пожалуйста удалите данный канал - {channel_link}, в этом канале находится контент с фотографиями и видео шокирующего характера, а именно раслечение и убийство людей. Ссылки на нарушения - {violation_chat_link}. Еще раз прошу вас заблокировать данный канал, чтоб людям которые из интереса решили зайти и посмотреть что в канале, не стало плохо от такого контента. Спасибо за понимание и содействие.",
                    "12": f"Прошу обратить внимание на то, что в вашей сети был создан канал, который нарушает правила телеграм, а также УК РФ ст. 245 - жестокое обращение с животными в целях причинения им боли и/или страданий. В этом канале - {channel_link} находятся видео, а также фото с жестоким обращением с животными, если говорить конкретнее, то избиение животных, убийство, пытки животного. Ссылки на нарушения - {violation_chat_link}",
                    "13": f"Доброй ночи, нашел канал который использовал накрутку просмотров и возможно реакций, просьба заблокировать данный канал так как он нарушает правила платформы. Предоставляю ссылку на канал - {channel_link}, а также ссылку на сообщение с накручеными просмотрами - {violation_chat_link}",
                    "14": f"Доброй ночи, на просторах вашей платформы, нашел канал в котором использьзовалась накрута подписчиков, ибо в канале {manysub}, а просмотров {manyviews} просьба проверить данный канал и в случае нарушения принять меры. Ссыдка на канал - {channel_link}, ссылки на посты с минимальным количеством просмотров и максмальных - {violation_chat_link}"
                }
                
                for sender_email, sender_password in senders.items():
                    for receiver_email in receivers:
                        complaint_text = complaint_texts[complaint_choice]
                        complaint_body = complaint_text.format(
                            channel_link=channel_link.strip(),
                            violation_chat_link=violation_chat_link.strip()
                        )
                        
                        email_subject = random.choice(channel_email_subjects)
                        if send_email(receiver_email, sender_email, sender_password, email_subject, complaint_body):
                            print(f"\nОтправлено на {receiver_email} от {sender_email} (Тема: {email_subject})")
                            sent_email += 1
                            delay = random.randint(5, 10)
                            for i in range(delay, 0, -1):
                                print(f"\rОжидание: {i//60} мин {i%60} сек ", end='')
                                time.sleep(1)
                            print("\r" + " " * 30, end='')   
        
        elif snosCh == "3":
            print("\n=== Информация о софте ===")
            print("Создатель софта: espada.")
            print("Связь с создателем в тг / предложить свои идеи для добавления в софт: @espadawo.")
            print("Создатель софта не отвечает и не несет последствия за ваши действия, данный софт был сделан в развлекательных целях, а также для закрепления знаний программирования.")
            input("\nНажмите Enter чтобы вернуться в меню...")

        elif snosCh == "4":
            print("\n=== Инстуркция по использованию софта ===")
            print("Привет, данная инстуркция поможет тебе правильно использовать софт, чтоб текст жалоб был логичным...")
            print("Снос происходит, через отправку жалоб на почту поддержки тг, снос аккаунта не гарантирован, так что не надо идти в лс создателя и дрочить ему сообщения о том, что софт хуйня и не сносит, насчет тг каналов, шансы почти 100%, за исключением каналов с накрутами, т.к там могут сначала тупо обнулить просмотры либо подписоту, а потом только уже удалят канал при повторном нарушении.")
            print("\n=== Немного подробнее про сносы каналов ===")
            print("ㅤ")
            print("Личные данные - к таким каналам относятся каналы с ворками доксеров, а также проекты где выставляют данные жертв. Из уважения к людям в км, не сносите просто так, если вас валиднули и скинули в проект либо ворк канал, то можете снести насчет проектов где дохуя подписчиков, не даю гарантии что снесет.")
            print("ㅤ")
            print("Прайс листы - думаю подробно объяснять не надо что это за каналы, опять же, просто так не сносите людям прайс листы для забавы, если у вас ворк по какому нибудь бичу и вы хотите не оставить от него следа, то можете нахуй сносить.")
            print("ㅤ")
            print("Детское порно - объяснять смысла нет что за каналы, при выборе этого пункта в меню сноса канала, прикрепляйте несколько сообщений на нарушние через запятую, например: ссылка на нарушение, ссылка на нарушение.")
            print("ㅤ")
            print("Расчлененка и живодерство - индентично с десткой порнухой.")
            print("ㅤ")
            print("Накрутка просмотров - в пункте `Ссылка на нарушение` указывайте ссылку на сообщение с наибольшем количеством проссмотров.")
            print("ㅤ")
            print("Накрутка подписчкиов - каналы у которых дохуя подписчкиков, при этом просмотры максимум до 1к доходят. Сразу отвечу на вопрос который у вас может возникнуть, с чего я думаю что это накрута подписчиков, если посмотреть другие каналы, где дохуя подписчиков, количество просмотров примерно такое же, как и количество подписчиков. В пункте `Количество просмотров` указывайте от минимального количества, до максимального, пример: от n до n. В пункте `Ссылка на нарушение` указывайте ссылку на минимальной количество просмотров и на максимальное.")
            print("ㅤ")
            input("\nНажмите Enter чтобы вернуться в меню...")

        elif snosCh == "5":  
            print("\nЗавершение работы программы...")
            break  
        else:
            print("\nНеверный выбор! Пожалуйста, введите число от 1 до 5")
            time.sleep(1)

if __name__ == "__main__":
    print_menu()