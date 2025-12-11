import mysql.connector
from mysql.connector import errorcode 

def print_users_with_roles():
    connection = None
    cursor = None
    
    # 1. настройки подключения 
    config = {
        'host': 'localhost',
        'database': 'mushok',
        'user': 'mewo',
        'password': 'mushok229mewo' 
    }

    try:
        #подключение к серверу MySQL
        connection = mysql.connector.connect(**config) #словарь config для чистоты
        
        # проверка и подтверждение подключения
        if connection.is_connected():
            print("Успешное подключение к базе данных MySQL.")
            
            # 2. создание курсора для выполнения запросов
            cursor = connection.cursor()

            # 3. SQL-запрос (вывод списка пользователей)
            sql_query = """
            SELECT 
                u.user_id, 
                u.username, 
                u.first_name, 
                u.last_name, 
                r.role_name
            FROM users u
            LEFT JOIN user_roles ur ON u.user_id = ur.user_id
            LEFT JOIN roles r ON ur.role_id = r.role_id;
            """
            cursor.execute(sql_query)
            records = cursor.fetchall()

            # 4. вывод данных
            print("\nСписок зарегистрированных пользователей и их прав:")
            print("-" * 60)
            print(f"{'ID':<5} | {'Логин':<15} | {'Имя Фамилия':<20} | {'Роль':<15}")
            print("-" * 60)

            for row in records:
                user_id = row[0]
                login = row[1]
                full_name = f"{row[2] or ''} {row[3] or ''}".strip() 
                role = row[4] if row[4] else "Нет роли"

                print(f"{user_id:<5} | {login:<15} | {full_name:<20} | {role:<15}")
            print("-" * 60)


    # 5. обработка ошибок 
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Ошибка подключения: Неверный логин или пароль для MySQL.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Ошибка подключения: База данных '{config['database']}' не существует.")
        else:
            print(f"Неизвестная ошибка MySQL: {err}")

    finally:
        # 6. закрываем соединение
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("\nСоединение с базой данных закрыто.")

# запуск функции
if __name__ == "__main__":
    print_users_with_roles()