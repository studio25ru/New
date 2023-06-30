import telebot
from telebot import types
import vk_api
import requests
#import pywhatkit
#import vk
import time
import requests
import bs4
from bs4 import BeautifulSoup
from PIL import Image
import os

#для вацапа
from whatsapp_api_client_python import API as API
ID_INSTANCE = '1101815837'
API_TOKEN_INSTANCE = '525135c309384273b83bebfcffeb046300013d6b42a841f890'
greenAPI = API.GreenApi(ID_INSTANCE, API_TOKEN_INSTANCE)

#для телеграма
def send_photo_telegram():
    files = {'photo': open('photo.jpg', 'rb')}
    token = "5999889977:AAH6qRKZv9SwvglJTtP698c2yunPrhVobK0"
    chat_id = "@moy_luchegorsk" # если у вас группа то будет так chat_id = "-1009999999"
    r = requests.post("https://api.telegram.org/bot"+token+"/sendPhoto?chat_id=" + chat_id, files=files)
    if r.status_code != 200:
        raise Exception("post_text error")


#токен бота TelPab_bot
bot = telebot.TeleBot('5999889977:AAH6qRKZv9SwvglJTtP698c2yunPrhVobK0')
#токен ВК
vk_token = "9854bbac9854bbac9854bbac379b475e5a998549854bbacfc00e0c24b7c96fba0abc3b8"
vk_ses = vk_api.VkApi('studio25ru@ya.ru', 'NewLife2523')



try:

   vk_ses.auth()
except vk_api.AuthError as error_msg:
   print(error_msg)
   exit(0)
vk = vk_ses.get_api()

my_app_id = 51624797
user_login = 'studio25ru@ya.ru'
user_password = 'NewLife2523'

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Текст")
    btn2 = types.KeyboardButton("Фото")
    btn3 = types.KeyboardButton("Фото с текстом")
    btn4 = types.KeyboardButton("Добавить логотип")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.from_user.id, "ПУБЛИКАЦИЯ:", reply_markup=markup)

@bot.message_handler(content_types=['text', 'photo'])
def get_text_messages(message):

    if message.content_type == 'photo':
        raw = message.photo[2].file_id
        name = 'photo.jpg'
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(name, 'wb') as new_file:
            new_file.write(downloaded_file)

    # Добавление логотипа
    if message.text == 'Добавить логотип':

        os.rename('photo.jpg', 'image.jpg')

        # Открываем исходную картинку
        image = Image.open('image.jpg')

        # Открываем логотип с прозрачным фоном
        logo = Image.open('logo_ml.png')

        # Вычисляем размеры логотипа, оставляя пропорции
        logo_size = int(min(image.width, image.height) * 0.4)
        logo.thumbnail((logo_size, logo_size))

        # Вычисляем позицию для размещения логотипа вверху по центру
        position = (int((image.width - logo.width) / 2), 0)

        # Вставляем логотип на картинку
        image.paste(logo, position, logo)

        # Сохраняем результат
        image.save('photo.jpg')


    if message.text == 'Фото':
        img = open('photo.jpg', 'rb')
        print(img)
        # публикация в VK в группе Мой Лучегорск
        #  получить объект для загрузки картинок
        upl = vk_api.VkUpload(vk_ses)
        #  загрузить картинку и разместить ее на стене
        photo = upl.photo_wall(['photo.jpg'])
        vk_photo_id = f"photo{photo[0]['owner_id']}_{photo[0]['id']}"
        vk.wall.post(owner_id='-192819139', attachments=[vk_photo_id])
        print('Фото опубликованно')
        #img.close()

        #отправка сообщения в Telegram
        send_photo_telegram()

        #Вац Ап
        def main():
            chatIds = ["79520815182@c.us"]
            #resultCreate = greenAPI.groups.createGroup('Мой Лучегорск', chatIds)
            result = greenAPI.sending.sendFileByUpload('120363129778676951@g.us', "photo.jpg", 'PicFromDisk.png')
            print(result.data)

        if __name__ == "__main__":
            main()

    elif message.text == 'Текст':
        f = open('text.txt', 'r')
        text = f.read()
        print(text)
        f.close()
        vk.wall.post(owner_id='-192819139', message=text)


        #отправка сообщения в телеграм
        token = '5999889977:AAH6qRKZv9SwvglJTtP698c2yunPrhVobK0'
        requests.get('https://api.telegram.org/bot{}/sendMessage'.format(token), params=dict(chat_id='@moy_luchegorsk', text=text))

        def main():
            chatIds = ["79520815182@c.us"]
            #resultCreate = greenAPI.groups.createGroup('Мой Лучегорск', chatIds)

            resultSend = greenAPI.sending.sendMessage('120363129778676951@g.us', text)
            print(resultSend.data)

        if __name__ == "__main__":
            main()

    elif message.text == 'Фото с текстом':
        #Открытия файла с картинкой
        img = open('photo.jpg', 'rb')
        f = open('text.txt', 'r')
        text = f.read()
        print(text)
        f.close()
        #публикация к ВК
        upl = vk_api.VkUpload(vk_ses)
        photo = upl.photo_wall(['photo.jpg'])
        vk_photo_id = f"photo{photo[0]['owner_id']}_{photo[0]['id']}"
        vk.wall.post(owner_id='-192819139', message=text, attachments=[vk_photo_id])

        #ВацАп
        def main():
            chatIds = ["79520815182@c.us"]
            #resultCreate = greenAPI.groups.createGroup('Мой Лучегорск', chatIds)
            result = greenAPI.sending.sendFileByUpload('120363129778676951@g.us', "photo.jpg", 'PicFromDisk.png', text)
            print(result.data)

        if __name__ == "__main__":
            main()

        # в Телеграм
        send_photo_telegram()
        token = '5999889977:AAH6qRKZv9SwvglJTtP698c2yunPrhVobK0'
        requests.get('https://api.telegram.org/bot{}/sendMessage'.format(token), params=dict(chat_id='@moy_luchegorsk', text=text))

    else:
        text = message.text
        name = 'text.txt'
        file = open(name, 'w')
        file.write(text)
        file.close()
        print(text)


        #ПАРСИНГ

        # Определение ключевых слов для парсинга
        pars_list = 'Губернатор, Верхний, Перевал, Светлогорье, Федосьевка, Пожарское, Ласточка, Игнатьевка, Новостройка, Красный, Яр, малочисленные, Этажерка, Зазеркалье, Сорванец, Фортуна, Аквамаринки, Лучегорск, Лучегорске, Лучегорску, Лучегорском, лучегорск, Пожарский, Пожарским, Пожарскому, ГРЭС, ДК, Дворец, культуры, Пожарский, район, Козак, Зускин, ЦВР, культура, культуре'
        pars_res = pars_list.split(', ')

        # print(pars_res)

        def vestiprim():
            # ВЕСТИ ПРИМОРЬЯ
            url = 'https://vestiprim.ru/news/'
            headers = {
                'Host': 'vestiprim.ru',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'}

            r = requests.get(url, headers=headers)

            from bs4 import BeautifulSoup
            # МЕНЯЕМ КОДИРОВКУ
            news = BeautifulSoup(r.content, "html.parser")

            # news = bs4.BeautifulSoup(r.text)
            news_cat = news.find_all('h2', {'class': 'b-item__title'})
            news_url = news.find_all('li', {'class': 'b-item col-6_xs-6'})

            for a in range(len(news_cat)):
                for i in pars_res:
                    s = str(news_cat[a])
                    s = s[26:-5]
                    s_res = s.split(' ')
                    for y in s_res:
                        if i == y:
                            print(i)
                            print(news_url[a])
                            bot.send_message(message.chat.id, news_url[a])

        def otvprim():
            # ОТВ ПРИМ
            url = 'https://otvprim.ru/category/news'
            headers = {
                'Host': 'otvprim.ru',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'}

            r = requests.get(url, headers=headers)

            from bs4 import BeautifulSoup
            # МЕНЯЕМ КОДИРОВКУ
            news = BeautifulSoup(r.content, "html.parser")
            # news = bs4.BeautifulSoup(r.text)
            news_cat = news.find_all('div', {'class': 'genpost-entry-content'})

            for a in range(len(news_cat)):
                for i in pars_res:
                    s = str(news_cat[a])
                    s = s[26:-5]
                    s_res = s.split(' ')
                    for y in s_res:
                        if i == y:
                            print(i)
                            print(news_cat[a])
                            bot.send_message(message.chat.id, news_cat[a])

        def admprimkray():
            # Администрация приморского края
            url = 'https://primorsky.ru/news/'
            headers = {
                'Host': 'primorsky.ru',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'}

            r = requests.get(url, headers=headers)
            # print(r)

            # МЕНЯЕМ КОДИРОВКУ
            news = BeautifulSoup(r.content, "html.parser")
            # news = bs4.BeautifulSoup(r.text)
            news_cat = news.find_all('div', {'class': 'row news-blk mb-4'})
            # print(news_cat)

            for a in range(len(news_cat)):
                for i in pars_res:
                    s = str(news_cat[a])
                    s = s[26:-5]
                    s_res = s.split(' ')
                    for y in s_res:
                        if i == y:
                            print(i)
                            print(news_cat[a])
                            #bot.send_message(message.from_user.id, news_cat[a])

        #print(n)
        print("Вести Приморья")
        vestiprim()
        print("ОТВ ПРИМ")
        otvprim()
        print("Администрация Приморского края")
        admprimkray()



bot.infinity_polling()
