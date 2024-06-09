import psycopg2
from tkinter import messagebox


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

    def fetch_query_result(self, query, params=None):
        try:
            if params:
                self.cur.execute(query, params)
            else:
                self.cur.execute(query)
            data = self.cur.fetchall()
            column_names = [desc[0] for desc in self.cur.description]
            return column_names, data
        except Exception as e:
            messagebox.showerror("Помилка", str(e))
            return None, None

    def execute_query_and_return_one(self, query, params=None):
        try:
            if params:
                self.cur.execute(query, params)
            else:
                self.cur.execute(query)
            self.conn.commit()
            return self.cur.fetchone()  # Повернення результату запиту
        except Exception as e:
            messagebox.showerror("Помилка", str(e))
            return None
