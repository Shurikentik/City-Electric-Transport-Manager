from data.postgresql_connection import Database
from data.db_config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


# Клас "Вихід транспорту на маршрут"
class TransportAssignment:
    def __init__(self, transport_assignment_id=None, transport_id=None, route_id=None, schedule_id=None,
                 employee_id=None, departure_time=None):
        self.transport_assignment_id = transport_assignment_id
        self.transport_id = transport_id
        self.route_id = route_id
        self.schedule_id = schedule_id
        self.employee_id = employee_id
        self.departure_time = departure_time

    @staticmethod
    def from_db_row(row):
        return TransportAssignment(
            transport_assignment_id=row[0],
            transport_id=row[1],
            route_id=row[2],
            schedule_id=row[3],
            employee_id=row[4],
            departure_time=row[5]
        )

    def save(self):
        query = """
            INSERT INTO TransportAssignment (transport_id, route_id, schedule_id, employee_id, departure_time)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING transport_assignment_id
        """
        params = (self.transport_id, self.route_id, self.schedule_id, self.employee_id, self.departure_time)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            self.transport_assignment_id = db.execute_query_and_return_one(query, params)[0]

    def update(self):
        if not self.transport_assignment_id:
            raise ValueError("Cannot update record without transport_assignment_id")
        query = """
            UPDATE TransportAssignment
            SET transport_id = %s, route_id = %s, schedule_id = %s, employee_id = %s, departure_time = %s
            WHERE transport_assignment_id = %s
        """
        params = (self.transport_id, self.route_id, self.schedule_id, self.employee_id,
                  self.departure_time, self.transport_assignment_id)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, params)

    def delete(self):
        if not self.transport_assignment_id:
            raise ValueError("Cannot delete record without transport_assignment_id")
        query = "DELETE FROM TransportAssignment WHERE transport_assignment_id = %s"
        params = (self.transport_assignment_id,)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, params)

    @staticmethod
    def get_all():
        query = "SELECT * FROM TransportAssignment"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            rows = db.fetch_data(query)
            return [TransportAssignment.from_db_row(row) for row in rows]

    @staticmethod
    def get_by_id(transport_assignment_id):
        query = "SELECT * FROM TransportAssignment WHERE transport_assignment_id = %s"
        params = (transport_assignment_id,)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            row = db.fetch_data(query, params)
            if row:
                return TransportAssignment.from_db_row(row[0])
            return None

    @staticmethod
    def get_all_for_table():
        query = """
                SELECT 
                    ta.transport_assignment_id AS "id",
                    t.transport_number AS "Номер транспорту",
                    r.route_number AS "Номер маршруту",
                    e.full_name AS "Водій",
                    s.start_time AS "Час виходу за розкладом",
                    ta.departure_time AS "Реальний час"
                FROM TransportAssignment ta
                LEFT JOIN Transport t ON ta.transport_id = t.transport_id
                LEFT JOIN Route r ON ta.route_id = r.route_id
                LEFT JOIN Employee e ON ta.employee_id = e.employee_id
                LEFT JOIN Schedule s ON ta.schedule_id = s.schedule_id
            """
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            rows = db.fetch_data(query)
            return [
                {
                    "id": row[0],
                    "Номер транспорту": row[1],
                    "Номер маршруту": row[2],
                    "Водій": row[3],
                    "Час виходу за розкладом": row[4],
                    "Реальний час": row[5]
                }
                for row in rows
            ]
