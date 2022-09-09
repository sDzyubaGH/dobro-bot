from models import base
from config import DATABASE_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Volunteer
import sqlalchemy

engine = create_engine(DATABASE_URI)
base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
s = Session()


# def startConnection():
#     # engine = create_engine(DATABASE_URI)
#     base.metadata.create_all(engine)

#     Session = sessionmaker(bind=engine)
#     s = Session()


def recreate_database():
    base.metadata.drop_all(engine)
    base.metadata.create_all(engine)


def check_volunteer(tgId):
    return s.query(Volunteer).filter(Volunteer.tgId == tgId).first()


async def add_volunteer(state):
    async with state.proxy() as data:
        volunteerData = data.as_dict()
        print(volunteerData['birth_date'])
        volunteer = Volunteer(
            tgId=volunteerData['user_id'],
            first_name=volunteerData['first_name'],
            last_name=volunteerData['last_name'],
            patronymic=volunteerData['patronymic'],
            birthdate=volunteerData['birth_date'],
            tel=volunteerData['tel'],
            VKLink=volunteerData['VKLink'],
            mail=volunteerData['mail']
        )

        s.add(volunteer)
        try:
            s.commit()
        except sqlalchemy.exc.IntegrityError:
            print('Ошибка при записи волонтера в БД')
            return -1

        return 0


# import mysql.connector

# try:
#     cnx = mysql.connector.connect(user='u0835005_admin', password='Cocos2003',
#                                   host='31.31.196.162',
#                                   database='u0835005_botdb')

#     cnx.close()
# except mysql.connector.Error as err:
#     print(err)
