from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from Data_Setup import *

engine = create_engine('sqlite:///cosmetics.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Delete CosmeticsCompanyName if exisitng.
session.query(CompanyName).delete()
# Delete CosmeticName if exisitng.
session.query(ItemName).delete()
# Delete User if exisitng.
session.query(User).delete()

# Create sample users data
User1 = User(
 name="SRAVANA SANDHYA KARNATI", email="ssrrkarnati@gmail.com",
 picture='http://www.enchanting-costarica.com/wp-content/'
 'uploads/2018/02/jcarvaja17-min.jpg'
 )
session.add(User1)
session.commit()
print("Successfully Add First User")
# Create sample cosmetic companies
Company1 = CompanyName(name="AVON", user_id=1)
session.add(Company1)
session.commit()

Company2 = CompanyName(name="ACTIDERM",  user_id=1)
session.add(Company2)
session.commit()

Company3 = CompanyName(name="OVIFLAME",  user_id=1)
session.add(Company3)
session.commit()

Company4 = CompanyName(name="DIOR",  user_id=1)
session.add(Company4)
session.commit()

Company5 = CompanyName(name="CHANEL", user_id=1)
session.add(Company5)
session.commit()

Company6 = CompanyName(name="YOUNIQUE", user_id=1)
session.add(Company6)
session.commit()

Company7 = CompanyName(name="LAKME", user_id=1)
session.add(Company7)
session.commit()

# Populare a cosmetics with details
# Using different users for cosmetics names and details also
Item1 = ItemName(name="Foundation", description="It is used to apply on face",
                 price="1000rs", feedback="Nice", date=datetime.datetime.now(),
                 companynameid=1, user_id=1)
session.add(Item1)
session.commit()

Item2 = ItemName(
    name="Facewash",
    description="It is like geely item used to wash face", price="500rs",
    feedback="Excellent", date=datetime.datetime.now(),
    companynameid=2, user_id=1)
session.add(Item2)
session.commit()

Item3 = ItemName(
                name="Nailpolish",
                description="It is used to apply on Nails to make  beautiful",
                price="250rs",
                feedback="Good",
                date=datetime.datetime.now(),
                companynameid=3,
                user_id=1)
session.add(Item3)
session.commit()

Item4 = ItemName(
    name="Makeup powder",
    description="It is used to apply on face to make face white",
    price="700rs",
    feedback="very good", date=datetime.datetime.now(), companynameid=4,
    user_id=1)
session.add(Item4)
session.commit()
Item5 = ItemName(
    name="Lipstic",
    description="It is used to apply on lips", price="350rs",
    feedback="Awesome", date=datetime.datetime.now(), companynameid=5,
    user_id=1)
session.add(Item5)
session.commit()
Item6 = ItemName(
    name="eyelashe", description="It is used to apply on eyelashes",
    price="400rs", feedback="Good", date=datetime.datetime.now(),
    companynameid=6, user_id=1)
session.add(Item6)
session.commit()

Item7 = ItemName(
    name="Body lotion",
    description="It is used to apply on skin to keep it moisture",
    price="800rs", feedback="Not bad", date=datetime.datetime.now(),
    companynameid=7, user_id=1)
session.add(Item7)
session.commit()
print("Your cosmetics database has been inserted!")
