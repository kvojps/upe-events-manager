from sqlalchemy import Column, Integer, String
from api.config.postgres import Base


class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    pdf_id = Column(String, unique=True, index=True)
    pdf_filename = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    title = Column(String)
    authors = Column(String)
