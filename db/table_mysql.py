from sqlalchemy import String, DateTime, Integer, Boolean
from sqlalchemy import ForeignKey, Column, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import registry


reg = registry()
Base = reg.generate_base()


class FilesTable(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)


class LinesFilesTable(Base):
    __tablename__ = 'lines_files'

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('files.id'), nullable=False)
    line = Column(String(256))
    key = Column(Integer)
    is_locked = Column(Boolean, default=False)
    version = Column(DateTime(timezone=True), server_default=func.now())
    released_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('file_id', 'key', name='uq_file_key'),
    )


def create_tables(engine):
    reg.metadata.create_all(engine)


def delete_tables(engine):
    reg.metadata.drop_all(engine)
