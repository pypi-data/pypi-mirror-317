# from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# # Модель для автобусов
# class Bus(Base):
#     __tablename__ = 'buses'
    
#     id = Column(Integer, primary_key=True, index=True)
#     bus_number = Column(String)  # Бортовой номер автобуса
#     license_plate = Column(String)  # Гос.номер автобуса
#     brand = Column(String)  # Марка автобуса
#     year_of_manufacture = Column(Integer)  # Год выпуска
#     mileage = Column(Integer)  # Пробег

# # Модель для маршрутов
# class Route(Base):
#     __tablename__ = 'routes'
    
#     id = Column(Integer, primary_key=True, index=True)
#     route_number = Column(String)  # Номер маршрута
#     route_name = Column(String)  # Название маршрута
#     route_length = Column(Float)  # Протяженность маршрута в км
#     average_trip_time = Column(Float)  # Среднее время одного рейса в часах
#     planned_trips_per_shift = Column(Integer)  # Плановое количество рейсов за смену

# # Модель для персонала
# class Staff(Base):
#     __tablename__ = 'staff'
    
#     id = Column(Integer, primary_key=True, index=True)
#     tab_number = Column(String)  # Табельный номер
#     first_name = Column(String)  # Имя
#     last_name = Column(String)  # Фамилия
#     middle_name = Column(String)  # Отчество
#     birth_date = Column(Date)  # Дата рождения
#     home_address = Column(String)  # Домашний адрес
#     home_phone = Column(String)  # Домашний телефон
#     work_phone = Column(String)  # Рабочий телефон

# # Модель для учетных данных персонала
# class StaffRecord(Base):
#     __tablename__ = 'staff_records'
    
#     id = Column(Integer, primary_key=True, index=True)
#     staff_id = Column(Integer, ForeignKey('staff.id'))  # Ссылка на персонал
#     category = Column(String)  # Категория
#     position = Column(String)  # Должность
#     hire_date = Column(Date)  # Дата приема на работу
#     bus_id = Column(Integer, ForeignKey('buses.id'))  # Номер автобуса для водителей и кондукторов

#     staff = relationship("Staff")  # Связь с персоналом
#     bus = relationship("Bus")  # Связь с автобусом

# # Модель для маршрутных листов
# class RouteSheet(Base):
#     __tablename__ = 'route_sheets'
    
#     id = Column(Integer, primary_key=True, index=True)
#     route_id = Column(Integer, ForeignKey('routes.id'))  # Номер маршрута
#     bus_id = Column(Integer, ForeignKey('buses.id'))  # Бортовой номер автобуса
#     date = Column(Date)  # Дата маршрута
#     completed_trips = Column(Integer)  # Количество выполненных рейсов
#     driver_id = Column(Integer, ForeignKey('staff.id'))  # Водитель
#     conductor_id = Column(Integer, ForeignKey('staff.id'))  # Кондуктор

#     route = relationship("Route")  # Связь с маршрутом
#     bus = relationship("Bus")  # Связь с автобусом
#     driver = relationship("Staff", foreign_keys=[driver_id])  # Связь с водителем
#     conductor = relationship("Staff", foreign_keys=[conductor_id])  # Связь с кондуктором
