# from sqlalchemy import (
#     Column, String, Integer, ForeignKey, Float, Enum, Table, UniqueConstraint
# )
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import relationship
# import uuid
# import enum
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class RoleEnum(enum.Enum):
#     CLIENT = "client"
#     ADMIN = "admin"


# class User(Base):
#     __tablename__ = "users"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     username = Column(String, unique=True, nullable=False)
#     password = Column(String, nullable=False)
#     role = Column(Enum(RoleEnum), nullable=False)


# class Pharmacy(Base):
#     __tablename__ = "pharmacies"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name = Column(String, nullable=False)
#     phone = Column(String, nullable=False)
#     address = Column(String, nullable=False)
#     director_full_name = Column(String, nullable=False)

#     products = relationship("PharmacyProduct", back_populates="pharmacy")


# class Product(Base):
#     __tablename__ = "products"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name = Column(String, nullable=False)
#     manufacturer_country = Column(String, nullable=False)
#     pharmaceutical_groups = relationship(
#         "PharmaceuticalGroup",
#         secondary="product_pharmaceutical_group",
#         back_populates="products",
#     )
#     pharmacies = relationship("PharmacyProduct", back_populates="product")


# class PharmaceuticalGroup(Base):
#     __tablename__ = "pharmaceutical_groups"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     code = Column(String, nullable=False)
#     name = Column(String, nullable=False)

#     products = relationship(
#         "Product",
#         secondary="product_pharmaceutical_group",
#         back_populates="pharmaceutical_groups",
#     )


# product_pharmaceutical_group = Table(
#     "product_pharmaceutical_group",
#     Base.metadata,
#     Column("product_id", UUID(as_uuid=True), ForeignKey("products.id"), primary_key=True),
#     Column("pharmaceutical_group_id", UUID(as_uuid=True), ForeignKey("pharmaceutical_groups.id"), primary_key=True),
# )



# class PharmacyProduct(Base):
#     __tablename__ = "pharmacy_products"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     pharmacy_id = Column(UUID(as_uuid=True), ForeignKey("pharmacies.id"), nullable=False)
#     product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
#     price = Column(Float, nullable=False)
#     payment_method = Column(String, nullable=False)  

#     pharmacy = relationship("Pharmacy", back_populates="products")
#     product = relationship("Product", back_populates="pharmacies")

#     __table_args__ = (
#         UniqueConstraint("pharmacy_id", "product_id", name="unique_pharmacy_product"),
#     )


# def get_pharmacy_products(pharmacy_id: str, db: Session):
#     return (
#         db.query(PharmacyProduct)
#         .filter(PharmacyProduct.pharmacy_id == pharmacy_id)
#         .join(Product)
#         .all()
#     )


# def search_products_by_name(name: str, db: Session):
#     return db.query(Product).filter(Product.name.ilike(f"%{name}%")).all()


# def add_product_to_pharmacy(pharmacy_id: str, product_id: str, price: float, payment_method: str, db: Session):
#     pharmacy_product = PharmacyProduct(
#         pharmacy_id=pharmacy_id,
#         product_id=product_id,
#         price=price,
#         payment_method=payment_method,
#     )
#     db.add(pharmacy_product)
#     db.commit()
#     return pharmacy_product
