import telebot
import logging
import codecs
import textract
from telebot import types
from PIL import Image
import pytesseract
import cv2
import os
import requests
API_TOKEN = '585299899:AAGxkkmOKgJY8t8wYUyLgaAwQtuu95FT0B4'

dic = {'А':'A', 'а':'a', 'Ә':'Á', 'ә':'á', 'Б':'B', 'б':'b', 'Д':'D', 'д':'d', 'Е':'E', 'е':'e',
       'Ф':'F', 'ф':'f', 'Ғ':'Ǵ', 'ғ':'ǵ', 'Г':'G', 'г':'g', 'Х':'H', 'х':'h', 'І':'I', 'і':'i',
       'И':'I', 'и':'ı', 'Й':'I', 'й':'ı', 'Һ':'H', 'һ':'h', 'Ж':'J', 'ж':'j', 'К':'K', 'к':'k',
       'Л':'L', 'л':'l', 'М':'M', 'м':'m', 'Н':'N', 'н':'n', 'Ң':'Ń', 'ң':'ń', 'О':'O', 'о':'o',
       'Ө':'Ó', 'ө':'ó', 'П':'P', 'п':'p', 'Қ':'Q', 'қ':'q', 'Р':'R', 'р':'r', 'Ш':'Sh', 'ш':'sh',
       'С':'S', 'с':'s', 'Т':'T', 'т':'t', 'Ұ':'U', 'ұ':'u', 'Ү':'Ú', 'ү':'ú', 'В':'V',
       'в':'v', 'Ы':'Y', 'ы':'y', 'У':'Ý', 'у':'ý', 'З':'Z', 'з':'z', 'Ч':'Ch', 'ч':'ch',
       'Э':'E', 'э':'e', 'Щ':'', 'щ':'', 'Ь':'','ь':'', 'Ъ':'', 'ъ':'', 'Я':'Ia','я':'ia', 'Ц':'Ts', 'ц':'ts' }

alphabet = ['А', 'а', 'Ә', 'ә', 'Б', 'б', 'Д', 'д', 'Е', 'е', 'Ф', 'ф',
'Ғ', 'ғ', 'Г', 'г', 'Х', 'х',
                'І', 'і', 'И', 'и', 'Й', 'й', 'Һ', 'һ', 'Ж', 'ж', 'К', 'к', 'Л', 'л', 'М', 'м', 'Н', 'н',
            'Ң', 'ң', 'О', 'о', 'Ө', 'ө', 'П', 'п', 'Қ', 'қ', 'Р', 'р', 'Ш', 'ш', 'С', 'с', 'Т', 'т',
            'Ұ', 'ұ', 'Ү', 'ү', 'В', 'в', 'Ы', 'ы', 'У', 'у', 'З', 'з', 'Ч', 'ч', 'Э', 'э', 'Щ', 'щ',
            'Ь', 'ь', 'Ъ', 'ъ', 'Я','я', 'Ц','ц']
preprocess = "thresh"
bot = telebot.TeleBot(API_TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


@bot.message_handler(func=lambda message: True,content_types=['text'])
def latin(message):
    textcyr = message.text
    st = str(textcyr)
    resultx = str()

    len_st = len(st)
    for i in range (0, len_st):
        if st[i] in alphabet:
            simb = dic[st[i]]
        else:
            simb = st[i]
        resultx = resultx + simb
    bot.send_message(message.chat.id, resultx)


@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):

    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src='/home/squbble/bot/files/'+message.document.file_id;
        with open(src, 'wb') as new_file:
           new_file.write(downloaded_file)
        with open(src, 'r') as f:
           lines = f.read()
           #lines = new_file.read()
        file = open(src, "w")
        bot.send_document(message.chat.id, open(src, "rb"))
        for line in lines:
           file.write((''.join([dic.get(char, char) for char in line])))
        urllib2.urlretrieve(src, message.document.file_name)
        file = open(message.document.file_name,'rb')
        bot.send_document(message.chat.id, file)
        
        
    except Exception as e:
        bot.send_message(message.chat.id,e )
    
@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    
    try:
      
       
        file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
      
        src='/home/squbble/bot/files/'+file_info.file_path;
        image = src
        with open(src, 'wb') as new_file:
           new_file.write(downloaded_file)
           image = cv2.imread(image)
           gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
           if preprocess == "thresh":
                gray = cv2.threshold(gray, 0, 255,
                    cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
           elif preprocess == "blur":
                gray = cv2.medianBlur(gray, 3)
           filename = "{}.png".format(os.getpid())
           cv2.imwrite(filename, gray)
           lines = pytesseract.image_to_string(Image.open(src), lang='kaz')
           #os.remove(filename)
           for line in lines:
               lat = ((''.join([dic.get(char, char) for char in lines])))

        bot.send_message(message.chat.id,lat) 
   
    except Exception as e:
        bot.send_message(message.chat.id,e )
        


bot.polling(none_stop=True, interval=0, timeout=3)
