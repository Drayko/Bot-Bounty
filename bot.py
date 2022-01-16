#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time

import telebot
from telebot import types
from telebot import util

from config import TOKEN
from config import authorizedUsers

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
    log_file = open('logFileBot.txt', 'a')
    log_file.write(repr(msg) + '\n')
    log_file.close()


# LISTENER
def listener(messages):
    for message in messages:
        if message.content_type == 'text':
            log_actions_info = (time.strftime('%d/%m/%y-%H:%M:%S') + Color.GREEN +
                                ' [' + str(message.chat.id) + '] ' + str(
                        message.chat.first_name) + ': ' + Color.ENDC + message.text)
            logger(log_actions_info)
            print(log_actions_info)


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)


class Color:
    RED = '\033[91m'
    BLUE = '\033[94m'
    GREEN = '\033[32m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# RECORD USER NOT ALLOWED ACTIONS
def user_not_allowed(message):
    log_activity = (time.strftime('%d/%m/%y-%H:%M:%S') + Color.GREEN +
                    ' [' + str(message.chat.id) + '] ' + str(
                message.chat.username) + ': ' + Color.ENDC + 'Try to access to the bot')
    logger(log_activity)
    print(log_activity)
    bot.send_message(
        message.chat.id, 'YOU ARE NOT ALLOWED TO USE THIS BOT, your user information was registered, pls go out!')


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
def command_exec(message):
    chat_id = message.chat.id
    if chat_id in authorizedUsers:
        bot.send_message(chat_id, 'Running: `$' +
                         message.text[len('/exec'):] + '`', parse_mode='Markdown')
        command = os.popen(message.text[len('/exec'):])
        result = command.read()
        splitted_text = util.split_string(result, 3000)
        bot.send_message(
            chat_id, '`$' + message.text[len('/exec'):] + '`\n', parse_mode='Markdown')
        for text in splitted_text:
            bot.send_message(chat_id, text)
        bot.send_message(
            chat_id, '-`$' + message.text[len('/exec'):] + '`- FINISHED ', parse_mode='Markdown')
    else:
        user_not_allowed(message)


# AMASSENUM COMMAND
@bot.message_handler(commands=['amassenum'])
def command_amass_enum(message):
    chat_id = message.chat.id
    if chat_id in authorizedUsers:
        bot.send_message(chat_id, 'Running: `$ amass enum -d' +
                         message.text[len('/amassEnum'):] + '`', parse_mode='Markdown')
        command = os.popen('amass enum -d' + message.text[len('/amassEnum'):])
        result = command.read()
        splitted_text = util.split_string(result, 3000)
        bot.send_message(
            chat_id, '`$ amass enum -d' + message.text[len('/amassEnum'):] + '`\n', parse_mode='Markdown')
        for text in splitted_text:
            bot.send_message(chat_id, text)
        bot.send_message(
            chat_id, '-`$ amass enum -d' + message.text[len('/amassEnum'):] + '`- FINISHED ', parse_mode='Markdown')
    else:
        user_not_allowed(message)


# NMAPADV COMMAND
@bot.message_handler(commands=['nmapadv'])
def command_nmap_adv(message):
    chat_id = message.chat.id
    if chat_id in authorizedUsers:
        bot.send_message(chat_id, 'Running: `$ nmap -sC -sV -Pn -p-' +
                         message.text[len('/nmapAdv'):] + '`', parse_mode='Markdown')
        command = os.popen('nmap -sC -sV -Pn -p-' + message.text[len('/nmapAdv'):])
        result = command.read()
        splitted_text = util.split_string(result, 3000)
        bot.send_message(
            chat_id, '`$ nmap -sC -sV -Pn -p-' + message.text[len('/nmapAdv'):] + '`\n', parse_mode='Markdown')
        for text in splitted_text:
            bot.send_message(chat_id, text)
        bot.send_message(
            chat_id, '-`$ nmap -sC -sV -Pn -p-' + message.text[len('/nmapAdv'):] + '`- FINISHED ',
            parse_mode='Markdown')
    else:
        user_not_allowed(message)


# HELP COMMAND
@bot.message_handler(commands=['help'])
def command_help(message):
    chat_id = message.chat.id
    if chat_id in authorizedUsers:
        bot.send_message(chat_id, '/start : starts/reset the bot')
        bot.send_message(
            chat_id, '/exec : execute a command line\n\nE.g: /exec echo "hello from the other side"')
        bot.send_message(
            chat_id, '/amassenum : execute `$amass enum -d`\n\nE.g: /amassenum example.com', parse_mode='Markdown')
        bot.send_message(
            chat_id, '/nmapadv : execute `$nmap -sC -sV -Pn -p-`\n\nE.g: /nmapadv example.com', parse_mode='Markdown')
        bot.send_message(chat_id, '/help : show this message')
        bot.send_message(
            chat_id, '*TIP* : If your output is too large, you should save it in a file with no output.',
            parse_mode='Markdown')
    else:
        user_not_allowed(message)


# START
@bot.message_handler(commands=['start'])
def command_start(message):
    chat_id = message.chat.id
    userStep[chat_id] = 0
    if chat_id in authorizedUsers:
        bot.send_message(chat_id, 'Welcome back ' + str(message.chat.first_name) + '...')
        bot.send_message(chat_id, "I'm ready to receive your orders...")
        time.sleep(1)
        bot.send_message(chat_id, 'Hack the planet!', reply_markup=menu)
    else:
        log_activity = (time.strftime('%d/%m/%y-%H:%M:%S') + Color.GREEN +
                        ' [' + str(message.chat.id) + '] ' + str(
                    message.chat.username) + ': ' + Color.ENDC + 'Try to access to the bot')
        logger(log_activity)
        print(log_activity)
        bot.send_message(
            chat_id, 'YOU ARE NOT ALLOWED TO USE THIS BOT, your user information was registered, pls go out!')


def ip_route(chat_id):
    bot.send_message(chat_id, 'Result:')
    result = os.popen('ip route').read()
    splitted_text = util.split_string(result, 3000)
    for text in splitted_text:
        bot.send_message(chat_id, text)


def inf_serv(chat_id):
    bot.send_message(chat_id, 'Information available:', reply_markup=info_menu)
    userStep[chat_id] = 1


def ip_public(chat_id):
    bot.send_message(chat_id, 'Your Public IP Address is:')
    public_ip = os.popen(
        r"curl https://ifconfig.me").read()
    bot.send_message(chat_id, public_ip)


def who_is_logged(chat_id):
    bot.send_message(chat_id, 'Who are logged in:')
    bot.send_message(chat_id, os.popen("who | grep -Eo '^[^ ]+'").read())


def active_processes(chat_id):
    bot.send_message(chat_id, 'Active processes:')
    active_process = os.popen('ps -e').read()
    splitted_text = util.split_string(active_process, 3000)
    for text in splitted_text:
        bot.send_message(chat_id, text)


def netstat(chat_id):
    bot.send_message(chat_id, 'Netstat by services:')
    net = os.popen('netstat -tp').read()
    splitted_text = util.split_string(net, 3000)
    for text in splitted_text:
        bot.send_message(chat_id, text)


optionsMainMenu = {
    'info serv': inf_serv,
    'ip route': ip_route,
    'public ip': ip_public,
    'active processes': active_processes,
    'netstat': netstat,
    'who': who_is_logged
}


# MAIN MENU
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 0)
def main_menu(message):
    chat_id = message.chat.id
    text = message.text
    if chat_id in authorizedUsers:
        func = (optionsMainMenu.get(text))
        try:
            func(chat_id)
        except Exception as e:
            bot.send_message(
                chat_id, "I can't understand that command, sorry :'(")
            print(e)
    else:
        user_not_allowed(message)


# INFO RAM
def get_ram_info():
    p = os.popen('free -h')
    i = 0
    while 1:
        i += 1
        line = p.readline()
        if i == 2:
            return line.split()[1:4]


def ram_info(chat_id):
    total = get_ram_info()[0]
    used = get_ram_info()[1]
    available = get_ram_info()[2]
    bot.send_message(chat_id, '[+] RAM MEMORY')
    bot.send_message(chat_id, '  [i]   Total: %s' % total)
    bot.send_message(chat_id, '  [i]   Used: %s' % used)
    bot.send_message(chat_id, '  [i]   Available: %s' % available)
    print(Color.BLUE + '[+] RAM MEMORY' + Color.ENDC)
    print(Color.GREEN + ' [i] Total: %s' % total + Color.ENDC)
    print(Color.GREEN + ' [i] Used: %s' % used + Color.ENDC)
    print(Color.GREEN + ' [i] Available: %s' % available + Color.ENDC)


# GETTING HD INFO
def info_hd():
    p = os.popen('df -h /')
    i = 0
    while 1:
        i += 1
        line = p.readline()
        if i == 2:
            return line.split()[1:5]


# INFO HD SPACE
def disk_space(chat_id):
    total = info_hd()[0]
    used = info_hd()[1]
    available = info_hd()[2]
    bot.send_message(chat_id, '[+] HARD DISK SPACE')
    bot.send_message(chat_id, '  [i]   Total: %s' % total)
    bot.send_message(chat_id, '  [i]   Used: %s' % used)
    bot.send_message(chat_id, '  [i]   Available: %s' % available)
    print(Color.BLUE + '[+] HARD DISK SPACE' + Color.ENDC)
    print(Color.GREEN + ' [i] Total: %s' % total + Color.ENDC)
    print(Color.GREEN + ' [i] Used: %s' % used + Color.ENDC)
    print(Color.GREEN + ' [i] Available: %s' % available + Color.ENDC)


# TEMPERATURE
def temp(chat_id):
    temp_file = open('/sys/class/thermal/thermal_zone0/temp')
    cpu_temp = temp_file.read()
    temp_file.close()
    tmp = round(float(cpu_temp) / 1000)
    bot.send_message(chat_id, '[+] TEMPERATURE')
    bot.send_message(chat_id, '  [i]   CPU: %s' % tmp)
    print(Color.BLUE + '[+] TEMPERATURE' + Color.ENDC)
    print(Color.GREEN + ' [i] CPU: %s' % tmp + Color.ENDC)


# CPU USAGE
def cpu_usage(chat_id):
    cpu_use = os.popen("mpstat 1 5 | awk 'END{print 100-$NF}'").read()
    bot.send_message(chat_id, '[+] CPU')
    bot.send_message(chat_id, '  [i]   Used: %s' % cpu_use)
    print(Color.BLUE + '[+] CPU' + Color.ENDC)
    print(Color.GREEN + ' [i] Used: %s' % cpu_use + Color.ENDC)


def back2_main_menu(chat_id):
    userStep[chat_id] = 0
    bot.send_message(chat_id, 'Main menu:', reply_markup=menu)


optionsInfoMenu = {
    'Temp': temp,
    'Hard Disk Space': disk_space,
    'RAM': ram_info,
    'CPU': cpu_usage,
    'Back': back2_main_menu
}


# MENU INFO
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def info_opt(message):
    chat_id = message.chat.id
    txt = message.text
    func = (optionsInfoMenu.get(txt))
    try:
        func(chat_id)
    except Exception as e:
        bot.send_message(chat_id, "I can't understand that command, sorry :'(")
        print(e)


print('Running...')
bot.polling(none_stop=True)