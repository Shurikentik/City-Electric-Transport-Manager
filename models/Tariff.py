from data.postgresql_connection import Database
from data.db_config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


# Клас "Тариф"
class Tariff:
    def __init__(self, tariff_id=None, ticket_price=None, validity_type_id=None, transport_type_id=None):
        self.tariff_id = tariff_id
        self.ticket_price = ticket_price
        self.validity_type_id = validity_type_id
        self.transport_type_id = transport_type_id

    def save(self):
        query = "INSERT INTO Tariff (ticket_price, validity_type_id, transport_type_id) VALUES (%s, %s, %s) RETURNING tariff_id"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            self.tariff_id = db.execute_query(query, (self.ticket_price, self.validity_type_id, self.transport_type_id))[0][0]

    def update(self):
        if not self.tariff_id:
            raise ValueError("Cannot update record without tariff_id")
        query = "UPDATE Tariff SET ticket_price = %s, validity_type_id = %s, transport_type_id = %s WHERE tariff_id = %s"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, (self.ticket_price, self.validity_type_id, self.transport_type_id, self.tariff_id))

    def delete(self):
        if not self.tariff_id:
            raise ValueError("Cannot delete record without tariff_id")
        query = "DELETE FROM Tariff WHERE tariff_id = %s"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, (self.tariff_id,))

    @staticmethod
    def get_all():
        query = "SELECT * FROM Tariff"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            return [Tariff(*row) for row in db.fetch_data(query)]

    @staticmethod
    def get_by_id(tariff_id):
        query = "SELECT * FROM Tariff WHERE tariff_id = %s"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            result = db.fetch_data(query, (tariff_id,))
            if result:
                return Tariff(*result[0])
            return None
