from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.infrastructure.settings.env_handler import settings

"""
The engine variable is an instance of the create_engine class from the SQLAlchemy library,
responsible for managing the connection to the database.
"""
engine = create_engine(settings.POSTGRES_DB_URI)

"""
The SessionLocal variable is an instance of the sessionmaker class from the SQLAlchemy library,
responsible for managing the session with the database.
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

"""
The SqlAlchemyBaseEntity variable is an instance of the declarative_base class from the SQLAlchemy library,
responsible for managing the base class for all the models in the application.
"""
SqlAlchemyBaseEntity = declarative_base()


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()
