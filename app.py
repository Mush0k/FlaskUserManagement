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

#инициализация Flask и настройки БД

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

#вставка нового контента
def insert_new_content(user_id, category_id, type_id, title, content_body):
    cnx = None
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()
        content_slug = slugify(title)
        
        query = """
        INSERT INTO content 
        (user_id, category_id, type_id, title, slug, content_body, status, published_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """
        
        default_status = 'Draft' 
        
        cursor.execute(query, (
            user_id, 
            category_id, 
            type_id, 
            title, 
            content_slug, 
            content_body,
            default_status  
        ))
        
        cnx.commit() 
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка БД при добавлении материала: {err}")
        return False
    finally:
        if cnx and cnx.is_connected():
            cnx.close()

#удаление 
def delete_content_by_id(content_id):
    cnx = None
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()
        
        #удаляю по айди
        query = "DELETE FROM content WHERE content_id = %s"
        cursor.execute(query, (content_id,)) 
        
        cnx.commit() 
        # проверка
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        print(f"Ошибка БД при удалении материала: {err}")
        return False
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




# Получение списка категорий для выпадающего меню
def get_all_categories():
    cnx = None
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        query = "SELECT category_id, category_name FROM categories ORDER BY category_name"
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Ошибка БД при получении категорий: {err}")
        return []
    finally:
        if cnx and cnx.is_connected():
            cnx.close()

# вставка нового материала
def insert_new_content(user_id, category_id, type_id, title, content_body):
    cnx = None
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()
        content_slug = slugify(title)
        
        query = """
        INSERT INTO content 
        (user_id, category_id, type_id, title, slug, content_body, status, published_at) 
        VALUES (%s, %s, %s, %s, %s, %s, 'Draft', NOW())
        """
        
        cursor.execute(query, (user_id, category_id, type_id, title, content_slug, content_body))
        
        cnx.commit() 
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка БД при добавлении материала: {err}")
        return False
    finally:
        if cnx and cnx.is_connected():
            cnx.close()

# получение списка всех материалов для таблицы
def get_all_content():
    cnx = None
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor(dictionary=True)
        
        # JOIN с users, чтобы получить имя автора (username)
        query = """
        SELECT 
            c.content_id, c.title, c.status, c.published_at, c.user_id,
            u.username AS author_name 
        FROM content c
        JOIN users u ON c.user_id = u.id
        ORDER BY c.published_at DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Ошибка БД при получении списка материалов: {err}")
        return []
    finally:
        if cnx and cnx.is_connected():
            cnx.close()

# получение данных одного материала для редактирования
def get_content_by_id(content_id):
    cnx = None
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM content WHERE content_id = %s"
        cursor.execute(query, (content_id,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Ошибка БД при получении материала: {err}")
        return None
    finally:
        if cnx and cnx.is_connected():
            cnx.close()

# обновление данных материала
def update_content(content_id, category_id, type_id, title, content_body, status):
    cnx = None
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()
        content_slug = slugify(title)
        
        query = """
        UPDATE content SET 
            category_id = %s, type_id = %s, title = %s, slug = %s, 
            content_body = %s, status = %s
        WHERE content_id = %s
        """
        
        cursor.execute(query, (category_id, type_id, title, content_slug, content_body, status, content_id))
        
        cnx.commit() 
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        print(f"Ошибка БД при обновлении материала: {err}")
        return False
    finally:
        if cnx and cnx.is_connected():
            cnx.close()

# удаление материала
def delete_content_by_id(content_id):
    cnx = None
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()
        query = "DELETE FROM content WHERE content_id = %s"
        cursor.execute(query, (content_id,))
        cnx.commit() 
        return cursor.rowcount > 0 
    except mysql.connector.Error as err:
        print(f"Ошибка БД при удалении материала: {err}")
        return False
    finally:
        if cnx and cnx.is_connected():
            cnx.close()

#проверка прав
def get_content_author_and_user_role(content_id, current_user_id):
    cnx = None
    result = {'content_user_id': None, 'user_role_id': None} 
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()
        
        # 1. Получаем ID автора материала (user_id из content)
        query_author = "SELECT user_id FROM content WHERE content_id = %s"
        cursor.execute(query_author, (content_id,))
        content_user_id_data = cursor.fetchone()
        if content_user_id_data:
            result['content_user_id'] = content_user_id_data[0]
            
        # 2. Получаем ЧИСЛОВОЙ ID роли текущего пользователя (role_id из users)
        query_role = "SELECT role_id FROM users WHERE id = %s" 
        cursor.execute(query_role, (current_user_id,))
        user_role_data = cursor.fetchone()
        if user_role_data:
            result['user_role_id'] = user_role_data[0] 

        return result
    except mysql.connector.Error as err:
        print(f"Ошибка БД при проверке роли: {err}")
        return result
    finally:
        if cnx and cnx.is_connected():
            cnx.close()



ADMIN_ROLE_ID = 1 

#создание
@app.route('/content/create', methods=['GET', 'POST'])
def create_content_page():
    session_hash = request.cookies.get('session_hash')
    user_id = get_user_id_by_session_hash(session_hash)
    if not user_id:
        flash("Необходимо авторизоваться.", "error")
        return redirect(url_for('login_page'))
        
    categories = get_all_categories()
    
    if request.method == 'POST':
        title = request.form.get('title')
        content_body = request.form.get('content_body') 
        category_id = request.form.get('category_id')
        type_id = request.form.get('type_id')
        
        if not title or not content_body or not category_id:
            flash("Заполните все поля.", "error")
            return render_template('create_content.html', categories=categories)
            
        if insert_new_content(user_id, category_id, type_id, title, content_body):
            flash("Материал успешно добавлен!", "success")
            return redirect(url_for('list_content_page')) 
        else:
            flash("Ошибка сервера при добавлении материала.", "error")
            
    return render_template('create_content.html', categories=categories)


# вывод списка материалов
@app.route('/content/list')
def list_content_page():
    all_content = get_all_content()
    return render_template('list_content.html', content_list=all_content)


# редкатирвоание 
@app.route('/content/update', methods=['GET', 'POST'])
def edit_content_page():
    content_id = request.args.get('content_id')
    user_id = get_user_id_by_session_hash(request.cookies.get('session_hash'))
    
    if not user_id:
        flash("Необходимо авторизоваться.", "error")
        return redirect(url_for('login_page')) 
    if not content_id or not content_id.isdigit():
        flash("Неверный ID.", "error")
        return redirect(url_for('list_content_page'))
    
    # ПРОВЕРКА ПРАВ
    auth_data = get_content_author_and_user_role(content_id, user_id) 
    content_user_id = auth_data['content_user_id']
    user_role_id = auth_data['user_role_id']
    
    if content_user_id is None:
        flash(f"Материал ID {content_id} не найден.", "error")
        return redirect(url_for('list_content_page'))
    if not (content_user_id == user_id or user_role_id == ADMIN_ROLE_ID):
        flash("У вас нет прав для редактирования.", "error")
        return redirect(url_for('list_content_page'))
        
    categories = get_all_categories()
    possible_statuses = ['Draft', 'Published', 'Archived'] 
    content_data = get_content_by_id(content_id) 
    
    if request.method == 'POST':
        title = request.form.get('title')
        content_body = request.form.get('content_body') 
        category_id = request.form.get('category_id')
        type_id = request.form.get('type_id') or 1
        status = request.form.get('status')

        if update_content(content_id, category_id, type_id, title, content_body, status):
            flash("Материал успешно обновлен!", "success")
            return redirect(url_for('list_content_page')) 
        else:
            flash("Ошибка при обновлении.", "error")
            
    return render_template('edit_content.html', content=content_data, categories=categories, statuses=possible_statuses)


#удаление контента
@app.route('/content/delete', methods=['GET'])
def delete_content_action():
    content_id = request.args.get('content_id')
    user_id = get_user_id_by_session_hash(request.cookies.get('session_hash'))
    if not user_id or not content_id or not content_id.isdigit():
        flash("Ошибка доступа или неверный ID.", "error")
        return redirect(url_for('list_content_page'))
    
    # ПРОВЕРКА ПРАВ
    auth_data = get_content_author_and_user_role(content_id, user_id) 
    content_user_id = auth_data['content_user_id']
    user_role_id = auth_data['user_role_id']
    
    if content_user_id is None:
        flash(f"Материал не найден.", "error")
        return redirect(url_for('list_content_page'))

    if content_user_id == user_id or user_role_id == ADMIN_ROLE_ID:
        if delete_content_by_id(content_id):
            flash(f"Материал успешно удален!", "success")
        else:
            flash(f"Ошибка БД при удалении.", "error")
    else:
        flash("У вас нет прав для удаления.", "error")
        
    return redirect(url_for('list_content_page'))




@app.route('/content/create', methods=['GET', 'POST'])
def create_content_page():
    
    #прорверка авторизациии
    session_hash = request.cookies.get('session_hash')
    if not session_hash:
        flash("Для добавления материалов необходимо авторизоваться.")
        return redirect(url_for('login_page'))
        
    user_id = get_user_id_by_session_hash(session_hash)
    if not user_id:
        # если сессия недействительна, выходим
        return redirect(url_for('logout_page')) 

    categories = get_all_categories()
   
    if request.method == 'POST':
        title = request.form.get('title')
        content_body = request.form.get('content_body') 
        category_id = request.form.get('category_id')
        type_id = request.form.get('type_id') 
        
        if not title or not content_body or not category_id:
            flash("Пожалуйста, заполните все обязательные поля.", "error")
            return render_template('create_content.html', categories=categories)
            
        if insert_new_content(user_id, category_id, type_id, title, content_body):
            flash("Материал успешно добавлен!", "success")

            return redirect(url_for('list_content_page')) 
        else:
            flash("Ошибка сервера при добавлении материала. Проверьте консоль.", "error")
            

    return render_template('create_content.html', categories=categories)

#роут для удаления контента
@app.route('/content/delete', methods=['GET'])
def delete_content_action():
    
    content_id = request.args.get('content_id')
    
    # проверяю существует ли ваще контент
    if not content_id or not content_id.isdigit():
        flash("Неверный ID материала.", "error")
        return redirect(url_for('list_content_page'))
    
    # мб потом добавлю проверку что удаляет только автор или админ
    
    if delete_content_by_id(content_id):
        flash(f"Материал ID {content_id} успешно удален!", "success")
    else:
        flash(f"Материал ID {content_id} не найден или произошла ошибка.", "error")
        
    # перенаправляем обратно на список
    return redirect(url_for('list_content_page'))

# 4. точка входа для запуска

if __name__ == '__main__':
    # запуск сервера
    app.run(debug=True)