from data.postgresql_connection import Database
from data.db_config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


# Клас "Квиток"
class Ticket:
    def __init__(self, ticket_id=None, price=None, validity_date=None, is_active=None, sale_date=None,
                 tariff_id=None, benefit_id=None, employee_id=None):
        self.ticket_id = ticket_id
        self.price = price
        self.validity_date = validity_date
        self.is_active = is_active
        self.sale_date = sale_date
        self.tariff_id = tariff_id
        self.benefit_id = benefit_id
        self.employee_id = employee_id

    @staticmethod
    def from_db_row(row):
        return Ticket(
            ticket_id=row[0],
            price=row[1],
            validity_date=row[2],
            is_active=row[3],
            sale_date=row[4],
            tariff_id=row[5],
            benefit_id=row[6],
            employee_id=row[7]
        )

    def save(self):
        query = """
            INSERT INTO Ticket (price, validity_date, is_active, sale_date, tariff_id, benefit_id, employee_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING ticket_id
        """
        params = (self.price, self.validity_date, self.is_active, self.sale_date,
                  self.tariff_id, self.benefit_id, self.employee_id)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            self.ticket_id = db.execute_query(query, params)[0][0]

    def update(self):
        if not self.ticket_id:
            raise ValueError("Cannot update record without ticket_id")
        query = """
            UPDATE Ticket
            SET price = %s, validity_date = %s, is_active = %s, sale_date = %s, 
                tariff_id = %s, benefit_id = %s, employee_id = %s
            WHERE ticket_id = %s
        """
        params = (self.price, self.validity_date, self.is_active, self.sale_date,
                  self.tariff_id, self.benefit_id, self.employee_id, self.ticket_id)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, params)

    def delete(self):
        if not self.ticket_id:
            raise ValueError("Cannot delete record without ticket_id")
        query = "DELETE FROM Ticket WHERE ticket_id = %s"
        params = (self.ticket_id,)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, params)

    @staticmethod
    def get_all():
        query = "SELECT * FROM Ticket"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            rows = db.fetch_data(query)
            return [Ticket.from_db_row(row) for row in rows]

    @staticmethod
    def get_by_id(ticket_id):
        query = "SELECT * FROM Ticket WHERE ticket_id = %s"
        params = (ticket_id,)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            row = db.fetch_data(query, params)
            if row:
                return Ticket.from_db_row(row[0])
            return None
