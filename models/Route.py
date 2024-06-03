from data.postgresql_connection import Database
from data.db_config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


# Клас "Маршрут"
class Route:
    def __init__(self, route_id=None, route_number=None, start_station=None, end_station=None):
        self.route_id = route_id
        self.route_number = route_number
        self.start_station = start_station
        self.end_station = end_station

    @staticmethod
    def from_db_row(row):
        return Route(
            route_id=row[0],
            route_number=row[1],
            start_station=row[2],
            end_station=row[3]
        )

    def save(self):
        query = """
            INSERT INTO Route (route_number, start_station, end_station)
            VALUES (%s, %s, %s)
            RETURNING route_id
        """
        params = (self.route_number, self.start_station, self.end_station)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            self.route_id = db.execute_query(query, params)[0][0]

    def update(self):
        if not self.route_id:
            raise ValueError("Cannot update record without route_id")
        query = """
            UPDATE Route
            SET route_number = %s, start_station = %s, end_station = %s
            WHERE route_id = %s
        """
        params = (self.route_number, self.start_station, self.end_station, self.route_id)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, params)

    def delete(self):
        if not self.route_id:
            raise ValueError("Cannot delete record without route_id")
        query = "DELETE FROM Route WHERE route_id = %s"
        params = (self.route_id,)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            db.execute_query(query, params)

    @staticmethod
    def get_all():
        query = "SELECT * FROM Route"
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            rows = db.fetch_data(query)
            return [Route.from_db_row(row) for row in rows]

    @staticmethod
    def get_by_id(route_id):
        query = "SELECT * FROM Route WHERE route_id = %s"
        params = (route_id,)
        with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
            row = db.fetch_data(query, params)
            if row:
                return Route.from_db_row(row[0])
            return None
