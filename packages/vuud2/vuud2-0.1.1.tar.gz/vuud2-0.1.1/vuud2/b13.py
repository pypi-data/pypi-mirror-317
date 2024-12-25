# from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Enum
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
# from datetime import datetime
# import enum

# Base = declarative_base()

# # Перечисление для классов рейса
# class FlightClass(enum.Enum):
#     economy = "Эконом"
#     business = "Бизнес"

# # Модель для рейса
# class Flight(Base):
#     __tablename__ = 'flights'
    
#     id = Column(Integer, primary_key=True, index=True)
#     flight_number = Column(String, unique=True)  # Номер рейса
#     route = Column(String)  # Маршрут
#     departure_point = Column(String)  # Пункт отправления
#     destination_point = Column(String)  # Пункт назначения
#     departure_time = Column(DateTime)  # Время вылета
#     airplane_type = Column(String)  # Тип самолета
#     flight_date = Column(DateTime)  # Дата вылета
#     flight_duration = Column(Float)  # Время полета в часах
#     flight_class = Column(Enum(FlightClass))  # Класс (эконом/бизнес)
#     price = Column(Float)  # Цена билета
    
#     # Связь с самолетом
#     airplane_id = Column(Integer, ForeignKey('airplanes.id'))
#     airplane = relationship("Airplane", back_populates="flights")
    
#     # Связь с билетами
#     tickets = relationship("Ticket", back_populates="flight")
    
#     # Метод для получения количества свободных мест
#     def available_seats(self):
#         total_seats = self.airplane.total_seats
#         booked_seats = len(self.tickets)
#         return total_seats - booked_seats
    
#     # Метод для подсчета средней стоимости билетов
#     @property
#     def average_price(self):
#         total_price = sum(ticket.price for ticket in self.tickets)
#         return total_price / len(self.tickets) if self.tickets else 0

# # Модель для самолета
# class Airplane(Base):
#     __tablename__ = 'airplanes'
    
#     id = Column(Integer, primary_key=True, index=True)
#     type = Column(String)  # Тип самолета
#     total_seats = Column(Integer)  # Количество мест
#     technical_specifications = Column(String)  # Технические характеристики
    
#     # Связь с рейсами
#     flights = relationship("Flight", back_populates="airplane")

# # Модель для пассажира
# class Passenger(Base):
#     __tablename__ = 'passengers'
    
#     id = Column(Integer, primary_key=True, index=True)
#     last_name = Column(String)  # Фамилия
#     first_name = Column(String)  # Имя
#     middle_name = Column(String)  # Отчество
#     document_type = Column(String)  # Тип документа (например, паспорт)
#     document_series = Column(String)  # Серия документа
#     document_number = Column(String)  # Номер документа
    
#     # Связь с билетами
#     tickets = relationship("Ticket", back_populates="passenger")

# # Модель для билета
# class Ticket(Base):
#     __tablename__ = 'tickets'
    
#     id = Column(Integer, primary_key=True, index=True)
#     passenger_id = Column(Integer, ForeignKey('passengers.id'))  # Код пассажира
#     flight_id = Column(Integer, ForeignKey('flights.id'))  # Код рейса
#     price = Column(Float)  # Цена билета
    
#     # Связь с пассажиром и рейсом
#     passenger = relationship("Passenger", back_populates="tickets")
#     flight = relationship("Flight", back_populates="tickets")

# upcoming_flights = db.query(Flight).filter(Flight.flight_date > datetime.utcnow()).order_by(Flight.flight_date).all()

# flight = db.query(Flight).filter(Flight.id == flight_id).first()
# available_seats = flight.available_seats()

# passengers = db.query(Passenger).join(Ticket).filter(Ticket.flight_id == flight_id).all()

# total_price = sum(ticket.price for ticket in flight.tickets)

# average_price = flight.average_price

# passengers_count = db.query(Passenger).join(Ticket).join(Flight).filter(Flight.flight_date >= start_date, Flight.flight_date <= end_date).count()

# average_load = (len(flight.tickets) / flight.airplane.total_seats) * 100  # В процентах
