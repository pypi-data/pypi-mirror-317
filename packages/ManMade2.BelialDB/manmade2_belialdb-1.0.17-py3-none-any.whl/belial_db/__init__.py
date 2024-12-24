from sqlalchemy import create_engine

from belial_db.models.relationships import Base


def create_connection(db_url: str, echo: bool = False, timeout: int = 30):
    """
    Create a database connection and initialize the database schema.

    Args:
        db_url (str): The database URL to connect to.
        echo (bool): If True, the engine will log all statements. Default is False.
        timeout (int): The timeout for the database connection in seconds. Default is 30.

    Returns:
        Engine: A SQLAlchemy Engine instance connected to the specified database.
    """
    engine = create_engine(db_url, echo=echo, connect_args={"timeout": timeout})
    Base.metadata.create_all(engine)
    return engine
