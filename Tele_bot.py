# загружаем нужные библиотеки
import cv2
import pandas as pd
from datetime import datetime
import time
import telebot
import matplotlib.pyplot as plt
from telebot import types
import numpy as np
from tabulate import tabulate

TOKEN = '5839618154:AAF4BcIfbGmJYUMYoZYi75ifKK-RpPOWjXM'
bot = telebot.TeleBot(TOKEN)

df = pd.DataFrame(columns=['Дата', 'Время', 'Количество'])


# блок распознавание и определения количества лиц
cap = cv2.VideoCapture(1)
face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


# Telegram Bot
@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Запись")
    btn2 = types.KeyboardButton("График")
    btn3 = types.KeyboardButton("График_год")
    btn4 = types.KeyboardButton("Анализ")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.from_user.id, "МЕНЮ:", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text(message):
    cap = cv2.VideoCapture(1)
    face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    if message.text == 'Запись':
        #now = datetime.now()
        current_date = datetime.now()
        t = ''

        ret, img = cap.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face.detectMultiScale(gray, 1.1, 19)
        i = 0

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]  # Вырезаем область с лицами
            roi_color = img[y:y + h, x:x + w]
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            i += 1

        s = [{'Дата': current_date.strftime("%Y%m%d"), 'Время': current_date.strftime("%H%M%S"), 'Количество': i}]
        # Записываем в файл
        cv2.imwrite('cam.png', img)
        cap.release()
        cv2.destroyAllWindows()
        bot.send_photo(message.from_user.id, photo=open('cam.png', 'rb'))
        bot.send_message(message.chat.id, 'Количество людей в кадре - ' + str(i))

        df = pd.DataFrame(columns=['Дата', 'Время', 'Количество'])
        df = df._append(s, ignore_index=True)
        df_read = pd.read_csv('cam.csv')
        df_read = df_read.drop(['Unnamed: 0'], axis=1)
        frames = [df_read, df]
        res1 = pd.concat(frames)
        res1.to_csv('cam.csv')
        tt = (tabulate(res1, tablefmt="pipe", headers="keys"))
        bot.send_message(message.from_user.id, tt)
        time.sleep(1)
        print(res1)


    if message.text == 'График':
        df_read = pd.read_csv('cam.csv')
        df_read = df_read.drop(['Unnamed: 0'], axis=1)

        #Добавление разделителей в Дату и Время
        df_new = pd.DataFrame(columns=['Дата', 'Время', 'Количество'])
        for r in range(len(df_read['Дата'])):
            s = df_read['Дата'][r]
            t = df_read['Время'][r]
            n = df_read['Количество'][r]
            s = str(s)
            t = str(t)
            print(t)
            s_d = s[0:4] + '/' + s[4:6] + '/' + s[6:]
            s_t = t[0:2] + ':' + t[2:4] + ':' + t[4:]
            s_new = [{'Дата': s_d, 'Время': s_t, 'Количество': n}]
            df_new = df_new._append(s_new, ignore_index=True)
            print(df_new)


        #st_date = df_read['Дата']
        st_name = df_new['Время']
        marks = df_new['Количество']
        x = list(st_name)
        y = list(marks)
        #plt.bar(x, y, color='g', width=0.5, label="Количество")
        plt.plot(x, y)
        plt.xlabel('Время')
        plt.ylabel('Количество')
        plt.title('Наполняемость зала за период времени')
        #plt.legend()
        #plt.bar(x, y)
        plt.savefig('Graphic.png', transparent=True)
        #plt.show()
        bot.send_photo(message.from_user.id, photo=open('Graphic.png', 'rb'))



    if message.text == 'График_год':
        df_read = pd.read_csv('cam.csv')
        df_read = df_read.drop(['Unnamed: 0'], axis=1)
        # st_date = df_read['Дата']

        # Добавление разделителей в Дату и Время
        df_new = pd.DataFrame(columns=['Дата', 'Время', 'Количество'])
        for r in range(len(df_read['Дата'])):
            s = df_read['Дата'][r]
            t = df_read['Время'][r]
            n = df_read['Количество'][r]
            s = str(s)
            t = str(t)
            print(t)
            s_d = s[0:4] + '/' + s[4:6] + '/' + s[6:]
            s_t = t[0:2] + ':' + t[2:4] + ':' + t[4:]
            s_new = [{'Дата': s_d, 'Время': s_t, 'Количество': n}]
            df_new = df_new._append(s_new, ignore_index=True)
            #print(df_new)


        st_name = df_new['Дата']
        marks = df_new['Количество']
        x = list(st_name)
        y = list(marks)
        plt.plot(x, y)
        plt.xlabel('Дата')
        plt.ylabel('Количество')
        plt.title('Наполняемость зала за период времени')
        # plt.legend()
        # plt.bar(x, y)
        plt.savefig('Graphic.png', transparent=True)
        # plt.show()
        bot.send_photo(message.from_user.id, photo=open('Graphic.png', 'rb'))

    if message.text == 'Анализ':
        df_read = pd.read_csv('cam.csv')
        df_read = df_read.drop(['Unnamed: 0'], axis=1)


        '''st_name = df_read['Время']
        marks = df_read['Количество']
        x = list(st_name)
        y = list(marks)
        plt.plot(x, y)
        plt.xlabel('Время')
        plt.ylabel('Количество')
        plt.title('Наполняемость зала за период времени')
        plt.show()
        df_read.info()'''
        X = df_read[['Дата', 'Время']]
        y = df_read['Количество']
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
        from sklearn.linear_model import LinearRegression
        regressor = LinearRegression()
        regressor.fit(X_train, y_train)

        coeff_df = pd.DataFrame(regressor.coef_, X.columns, columns=['Coefficient'])
        print(coeff_df)

        # print(regressor.intercept_)
        y_pred = regressor.predict(X_test)
        df2 = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
        print(df2)


        tt = (tabulate(df2, tablefmt="pipe", headers="keys"))
        bot.send_message(message.from_user.id, tt)


bot.infinity_polling()
