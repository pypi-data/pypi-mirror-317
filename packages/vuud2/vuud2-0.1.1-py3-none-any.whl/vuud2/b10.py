# from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
# from datetime import datetime

# Base = declarative_base()

# # Модель для поставщика
# class Supplier(Base):
#     __tablename__ = 'suppliers'
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)  # Название фирмы-поставщика
#     address = Column(String)
#     phone = Column(String)
    
#     # Связь с товарами
#     products = relationship("Product", back_populates="supplier")
    
#     # Связь с сделками
#     sale_transactions = relationship("SaleTransaction", back_populates="supplier")


# # Модель для покупателя
# class Buyer(Base):
#     __tablename__ = 'buyers'
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)  # Название фирмы-покупателя
#     address = Column(String)
#     phone = Column(String)
    
#     # Связь с сделками
#     sale_transactions = relationship("SaleTransaction", back_populates="buyer")


# # Модель для товара на складе
# class Product(Base):
#     __tablename__ = 'products'
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)  # Название товара
#     unit = Column(String)  # Единицы измерения
#     quantity = Column(Float)  # Количество на складе
#     purchase_price = Column(Float)  # Цена покупки за единицу товара
#     sale_price = Column(Float)  # Цена продажи за единицу товара
#     supplier_id = Column(Integer, ForeignKey('suppliers.id'))  # Поставщик
    
#     # Связь с поставщиком
#     supplier = relationship("Supplier", back_populates="products")
    
#     # Связь с сделками
#     sale_transactions = relationship("SaleTransaction", back_populates="product")


# # Модель для сделки о продаже
# class SaleTransaction(Base):
#     __tablename__ = 'sale_transactions'
    
#     id = Column(Integer, primary_key=True, index=True)
#     product_id = Column(Integer, ForeignKey('products.id'))  # Код товара
#     supplier_id = Column(Integer, ForeignKey('suppliers.id'))  # Поставщик
#     buyer_id = Column(Integer, ForeignKey('buyers.id'))  # Покупатель
#     quantity_sold = Column(Float)  # Количество проданного товара
#     total_amount = Column(Float)  # Сумма сделки
#     transaction_date = Column(DateTime, default=datetime.utcnow)  # Дата сделки
    
#     # Связь с товаром
#     product = relationship("Product", back_populates="sale_transactions")
    
#     # Связь с поставщиком
#     supplier = relationship("Supplier", back_populates="sale_transactions")
    
#     # Связь с покупателем
#     buyer = relationship("Buyer", back_populates="sale_transactions")
