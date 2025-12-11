from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import errorcode

# 1. инициализация Flask и настройки БД

# создание экземпляра Flask-приложения
app = Flask(__name__)

# настройки подключения к БД 
DB_CONFIG = {
    'host': 'localhost',
    'database': 'mushok',
    'user': 'mewo',
    'password': 'mushok229mewo' 
}

# 2. проверка авторизации в БД 

def check_user_credentials(username, password):
  #проверка данных 
    cnx = None
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()

        # SQL-запрос для поиска пользователя
        #ПОМЕТКА: в моей бд используются
        #хэш-затыки паролей (например "hash1"), поэтому 
        # я использую их вместо самого пароля. в идеале конечно же
        #чтоб там был реальный хэш пароля и происходило какое-то сравнение(?)
        query = "SELECT user_id FROM users WHERE username = %s AND password_hash = %s"
        cursor.execute(query, (username, password))
        
        # если найдена хотя бы одна строка, возвращаем True (авторизация успешна)
        return cursor.fetchone() is not None

    except mysql.connector.Error as err:
        # вывод ошибки подключения БД в консоль (если БД выключена, логин неверный и т.п.)
        print(f"Ошибка БД при проверке: {err}")
        return False
    finally:
        if cnx and cnx.is_connected():
            cnx.close()



# 3. роуты

# роут для главной страницы (Пункт 4)
@app.route('/')
def home():
    # возвращаем простой роут, который открывается в браузере
    return render_template('home.html')


# роут для авторизации 
@app.route('/login', methods=['GET', 'POST']) #GET - показать форму, POST - принять данные
def login_page():
    message = None # Переменная для сообщения пользователю

    if request.method == 'POST':
        #принятие данных из фоурмы
        username = request.form['username']
        password = request.form['password']
        
        # вывод принятых данных в консоль 
        print(f"\n   Полученные данные   ")
        print(f"Логин: {username}")
        print(f"Пароль: {password}")
        print(f"----------------------------------\n")
        
 #обработка формы
        if check_user_credentials(username, password):
            message = "Авторизация прошла успешно!"
        else:
            message = "Неверный логин или пароль!"
            
    # отображение шаблона login.html и передача ему сообщния
    return render_template('login.html', message=message)


# 4. точка входа для запуска

if __name__ == '__main__':
    # запуск сервера
    app.run(debug=True)