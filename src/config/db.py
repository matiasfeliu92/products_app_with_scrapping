from sqlmodel import SQLModel, Session, create_engine

from src.config.settings import Settings
from src.models.product import Product
from src.models.brand import Brand
from src.models.store import Store
from src.models.category import Category
from src.models.history import History

class ManageDB:
    engine = None
    def __init__(self):
        self.settings = Settings()
        self.engine = create_engine(self.settings.DATABASE_URL, echo=True)

    def init_db(self):
        """Carga los modelos y crea las tablas"""
        SQLModel.metadata.create_all(self.engine)

    def get_session(self):
        """Generador de sesión para FastAPI"""
        with Session(self.engine) as session:
            yield session