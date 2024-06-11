from data.postgresql_connection import Database
from data.db_config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


# Клас "Ремонт"
class Repair:
    def __init__(self, repair_id=None, start_date=None, end_date=None, description=None, transport_id=None):
        self.repair_id = repair_id
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.transport_id = transport_id

    @staticmethod
    def from_db_row(row):
        return Repair(
            repair_id=row[0],
            start_date=row[1],
            end_date=row[2],
            description=row[3],
            transport_id=row[4]
        )

    def save(self):
        query = """
            INSERT INTO Repair (start_date, end_date, description, transport_id)
            VALUES (%s, %s, %s, %s)
            RETURNING repair_id
        """
        params = (self.start_date, self.end_date, self.description, self.transport_id)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            self.repair_id = db.execute_query(query, params)[0][0]

    def update(self):
        if not self.repair_id:
            raise ValueError("Cannot update record without repair_id")
        query = """
            UPDATE Repair
            SET start_date = %s, end_date = %s, description = %s, transport_id = %s
            WHERE repair_id = %s
        """
        params = (self.start_date, self.end_date, self.description, self.transport_id, self.repair_id)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, params)

    def delete(self):
        if not self.repair_id:
            raise ValueError("Cannot delete record without repair_id")
        query = "DELETE FROM Repair WHERE repair_id = %s"
        params = (self.repair_id,)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, params)

    @staticmethod
    def get_all():
        query = "SELECT * FROM Repair"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            rows = db.fetch_data(query)
            return [Repair.from_db_row(row) for row in rows]

    @staticmethod
    def get_by_id(repair_id):
        query = "SELECT * FROM Repair WHERE repair_id = %s"
        params = (repair_id,)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            row = db.fetch_data(query, params)
            if row:
                return Repair.from_db_row(row[0])
            return None

    @staticmethod
    def get_all_for_table():
        query = """
                SELECT 
                    r.repair_id AS "id",
                    t.transport_number AS "Номер транспорту",
                    r.start_date AS "Дата початку",
                    COALESCE(TO_CHAR(r.end_date, 'YYYY-MM-DD'), 'Не завершено') AS "Дата завершення",
                    r.description AS "Опис"
                FROM Repair r
                JOIN Transport t ON r.transport_id = t.transport_id
            """
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            rows = db.fetch_data(query)
            return [
                {
                    "id": row[0],
                    "Номер транспорту": row[1],
                    "Дата початку": row[2],
                    "Дата завершення": row[3],
                    "Опис": row[4]
                }
                for row in rows
            ]
