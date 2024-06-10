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
            self.tariff_id = db.execute_query_and_return_one(query, (self.ticket_price, self.validity_type_id, self.transport_type_id))[0]

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
    def from_db_row(row):
        return Tariff(
            tariff_id=row[0],
            ticket_price=float(row[1]),
            validity_type_id=row[2],
            transport_type_id=row[3]
        )

    @staticmethod
    def get_all():
        query = "SELECT * FROM Tariff"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            return [Tariff.from_db_row(row) for row in db.fetch_data(query)]

    @staticmethod
    def get_by_id(tariff_id):
        query = "SELECT * FROM Tariff WHERE tariff_id = %s"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            result = db.fetch_data(query, (tariff_id,))
            if result:
                return Tariff.from_db_row(result[0])
            return None

    @staticmethod
    def get_all_for_table():
        query = """
                SELECT 
                    t.tariff_id AS "id",
                    tt.transport_name AS "Тип транспорту",
                    vt.validity_name AS "Термін чинності",
                    t.ticket_price AS "Ціна квитка"
                FROM Tariff t
                JOIN TransportType tt ON t.transport_type_id = tt.transport_type_id
                JOIN ValidityType vt ON t.validity_type_id = vt.validity_type_id
            """
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            rows = db.fetch_data(query)
            return [
                {
                    "id": row[0],
                    "Тип транспорту": row[1],
                    "Термін чинності": row[2],
                    "Ціна квитка": row[3]
                }
                for row in rows
            ]

    @staticmethod
    def get_tariff_by_transport_and_validity(transport_type_id, validity_type_id):
        query = "SELECT * FROM Tariff WHERE transport_type_id = %s AND validity_type_id = %s"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            result = db.fetch_data(query, (transport_type_id, validity_type_id))
            if result:
                return Tariff.from_db_row(result[0])
            return None

    # Функція отримання тарифу та ціни для квитка
    @staticmethod
    def get_tariff_id_and_price(transport_type_id, validity_type_id):
        query = "SELECT tariff_id, ticket_price FROM Tariff WHERE transport_type_id = %s AND validity_type_id = %s"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            result = db.fetch_data(query, (transport_type_id, validity_type_id))
            if result:
                return result[0][0], float(result[0][1])
            else:
                return None, None

    # Функція розрахунку решти
    @staticmethod
    def get_rest(price, passed_money):
        return passed_money - float(price)
