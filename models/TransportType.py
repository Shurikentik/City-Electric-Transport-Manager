from data.postgresql_connection import Database
from data.db_config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


# Клас "Тип транспорту"
class TransportType:
    def __init__(self, transport_type_id=None, transport_name=None):
        self.transport_type_id = transport_type_id
        self.transport_name = transport_name

    def save(self):
        query = "INSERT INTO TransportType (transport_name) VALUES (%s) RETURNING transport_type_id"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            self.transport_type_id = db.execute_query(query, (self.transport_name,))[0][0]

    def update(self):
        if not self.transport_type_id:
            raise ValueError("Cannot update record without transport_type_id")
        query = "UPDATE TransportType SET transport_name = %s WHERE transport_type_id = %s"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, (self.transport_name, self.transport_type_id))

    def delete(self):
        if not self.transport_type_id:
            raise ValueError("Cannot delete record without transport_type_id")
        query = "DELETE FROM TransportType WHERE transport_type_id = %s"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, (self.transport_type_id,))

    @staticmethod
    def get_all():
        query = "SELECT * FROM TransportType"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            return [TransportType(*row) for row in db.fetch_data(query)]

    @staticmethod
    def get_by_id(transport_type_id):
        query = "SELECT * FROM TransportType WHERE transport_type_id = %s"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            result = db.fetch_data(query, (transport_type_id,))
            if result:
                return TransportType(*result[0])
            return None
