from data.postgresql_connection import Database
from data.db_config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


# Клас "Розклад"
class Schedule:
    def __init__(self, schedule_id=None, day_of_week=None, start_time=None, end_time=None, route_id=None, transport_id=None):
        self.schedule_id = schedule_id
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time
        self.route_id = route_id
        self.transport_id = transport_id

    @staticmethod
    def from_db_row(row):
        return Schedule(
            schedule_id=row[0],
            day_of_week=row[1],
            start_time=row[2],
            end_time=row[3],
            route_id=row[4],
            transport_id=row[5]
        )

    def save(self):
        query = """
            INSERT INTO Schedule (day_of_week, start_time, end_time, route_id, transport_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING schedule_id
        """
        params = (self.day_of_week, self.start_time, self.end_time, self.route_id, self.transport_id)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            self.schedule_id = db.execute_query_and_return_one(query, params)[0]

    def update(self):
        if not self.schedule_id:
            raise ValueError("Cannot update record without schedule_id")
        query = """
            UPDATE Schedule
            SET day_of_week = %s, start_time = %s, end_time = %s, route_id = %s, transport_id = %s
            WHERE schedule_id = %s
        """
        params = (self.day_of_week, self.start_time, self.end_time, self.route_id, self.transport_id, self.schedule_id)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, params)

    def delete(self):
        if not self.schedule_id:
            raise ValueError("Cannot delete record without schedule_id")
        query = "DELETE FROM Schedule WHERE schedule_id = %s"
        params = (self.schedule_id,)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, params)

    @staticmethod
    def get_all():
        query = "SELECT * FROM Schedule"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            rows = db.fetch_data(query)
            return [Schedule.from_db_row(row) for row in rows]

    @staticmethod
    def get_by_id(schedule_id):
        query = "SELECT * FROM Schedule WHERE schedule_id = %s"
        params = (schedule_id,)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            row = db.fetch_data(query, params)
            if row:
                return Schedule.from_db_row(row[0])
            return None

    @staticmethod
    def get_all_for_table():
        query = """
                SELECT 
                    s.schedule_id AS "id",
                    s.day_of_week AS "День тижня",
                    r.route_number AS "Номер маршруту",
                    t.transport_number AS "Номер транспорту",
                    s.start_time AS "Час початку",
                    s.end_time AS "Час завершення"
                FROM Schedule s
                JOIN Route r ON s.route_id = r.route_id
                JOIN Transport t ON s.transport_id = t.transport_id
            """
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            rows = db.fetch_data(query)
            return [
                {
                    "id": row[0],
                    "День тижня": row[1],
                    "Номер маршруту": row[2],
                    "Номер транспорту": row[3],
                    "Час початку": row[4],
                    "Час завершення": row[5]
                }
                for row in rows
            ]
