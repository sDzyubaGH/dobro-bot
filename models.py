from re import T
# from time import timezone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, DateTime

base = declarative_base()


class Volunteer(base):
    __tablename__ = 'volunteers'

    tgId = Column(String(20), primary_key=True, autoincrement=False)
    first_name = Column('first_name', String(40))
    last_name = Column('last_name', String(40))
    patronymic = Column('patronymic', String(20))
    birthdate = Column('birthdate', DateTime())
    tel = Column('tel', String(11))
    VKLink = Column('vklink', String(255))
    mail = Column('mail', String(255))

    def __init__(self, tgId, first_name, last_name, patronymic, birthdate, tel, VKLink, mail):
        self.tgId = tgId
        self.first_name = first_name
        self.last_name = last_name
        self.patronymic = patronymic
        self.birthdate = birthdate
        self.tel = tel
        self.VKLink = VKLink
        self.mail = mail

    # def __repr__(self):
        # return (self.tgId, self.first_name, self.last_name, self.patronymic, self.birthdate, self.tel, self.VKLink, self.mail)
    def __repr__(self):
        return "<Volunteer(tgId='{}', first_name='{}', last_name='{}', patronymic='{}', birthdate='{}', tel='{}', VKLink='{}', mail='{}')>"\
            .format(self.tgId, self.first_name, self.last_name, self.patronymic, self.birthdate, self.tel, self.VKLink, self.mail)


class Admin(base):
    __tablename__ = 'admins'

    # id = Column(Integer, primary_key=True)
    tgId = Column('tgId', String(255), primary_key=True, autoincrement=False)
    name = Column('name', String(40))

    def __init__(self, tgId, name):
        self.tgId = tgId
        self.name = name

    def __repr__(self):
        return "<Admin(tgId='{}', name='{}')>"\
            .fromat(self.tgId, self.name)



# class Evenv(base):
#     __tablename__ = 'events'

#     id = Column('')