#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import User, Category, CategoryItem, Base

engine = create_engine('sqlite:///bookcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Create Book Categories
category1 = Category(name='Adventure')

session.add(category1)
session.commit()

category2 = Category(name='Drama')

session.add(category2)
session.commit()

category3 = Category(name='Dystopia')

session.add(category3)
session.commit()

category4 = Category(name='Fantasy')

session.add(category4)
session.commit()

category5 = Category(name='Horror')

session.add(category5)
session.commit()

category6 = Category(name='Mystery')

session.add(category6)
session.commit()

category7 = Category(name='Mythology')

session.add(category7)
session.commit()

category8 = Category(name='Non-Fiction')

session.add(category8)
session.commit()

category9 = Category(name='Romance')

session.add(category9)
session.commit()

category10 = Category(name='Satire')

session.add(category10)
session.commit()

category11 = Category(name='Science Fiction')

session.add(category11)
session.commit()

category12 = Category(name='Tragedy')

session.add(category12)
session.commit()
