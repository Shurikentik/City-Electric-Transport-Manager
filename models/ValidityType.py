from data.postgresql_connection import Database
from data.db_config import DB_HOST, DB_NAME, DB_PORT, DB_USER, DB_PASSWORD


# Клас "Тип чинності квитка"
class ValidityType:
    def __init__(self, validity_type_id=None, validity_name=None):
        self.validity_type_id = validity_type_id
        self.validity_name = validity_name

    def save(self):
        query = "INSERT INTO ValidityType (validity_name) VALUES (%s) RETURNING validity_type_id"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            self.validity_type_id = db.execute_query_and_return_one(query, (self.validity_name,))[0]

    def update(self):
        if not self.validity_type_id:
            raise ValueError("Cannot update record without validity_type_id")
        query = "UPDATE ValidityType SET validity_name = %s WHERE validity_type_id = %s"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, (self.validity_name, self.validity_type_id))

    def delete(self):
        if not self.validity_type_id:
            raise ValueError("Cannot delete record without validity_type_id")
        query = "DELETE FROM ValidityType WHERE validity_type_id = %s"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, (self.validity_type_id,))

    @staticmethod
    def get_all():
        query = "SELECT * FROM ValidityType"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            return [ValidityType(*row) for row in db.fetch_data(query)]

    @staticmethod
    def get_by_id(validity_type_id):
        query = "SELECT * FROM ValidityType WHERE validity_type_id = %s"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            result = db.fetch_data(query, (validity_type_id,))
            if result:
                return ValidityType(*result[0])
            return None
