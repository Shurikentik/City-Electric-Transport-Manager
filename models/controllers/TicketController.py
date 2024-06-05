from models.Ticket import Ticket
from models.Tariff import Tariff


# Клас-контроллер для оформлення продажів квитків
class TicketController:
    # Функція ініціалізації об'єкта класу
    def __init__(self, transport_type_id, validity_type_id, benefit=None):
        self.transport_type_id = transport_type_id
        self.validity_type_id = validity_type_id
        self.benefit = benefit
        self.tariff = Tariff
        self.ticket = None

    # Функція створення нового продажу
    def create_new_sale(self) -> None:
        self.ticket = Ticket()

    # Функція перевірки наявності тарифу
    def is_tariff(self) -> bool:
        return self.ticket.is_tariff(self.tariff, self.transport_type_id, self.validity_type_id)

    # Функція отримання ціни на квиток з урахуванням діючого тарифу та можливих пільг
    def get_ticket_price(self) -> float:
        if self.benefit:
            self.ticket.apply_benefit(self.benefit)
        return self.ticket.price

    # Функція отримання решти
    def get_rest(self, passed_money: float) -> float:
        return self.ticket.get_rest(self.tariff, passed_money)

    # Функція реєстрації продажу квитка у базі даних
    def save_sale(self) -> None:
        self.ticket.save()
