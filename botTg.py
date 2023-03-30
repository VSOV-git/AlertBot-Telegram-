import telebot
import time
import datetime
import subprocess


def file_write(text, filename="logconf.txt", rej="w", encod="utf8") -> bool:
    # writing data in file
    try:
        with open(filename, mode=rej, encoding=encod) as file:
            # file.write(text)
            file.writelines(text)
            return True
    except OSError as m:
        print(m)
        return False


def file_read(filename: str, rej="r", encod="utf-8") -> list:
    # Read data from file
    try:
        with open(filename, rej, encoding=encod) as file:
            m = file.readlines()
            return m
    except FileNotFoundError:
        print(f'No such file or directory: {filename}')
        return []


def get_date() -> str:
    # Returned date
    my_date = datetime.date.today()
    return str(my_date)


def command_execution(command=""):
    # Func returned package from cmd
    result = subprocess.Popen(args=command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return result.stdout.readlines()


def command_execution_write(decode="cp866", command="") -> list:
    """
    Func() append all task process from cmd in array
    :param decode:
    :param command:
    :return:
    """
    Lbyte_arr = []
    for byte_line in command_execution(command):
        # decode 'cp866'
        line = byte_line.decode(decode).replace("\r", "")
        line_now = line.split(",")
        if line_now[0] not in blacklist:
            if len(line) > 3:
                Lbyte_arr.append(line)
            else:
                return Lbyte_arr

    return Lbyte_arr


def netstat(command="netstat"):
    """
    This Func take netstat from ur pc
    :param command: str command for CMD
    :return: List() with filtered values
    """
    com = (command_execution(command))[4:]
    m = []
    for b_line in com:
        line = " "
        b_line = b_line.decode('cp866')
        b_line = b_line.replace("\r","")
        b_line = b_line.replace("\n","")
        for i in b_line.split(" "):
            if len(i) > 2:
                line = line + " " + i
        m.append(line.split(" ")[2::])
    return m


def convert_type(lst: list) -> list:
    """
    This func() is not using in work
    Its test func() for debug
    :param lst:
    :return:
    """
    m = []
    for line in lst:
        if "\n" in line:
            line = line[:-1]
            m.append(f"{line}")
        else:
            m.append(f"{line}")
    return m


bot = telebot.TeleBot("5828330086:AAEYkzPskI5TTcb2yacFn165erjgeM6l21Q")
blacklist = file_read("blacklist.txt")
Lcheck_app = file_read(f"killApp.txt")
# check_app = convert_type(kill_app)
Btg_bot_send = True
Btask_cmd = True
Bcommand_wait_cmd = False
Bgot_True = None
Lpid_tasklist = []
language = "ru"
port = ["80"]
state = ["ESTABLISHED","TIME_WAIT"]
# 'json': {'message_id': 53512,
#     'from': {'id': 234241142,
#     'is_bot': False,
#     'first_name': 'IVAN',
#     'last_name': 'PETROV',
#     'username': 'ivanPetrov',
#     'language_code': 'eu'},
# 'chat': {'id': 234241142,
# 'first_name': 'IVAN',
# 'last_name': 'PETROV',
# 'username': 'ivanPetrov',
# 'type': 'private'},
# 'date': 12434253,
# 'text': '/start', '
# entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}}


def pid_inf(pid_id: str):
    process = command_execution_write('cp866', f'tasklist /FI "PID eq {pid_id}" /v /fo csv /nh')
    return process[0]


def pid_kill(pid_id: str):
    command_execution(f'taskkill /pid {pid_id}')


def get_proclist():
    Pid_list_out = set()
    Lpid_tasklist = command_execution_write('cp866', 'TASKLIST /FO CSV /NH /FI "IMAGENAME ne svchost.exe"')
    for line in Lpid_tasklist:
        lst = line.split(",")
        if lst[0] in Lcheck_app:
            Pid_list_out.add(lst[1])
    return Pid_list_out


@bot.message_handler(commands=['start'])
def send_message(message):
    """
    This function() is main
    Taking new tasklist from cmd and check take process which are in black_list
    And print them in Telegram chat
    :param message:
    :return: bot.send_message
    """
    global Btg_bot_send, Btask_cmd, Bcommand_wait_cmd, Lpid_tasklist
    # time_test = time.time()
    Btg_bot_send = True
    Btask_cmd = None
    Spid_procsess = set()
    Snetstat_proc = set()
    bot.send_message(message.chat.id, f">>Процесс сканирования запущен<<")
    while Btg_bot_send:
        while len(Spid_procsess) >= 1:
            for PID in Spid_procsess:
                PID = PID.replace('"', "")
                Stext_out_bot = str(pid_inf(PID))
                bot.send_message(message.chat.id, Stext_out_bot)
                # bot.send_message(message.chat.id, str(time.time() - time_test))
                time_in = time.time()
                time_out = 0
                while True:
                    time_out = time.time()
                    if not Btg_bot_send:
                        break
                    if (time_out - time_in) >= 15:
                        if Bcommand_wait_cmd:
                            pid_kill(PID)
                            bot.send_message(message.chat.id, "Процесс завершён! По причине бездействия!")
                            break
                        if not Bcommand_wait_cmd:
                            bot.send_message(message.chat.id, "Процесс пропущен! По причине бездействия!")
                            break
                    else:
                        if Bgot_True is True:
                            pid_kill(PID)
                            bot.send_message(message.chat.id, "Процесс завершён!")
                            break
                        if Bgot_True is False:
                            bot.send_message(message.chat.id, "Процесс пропущен!")
                            break
                        if not Btg_bot_send:
                            break
                time.sleep(2)
            Spid_procsess = set()

        else:
            Spid_procsess = get_proclist()
            # Lpid_tasklist = command_execution_write('cp866', 'TASKLIST /FO CSV /NH /FI "IMAGENAME ne svchost.exe"')
            # for line in Lpid_tasklist:
            #     lst = line.split(",")
            #     if lst[0] in Lcheck_app:
            #         Spid_procsess.add(lst[1])

    bot.send_message(message.chat.id, ">>end<<")


@bot.message_handler(commands=['stop'])
def send_message(message):
    global Btg_bot_send
    Btg_bot_send = False
    bot.send_message(message.chat.id, "Команда /stop выполнена\nДождитесь надписи >>end<<")


@bot.message_handler(commands=['help'])
def send_message(message):
    bot.send_message(message.chat.id, f'AlertBot-бот для отслеживания процессов на вашем ПК\n\n'
                                      f'Список команд бота\n'
                                      f'/help - выводит список команд\n\n'
                                      f'/start - начинает сканирование системы и работу программу\n\n'
                                      f'/stop - останавливает сканирование системы и работу программы\n\n'
                                      f'/yes - останавливает процесс на ПК\n\n'
                                      f'/no - пропускает процесс на ПК \n\n'
                                      f'/wait (yes/no) - какую команду выполнить при бездействии\n\n'
                                      f'/addproc (yes/no) - добавляет дополнительный процесс в файл поиска \n\n'
                                      f'/delproc (yes/no) - удаляет процесс из файла поиска  \n\n')


@bot.message_handler(commands=['wait'])
def send_message_in(message):
    global Bgot_True,Bcommand_wait_cmd
    bot.send_message(message.chat.id, f"Какую команду выполнить при длительном ожидании?\n\n"
                                      f"На данный момент активна команда /{Bcommand_wait_cmd}\n\n"
                                      f"Если хотите поменять, то напишите команду\n\n"
                                      f"/yes - чтобы процесс сам завершался при бездействии\n\n"
                                      f"/no - чтобы процесс не завершался при бездействии")
    time_in = time.time()
    time_out = 0
    while (time_out - time_in) <= 10:
        if Bgot_True is True:
            Bcommand_wait_cmd = True
            bot.send_message(message.chat.id, f"Вы поменяли команду ожидания на /{Bcommand_wait_cmd}")
            break
        if Bgot_True is False:
            Bcommand_wait_cmd = False
            bot.send_message(message.chat.id, f"Вы поменяли команду ожидания на /{Bcommand_wait_cmd}")
            break
    bot.send_message(message.chat.id, f">>quit<<\n >>{send_message_in.__name__}<<")


@bot.message_handler(commands=['yes'])
def send_message_yes(message):
    bot.send_message(message.chat.id, f'>>DONE<<')
    global Bgot_True
    Bgot_True = True
    time.sleep(1)
    Bgot_True = None


@bot.message_handler(commands=['no'])
def send_message_yes(message):
    bot.send_message(message.chat.id, f'>>DONE<<')
    global Bgot_True
    Bgot_True = False
    time.sleep(1)
    Bgot_True = None


@bot.message_handler(commands=['prproc'])
def send_message_del(message):
    Stext_out = ""
    for i in range(len(Lcheck_app)):
        Stext_out = Stext_out + f"index={i} {Lcheck_app[i]}\n"
    bot.send_message(message.chat.id, Stext_out)


@bot.message_handler(commands=['addproc'])
def send_message_del(message):
    try:
        global Bgot_True
        Stext_mes = message.text.split(" ")[1]
        bot.send_message(message.chat.id, f"Введите команды\n\n"
                                          f"/yes - для добавления процесса\n\n"
                                          f"/no - для завершения")
        time_out_func = 0
        time_in_func = time.time()
        while (time_out_func - time_in_func) <= 20:
            time_out_func = time.time()
            if Bgot_True is True:
                Lcheck_app.append(f'"{Stext_mes}.exe"')
                bot.send_message(message.chat.id, f'Процесс "{Stext_mes}.exe" добавлен')
                break
            if Bgot_True is False:
                bot.send_message(message.chat.id, "Вы завершили добавление")
                break
        bot.send_message(message.chat.id, f">>quit<<\n >>{send_message_del.__name__}<<")
    except Exception as error:
        if error.__class__.__name__ == "IndexError":
            bot.send_message(message.chat.id, f">>IndexError: {str(error)}<<")
            bot.send_message(message.chat.id, ">>Нельзя добавить пустоту<<")
        else:
            bot.send_message(message.chat.id, str(error))


@bot.message_handler(commands=['delproc'])
def send_message_add(message):
    try:
        global Bgot_True
        Stext_mes = message.text.split(" ")[1]
        bot.send_message(message.chat.id, str(Lcheck_app[int(Stext_mes)]))
        bot.send_message(message.chat.id, f"Введите команды\n\n"
                                          f"/yes - для удаления процесса\n\n"
                                          f"/no - для завершения")
        time_out_func = 0
        time_in_func = time.time()
        while (time_out_func - time_in_func) <= 20:
            time_out_func = time.time()
            if Bgot_True is True:
                bot.send_message(message.chat.id, f"Процесс {Lcheck_app[int(Stext_mes)]} удален")
                Lcheck_app.pop(int(Stext_mes))
                break
            if Bgot_True is False:
                bot.send_message(message.chat.id, "Вы завершили удаление")
                break
        bot.send_message(message.chat.id, f">>quit<<\n >>{send_message_add.__name__}<<")
    except Exception as error:
        if error.__class__.__name__ == "IndexError":
            bot.send_message(message.chat.id, f">>IndexError: {str(error)}<<")
            bot.send_message(message.chat.id, ">>Процесса с таким индексом нет<<")
        else:
            bot.send_message(message.chat.id, f"{error.__class__.__name__}: {str(error)}")

#add a ful support
@bot.message_handler(commands=['language'])
def send_message_leng(message):
    global language
    time_in = time.time()
    if language == "ru":
        bot.send_message(message.chat.id, "Send /yes, if u want change a language to English"
                                          "\n\n Send /no to continue")
    elif language == "eu":
        bot.send_message(message.chat.id, "Отправьте /yes, если хотите поменять язык на Русский"
                                          "\n\n Отпавьте /no для продолжения")
    while time.time() - time_in <= 10:
        if Bgot_True is True:
            if language == "ru":
                language = "eu"
                bot.send_message(message.chat.id, f"Language changed to {language}")
                break
            if language == "eu":
                language = "ru"
                bot.send_message(message.chat.id, f"Язык поменян на  {language}")
                break
        if Bgot_True is False:
            break
    bot.send_message(message.chat.id, f">>{send_message_leng.__name__}<<")


bot.polling()
