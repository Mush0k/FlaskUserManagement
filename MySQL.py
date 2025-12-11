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
           select 
           u.user_id, 
           u.username, 
           u.first_name,
           u.last_name, 
           GROUP_CONCAT(r.role_name SEPARATOR ', ') as role_list
from users u
left join user_roles ur on u.user_id = ur.user_id -- users -> user_roles -> roles
left join roles r on ur.role_id = r.role_id
group by u.user_id, u.first_name, u.last_name -- группировка
order by u.user_id;
            """
            cursor.execute(sql_query)
            records = cursor.fetchall()

            # 4. вывод данных
            print("\nСписок зарегистрированных пользователей и их прав:")
            print("-" * 75)
            print(f"{'ID':<5} | {'Логин':<15} | {'Имя':<15} | {'Фамилия':<15} | {'Роль':<30}")
            print("-" * 75)

            for row in records:
                user_id = row[0]
                username = row[1]
                first_name = row[2]
                last_name = row[3]
                role = row[4] if row[4] else "Нет роли"

                print(f"{user_id:<5} | {username:<15} | {first_name:<15} | {last_name:<15} | {role:<30}")
            print("-" * 75)


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