from flask import (
    Flask, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    make_response, 
    flash
)
import mysql.connector
from mysql.connector import errorcode
import secrets
from logic.catalog_builder import catalog_builder
from logic.slugify import slugify

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

#    ФУНКЦИИИ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#проверка авторизации в БД 
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
        
        #!!! теперь возвращает не true/false, а result (user_id) или None
        result = cursor.fetchone()
        return result[0] if result else None

    except mysql.connector.Error as err:
        # вывод ошибки подключения БД в консоль (если БД выключена, логин неверный и т.п.)
        print(f"Ошибка БД при проверке: {err}")
        return None
    finally:
        if cnx and cnx.is_connected():
            cnx.close()

#функиця для получения данных пользователя
def get_user_data_by_id(user_id):
    cnx = None
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor(dictionary=True) # dictionary=True для удобного получения данных
        
        query = "SELECT user_id, username, first_name, last_name, patronymic, email FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        
        return cursor.fetchone() # возвращаем словарь с данными пользователя
    except mysql.connector.Error as err:
        print(f"Ошибка БД при получении данных: {err}")
        return None
    finally:
        if cnx and cnx.is_connected():
            cnx.close()

def generate_session_hash():
   # генерирует случайный хеш для сессии,
    return secrets.token_hex(16) #16(N) случайных байтов. каждый байт кодируется в виде 16-иричных символов
   #функция по итогу возвращает строку длиной 2N (как раз 32 символа)

def insert_session_hash(user_id, session_hash):
    #записывает новый сессионный хеш в таблицу sessions

    cnx = None
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()
        
        # записываем user_id и хеш сессии
        query = "INSERT INTO sessions (user_id, session_hash) VALUES (%s, %s)"
        cursor.execute(query, (user_id, session_hash))
        
        cnx.commit() 
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка БД при записи сессии: {err}")
        return False
    finally:
        if cnx and cnx.is_connected():
            cnx.close()

#ПОИСК АЙДИ ПО ШЕХУ СЕССИИ
def get_user_id_by_session_hash(session_hash):
   #ищет user_id по хешу сессии в таблице sessions.

    cnx = None
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()
        
        # ищем ID пользователя по токену сессии
        # в идеале здесь должна быть проверка expires_at
        query = "SELECT user_id FROM sessions WHERE session_hash = %s"
        cursor.execute(query, (session_hash,))
        
        result = cursor.fetchone()
        
        # возвращаем user_id или None
        return result[0] if result else None
    except mysql.connector.Error as err:
        print(f"Ошибка БД при поиске сессии: {err}")
        return None
    finally:
        if cnx and cnx.is_connected():
            cnx.close()
#ФУНКИЦЯ ОЧИСТКИ ХЭША
def delete_session_hash(session_hash):
    #удаляет сессию из таблицы sessions при выходе пользователя
    cnx = None
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()
        
        # удаляем запись по хешу
        query = "DELETE FROM sessions WHERE session_hash = %s"
        cursor.execute(query, (session_hash,))
        
        cnx.commit() 
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка БД при удалении сессии: {err}")
        return False
    finally:
        if cnx and cnx.is_connected():
            cnx.close()
#ПОЛУЧЕНИЕ СПИСКА КАТЕГОРИЙ
def get_all_categories():
    cnx = None
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        # получаю данные как словарь
        cursor = cnx.cursor(dictionary=True) 
        
        #  возврщаювсе строки из таблицы categories
        query = "SELECT category_id, parent_id, category_name, slug, order_index FROM categories"
        cursor.execute(query)
        
        return cursor.fetchall() # возвращаю список всех категорий
    except mysql.connector.Error as err:
        print(f"Ошибка БД при получении категорий: {err}")
        return []
    finally:
        if cnx and cnx.is_connected():
            cnx.close()

# 3. роуты

# роут для главной страницы 
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
        
        user_id = check_user_credentials(username, password) #функция проверки, в идеале возвращает ID
        # вывод принятых данных в консоль 
        print(f"\n   Полученные данные   ")
        print(f"Логин: {username}")
        print(f"Пароль: {password}")
        print(f"----------------------------------\n")
        
 #обработка куки
        if user_id:
            # 1. генерируем токен
            session_hash = generate_session_hash()
            
            # 2. сохраняем токен в таблице sessions
            if not insert_session_hash(user_id, session_hash):
                message = "Ошибка сервера при создании сессии."
                return render_template('login.html', message=message)

            # 3. создаем ответ
            resp = make_response(redirect(url_for('profile_page'))) #перекидывает на страницу профиля
            
            # 4. устанавливаем куки с именем session_hash, равным токену
            resp.set_cookie('session_hash', session_hash, max_age=3600) 
            return resp
        else:
            message = "Неверный логин или пароль!"

    # отображение шаблона login.html и передача ему сообщния
    return render_template('login.html', message=message)

#роут для профиля
@app.route('/profile')
def profile_page():
    # 1. читаем session_hash из куки
    session_hash = request.cookies.get('session_hash')
    
    # 2. проверяем наличие токена
    if not session_hash:
        # если куки нет, возвращаем код 401
        return redirect(url_for('login_page')), 401 
        
    # 3. ищем user_id по токену в таблице sessions 
    user_id = get_user_id_by_session_hash(session_hash)
    
    if not user_id:
        # если сессия не действительна (токен не найден или истек)
        return redirect(url_for('logout_page')) 
        
    # получаем персональную информацию из БД users (теперь у нас есть user_id)
    user_data = get_user_data_by_id(user_id)
    
    if not user_data:
        # если пользователь удален
        return redirect(url_for('logout_page')) 
        
    # 5. отображаем страницу профиля
    return render_template('profile.html', user = user_data)


# роут для выхода
@app.route('/logout')
def logout_page():
    session_hash = request.cookies.get('session_hash') #считываем токен и очищаем хеш
    if session_hash:
        delete_session_hash(session_hash)
    # 1. создаем ответ
    resp = make_response(redirect(url_for('home'))) #пользователя перекинет на главную страницу
    
    # 2. удаляем хеш
    resp.set_cookie('session_hash', '', expires = 0) 
    
    return resp

# роут для отображения каталога
@app.route('/catalog')
def catalog_page():
    
    #получаю список категорий
    all_categories_data = get_all_categories()
    
    #None для поиска корневых элементов (там, где parent_id = NULL)
    catalog_html = catalog_builder(None, all_categories_data) 
    
    return render_template('catalog.html', catalog_html=catalog_html)


# 4. точка входа для запуска

if __name__ == '__main__':
    # запуск сервера
    app.run(debug=True)