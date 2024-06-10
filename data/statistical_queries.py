from data.postgresql_connection import Database
from data.db_config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


# Запит "Квитки з пільгами"
def get_tickets_with_benefits():
    query = """
    SELECT 
        t.ticket_id AS id,
        t.price AS Ціна,
        tt.transport_name AS "Тип транспорту",
        vt.validity_name AS "Термін чинності",
        b.benefit_name AS "Пільга",
        t.sale_date AS "Дата продажу",
        e.full_name AS "Ким проданий"
    FROM Ticket t
    LEFT JOIN Tariff tar ON t.tariff_id = tar.tariff_id
    LEFT JOIN TransportType tt ON tar.transport_type_id = tt.transport_type_id
    LEFT JOIN ValidityType vt ON tar.validity_type_id = vt.validity_type_id
    LEFT JOIN Benefit b ON t.benefit_id = b.benefit_id
    LEFT JOIN Employee e ON t.employee_id = e.employee_id
    WHERE t.benefit_id IS NOT NULL
    ORDER BY t.price;
    """
    with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
        return db.fetch_query_result(query)


# Запит "Усі маршрути, які мають станцію, назва якої містить "Центр""
def get_routes_with_center_station():
    query = """
    SELECT 
        route_id AS id,
        route_number AS "Номер маршруту",
        start_station AS "Початкова станція",
        end_station AS "Кінцева станція"
    FROM Route
    WHERE start_station LIKE '%Центр%' OR end_station LIKE '%Центр%';
    """
    with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
        return db.fetch_query_result(query)


# Запит "Усі квитки, продані за останній місяць"
def get_tickets_sold_in_last_30_days():
    query = """
        SELECT 
            t.ticket_id AS "id", 
            t.price AS "Ціна",                        
            tt.transport_name AS "Тип транспорту", 
            vt.validity_name AS "Термін чинності", 
            COALESCE(b.benefit_name, 'Немає') AS "Пільга", 
            t.sale_date AS "Дата продажу",
            e.full_name AS "Ким проданий"
        FROM Ticket t
        LEFT JOIN Tariff tr ON t.tariff_id = tr.tariff_id
        LEFT JOIN TransportType tt ON tr.transport_type_id = tt.transport_type_id
        LEFT JOIN ValidityType vt ON tr.validity_type_id = vt.validity_type_id
        LEFT JOIN Benefit b ON t.benefit_id = b.benefit_id
        LEFT JOIN Employee e ON t.employee_id = e.employee_id
        WHERE sale_date BETWEEN NOW() - INTERVAL '30 DAY' AND NOW();
        """
    with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
        return db.fetch_query_result(query)


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
        SELECT 
            e.employee_id AS "ID касира",
            e.full_name AS "ПІБ касира",
            COUNT(*) AS "Кількість квитків"
        FROM Ticket t
        JOIN Employee e ON t.employee_id = e.employee_id
        GROUP BY e.employee_id, e.full_name;
        """
    with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
        return db.fetch_query_result(query)


# Запит "Транспортні засоби, які наразі знаходяться на ремонті"
def get_transport_under_repair():
    query = """
        SELECT 
            t.transport_id,
            tt.transport_name AS "Тип транспорту",
            t.transport_number AS "Номер транспорту",
            e.full_name AS "Під керуванням",
            CASE
                WHEN t.availability THEN 'Доступний'
                ELSE 'Зайнятий'
            END AS "Доступність",
            CASE
                WHEN t.technical_condition THEN 'Робочий'
                ELSE 'Несправний'
            END AS "Технічний стан"
        FROM Transport t
        LEFT JOIN TransportType tt ON t.transport_type_id = tt.transport_type_id
        LEFT JOIN Employee e ON t.employee_id = e.employee_id
        WHERE t.transport_id = ANY (SELECT transport_id FROM Repair WHERE end_date IS NULL);
        """
    with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
        return db.fetch_query_result(query)


# Квитки з ціною, меншою за середню на той же тип транспорту
def find_tickets_below_average_price():
    query = """
    SELECT 
        t.ticket_id AS "id", 
        t.price AS "Ціна",                        
        tt.transport_name AS "Тип транспорту", 
        vt.validity_name AS "Термін чинності", 
        COALESCE(b.benefit_name, 'Немає') AS "Пільга", 
        t.sale_date AS "Дата продажу",
        e.full_name AS "Ким проданий"
    FROM Ticket t
    LEFT JOIN Tariff tr ON t.tariff_id = tr.tariff_id
    LEFT JOIN TransportType tt ON tr.transport_type_id = tt.transport_type_id
    LEFT JOIN ValidityType vt ON tr.validity_type_id = vt.validity_type_id
    LEFT JOIN Benefit b ON t.benefit_id = b.benefit_id
    LEFT JOIN Employee e ON t.employee_id = e.employee_id
    WHERE t.price < (
        SELECT AVG(t2.price)
        FROM Ticket t2
        LEFT JOIN Tariff tr2 ON t2.tariff_id = tr2.tariff_id
        LEFT JOIN TransportType tt2 ON tr2.transport_type_id = tt2.transport_type_id
        WHERE tt2.transport_type_id = tt.transport_type_id
    );
    """
    with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
        return db.fetch_query_result(query)


# Маршрути без розкладу
def find_routes_without_schedule():
    query = """
    SELECT 
        r.route_id, 
        r.route_number as "Номер маршруту", 
        r.start_station as "Початкова станція", 
        r.end_station as "Кінцева станція"
    FROM Route r
    LEFT JOIN Schedule s ON r.route_id = s.route_id
    WHERE s.schedule_id IS NULL;
    """
    with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
        return db.fetch_query_result(query)


# Ціни квитків порівняно з середньою
def compare_ticket_prices_with_average():
    query = """
    SELECT 
        t.ticket_id AS "id", 
        t.price AS "Ціна",                        
        tt.transport_name AS "Тип транспорту", 
        vt.validity_name AS "Термін чинності", 
        COALESCE(b.benefit_name, 'Немає') AS "Пільга", 
        t.sale_date AS "Дата продажу",
        e.full_name AS "Ким проданий",
        'Нижча' as "Порівняно з середньою"
    FROM Ticket t
    LEFT JOIN Tariff tr ON t.tariff_id = tr.tariff_id
    LEFT JOIN TransportType tt ON tr.transport_type_id = tt.transport_type_id
    LEFT JOIN ValidityType vt ON tr.validity_type_id = vt.validity_type_id
    LEFT JOIN Benefit b ON t.benefit_id = b.benefit_id
    LEFT JOIN Employee e ON t.employee_id = e.employee_id
    WHERE t.price < (SELECT AVG(price) FROM Ticket)
    UNION
    SELECT 
        t.ticket_id AS "id", 
        t.price AS "Ціна",                        
        tt.transport_name AS "Тип транспорту", 
        vt.validity_name AS "Термін чинності", 
        COALESCE(b.benefit_name, 'Немає') AS "Пільга", 
        t.sale_date AS "Дата продажу",
        e.full_name AS "Ким проданий",
        'Вища' as "Порівняно з середньою"
    FROM Ticket t
    LEFT JOIN Tariff tr ON t.tariff_id = tr.tariff_id
    LEFT JOIN TransportType tt ON tr.transport_type_id = tt.transport_type_id
    LEFT JOIN ValidityType vt ON tr.validity_type_id = vt.validity_type_id
    LEFT JOIN Benefit b ON t.benefit_id = b.benefit_id
    LEFT JOIN Employee e ON t.employee_id = e.employee_id
    WHERE t.price > (SELECT AVG(price) FROM Ticket)
    UNION
    SELECT 
        t.ticket_id AS "id", 
        t.price AS "Ціна",                        
        tt.transport_name AS "Тип транспорту", 
        vt.validity_name AS "Термін чинності", 
        COALESCE(b.benefit_name, 'Немає') AS "Пільга", 
        t.sale_date AS "Дата продажу",
        e.full_name AS "Ким проданий",
        'Середня' as "Порівняно з середньою"
    FROM Ticket t
    LEFT JOIN Tariff tr ON t.tariff_id = tr.tariff_id
    LEFT JOIN TransportType tt ON tr.transport_type_id = tt.transport_type_id
    LEFT JOIN ValidityType vt ON tr.validity_type_id = vt.validity_type_id
    LEFT JOIN Benefit b ON t.benefit_id = b.benefit_id
    LEFT JOIN Employee e ON t.employee_id = e.employee_id
    WHERE t.price = (SELECT AVG(price) FROM Ticket);
    """
    with Database(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as db:
        return db.fetch_query_result(query)
