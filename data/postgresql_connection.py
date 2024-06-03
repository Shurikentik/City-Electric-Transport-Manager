from tkinter import messagebox
import psycopg2
import hashlib


# Клас для підключення до бази даних
class Database:
    def __init__(self, host, port, dbname, user, password):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Помилка", "Unable to connect to the database: " + str(e))

    def disconnect(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cur.execute(query, params)
            else:
                self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def fetch_data(self, query, params=None):
        try:
            if params:
                self.cur.execute(query, params)
            else:
                self.cur.execute(query)
            return self.cur.fetchall()
        except Exception as e:
            messagebox.showerror("Помилка", str(e))
            return None


def hash_password(password):
    # Перетворюємо пароль у байтовий об'єкт, оскільки хеш-функція очікує байти
    password_bytes = password.encode('utf-8')

    # Використовуємо SHA-256 для хешування паролю
    hashed_password = hashlib.sha256(password_bytes).hexdigest()

    return hashed_password


def add_employee(db, full_name, position, address, phone_number, login, password):
    hashed_password = hash_password(password)
    query = """
        INSERT INTO employee (full_name, employee_position, address, phone_number, login, employee_password)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (full_name, position, address, phone_number, login, hashed_password)
    db.execute_query(query, params)


def verify_login_password(db, login, password):
    # Отримуємо дані з бази даних
    query = "SELECT employee_position, employee_password FROM employee WHERE login = %s"
    params = (login,)
    result = db.fetch_data(query, params)

    # Перевіряємо, чи отримали ми результат з бази даних
    if result:
        # Отримуємо з бази даних захешований пароль і посаду працівника
        employee_position, hashed_db_password = result[0]

        # Хешуємо пароль, який ввів користувач для порівняння з базовим
        hashed_input_password = hash_password(password)

        # Порівнюємо хешовані паролі
        if hashed_input_password == hashed_db_password:
            # Якщо паролі співпадають, повертаємо посаду працівника
            return employee_position
    # Якщо пароль не співпадає або користувача не знайдено, повертаємо None
    return None
