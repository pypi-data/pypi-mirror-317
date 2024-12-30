import sqlite3
import datetime
from datetime import timedelta

class SecurityModule:
    def __init__(self):
        self.conn = sqlite3.connect('users.db', check_same_thread=False)
        self.create_table()
        self.valid_numbers = self.load_valid_numbers('alldatabase.txt')

    def load_valid_numbers(self, filename):
        """Загружает номера телефонов из текстового файла в множество."""
        try:
            with open(filename, 'r') as file:
                return {line.strip() for line in file if line.strip()}
        except FileNotFoundError:
            print(f"Файл {filename} не найден. Пожалуйста, создайте файл с номерами телефонов.")
            return set()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- уникальный идентификатор пользователя
                phone TEXT UNIQUE NOT NULL,              -- номер телефона
                role TEXT DEFAULT 'user'                  -- роль пользователя, по умолчанию 'user'
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.conn.commit()

    def is_valid_phone(self, phone):
        """Проверяет, что номер состоит только из цифр и имеет разумную длину."""
        return phone.isdigit() and 10 <= len(phone) <= 15 and phone.startswith('7')

    def user_exists(self, phone):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users WHERE phone = ?', (phone,))
        return cursor.fetchone()[0] > 0

    def register_user(self, phone):
        if not self.is_valid_phone(phone):
            print("Неверный номер телефона.")
            return False

        if phone not in self.valid_numbers:
            print("Такой номер телефона не найден в списке разрешенных.")
            return False

        # Проверяем, существует ли пользователь с данным номером
        if self.user_exists(phone):
            return True  # Возвращаем True, так как пользователь уже зарегистрирован

        # Если пользователя нет, то регистрируем его
        with self.conn:
            cursor = self.conn.cursor()
            try:
                cursor.execute('INSERT INTO users (phone) VALUES (?)', (phone,))
                print("Пользователь успешно зарегистрирован.")
                return True
            except sqlite3.IntegrityError:
                print("Ошибка регистрации пользователя. Номер телефона уже зарегистрирован.")
                return False

    def get_user_id_by_phone(self, phone):
        """Возвращает идентификатор пользователя по номеру телефона."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM users WHERE phone = ?', (phone,))
        result = cursor.fetchone()
        return result[0] if result else None

    def check_user_registration(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        return user is not None

    def assign_role(self, phone, role):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET role = ? WHERE phone = ?', (role, phone))
        self.conn.commit()

    def is_spam(self, user_id):
        cursor = self.conn.cursor()
        ten_seconds_ago = datetime.datetime.now() - timedelta(seconds=10)
        cursor.execute('''
                SELECT COUNT(*) FROM user_actions 
                WHERE user_id = ? AND action_time >= ?
            ''', (user_id, ten_seconds_ago))

        action_count = cursor.fetchone()[0]
        return action_count > 5

    def log_user_action(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO user_actions (user_id) VALUES (?)', (user_id,))
        self.conn.commit()

    def is_number_in_database(self, phone):
        """Проверяет, существует ли номер телефона в базе данных."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users WHERE phone = ?', (phone,))
        exists = cursor.fetchone()[0] > 0
        return exists


    def close(self):
        self.conn.close()
