# from sqlalchemy import Column, Integer, String, ForeignKey, Date
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# # Модель для безработных
# class Unemployed(Base):
#     __tablename__ = 'unemployed'
    
#     id = Column(Integer, primary_key=True, index=True)
#     first_name = Column(String)  # Имя
#     last_name = Column(String)  # Фамилия
#     middle_name = Column(String)  # Отчество
#     profession = Column(String)  # Профессия
#     education = Column(String)  # Образование
#     last_job = Column(String)  # Последняя работа
#     last_job_position = Column(String)  # Должность на последней работе
#     reason_for_dismissal = Column(String)  # Причина увольнения
#     marital_status = Column(String)  # Семейное положение
#     housing_conditions = Column(String)  # Жилищные условия
#     contact_info = Column(String)  # Контактные данные
#     job_requirements = Column(String)  # Требования к будущей работе
#     application_date = Column(Date)  # Дата подачи заявки на вакансию

# # Модель для вакансий
# class Vacancy(Base):
#     __tablename__ = 'vacancies'
    
#     id = Column(Integer, primary_key=True, index=True)
#     company_name = Column(String)  # Название фирмы
#     position = Column(String)  # Должность
#     working_conditions = Column(String)  # Условия труда
#     salary_conditions = Column(String)  # Условия оплаты
#     requirements = Column(String)  # Требования к специалисту

# # Модель для заявок на вакансии
# class Application(Base):
#     __tablename__ = 'applications'
    
#     id = Column(Integer, primary_key=True, index=True)
#     unemployed_id = Column(Integer, ForeignKey('unemployed.id'))  # Связь с безработным
#     vacancy_id = Column(Integer, ForeignKey('vacancies.id'))  # Связь с вакансией
#     application_date = Column(Date)  # Дата подачи заявки
#     status = Column(String)  # Статус заявки (например, "подана", "трудоустроен", "отказ")

#     unemployed = relationship("Unemployed")  # Связь с безработным
#     vacancy = relationship("Vacancy")  # Связь с вакансией

# # Модель для объявления о вакансии (для печати)
# class Advertisement(Base):
#     __tablename__ = 'advertisements'
    
#     id = Column(Integer, primary_key=True, index=True)
#     vacancy_id = Column(Integer, ForeignKey('vacancies.id'))  # Связь с вакансией
#     publication_date = Column(Date)  # Дата публикации объявления

#     vacancy = relationship("Vacancy")  # Связь с вакансией
