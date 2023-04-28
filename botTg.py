import telebot
import time
import datetime
import subprocess
from typing import Any
# dict
dict_start = {
    "start": {"ru": ">>Процесс сканирования запущен<<",
              "en": ">>Scanning system<<"
              },
    "while": {
        "yes": {
            "ru": "Процесс завершён!",
            "en": "Process terminate"
        },
        "no": {
            "ru": "Процесс пропущен!",
            "en": "Process skipped"
        }
    },
    "wait": {
        "yes": {
            "ru": "Процесс завершён! По причине бездействия!",
            "en": "Process terminate while inaction"
        },
        "no": {
            "ru": "Процесс пропущен! По причине бездействия!",
            "en": "Process skipped while inaction"
        }
    }
}
dict_stop = {
    "ru": "Команда /stop выполнена\nДождитесь надписи >>end<<",
    "en": "Command /stop complete\nWait message >>end<<"
}
dict_help = {
    "ru": 'AlertBot-бот для отслеживания процессов на вашем ПК\n'
          'Список команд бота\n\n'
          '/help - выводит список команд\n\n'
          '/start - начинает сканирование системы и работу программу\n\n'
          '/stop - останавливает сканирование системы и работу программы\n\n'
          '/yes - останавливает процесс на ПК\n\n'
          '/no - пропускает процесс на ПК \n\n'
          '/wait (yes/no) - какую команду выполнить при бездействии\n\n'
          '/addproc (yes/no) - добавляет дополнительный процесс в файл поиска \n\n'
          '/delproc (yes/no) - удаляет процесс из файла поиска  \n\n'
          '/prproc - вывести все процессы из файла killApp.txt\n\n'
          '/language - поменять язык "ru" или "en""\n\n',

    "en": 'AlertBot is a bot to monitor processes on your PC\n'
          'List of bot commands\n\n'
          '/help - displays a list of commands\n\n'
          '/start - starts scanning the system and running the program\n\n'
          '/stop - Stops system scan and program\n\n'
          '/yes - Stop process on PC\n\n'
          '/no - skip process on PC\n\n'
          '/wait (yes/no) - what command to execute when idle\n\n'
          '/addproc (yes/no) - Adds an extra process to the search file\n\n'
          '/delproc (yes/no) - remove process from search file\n\n'
          '/prproc - print process in killApp.txt file\n\n'
          '/language - change language "ru" or "en"\n\n'

}
dict_wait = {
    "start": {
        "ru": "Какую команду выполнить при длительном ожидании?\n\n"
              "На данный момент активна команда /{}\n\n"
              "Если хотите поменять, то напишите команду\n\n"
              "/yes - чтобы процесс сам завершался при бездействии\n\n"
              "/no - чтобы процесс не завершался при бездействии",

        "en": "What command to execute when waiting for a long time?\n\n"
              "At that moment it's /{}\n\n"
              "If u want to change it\n\n"
              "/yes - the process itself terminates when idle\n\n"
              "/no - the process itself continue when idle"
    },
    "inside": {
        "ru": "Вы поменяли команду ожидания на /{}",

        "en": "You change command on /{}"
    }

}
dict_addproc = {
    "start": {"ru": f"Введите команды\n\n"
                    f"/yes - для добавления процесса\n\n"
                    f"/no - для завершения",
              "en": f"Send command\n\n"
                    f"/yes - for add proces\n\n"
                    f"/no - for break"
              },
    "exept": {
        "ru": ">>Нельзя добавить пустоту<<",
        "en": ">>u cant add None<<"
    },
    "while": {
        "ru": "Вы завершили добавление процесса",
        "en": "You break adding the process"
    },
    "answ": {
        "ru": 'Процесс "{}.exe" добавлен',
        "en": 'Process "{}.exe" added'
    }
}
dict_delproc = {
    "start": {"ru": f"Введите команды\n\n"
                    f"/yes - для удаления процесса\n\n"
                    f"/no - для завершения",
              "en": f"Send command\n\n"
                    f"/yes - for delete proces\n\n"
                    f"/no - for break"
              },
    "exept": {
        "ru": ">>Процесса с таким индексом нет<<",
        "en": ">>there is no process with this index<<"
    },
    "while": {
        "ru": "Вы завершили удаление",
        "en": "Process was deleted"
    },
    "answ": {
        "ru": "Процесс {} удален",
        "en": "Process {} deleted"
    }
}


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
    """
    Func returned package from cmd
    """
    result = subprocess.Popen(args=command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return result.stdout.readlines()


def command_execution_write(decode="cp866", command="") -> list:
    """
    Func() append all task process from cmd in array
    :param decode:
    :param command:
    :return:
    """
    byte_arr: list = []
    for byte_line in command_execution(command):
        # decode 'cp866'
        line = byte_line.decode(decode).replace("\r", "")
        line_now = line.split(",")
        if line_now[0] not in blacklist:
            if len(line) > 3:
                byte_arr.append(line)
            else:
                return byte_arr

    return byte_arr


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
        b_line = b_line.replace("\r", "")
        b_line = b_line.replace("\n", "")
        for i in b_line.split(" "):
            if len(i) > 2:
                line = line + " " + i
        m.append(line.split(" ")[2::])
    return m


# IDK, but just stay there
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


bot = telebot.TeleBot("5828330086:AAGCyMebjBxrzFDzKXOhJYhG3c__LjWEkCA")
blacklist: list = file_read("blacklist.txt")
kill_app: list = file_read(f"killApp.txt")
# check_app = convert_type(kill_app)
tg_bot_send: bool = True
task_cmd: bool = True
command_wait_cmd: bool = False
got_True: Any = None
pid_tasklist: list = []
language = "ru"


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
    """
     terminate process
    """
    command_execution(f'taskkill /pid {pid_id}')


def get_proclist():
    """
    :return: All process in killApp
    """
    
    global pid_tasklist
    Pid_list_out = set()
    pid_tasklist: list = command_execution_write('cp866', 'TASKLIST /FO CSV /NH /FI "IMAGENAME ne svchost.exe"')

    for line in pid_tasklist:
        lst = line.split(",")
        if lst[0] in kill_app:
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

    global tg_bot_send, task_cmd, command_wait_cmd, pid_tasklist
    tg_bot_send = True
    task_cmd = None
    pid_process: set = set()
    bot.send_message(message.chat.id, dict_start["start"][language])

    while tg_bot_send:

        while len(pid_process) >= 1:

            for PID in pid_process:
                PID: str = PID.replace('"', "")
                text_out_bot: str = str(pid_inf(PID))
                bot.send_message(message.chat.id, text_out_bot)
                time_in: float = time.time()

                while True:
                    time_out: float = time.time()

                    if not tg_bot_send:
                        break

                    if (time_out - time_in) >= 15:
                        if command_wait_cmd:
                            pid_kill(PID)
                            bot.send_message(message.chat.id, dict_start["wait"]["yes"][language])
                            break
                        if not command_wait_cmd:
                            bot.send_message(message.chat.id, dict_start["wait"]["no"][language])
                            break

                    else:
                        if got_True is True:
                            pid_kill(PID)
                            bot.send_message(message.chat.id, dict_start["while"]["yes"][language])
                            break
                        if got_True is False:
                            bot.send_message(message.chat.id, dict_start["while"]["yes"][language])
                            break
                        if not tg_bot_send:
                            break

                time.sleep(2)
            pid_process = set()

        else:
            pid_process: set = get_proclist()

    bot.send_message(message.chat.id, ">>end<<")


@bot.message_handler(commands=['stop'])
def send_message(message):
    global tg_bot_send
    tg_bot_send = False
    bot.send_message(message.chat.id, dict_stop[language])


@bot.message_handler(commands=['help'])
def send_message(message):
    bot.send_message(message.chat.id, dict_help[language])


@bot.message_handler(commands=['wait'])
def send_message_in(message):
    global got_True, command_wait_cmd
    bot.send_message(message.chat.id, dict_wait["start"][language].format(command_wait_cmd))
    time_in = time.time()
    time_out = 0
    while (time_out - time_in) <= 10:
        if got_True is True:
            command_wait_cmd = True
            bot.send_message(message.chat.id, dict_wait["inside"][language].format(command_wait_cmd))
            break
        if got_True is False:
            command_wait_cmd = False
            bot.send_message(message.chat.id, dict_wait["inside"][language].format(command_wait_cmd))
            break
    bot.send_message(message.chat.id, f">>quit<<\n >>{send_message_in.__name__}<<")


@bot.message_handler(commands=['yes'])
def send_message_yes(message):
    bot.send_message(message.chat.id, f'>>DONE<<')
    global got_True
    got_True = True
    time.sleep(1)
    got_True = None


@bot.message_handler(commands=['no'])
def send_message_yes(message):
    bot.send_message(message.chat.id, f'>>DONE<<')
    global got_True
    got_True = False
    time.sleep(1)
    got_True = None


@bot.message_handler(commands=['prproc'])
def send_message_del(message):
    text_out = ""

    for i in range(len(kill_app)):
        text_out = text_out + f"index={i} {kill_app[i]}\n"

    bot.send_message(message.chat.id, text_out)


@bot.message_handler(commands=['addproc'])
def send_message_add(message):
    try:
        global got_True
        text_mes: str = message.text.split(" ")[1]
        bot.send_message(message.chat.id, dict_addproc["start"][language])
        time_out_func = 0
        time_in_func = time.time()

        while (time_out_func - time_in_func) <= 20:
            time_out_func = time.time()

            if got_True is True:
                kill_app.append(f'"{text_mes}.exe"')
                bot.send_message(message.chat.id, dict_addproc["answ"][language].format(text_mes))
                break

            if got_True is False:
                bot.send_message(message.chat.id, dict_addproc["while"][language])
                break

        bot.send_message(message.chat.id, f">>quit<<\n >>{send_message_add.__name__}<<")
    except Exception as error:

        if error.__class__.__name__ == "IndexError":
            bot.send_message(message.chat.id, f">>IndexError: {str(error)}<<")
            bot.send_message(message.chat.id, dict_addproc["exept"][language])

        else:
            bot.send_message(message.chat.id, str(error))


@bot.message_handler(commands=['delproc'])
def send_message_del(message):
    try:
        global got_True
        text_mes: str = message.text.split(" ")[1]
        # print info
        bot.send_message(message.chat.id, str(kill_app[int(text_mes)]))
        bot.send_message(message.chat.id, dict_delproc["start"][language])
        time_out_func = 0
        time_in_func = time.time()

        while (time_out_func - time_in_func) <= 20:
            time_out_func = time.time()

            if got_True is True:
                bot.send_message(message.chat.id, dict_delproc["answ"][language].format(kill_app[int(text_mes)]))
                kill_app.pop(int(text_mes))
                break

            if got_True is False:
                bot.send_message(message.chat.id, dict_delproc["while"][language])
                break

        bot.send_message(message.chat.id, f">>quit<<\n >>{send_message_del.__name__}<<")
    except Exception as error:

        if error.__class__.__name__ == "IndexError":
            bot.send_message(message.chat.id, f">>IndexError: {str(error)}<<")
            bot.send_message(message.chat.id, dict_delproc["exept"][language])

        else:
            bot.send_message(message.chat.id, f"{error.__class__.__name__}: {str(error)}")


@bot.message_handler(commands=['language'])
def send_message_lang(message):
    global language
    time_in = time.time()

    if language == "ru":
        bot.send_message(message.chat.id, "Send /yes, if u want change a language to English"
                                          "\n\n Send /no to continue")
    elif language == "en":
        bot.send_message(message.chat.id, "Отправьте /yes, если хотите поменять язык на Русский"
                                          "\n\n Отправьте /no для продолжения")
    while time.time() - time_in <= 10:

        if got_True is True:

            if language == "ru":
                language = "en"
                bot.send_message(message.chat.id, f"Language changed to {language}")
                break

            if language == "en":
                language = "ru"
                bot.send_message(message.chat.id, f"Язык поменян на  {language}")
                break

        if got_True is False:
            break
    bot.send_message(message.chat.id, f">>{send_message_lang.__name__}<<")


# loop
bot.polling()
