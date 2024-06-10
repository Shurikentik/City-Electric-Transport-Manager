from data.postgresql_connection import Database
from data.db_config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
import hashlib


# Клас "Співробітник"
class Employee:
    def __init__(self, employee_id=None, full_name=None, employee_position=None, address=None, phone_number=None, login=None, employee_password=None):
        self.employee_id = employee_id
        self.full_name = full_name
        self.employee_position = employee_position
        self.address = address
        self.phone_number = phone_number
        self.login = login
        self.employee_password = employee_password

    # Функція хешування паролю
    @staticmethod
    def hash_password(password):
        password_bytes = password.encode('utf-8')
        hashed_password = hashlib.sha256(password_bytes).hexdigest()
        return hashed_password

    def save(self):
        hashed_password = Employee.hash_password(self.employee_password)
        query = """
            INSERT INTO employee (full_name, employee_position, address, phone_number, login, employee_password)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING employee_id
        """
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            self.employee_id = db.execute_query_and_return_one(query, (self.full_name, self.employee_position, self.address, self.phone_number, self.login, hashed_password))[0]

    def update(self):
        if not self.employee_id:
            raise ValueError("Cannot update record without employee_id")
        query = """
            UPDATE employee SET full_name = %s, employee_position = %s, address = %s, phone_number = %s, login = %s
            WHERE employee_id = %s
        """
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, (self.full_name, self.employee_position, self.address, self.phone_number, self.login, self.employee_id))

    def delete(self):
        if not self.employee_id:
            raise ValueError("Cannot delete record without employee_id")
        query = "DELETE FROM employee WHERE employee_id = %s"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, (self.employee_id,))

    # Метод для оновлення паролю
    def update_password(self, old_password, new_password):
        # Перевіряється старий введений пароль
        if not Employee.hash_password(old_password) == self.employee_password:
            raise ValueError("Старий пароль введено неправильно")
        # Хешується і встановлюється новий заданий пароль
        hashed_new_password = Employee.hash_password(new_password)
        self.employee_password = hashed_new_password
        # Оновлюється пароль у таблиці бази даних
        query = """
                    UPDATE employee SET employee_password = %s
                    WHERE employee_id = %s
                """
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, (self.employee_password, self.employee_id))

    @staticmethod
    def get_all():
        query = "SELECT * FROM employee"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            return [Employee(*row) for row in db.fetch_data(query)]

    @staticmethod
    def get_by_id(employee_id):
        query = "SELECT * FROM employee WHERE employee_id = %s"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            result = db.fetch_data(query, (employee_id,))
            if result:
                return Employee(*result[0])
            return None

    @staticmethod
    def get_all_for_table():
        query = """
                SELECT 
                    employee_id AS "id",
                    full_name AS "ПІБ",
                    employee_position AS "Посада",
                    address AS "Адреса",
                    phone_number AS "Номер телефону",
                    login AS "Логін"
                FROM Employee
            """
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            rows = db.fetch_data(query)
            return [
                {
                    "id": row[0],
                    "ПІБ": row[1],
                    "Посада": row[2],
                    "Адреса": row[3],
                    "Номер телефону": row[4],
                    "Логін": row[5]
                }
                for row in rows
            ]

    # Функція верифікації логіну і паролю
    @staticmethod
    def verify_login_password(login, password):
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            query = "SELECT employee_id, full_name, employee_position, address, phone_number, login, employee_password FROM employee WHERE login = %s"
            params = (login,)
            result = db.fetch_data(query, params)

            if result:
                employee_id, full_name, employee_position, address, phone_number, login, hashed_db_password = result[0]
                hashed_input_password = Employee.hash_password(password)

                if hashed_input_password == hashed_db_password:
                    return Employee(employee_id, full_name, employee_position, address, phone_number, login,
                                    hashed_db_password)
        return None

    # Функція перевірки унікальності логіну
    @staticmethod
    def is_login_unique(login):
        query = "SELECT 1 FROM employee WHERE login = %s"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            result = db.fetch_data(query, (login,))
            return len(result) == 0

    @staticmethod
    def get_all_drivers():
        query = "SELECT * FROM employee WHERE employee_position = 'Водій'"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            return [Employee(*row) for row in db.fetch_data(query)]
