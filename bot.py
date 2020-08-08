#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telebot
from telebot import types
from telebot import util
import time
import os


# Change to your token of @BotFather
TOKEN = 'XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXX'
# Change to the id number(s) of the user(s) who is/are authorized to use the bot
authorizedUsers = [12345678, 987654321]
userStep = {}

menu = types.ReplyKeyboardMarkup()
menu.add('info serv', 'ip route', 'public ip')
menu.add('active processes', 'netstat', 'who')

info_menu = types.ReplyKeyboardMarkup()
info_menu.add('Temp', 'Hard Disk Space')
info_menu.add('RAM', 'CPU')
info_menu.add('Back')


# LOGGER
def logger(msg):
    logFile = open('logFileBot.txt', 'a')
    logFile.write(repr(msg) + '\n')
    logFile.close()


# LISTENER
def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            logActionsInfo = (time.strftime('%d/%m/%y-%H:%M:%S') + color.GREEN +
                              ' [' + str(m.chat.id) + '] ' + str(m.chat.first_name) + ': ' + color.ENDC + m.text)
            logger(logActionsInfo)
            print(logActionsInfo)


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)


class color:
    RED = '\033[91m'
    BLUE = '\033[94m'
    GREEN = '\033[32m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# USER NOT ALLOWED ACTIONS
def userNotAlowed(m):
    logActivity = (time.strftime('%d/%m/%y-%H:%M:%S') + color.GREEN +
                   ' [' + str(m.chat.id) + '] ' + str(m.chat.username) + ': ' + color.ENDC + 'Try to access to the bot')
    logger(logActivity)
    print(logActivity)
    bot.send_message(
        m.chat.id, 'YOU ARE NOT ALLOWED TO USE THIS BOT, your user information was registered, pls go out!')


# USER STEP
def get_user_step(uid):
    if (uid in authorizedUsers) & (uid in userStep):
        return userStep[uid]
    else:
        userStep[uid] = 0
        logger('User ' + str(uid) + ' try to access at: ' +
               time.strftime('%d/%m/%y-%H:%M:%S'))
        bot.send_message(
            uid, 'YOU ARE NOT ALLOWED TO USE THIS BOT, your user information was registered, pls go out!')
    if uid in userStep:
        return userStep[uid]


# EXEC COMMAND
@bot.message_handler(commands=['exec'])
def command_exec(m):
    cid = m.chat.id
    if cid in authorizedUsers:
        bot.send_message(cid, 'Running: `$' +
                         m.text[len('/exec'):] + '`', parse_mode='Markdown')
        f = os.popen(m.text[len('/exec'):])
        result = f.read()
        splitted_text = util.split_string(result, 3000)
        bot.send_message(
            cid, '`$' + m.text[len('/exec'):] + '`\n', parse_mode='Markdown')
        for text in splitted_text:
            bot.send_message(cid, text)
        bot.send_message(
            cid, '-`$' + m.text[len('/exec'):] + '`- FINISHED ', parse_mode='Markdown')
    else:
        userNotAlowed(m)


# AMASSENUM COMMAND
@bot.message_handler(commands=['amassenum'])
def command_amassEnum(m):
    cid = m.chat.id
    if cid in authorizedUsers:
        bot.send_message(cid, 'Running: `$ amass enum -d' +
                         m.text[len('/amassEnum'):] + '`', parse_mode='Markdown')
        f = os.popen('amass enum -d' + m.text[len('/amassEnum'):])
        result = f.read()
        splitted_text = util.split_string(result, 3000)
        bot.send_message(
            cid, '`$ amass enum -d' + m.text[len('/amassEnum'):] + '`\n', parse_mode='Markdown')
        for text in splitted_text:
            bot.send_message(cid, text)
        bot.send_message(
            cid, '-`$ amass enum -d' + m.text[len('/amassEnum'):] + '`- FINISHED ', parse_mode='Markdown')
    else:
        userNotAlowed(m)


# NMAPADV COMMAND
@bot.message_handler(commands=['nmapadv'])
def command_nmapAdv(m):
    cid = m.chat.id
    if cid in authorizedUsers:
        bot.send_message(cid, 'Running: `$ nmap -sC -sV -Pn -p-' +
                         m.text[len('/nmapAdv'):] + '`', parse_mode='Markdown')
        f = os.popen('nmap -sC -sV -Pn -p-' + m.text[len('/nmapAdv'):])
        result = f.read()
        splitted_text = util.split_string(result, 3000)
        bot.send_message(
            cid, '`$ nmap -sC -sV -Pn -p-' + m.text[len('/nmapAdv'):] + '`\n', parse_mode='Markdown')
        for text in splitted_text:
            bot.send_message(cid, text)
        bot.send_message(
            cid, '-`$ nmap -sC -sV -Pn -p-' + m.text[len('/nmapAdv'):] + '`- FINISHED ', parse_mode='Markdown')
    else:
        userNotAlowed(m)


# HELP COMMAND
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    if cid in authorizedUsers:
        bot.send_message(cid, '/start : starts/reset the bot')
        bot.send_message(
            cid, '/exec : execute a command line\n\nE.g: /exec echo "hello from the other side"')
        bot.send_message(
            cid, '/amassenum : execute `$amass enum -d`\n\nE.g: /amassenum example.com', parse_mode='Markdown')
        bot.send_message(
            cid, '/nmapadv : execute `$nmap -sC -sV -Pn -p-`\n\nE.g: /nmapadv example.com', parse_mode='Markdown')
        bot.send_message(cid, '/help : show this message')
        bot.send_message(
            cid, '*TIP* : If your output is too large, you should save it in a file with no output.', parse_mode='Markdown')
    else:
        userNotAlowed(m)


# START
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    userStep[cid] = 0
    if cid in authorizedUsers:
        bot.send_message(cid, 'Welcome back ' + str(m.chat.first_name) + '...')
        bot.send_message(cid, "I'm ready to receive your orders...")
        time.sleep(1)
        bot.send_message(cid, 'Hack the planet!', reply_markup=menu)
    else:
        logActivity = (time.strftime('%d/%m/%y-%H:%M:%S') + color.GREEN +
                       ' [' + str(m.chat.id) + '] ' + str(m.chat.username) + ': ' + color.ENDC + 'Try to access to the bot')
        logger(logActivity)
        print(logActivity)
        bot.send_message(
            cid, 'YOU ARE NOT ALLOWED TO USE THIS BOT, your user information was registered, pls go out!')


def ipRoute(cid):
    bot.send_message(cid, 'Result:')
    result = os.popen('ip route').read()
    splitted_text = util.split_string(result, 3000)
    for text in splitted_text:
        bot.send_message(cid, text)


def infServ(cid):
    bot.send_message(cid, 'Information available:', reply_markup=info_menu)
    userStep[cid] = 1


def ipPublic(cid):
    bot.send_message(cid, 'Your Public IP Address is:')
    publicIp = os.popen(
        r"wget http://checkip.dyndns.org/ -q -O - | grep -Eo '\<[[:digit:]]{1,3}(\.[[:digit:]]{1,3}){3}\>'").read()
    bot.send_message(cid, publicIp)


def whoIsLogged(cid):
    bot.send_message(cid, 'Who are logged in:')
    bot.send_message(cid, os.popen("who | grep -Eo '^[^ ]+'").read())


def activeProc(cid):
    bot.send_message(cid, 'Active processes:')
    activeProc = os.popen('ps -e').read()
    splitted_text = util.split_string(activeProc, 3000)
    for text in splitted_text:
        bot.send_message(cid, text)


def netstat(cid):
    bot.send_message(cid, 'Netstat by services:')
    net = os.popen('netstat -tp').read()
    splitted_text = util.split_string(net, 3000)
    for text in splitted_text:
        bot.send_message(cid, text)


optionsMainMenu = {
    'info serv': infServ,
    'ip route': ipRoute,
    'public ip': ipPublic,
    'active processes': activeProc,
    'netstat': netstat,
    'who': whoIsLogged
}


# MAIN MENU
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 0)
def main_menu(m):
    cid = m.chat.id
    text = m.text
    if cid in authorizedUsers:
        func = (optionsMainMenu.get(text))
        try:
            func(cid)
        except Exception as e:
            bot.send_message(
                cid, "I can't understand that command, sorry :'(")
            print(e)
    else:
        userNotAlowed(m)


# INFO RAM
def getRAMInfo():
    p = os.popen('free -h')
    i = 0
    while 1:
        i += 1
        line = p.readline()
        if i == 2:
            return(line.split()[1:4])


def ramInfo(cid):
    total = getRAMInfo()[0]
    used = getRAMInfo()[1]
    available = getRAMInfo()[2]
    bot.send_message(cid, '[+] RAM MEMORY')
    bot.send_message(cid, '  [i]   Total: %s' % total)
    bot.send_message(cid, '  [i]   Used: %s' % used)
    bot.send_message(cid, '  [i]   Available: %s' % available)
    print(color.BLUE + '[+] RAM MEMORY' + color.ENDC)
    print(color.GREEN + ' [i] Total: %s' % total + color.ENDC)
    print(color.GREEN + ' [i] Used: %s' % used + color.ENDC)
    print(color.GREEN + ' [i] Available: %s' % available + color.ENDC)


# GETTING HD INFO
def infoHD():
    p = os.popen('df -h /')
    i = 0
    while 1:
        i += 1
        line = p.readline()
        if i == 2:
            return(line.split()[1:5])


# INFO HD SPACE
def diskSpace(cid):
    total = infoHD()[0]
    used = infoHD()[1]
    available = infoHD()[2]
    bot.send_message(cid, '[+] HARD DISK SPACE')
    bot.send_message(cid, '  [i]   Total: %s' % total)
    bot.send_message(cid, '  [i]   Used: %s' % used)
    bot.send_message(cid, '  [i]   Available: %s' % available)
    print(color.BLUE + '[+] HARD DISK SPACE' + color.ENDC)
    print(color.GREEN + ' [i] Total: %s' % total + color.ENDC)
    print(color.GREEN + ' [i] Used: %s' % used + color.ENDC)
    print(color.GREEN + ' [i] Available: %s' % available + color.ENDC)


# TEMPERATURE
def temp(cid):
    tempFile = open('/sys/class/thermal/thermal_zone0/temp')
    cpu_temp = tempFile.read()
    tempFile.close()
    tmp = round(float(cpu_temp) / 1000)
    bot.send_message(cid, '[+] TEMPERATURE')
    bot.send_message(cid, '  [i]   CPU: %s' % tmp)
    print(color.BLUE + '[+] TEMPERATURE' + color.ENDC)
    print(color.GREEN + ' [i] CPU: %s' % tmp + color.ENDC)


# CPU USAGE
def cpuUsage(cid):
    cpuUse = os.popen("mpstat 1 5 | awk 'END{print 100-$NF}'").read()
    bot.send_message(cid, '[+] CPU')
    bot.send_message(cid, '  [i]   Used: %s' % cpuUse)
    print(color.BLUE + '[+] CPU' + color.ENDC)
    print(color.GREEN + ' [i] Used: %s' % cpuUse + color.ENDC)


def backToMainMenu(cid):
    userStep[cid] = 0
    bot.send_message(cid, 'Main menu:', reply_markup=menu)


optionsInfoMenu = {
    'Temp': temp,
    'Hard Disk Space': diskSpace,
    'RAM': ramInfo,
    'CPU': cpuUsage,
    'Back': backToMainMenu
}


# MENU INFO
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def info_opt(m):
    cid = m.chat.id
    txt = m.text
    func = (optionsInfoMenu.get(txt))
    try:
        func(cid)
    except Exception as e:
        bot.send_message(cid, "I can't understand that command, sorry :'(")
        print(e)


print('Running...')
bot.polling(none_stop=True)
