from sqlalchemy import MetaData, Table, Integer
from sqlalchemy.orm import mapper
from User import User
from Admins import Admins
from Products import *
from sqlalchemy import create_engine
Base = automap_base()
metadata = MetaData()

users = Table('users', metadata,
            Column('name', String(20), primary_key=True),
            Column('password', String(40)),
            Column('email', String(40)))


admins = Table('admins', metadata,
            Column('name', String(20), primary_key=True),
            Column('password', String(40)),
            Column('email', String(40)))

products = Table('products', metadata,
            Column('userName', String(100)),
            Column('description', String(300), primary_key=True),
            Column('phoneNumber', String(20)),
            Column('price', String(10)),
            Column('date', Date))


mapper(User, users)
mapper(Products, products)
mapper(Admins, admins)



engine = create_engine("mysql+pymysql://root:12345@localhost/sql_db?host=localhost?port=3306", echo=True)
metadata.create_all(engine)

