# from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# # Модель для специализаций
# class Specialization(Base):
#     __tablename__ = 'specializations'
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True)  # Название специализации (например, овощеводство, животноводство)

# # Модель для хозяйств (КФХ)
# class Farm(Base):
#     __tablename__ = 'farms'
    
#     id = Column(Integer, primary_key=True, index=True)
#     farm_code = Column(String, unique=True)  # Код КФХ
#     farm_name = Column(String)  # Название хозяйства
#     specialization_id = Column(Integer, ForeignKey('specializations.id'))  # Специализация
#     farmer_name = Column(String)  # ФИО фермера
#     region = Column(String)  # Регион
#     address = Column(String)  # Адрес
#     phone = Column(String)  # Телефон

#     specialization = relationship("Specialization")  # Связь с таблицей специализаций

# # Модель для продукции
# class Product(Base):
#     __tablename__ = 'products'
    
#     id = Column(Integer, primary_key=True, index=True)
#     farm_id = Column(Integer, ForeignKey('farms.id'))  # Связь с хозяйством
#     product_name = Column(String)  # Название продукции (например, картофель, молоко)
#     unit = Column(String)  # Единица измерения (например, кг, литр)
#     price = Column(Float)  # Цена за единицу товара
#     quantity = Column(Float)  # Предлагаемое количество
#     production_date = Column(Date)  # Дата производства

#     farm = relationship("Farm")  # Связь с хозяйством

