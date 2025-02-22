from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import DbConfig


def create_engine(db:DbConfig,echo=False):
    engine=create_async_engine(db.construct_sqlalchemy_url(),
                               isolation_level='READ UNCOMMITTED'
                               )
    return engine


def create_session_pool(engine):
    session_pool=async_sessionmaker(bind=engine,expire_on_commit=False)
    return session_pool