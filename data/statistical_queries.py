from data.postgresql_connection import Database
from data.db_config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


# Запит "Список розкладів з номерами маршрутів і транспорту, у порядку спадання часу виходу"
def get_schedule_with_route_and_transport():
    query = """
    SELECT t.transport_number, r.route_number, s.start_time, s.end_time
    FROM Transport t
    JOIN Schedule s ON t.transport_id = s.transport_id
    JOIN Route r ON s.route_id = r.route_id
    ORDER BY s.start_time DESC;
    """
    with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
        return db.fetch_data(query)


# Запит "Усі маршрути, які починаються зі станції, назва якої містить "Центр""
def get_routes_starting_with_center():
    query = """
    SELECT route_id, route_number, start_station, end_station
    FROM Route
    WHERE start_station LIKE 'Центр%';
    """
    with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
        return db.fetch_data(query)


# Запит "Усі квитки, продані за останній місяць"
def get_tickets_sold_in_last_30_days():
    query = """
    SELECT ticket_id, price, sale_date
    FROM Ticket
    WHERE sale_date BETWEEN NOW() - INTERVAL '30 DAY' AND NOW();
    """
    with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
        return db.fetch_data(query)


# Запит "Дохід компанії за останній місяць"
def get_total_income_last_30_days():
    query = """
    SELECT SUM(price) AS total_income
    FROM Ticket
    WHERE sale_date >= CURRENT_DATE - INTERVAL '30 days';
    """
    with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
        result = db.fetch_data(query)
        return result[0][0] if result else 0


# Запит "Кількість квитків, проданих кожним касиром"
def get_tickets_sold_by_employee():
    query = """
    SELECT e.full_name, COUNT(t.ticket_id) AS tickets_sold
    FROM Ticket t
    JOIN Employee e ON t.employee_id = e.employee_id
    GROUP BY e.full_name
    ORDER BY tickets_sold DESC;
    """
    with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
        return db.fetch_data(query)


# Запит "Транспортні засоби, які наразі знаходяться на ремонті"
def get_transport_under_repair():
    query = """
    SELECT t.transport_id, t.transport_number
    FROM Transport t
    WHERE t.transport_id = ANY (SELECT transport_id FROM Repair WHERE end_date IS NULL);
    """
    with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
        return db.fetch_data(query)


# Запит "Транспорт, який доступний і виїжджав на маршрут протягом останнього тижня"
def get_active_transport_in_last_week():
    query = """
    SELECT t1.transport_id, t1.transport_number
    FROM Transport t1
    WHERE t1.availability = TRUE AND EXISTS (
        SELECT 1
        FROM TransportAssignment ta
        WHERE ta.transport_id = t1.transport_id AND ta.departure_time > NOW() - INTERVAL '7 DAY'
    );
    """
    with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
        return db.fetch_data(query)


# Запит "Транспортні засоби, які не знаходяться на ремонті"
def get_available_transport():
    query = """
    SELECT t.transport_id, t.transport_number
    FROM Transport t
    WHERE NOT EXISTS (
        SELECT 1
        FROM Repair r
        WHERE r.transport_id = t.transport_id AND r.end_date IS NULL
    );
    """
    with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
        return db.fetch_data(query)


# Запит "Активний транспорт і транспорт у ремонті"
def get_transport_status_summary():
    query = """
    SELECT 'Активний транспорт' AS category, transport_number, availability
    FROM Transport
    WHERE availability = TRUE
    UNION
    SELECT 'Ремонтований транспорт' AS category, transport_number, FALSE AS availability
    FROM Transport
    JOIN Repair ON Transport.transport_id = Repair.transport_id
    WHERE Repair.end_date IS NULL
    ORDER BY category;
    """
    with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
        return db.fetch_data(query)
