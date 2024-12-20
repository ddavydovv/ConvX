from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from servers.database.src.database.alchemy.core import Base


class USERS(Base):
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True, index=True, comment='Уникальный идентификатор пользователя')
    language = Column(String, default=None, unique=False, comment='Язык пользователя')
    role = Column(String, default='Обычный аккаунт', unique=False, comment='Доступ пользователя')
    create_date = Column(DateTime, default=datetime.now(), unique=False, comment='Дата создания профиля')
    processing_files_count = Column(Integer, default=0, unique=False, comment='Общее количество файлов обработанных пользователем')
    processing_csv_count = Column(Integer, default=0, unique=False, comment='Количество файлов обработанных пользователем из CSV формата')
    processing_xlsx_count = Column(Integer, default=0, unique=False, comment='Количество файлов обработанных пользователем из EXCEL формата')
    processing_pdf_count = Column(Integer, default=0, unique=False, comment='Количество файлов обработанных пользователем из PDF формата')
    processing_txt_count = Column(Integer, default=0, unique=False, comment='Количество файлов обработанных пользователем из TXT формата')
    processing_docx_count = Column(Integer, default=0, unique=False, comment='Количество файлов обработанных пользователем из DOCX формата')
    user_applications = relationship("APPLICATIONS", back_populates="user")



class APPLICATIONS(Base):
    __tablename__ = 'applications'

    message_id = Column(String, primary_key=True, index=True, comment='id сообщения телеграм')
    user_id = Column(String, ForeignKey('users.user_id'), unique=False, comment='Уникальный идентификатор пользователя')
    category = Column(String, unique=False, comment='Категория конвертации')
    mode = Column(String, unique=False, comment='Мод конвертирования')
    filename = Column(String, unique=False, comment='Исходное имя файла')
    filepath = Column(String, unique=False, comment='Исходное расположение файла')
    processed_filename = Column(String, unique=False, comment='Конечное имя файла')
    processed_filepath = Column(String, unique=False, comment='Конечное расположение файла')
    status = Column(String, unique=False, comment='Статус заявки "В обработке" / "Обработано"')
    create_date = Column(String, unique=False, comment='Дата создания заявки')
    processed_date = Column(String, unique=False, comment='Дата обработки')
    user = relationship("USERS", back_populates="user_applications")