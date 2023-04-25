import telebot
from telebot import types
import vk_api
import requests
import pywhatkit
#import vk
import time
import requests

#для вацапа
from whatsapp_api_client_python import API as API
ID_INSTANCE = '1101812610'
API_TOKEN_INSTANCE = '3fdc7e9a572c476a9df6c25b71b851d412aedbe72801456a9f'
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
vk_token = "20dc356920dc356920dc3569bd23cf8e34220dc20dc3569449abcfa10f030776fca80d2"
vk_ses = vk_api.VkApi('studio25ru@ya.ru', 'NewLife25')



try:

   vk_ses.auth()
except vk_api.AuthError as error_msg:
   print(error_msg)
   exit(0)
vk = vk_ses.get_api()

my_app_id = 51624797
user_login = 'studio25ru@ya.ru'
user_password = 'NewLife25'

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Текст")
    btn2 = types.KeyboardButton("Фото")
    btn3 = types.KeyboardButton("Фото с текстом")
    markup.add(btn1, btn2, btn3)
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
            chatIds = ["79147279900@c.us"]
            resultCreate = greenAPI.groups.createGroup('Мой Лучегорск', chatIds)
            result = greenAPI.sending.sendFileByUpload(resultCreate.data['chatId'], "photo.jpg", 'PicFromDisk.png')
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
            chatIds = ["79147279900@c.us"]
            resultCreate = greenAPI.groups.createGroup('Мой Лучегорск', chatIds)

            if resultCreate.code == 200:
                print(resultCreate.data)
                resultSend = greenAPI.sending.sendMessage(resultCreate.data['chatId'], text)
                if resultSend.code == 200:
                    print(resultSend.data)
                else:
                    print(resultSend.error)
            else:
                print(resultCreate.error)

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
            chatIds = ["79147279900@c.us"]
            resultCreate = greenAPI.groups.createGroup('Мой Лучегорск', chatIds)
            result = greenAPI.sending.sendFileByUpload(resultCreate.data['chatId'], "photo.jpg", 'PicFromDisk.png', text)
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

bot.infinity_polling()
