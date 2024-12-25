# from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Enum
# from sqlalchemy.orm import relationship, declarative_base
# import enum
# import uuid

# Base = declarative_base()

# # Role Enum for User model
# class RoleEnum(enum.Enum):
#     REGISTRAR = "registrar"
#     DOCTOR = "doctor"

# # User Model
# class User(Base):
#     __tablename__ = "users"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     username = Column(String, unique=True, nullable=False)
#     password = Column(String, nullable=False)
#     role = Column(Enum(RoleEnum), nullable=False)

# # Patient Model
# class Patient(Base):
#     __tablename__ = "patients"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     insurance_number = Column(String, unique=True, nullable=False)
#     full_name = Column(String, nullable=False)
#     address = Column(String, nullable=False)
#     gender = Column(String, nullable=False)
#     age = Column(Integer, nullable=False)

# # Doctor Model
# class Doctor(Base):
#     __tablename__ = "doctors"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     full_name = Column(String, nullable=False)
#     profile = Column(String, nullable=False)
#     schedules = relationship("Schedule", back_populates="doctor")

# # Schedule Model
# class Schedule(Base):
#     __tablename__ = "schedules"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     date = Column(Date, nullable=False)
#     start_time = Column(Time, nullable=False)
#     end_time = Column(Time, nullable=False)
#     room_number = Column(String, nullable=False)
#     doctor_id = Column(UUID(as_uuid=True), ForeignKey("doctors.id"), nullable=False)

#     doctor = relationship("Doctor", back_populates="schedules")
#     appointments = relationship("Appointment", back_populates="schedule")

# # Appointment Model
# class Appointment(Base):
#     __tablename__ = "appointments"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     schedule_id = Column(UUID(as_uuid=True), ForeignKey("schedules.id"), nullable=False)
#     patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)

#     schedule = relationship("Schedule", back_populates="appointments")
#     patient = relationship("Patient")
