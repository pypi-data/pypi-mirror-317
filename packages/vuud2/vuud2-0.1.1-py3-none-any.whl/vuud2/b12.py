# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Text
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
# from datetime import datetime

# Base = declarative_base()

# # Модель для клиента
# class Client(Base):
#     __tablename__ = 'clients'
    
#     id = Column(Integer, primary_key=True, index=True)
#     last_name = Column(String)  # Фамилия
#     first_name = Column(String)  # Имя
#     middle_name = Column(String)  # Отчество
#     city = Column(String)  # Город
#     address = Column(String)  # Адрес
#     phone = Column(String)  # Контактный телефон
    
#     # Связь с договорами
#     contracts = relationship("Contract", back_populates="client")
    
#     # Метод для подсчета количества договоров для клиента
#     def contract_count(self):
#         return len(self.contracts)


# # Модель для дилера
# class Dealer(Base):
#     __tablename__ = 'dealers'
    
#     id = Column(Integer, primary_key=True, index=True)
#     last_name = Column(String)  # Фамилия
#     first_name = Column(String)  # Имя
#     middle_name = Column(String)  # Отчество
#     photo = Column(String)  # Фотография (путь к файлу)
#     address = Column(String)  # Домашний адрес
#     phone = Column(String)  # Телефон
    
#     # Связь с договорами
#     contracts = relationship("Contract", back_populates="dealer")
    
#     # Метод для подсчета количества договоров, обслуживаемых дилером
#     def contract_count(self):
#         return len(self.contracts)


# # Модель для договора
# class Contract(Base):
#     __tablename__ = 'contracts'
    
#     id = Column(Integer, primary_key=True, index=True)
#     client_id = Column(Integer, ForeignKey('clients.id'))  # Код клиента
#     dealer_id = Column(Integer, ForeignKey('dealers.id'))  # Код дилера
#     contract_date = Column(DateTime, default=datetime.utcnow)  # Дата заключения договора
#     car_brand = Column(String)  # Марка автомобиля
#     car_photo = Column(String)  # Фото автомобиля (путь к файлу)
#     car_manufacture_date = Column(DateTime)  # Дата выпуска автомобиля
#     car_mileage = Column(Float)  # Пробег автомобиля
#     sale_date = Column(DateTime, nullable=True)  # Дата продажи
#     sale_price = Column(Float)  # Цена продажи
#     note = Column(Text)  # Примечание
    
#     # Связь с клиентом и дилером
#     client = relationship("Client", back_populates="contracts")
#     dealer = relationship("Dealer", back_populates="contracts")

# contracts = db.query(Contract).filter(Contract.contract_date >= start_date, Contract.contract_date <= end_date).all()
