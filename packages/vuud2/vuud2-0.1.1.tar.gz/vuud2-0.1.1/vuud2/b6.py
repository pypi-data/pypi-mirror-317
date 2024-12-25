# from sqlalchemy import (
#     Column, String, Integer, Float, ForeignKey, Date, Enum, Table
# )
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import relationship
# import uuid
# import enum
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# # Роли пользователей
# class RoleEnum(enum.Enum):
#     MEMBER = "member"  # Член профсоюза
#     MANAGER = "manager"  # Менеджер


# # Пользователь
# class User(Base):
#     __tablename__ = "users"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     username = Column(String, unique=True, nullable=False)
#     password = Column(String, nullable=False)
#     role = Column(Enum(RoleEnum), nullable=False)

#     member = relationship("UnionMember", back_populates="user", uselist=False)


# # Член профсоюза
# class UnionMember(Base):
#     __tablename__ = "union_members"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
#     membership_card_number = Column(String, unique=True, nullable=False)
#     full_name = Column(String, nullable=False)
#     work_experience = Column(Integer, nullable=False)
#     join_date = Column(Date, nullable=False)

#     user = relationship("User", back_populates="member")
#     applications = relationship("VoucherApplication", back_populates="member")
#     material_assistance = relationship("MaterialAssistance", back_populates="member")


# # Путевка
# class Voucher(Base):
#     __tablename__ = "vouchers"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     type = Column(Enum("medical", "tourist", name="voucher_type"), nullable=False)
#     organization_name = Column(String, nullable=False)
#     duration_days = Column(Integer, nullable=False)
#     start_date = Column(Date, nullable=False)

#     applications = relationship("VoucherApplication", back_populates="voucher")


# # Материальная помощь
# class MaterialAssistance(Base):
#     __tablename__ = "material_assistance"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     member_id = Column(UUID(as_uuid=True), ForeignKey("union_members.id"), nullable=False)
#     issue_date = Column(Date, nullable=False)
#     amount = Column(Float, nullable=False)
#     reason = Column(String, nullable=False)

#     member = relationship("UnionMember", back_populates="material_assistance")


# # Заявка на путевку
# class VoucherApplication(Base):
#     __tablename__ = "voucher_applications"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     member_id = Column(UUID(as_uuid=True), ForeignKey("union_members.id"), nullable=False)
#     voucher_id = Column(UUID(as_uuid=True), ForeignKey("vouchers.id"), nullable=False)
#     application_date = Column(Date, nullable=False)
#     status = Column(Enum("pending", "approved", "rejected", name="application_status"), nullable=False, default="pending")

#     member = relationship("UnionMember", back_populates="applications")
#     voucher = relationship("Voucher", back_populates="applications")


# def get_current_vouchers(db: Session):
#     return db.query(Voucher).filter(Voucher.start_date >= date.today()).all()


# def search_vouchers_by_organization(name: str, db: Session):
#     return db.query(Voucher).filter(Voucher.organization_name.ilike(f"%{name}%")).all()


# def create_voucher_application(member_id: str, voucher_id: str, db: Session):
#     application = VoucherApplication(
#         member_id=member_id,
#         voucher_id=voucher_id,
#         application_date=date.today(),
#         status="pending",
#     )
#     db.add(application)
#     db.commit()
#     return application


# def update_application_status(application_id: str, status: str, db: Session):
#     application = db.query(VoucherApplication).filter(VoucherApplication.id == application_id).first()
#     if application:
#         application.status = status
#         db.commit()
#     return application


# def add_new_voucher(type: str, organization_name: str, duration_days: int, start_date: date, db: Session):
#     voucher = Voucher(
#         type=type,
#         organization_name=organization_name,
#         duration_days=duration_days,
#         start_date=start_date,
#     )
#     db.add(voucher)
#     db.commit()
#     return voucher
