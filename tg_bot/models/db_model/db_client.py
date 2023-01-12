from sqlalchemy import create_engine


class DBClient:
    def __init__(self, sqlalchemy_url: str, base):
        self.sqlalchemy_url = sqlalchemy_url
        self.engine = create_engine(self.sqlalchemy_url)
        self.Base = base
        self.create_tables()

    def create_tables(self):
        self.Base.metadata.create_all(self.engine)
