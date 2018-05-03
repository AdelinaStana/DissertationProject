from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

# create engine
engine = create_engine("mysql+pymysql://root:12345@localhost/sql_db?host=localhost?port=3306", echo=True)

#create connection with engine
connection = engine.connect()

#create base
Base = automap_base()
Base.prepare(engine, reflect=True)

#create database session
dbSession = Session(engine)

Projects = Base.classes.projects
Classes = Base.classes.classes
Methods = Base.classes.methods
Attributes = Base.classes.attributes