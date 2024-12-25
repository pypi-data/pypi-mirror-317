from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

# Перечисление для вида оплаты
class PaymentMethod(enum.Enum):
    cash = "Наличные"
    credit = "Кредит"
    instant = "Сразу"

# Модель для автомобиля (товар)
class Car(Base):
    __tablename__ = 'cars'
    
    id = Column(Integer, primary_key=True, index=True)
    country_of_origin = Column(String)  # Страна-изготовитель
    brand = Column(String)  # Марка автомобиля
    model = Column(String)  # Модель автомобиля
    color = Column(String)  # Цвет
    in_stock = Column(Boolean)  # Наличие на складе
    available_date = Column(DateTime, nullable=True)  # Когда будет в наличии
    price = Column(Float)  # Цена автомобиля
    
    # Связь с техническими данными
    technical_data = relationship("TechnicalData", back_populates="car", uselist=False)
    
    # Связь с покупками
    purchases = relationship("Purchase", back_populates="car")

# Модель для технических данных автомобиля
class TechnicalData(Base):
    __tablename__ = 'technical_data'
    
    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey('cars.id'))
    body_type = Column(String)  # Тип кузова
    doors_count = Column(Integer)  # Количество дверей
    seats_count = Column(Integer)  # Количество мест
    engine_type = Column(String)  # Тип двигателя
    engine_position = Column(String)  # Расположение двигателя
    engine_volume = Column(Float)  # Рабочий объем двигателя
    
    # Связь с автомобилем
    car = relationship("Car", back_populates="technical_data")

# Модель для клиента
class Client(Base):
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)  # ФИО клиента
    passport_series = Column(String)  # Серия паспорта
    passport_number = Column(String)  # Номер паспорта
    address = Column(String)  # Домашний адрес
    phone_number = Column(String)  # Телефон
    
    # Связь с покупками
    purchases = relationship("Purchase", back_populates="client")

# Модель для покупки
class Purchase(Base):
    __tablename__ = 'purchases'
    
    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey('cars.id'))  # Код товара
    client_id = Column(Integer, ForeignKey('clients.id'))  # Код клиента
    purchase_date = Column(DateTime, default=datetime.utcnow)  # Дата покупки
    delivery = Column(Boolean)  # Доставка (да/нет)
    payment_method = Column(Enum(PaymentMethod))  # Вид оплаты
    
    # Связь с автомобилем
    car = relationship("Car", back_populates="purchases")
    
    # Связь с клиентом
    client = relationship("Client", back_populates="purchases")
