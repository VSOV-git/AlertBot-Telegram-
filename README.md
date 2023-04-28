# AlertBot  
**This bot is alerted u if his found stranger process on ur PC**
>## **SETUP PROGRAM**
- ### botTg.py
- ### killApp.py
- ### blacklist.py

## BotTg.py
>**It's main file.py** with all code for my bot

## killApp.py
>**It's file.txt** its text file with names with hostile proces 

## blacklist.py
>**It's file.txt** its text file with names with continue proces


## How it works ?
> The program is working only on **Windows 10** and older !
1. Open BotTg.py
2. In python file find **<line 100>**  
    `bot = telebot.TeleBot("UR API KEY")`  
     How create a Telegram bot u can find in internet !
3. **Now we can start !** 
4. When u start open ur Telegram bot and send "/start" then u got a message "Процесс сканирования запущен" 
its means the bot is working now.
5. U can try to open the CMD(terminal) and u can see the message about a CMD proces and u can send command
"/yes" to **break** proces or "/no" to continue
# Commands
1. /help - print all Bot commands
2. /start - starting a scan the system  
3. /stop - break the scan
4. /yes - command "yes"
5. /no - command "no"
6. /wait - what command use at inaction
7. /addproc(yes/no) - add a proces in Bot
8. /delproc(yes/no) - delete a proces in Bot
9. /prproc - print all proc in scan
10. /language - change ur language to "en" or "ru"

# Thanks for read
The info about updates in **[updates.md](updates.md)**
   

