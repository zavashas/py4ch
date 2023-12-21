import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        
        create_users_table = '''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT NOT NULL
        );
        '''

        create_types_of_cards_table = '''
    CREATE TABLE IF NOT EXISTS types_of_cards (
        card_id INTEGER PRIMARY KEY AUTOINCREMENT,
        card_type TEXT UNIQUE NOT NULL
    );
    '''

        create_types_of_activities_table = '''
    CREATE TABLE IF NOT EXISTS types_of_activities (
        activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity_type TEXT UNIQUE NOT NULL
    );
    '''
        create_appointments_table = '''
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                activity_id INTEGER NOT NULL,
                trainer_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (activity_id) REFERENCES types_of_activities (activity_id),
                FOREIGN KEY (trainer_id) REFERENCES users (user_id)
            );
        '''

        self.cursor.execute(create_appointments_table)
        self.conn.commit()

        self.cursor.execute(create_users_table)
       
        self.cursor.execute(create_types_of_cards_table)
        self.cursor.execute(create_types_of_activities_table)

        self.conn.commit()
    
    def make_appointment(self, user_id, activity_id, trainer_id):
        
        make_appointment_query = '''
            INSERT INTO appointments (user_id, activity_id, trainer_id)
            VALUES (?, ?, ?);
        '''
        trainer_id = trainer_id if trainer_id is not None else 'NULL'

        self.cursor.execute(make_appointment_query, (user_id, activity_id, trainer_id))
        self.conn.commit()

    def view_client_appointments(self, trainer_id):
        # Просмотр записей на занятия для клиентов, назначенных определенному тренеру
        view_appointments_query = '''
            SELECT users.full_name, types_of_activities.activity_type
            FROM users
            JOIN appointments ON users.user_id = appointments.user_id
            JOIN types_of_activities ON appointments.activity_id = types_of_activities.activity_id
            WHERE appointments.trainer_id = ?;
        '''

        self.cursor.execute(view_appointments_query, (trainer_id,))
        appointments = self.cursor.fetchall()

        if appointments:
            print("Список клиентов, записанных к вам:")
            for appointment in appointments:
                print(f"{appointment[0]} - {appointment[1]}")
            print()
        else:
            print("У вас нет записанных клиентов.\n")
    def view_all_types_of_cards(self):
        
        view_types_of_cards_query = '''
        SELECT * FROM types_of_cards;
        '''

        self.cursor.execute(view_types_of_cards_query)
        types_of_cards = self.cursor.fetchall()

        if types_of_cards:
            print("Список всех типов карт:")
            for card in types_of_cards:
                print(f"{card[0]}. {card[1]}")
            print()
        else:
            print("Типов карт пока нет.\n")

    def view_all_types_of_activities(self):
        
        view_types_of_activities_query = '''
        SELECT * FROM types_of_activities;
        '''

        self.cursor.execute(view_types_of_activities_query)
        types_of_activities = self.cursor.fetchall()

        if types_of_activities:
            print("Список всех типов занятий:")
            for activity in types_of_activities:
                print(f"{activity[0]}. {activity[1]}")
            print()
        else:
            print("Типов занятий пока нет.\n")

    def add_type_of_card(self, card_type):
        
        add_type_of_card_query = '''
        INSERT INTO types_of_cards (card_type) VALUES (?);
        '''

        self.cursor.execute(add_type_of_card_query, (card_type,))
        self.conn.commit()

    def add_type_of_activity(self, activity_type):
        
        add_type_of_activity_query = '''
        INSERT INTO types_of_activities (activity_type) VALUES (?);
        '''

        self.cursor.execute(add_type_of_activity_query, (activity_type,))
        self.conn.commit()   

    def add_user(self, user_data):
        
        insert_user_query = '''
        INSERT INTO users (username, password, role, full_name) 
        VALUES (?, ?, ?, ?);
        '''

        self.cursor.execute(insert_user_query, user_data)
        self.conn.commit()

    def get_user_by_credentials(self, username, password):
        
        get_user_query = '''
        SELECT * FROM users WHERE username=? AND password=?;
        '''

        self.cursor.execute(get_user_query, (username, password))
        user_data = self.cursor.fetchone()

        if user_data:
            return user_data
        else:
            return None

    def close_connection(self):
        self.conn.close()
        
    

    def get_user_data(self, user_id):
        # Получение данных пользователя по его ID
        get_user_data_query = '''
        SELECT * FROM users WHERE user_id=?;
        '''

        self.cursor.execute(get_user_data_query, (user_id,))
        user_data = self.cursor.fetchone()
        return user_data

    def update_user_data(self, user_id, new_full_name):
        # Обновление данных пользователя
        update_user_data_query = '''
        UPDATE users SET full_name=? WHERE user_id=?;
        '''

        self.cursor.execute(update_user_data_query, (new_full_name, user_id))
        self.conn.commit()

    def view_all_tovars(self):
        # Просмотр всех товаров
        tovars = self.get_all_tovars()

        if tovars:
            print("Список товаров:")
            for tovar in tovars:
                print(f"{tovar[0]}. {tovar[1]} - {tovar[2]} руб.")
            print()
        else:
            print("Товаров пока нет.\n")

    def add_order(self, user_id, tovar_id, quantity):
        # Добавление заказа
        add_order_query = '''
        INSERT INTO orders (user_id, tovar_id, quantity) VALUES (?, ?, ?);
        '''

        self.cursor.execute(add_order_query, (user_id, tovar_id, quantity))
        self.conn.commit()

    def delete_order(self, order_id):
        # Удаление заказа
        delete_order_query = '''
        DELETE FROM orders WHERE order_id=?;
        '''

        self.cursor.execute(delete_order_query, (order_id,))
        self.conn.commit()
        
    def update_type_of_card(self, card_id, new_card_type):
        # Изменение типа карты
        update_type_of_card_query = '''
        UPDATE types_of_cards SET card_type=? WHERE card_id=?;
        '''

        self.cursor.execute(update_type_of_card_query, (new_card_type, card_id))
        self.conn.commit()

    def delete_type_of_card(self, card_id):
        # Удаление типа карты
        delete_type_of_card_query = '''
        DELETE FROM types_of_cards WHERE card_id=?;
        '''

        self.cursor.execute(delete_type_of_card_query, (card_id,))
        self.conn.commit()

    def update_type_of_activity(self, activity_id, new_activity_type):
        # Изменение типа занятия
        update_type_of_activity_query = '''
        UPDATE types_of_activities SET activity_type=? WHERE activity_id=?;
        '''

        self.cursor.execute(update_type_of_activity_query, (new_activity_type, activity_id))
        self.conn.commit()

    def delete_type_of_activity(self, activity_id):
        # Удаление типа занятия
        delete_type_of_activity_query = '''
        DELETE FROM types_of_activities WHERE activity_id=?;
        '''

        self.cursor.execute(delete_type_of_activity_query, (activity_id,))
        self.conn.commit()
    def initialize_data(self):
        # Добавление начальных данных (типы карт и занятий)
        initial_data_query = '''
        INSERT OR IGNORE INTO types_of_cards (card_type) VALUES
            ('Basic'),
            ('Premium'),
            ('VIP');
        INSERT OR IGNORE INTO types_of_activities (activity_type) VALUES
            ('Yoga'),
            ('Pilates'),
            ('Cardio'),
            ('Weight Training');
        '''

        self.cursor.executescript(initial_data_query)
        self.conn.commit()

    def view_client_appointments(self, trainer_id):
        # Просмотр клиентов, записанных к тренеру
        view_appointments_query = '''
        SELECT users.full_name, types_of_activities.activity_type
        FROM users
        JOIN appointments ON users.user_id = appointments.user_id
        JOIN types_of_activities ON appointments.activity_id = types_of_activities.activity_id
        WHERE appointments.trainer_id = ?;
        '''

        self.cursor.execute(view_appointments_query, (trainer_id,))
        appointments = self.cursor.fetchall()

        if appointments:
            print("Список клиентов, записанных к вам:")
            for appointment in appointments:
                print(f"{appointment[0]} - {appointment[1]}")
            print()
        else:
            print("У вас нет записанных клиентов.\n")
    def view_all_users(self):
        # Просмотр всех пользователей
        view_all_users_query = '''
            SELECT * FROM users;
        '''

        self.cursor.execute(view_all_users_query)
        users = self.cursor.fetchall()

        if users:
            print("Список всех пользователей:")
            for user in users:
                print(f"{user[0]}. {user[1]} - {user[3]} ({user[4]})")
            print()
        else:
            print("Пользователей пока нет.\n")
    def update_user(self, user_id, new_username, new_password, new_role, new_full_name):
        # Изменение данных пользователя
            update_user_query = '''
                UPDATE users 
                SET username=?, password=?, role=?, full_name=? 
                WHERE user_id=?;
            '''

            self.cursor.execute(update_user_query, (new_username, new_password, new_role, new_full_name, user_id))
            self.conn.commit()

    def delete_user(self, user_id):
            # Удаление пользователя
            delete_user_query = '''
                DELETE FROM users WHERE user_id=?;
            '''

            self.cursor.execute(delete_user_query, (user_id,))
            self.conn.commit()
            
    def view_all_trainers(self):
        view_all_trainers_query = '''
            SELECT * FROM users WHERE role = 'trainer';
        '''

        self.cursor.execute(view_all_trainers_query)
        trainers = self.cursor.fetchall()

        if trainers:
            print("Список всех тренеров:")
            for trainer in trainers:
                print(f"{trainer[0]}. {trainer[4]}")
            print()
        else:
            print("Тренеров пока нет.\n")

    def view_clients_for_trainer(self, trainer_id):
        view_clients_for_trainer_query = '''
            SELECT users.full_name, types_of_activities.activity_type
            FROM users
            JOIN appointments ON users.user_id = appointments.user_id
            JOIN types_of_activities ON appointments.activity_id = types_of_activities.activity_id
            WHERE appointments.trainer_id = ?;
        '''

        self.cursor.execute(view_clients_for_trainer_query, (trainer_id,))
        clients = self.cursor.fetchall()

        if clients:
            print("Список клиентов, записанных к вам:")
            for client in clients:
                print(f"{client[0]} - {client[1]}")
            print()
        else:
            print("У вас нет записанных клиентов.\n")
            
class Client:
    def __init__(self, db):
        self.db = db
        self.user_data = None

    def client_menu(self):
        while True:
            print("1. Просмотр доступных занятий")
            print("2. Запись на занятие")
            print("3. Изменение своих данных")
            print("4. Выход")

            client_choice = input("Выберите действие: ")

            if client_choice == "1":
                self.db.view_all_types_of_activities()
            elif client_choice == "2":
                self.db.view_all_types_of_activities()
                activity_id = int(input("Введите ID занятия для записи: "))
                self.db.view_all_trainers()
                trainer_id = int(input("Введите ID тренера (оставьте пустым, если не выбран): ") or 0)
                self.db.make_appointment(self.user_data[0], activity_id, trainer_id)
                print("Вы успешно записаны на занятие!\n")
            
            elif client_choice == "3":
                new_full_name = input("Введите новое полное имя: ")
                self.db.update_user_data(self.user_data[0], new_full_name)
                print("Данные пользователя успешно изменены!\n")
            elif client_choice == "4":
                print("Выход из аккаунта.\n")
                break
            else:
                print("Неверный выбор. Повторите попытку.\n")

class Trainer:
    def __init__(self, db):
        self.db = db
        self.user_data = None

    def trainer_menu(self):
        while True:
            print("1. Просмотр клиентов, записанных к вам")
            print("2. Просмотр всех клиентов")
            print("3. Изменение своих данных")
            print("4. Выход")

            trainer_choice = input("Выберите действие: ")

            if trainer_choice == "1":
                self.db.view_clients_for_trainer(self.user_data[0])
            elif trainer_choice == "2":
                self.db.view_all_users()
            elif trainer_choice == "3":
                new_full_name = input("Введите новое полное имя: ")
                self.db.update_user_data(self.user_data[0], new_full_name)
                print("Данные пользователя успешно изменены!\n")
            elif trainer_choice == "4":
                print("Выход из аккаунта.\n")
                break
            else:
                print("Неверный выбор. Повторите попытку.\n")

class Admin:
    def __init__(self, db):
        self.db = db
        self.user_data = None

    def admin_menu(self):
        while True:
            print("1. Просмотр и изменение типов карт")
            print("2. Просмотр и изменение типов занятий")
            print("3. Просмотр всех пользователей")
            print("4. Изменение своих данных")
            print("5. Выход")

            admin_choice = input("Выберите действие: ")

            if admin_choice == "1":
                self.db.view_all_types_of_cards()
                admin_action = input("Выберите действие (1 - добавить, 2 - изменить, 3 - удалить, 4 - назад): ")
                if admin_action == "1":
                    new_card_type = input("Введите новый тип карты: ")
                    self.db.add_type_of_card(new_card_type)
                    print("Тип карты успешно добавлен!\n")
                elif admin_action == "2":
                    card_id = int(input("Введите ID типа карты для изменения: "))
                    new_card_type = input("Введите новый тип карты: ")
                    self.db.update_type_of_card(card_id, new_card_type)
                    print("Тип карты успешно изменен!\n")
                elif admin_action == "3":
                    card_id = int(input("Введите ID типа карты для удаления: "))
                    self.db.delete_type_of_card(card_id)
                    print("Тип карты успешно удален!\n")
                elif admin_action == "4":
                    pass
            elif admin_choice == "2":
                self.db.view_all_types_of_activities()
                admin_action = input("Выберите действие (1 - добавить, 2 - изменить, 3 - удалить, 4 - назад): ")
                if admin_action == "1":
                    new_activity_type = input("Введите новый тип занятия: ")
                    self.db.add_type_of_activity(new_activity_type)
                    print("Тип занятия успешно добавлен!\n")
                elif admin_action == "2":
                    activity_id = int(input("Введите ID типа занятия для изменения: "))
                    new_activity_type = input("Введите новый тип занятия: ")
                    self.db.update_type_of_activity(activity_id, new_activity_type)
                    print("Тип занятия успешно изменен!\n")
                elif admin_action == "3":
                    activity_id = int(input("Введите ID типа занятия для удаления: "))
                    self.db.delete_type_of_activity(activity_id)
                    print("Тип занятия успешно удален!\n")
                elif admin_action == "4":
                    pass
            elif admin_choice == "3":
                self.db.view_all_users()
                admin_action = input("Выберите действие (1 - добавить, 2 - изменить, 3 - удалить, 4 - назад): ")
                if admin_action == "1":
                    new_username = input("Введите логин нового пользователя: ")
                    new_password = input("Введите пароль нового пользователя: ")
                    new_role = input("Выберите роль нового пользователя (client/trainer/admin): ")
                    new_full_name = input("Введите полное имя нового пользователя: ")

                    user_data = (new_username, new_password, new_role, new_full_name)
                    self.db.add_user(user_data)
                    print("Пользователь успешно добавлен!\n")
                elif admin_action == "2":
                    user_id = int(input("Введите ID пользователя для изменения: "))

                    current_user_data = self.db.get_user_data(user_id)
                    if current_user_data:
                        print("Текущие данные пользователя:")
                        print(f"Логин: {current_user_data[1]}")
                        print(f"Пароль: {current_user_data[2]}")
                        print(f"Роль: {current_user_data[3]}")
                        print(f"Полное имя: {current_user_data[4]}")

                        new_username = input("Введите новый логин (оставьте пустым, чтобы не изменять): ")
                        new_password = input("Введите новый пароль (оставьте пустым, чтобы не изменять): ")
                        new_role = input("Введите новую роль (оставьте пустым, чтобы не изменять): ")
                        new_full_name = input("Введите новое полное имя (оставьте пустым, чтобы не изменять): ")

                        # Заменяем пустые данные новыми данными, если они были введены
                        new_username = new_username if new_username else current_user_data[1]
                        new_password = new_password if new_password else current_user_data[2]
                        new_role = new_role if new_role else current_user_data[3]
                        new_full_name = new_full_name if new_full_name else current_user_data[4]

                        self.db.update_user(user_id, new_username, new_password, new_role, new_full_name)
                        print("Данные пользователя успешно изменены!\n")
                    else:
                        print("Пользователь с указанным ID не найден.\n")
                elif admin_action == "3":
                    user_id = int(input("Введите ID пользователя для удаления: "))
                    self.db.delete_user(user_id)
                    print("Пользователь успешно удален!\n")
                elif admin_action == "4":
                    pass
                else:
                    print("Неверный выбор. Повторите попытку.\n")
            elif admin_choice == "4":
                new_full_name = input("Введите новое полное имя: ")
                self.db.update_user_data(self.user_data[0], new_full_name)
                print("Данные пользователя успешно изменены!\n")
            elif admin_choice == "5":
                print("Выход из аккаунта.\n")
                break
            else:
                print("Неверный выбор. Повторите попытку.\n")
def register_user(db):
    print("Регистрация нового пользователя:")
    username = input("Введите логин: ")
    password = input("Введите пароль: ")
    role = input("Выберите роль (client/trainer/admin): ")
    full_name = input("Введите ваше полное имя: ")

    user_data = (username, password, role, full_name)
    db.add_user(user_data)
    print("Пользователь успешно зарегистрирован!\n")


def login(db):
    print("Авторизация:")
    username = input("Введите логин: ")
    password = input("Введите пароль: ")

    user_data = db.get_user_by_credentials(username, password)

    if user_data:
        print(f"Добро пожаловать, {user_data[4]} ({user_data[3]})!\n")
        return user_data
    else:
        print("Неправильные логин или пароль. Повторите попытку.\n")
        return None

def main():
    db = Database("fitness_club.db")
    db.create_tables()
    db.initialize_data()

    user_data = None

    while True:
        print("1. Регистрация")
        print("2. Авторизация")
        print("3. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            register_user(db)
        elif choice == "2":
            user_data = login(db)
        elif choice == "3":
            break
        else:
            print("Неверный выбор. Повторите попытку.\n")

    while user_data:
        if user_data[3] == "client":
            client = Client(db)
            client.user_data = user_data
            client.client_menu()
        elif user_data[3] == "trainer":
            trainer = Trainer(db)
            trainer.user_data = user_data
            trainer.trainer_menu()
        elif user_data[3] == "admin":
            admin = Admin(db)
            admin.user_data = user_data
            admin.admin_menu()
            
        user_data = login(db)

    db.close_connection()

if __name__ == "__main__":
    main()



   
