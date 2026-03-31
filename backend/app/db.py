from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from flask_sqlalchemy import SQLAlchemy
import os


# engine = create_engine("sqlite:///anagrams.db")# we connect to our engine SQLite
engine = create_engine(os.environ.get("DATABASE_URL", "sqlite:///anagrams.db"))

# how we talk with the db, scoped session means that for every http request it will create one separate session
db_session = scoped_session(sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine 
))
Base = declarative_base() #clasa de baza pt obiectele ORM
Base.query = db_session.query_property() #ca sa putem face query mai usor



# ======= if we want to use flask_sqlalchemy library ========
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///anagrams_.db"
# db = SQLAlchemy(app)

# with app.app_context():
    # db.create_all()
# ===============


def init_db():
    from app.models import anagram_result # that's the base 
    Base.metadata.create_all(bind=engine)#here we create the db

