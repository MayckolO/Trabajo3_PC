from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///data.db"

engine = create_engine(DATABASE_URL, echo=False)


def create_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)