from data.postgresql_connection import Database
from data.db_config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


# Клас "Транспорт"
class Transport:
    def __init__(self, transport_id=None, transport_number=None, availability=None, technical_condition=None,
                 transport_type_id=None, employee_id=None):
        self.transport_id = transport_id
        self.transport_number = transport_number
        self.availability = availability
        self.technical_condition = technical_condition
        self.transport_type_id = transport_type_id
        self.employee_id = employee_id

    @staticmethod
    def from_db_row(row):
        return Transport(
            transport_id=row[0],
            transport_number=row[1],
            availability=row[2],
            transport_type_id=row[3],
            employee_id=row[4],
            technical_condition=row[5]
        )

    def save(self):
        query = """
            INSERT INTO Transport (transport_number, availability, technical_condition, transport_type_id, employee_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING transport_id
        """
        params = (self.transport_number, self.availability, self.technical_condition,
                  self.transport_type_id, self.employee_id)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            self.transport_id = db.execute_query_and_return_one(query, params)[0]

    def update(self):
        if not self.transport_id:
            raise ValueError("Cannot update record without transport_id")
        query = """
            UPDATE Transport
            SET transport_number = %s, availability = %s, technical_condition = %s, 
                transport_type_id = %s, employee_id = %s
            WHERE transport_id = %s
        """
        params = (self.transport_number, self.availability, self.technical_condition,
                  self.transport_type_id, self.employee_id, self.transport_id)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, params)

    def delete(self):
        if not self.transport_id:
            raise ValueError("Cannot delete record without transport_id")
        query = "DELETE FROM Transport WHERE transport_id = %s"
        params = (self.transport_id,)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, params)

    @staticmethod
    def get_all():
        query = "SELECT * FROM Transport"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            rows = db.fetch_data(query)
            return [Transport.from_db_row(row) for row in rows]

    @staticmethod
    def get_by_id(transport_id):
        query = "SELECT * FROM Transport WHERE transport_id = %s"
        params = (transport_id,)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            row = db.fetch_data(query, params)
            if row:
                return Transport.from_db_row(row[0])
            return None

    @staticmethod
    def is_transport_number_exists(transport_number):
        query = "SELECT COUNT(*) FROM Transport WHERE transport_number = %s"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            result = db.fetch_data(query, (transport_number,))
            return result[0][0] > 0
