# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# # Модель для улиц
# class Street(Base):
#     __tablename__ = 'streets'
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True)  # Название улицы (например, проспект, переулок)

# # Модель для почтовых отделений
# class PostOffice(Base):
#     __tablename__ = 'post_offices'
    
#     id = Column(Integer, primary_key=True, index=True)
#     postal_code = Column(String)  # Почтовый индекс
#     name = Column(String)  # Название почтового отделения

# # Модель для адреса
# class Address(Base):
#     __tablename__ = 'addresses'
    
#     id = Column(Integer, primary_key=True, index=True)
#     street_id = Column(Integer, ForeignKey('streets.id'))  # Связь с улицей
#     house_number = Column(String)  # Номер дома
#     apartment_number = Column(String)  # Номер квартиры
#     post_office_id = Column(Integer, ForeignKey('post_offices.id'))  # Связь с почтовым отделением
    
#     street = relationship("Street")  # Связь с улицей
#     post_office = relationship("PostOffice")  # Связь с почтовым отделением

# # Модель для абонента
# class Subscriber(Base):
#     __tablename__ = 'subscribers'
    
#     id = Column(Integer, primary_key=True, index=True)
#     phone_number = Column(String, unique=True)  # Номер телефона
#     first_name = Column(String)  # Имя
#     last_name = Column(String)  # Фамилия
#     middle_name = Column(String)  # Отчество
#     address_id = Column(Integer, ForeignKey('addresses.id'))  # Связь с адресом
    
#     address = relationship("Address")  # Связь с адресом

# search_term = "Иван*"  # Пример поискового запроса
# subscribers = session.query(Subscriber).filter(Subscriber.last_name.like(search_term)).all()

# phone_number = "123?"  # Пример поискового запроса
# subscribers_by_phone = session.query(Subscriber).filter(Subscriber.phone_number.like(phone_number)).all()

# address_search = "%площадь%"  # Пример поискового запроса
# subscribers_by_address = session.query(Subscriber).join(Address).join(Street).filter(Street.name.like(address_search)).all()