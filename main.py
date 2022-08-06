# Программа "ХОМЯК"

import config
import stt
import tts
from fuzzywuzzy import fuzz
import datetime
from num2t4ru import num2text
import webbrowser
import random


print(f"{config.VA_NAME} (v{config.VA_VER}) начала свою работу ...")


def va_respond(voice: str):
    print(voice)
    if voice.startswith(config.VA_ALIAS):
        # обращаются к ассистенту
        cmd = recognize_cmd(filter_cmd(voice))

        if cmd['cmd'] not in config.VA_CMD_LIST.keys():
            tts.va_speak("что?")
        else:
            execute_cmd(cmd['cmd'])


def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in config.VA_CMD_LIST.items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc


def execute_cmd(cmd: str):
    if cmd == 'help':
        # help
        text = "Я умею: ..."
        text += "произносить время ..."
        text += "рассказывать анекдоты ..."
        text += "и открывать браузер"
        tts.va_speak(text)
        pass
    elif cmd == 'ctime':
        # current time
        male_units = ((u'час', u'часа', u'часов'), 'm')
        female_units = ((u'минута', u'минуты', u'минут'), 'f')
        now = datetime.datetime.now()
        text = "Сейчас " + num2text(now.hour, male_units) + " " + num2text(now.minute, female_units)
        tts.va_speak(text)

    elif cmd == 'joke':
        jokes = ['Свекровь говорит невестке: - Живем мы хорошо, не ругаемся, все у нас есть, вот только хата не побелена! - Мама, а краска есть? - Краска есть, да щётки нет! Невестка бежит к свёкру, обрезает ему бороду, делает щётку и белит хату......... Свекровь: - Вот хата у нас теперь побелена, а окна не покрашены! - Мама, а краска есть? - Да есть, но кисточки нет! Невестка бежит к свёкру, обрезает ему усы, делает кисточку и красит окно. Возвращается с работы муж, видит на дереве своего отца и спрашивает: - Папа, что с тобой, почему ты на дереве сидишь? - Сынок, да бабы собрались блины печь, а я не знаю, есть ли у них яйца!',
                 'Папа научил маленького Вовочку считать, теперь папе приходится делить пельмени поровну.',
                 'Блин! - сказал слон, наступив на колобка.',
                 'Бабушка, а ты пришла сама? - Сама внученька, сама! - А папа сказал, что тебя черти принесли!',
                 'Увидев, что русский достает третью бутылку водки, немец начал писать завещание.',
                 'В школе Васю все боялись и уважали, все знали, что он занимается карате. В школу пришел новенький и побил Васю, он не знал, что Вася занимается карате.'
                 ]

        tts.va_speak(random.choice(jokes))

    elif cmd == 'open_browser':
        # chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        firefox_path = '/snap/bin/firefox %s'
        webbrowser.get(firefox_path).open("https://gb.ru/education")


# начать прослушивание команд
stt.va_listen(va_respond)
