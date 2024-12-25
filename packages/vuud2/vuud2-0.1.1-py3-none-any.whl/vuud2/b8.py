# from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
# from datetime import datetime

# Base = declarative_base()

# # Модель для клиента
# class Client(Base):
#     __tablename__ = 'clients'
    
#     id = Column(Integer, primary_key=True, index=True)
#     full_name = Column(String, index=True)
#     email = Column(String, unique=True, index=True)
#     phone_number = Column(String)

#     # Связь с заказами
#     orders = relationship("Order", back_populates="client")


# # Модель для ткани
# class Fabric(Base):
#     __tablename__ = 'fabrics'
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     manufacturer = Column(String)
#     width = Column(Float)  # Ширина ткани в метрах
#     price_per_meter = Column(Float)  # Цена за 1 метр ткани

#     # Связь с моделями
#     recommended_for_models = relationship("Model", back_populates="recommended_fabric")
    
#     # Связь с запасами на складе
#     inventory = relationship("FabricInventory", back_populates="fabric")


# # Модель для модели одежды
# class Model(Base):
#     __tablename__ = 'models'
    
#     id = Column(Integer, primary_key=True, index=True)
#     model_number = Column(String, unique=True, index=True)  # Номер модели
#     name = Column(String, index=True)
#     fabric_id = Column(Integer, ForeignKey('fabrics.id'))  # Рекомендуемая ткань
#     fabric_consumption = Column(Float)  # Расход ткани для модели (в метрах)
#     price = Column(Float)  # Цена готовой модели
    
#     # Связь с тканью
#     recommended_fabric = relationship("Fabric", back_populates="recommended_for_models")

#     # Связь с заказами
#     orders = relationship("Order", back_populates="model")


# # Модель для закройщика
# class Tailor(Base):
#     __tablename__ = 'tailors'
    
#     id = Column(Integer, primary_key=True, index=True)
#     full_name = Column(String, index=True)
    
#     # Связь с заказами
#     orders = relationship("Order", back_populates="tailor")


# # Модель для заказа
# class Order(Base):
#     __tablename__ = 'orders'
    
#     id = Column(Integer, primary_key=True, index=True)
#     client_id = Column(Integer, ForeignKey('clients.id'))
#     model_id = Column(Integer, ForeignKey('models.id'))
#     fabric_id = Column(Integer, ForeignKey('fabrics.id'))
#     tailor_id = Column(Integer, ForeignKey('tailors.id'))
#     order_date = Column(DateTime, default=datetime.utcnow)
#     completion_status = Column(Boolean, default=False)  # Статус выполнения заказа
#     completion_date = Column(DateTime, nullable=True)
    
#     # Связь с клиентом
#     client = relationship("Client", back_populates="orders")
    
#     # Связь с моделью
#     model = relationship("Model", back_populates="orders")
    
#     # Связь с тканью
#     fabric = relationship("Fabric")
    
#     # Связь с закройщиком
#     tailor = relationship("Tailor", back_populates="orders")
    
#     # Связь с примерками
#     fittings = relationship("Fitting", back_populates="order")


# # Модель для учета тканей на складе
# class FabricInventory(Base):
#     __tablename__ = 'fabric_inventory'
    
#     id = Column(Integer, primary_key=True, index=True)
#     fabric_id = Column(Integer, ForeignKey('fabrics.id'))
#     total_meters = Column(Float)  # Общий метраж ткани на складе
    
#     # Связь с тканью
#     fabric = relationship("Fabric", back_populates="inventory")


# # Модель для примерки
# class Fitting(Base):
#     __tablename__ = 'fittings'
    
#     id = Column(Integer, primary_key=True, index=True)
#     order_id = Column(Integer, ForeignKey('orders.id'))
#     fitting_date = Column(DateTime, default=datetime.utcnow)
#     notes = Column(String)  # Примечания по примерке
    
#     # Связь с заказом
#     order = relationship("Order", back_populates="fittings")
