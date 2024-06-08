from data.postgresql_connection import Database
from data.db_config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


# Клас "Пільга"
class Benefit:
    def __init__(self, benefit_id=None, benefit_name=None, discount_modifier=None):
        self.benefit_id = benefit_id
        self.benefit_name = benefit_name
        self.discount_modifier = discount_modifier

    def save(self):
        query = "INSERT INTO Benefit (benefit_name, discount_modifier) VALUES (%s, %s) RETURNING benefit_id"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            self.benefit_id = db.execute_query_and_return_one(query, (self.benefit_name, self.discount_modifier))[0]

    def update(self):
        if not self.benefit_id:
            raise ValueError("Cannot update record without benefit_id")
        query = "UPDATE Benefit SET benefit_name = %s, discount_modifier = %s WHERE benefit_id = %s"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, (self.benefit_name, self.discount_modifier, self.benefit_id))

    def delete(self):
        if not self.benefit_id:
            raise ValueError("Cannot delete record without benefit_id")
        query = "DELETE FROM Benefit WHERE benefit_id = %s"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, (self.benefit_id,))

    @staticmethod
    def get_all():
        query = "SELECT * FROM Benefit"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            return [Benefit.from_db_row(row) for row in db.fetch_data(query)]

    @staticmethod
    def from_db_row(row):
        return Benefit(
            benefit_id=row[0],
            benefit_name=row[1],
            discount_modifier=float(row[2])
        )

    @staticmethod
    def get_by_id(benefit_id):
        query = "SELECT * FROM Benefit WHERE benefit_id = %s"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            result = db.fetch_data(query, (benefit_id,))
            if result:
                return Benefit.from_db_row(result[0])
            return None

    # Функція застосування пільгової знижки до квитка
    def apply_benefit(self, price):
        return round(price * (1 - self.discount_modifier), 2)
