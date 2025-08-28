from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Float,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import date, datetime

Base = declarative_base()

class Animal(Base):
    __tablename__ = 'animals'

    id = Column(Integer, primary_key=True)
    tag = Column(String, unique=True, nullable=False)
    species = Column(String, nullable=False)
    breed = Column(String, nullable=True)
    dob = Column(Date, nullable=True)

    # one-to-many: Animal -> AnimalFeed
    feed_events = relationship('AnimalFeed', back_populates='animal', cascade='all, delete-orphan')
    sales = relationship("Sale", back_populates="animal", cascade="all, delete-orphan")
    # property constraints
    @property
    def age(self):
        if not self.dob:
            return None
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

    @property
    def tag_value(self):
        return self.tag

    @tag_value.setter
    def tag_value(self, v):
        if not v or not v.strip():
            raise ValueError('Tag must be a non-empty string')
        self.tag = v.strip()

    # ORM helper methods
    @classmethod
    def create(cls, session, tag, species, breed=None, dob=None):
        # validate
        if not tag or not tag.strip():
            raise ValueError('Tag required')
        if not species or not species.strip():
            raise ValueError('Species required')
        animal = cls(tag=tag.strip(), species=species.strip(), breed=breed, dob=dob)
        session.add(animal)
        session.flush()
        return animal

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, id_):
        return session.query(cls).filter_by(id=id_).first()

    @classmethod
    def find_by_tag(cls, session, tag):
        return session.query(cls).filter_by(tag=tag).first()

    @classmethod
    def delete_by_id(cls, session, id_):
        obj = cls.find_by_id(session, id_)
        if not obj:
            return False
        session.delete(obj)
        session.flush()
        return True


class Feed(Base):
    __tablename__ = 'feeds'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    unit = Column(String, default='kg')
    cost_per_unit = Column(Float, default=0.0)
    stock_quantity = Column(Float, default=0.0)

    feed_events = relationship('AnimalFeed', back_populates='feed', cascade='all, delete-orphan')

    @property
    def stock(self):
        return self.stock_quantity

    @stock.setter
    def stock(self, v):
        if v is None:
            v = 0.0
        if float(v) < 0:
            raise ValueError('Stock cannot be negative')
        self.stock_quantity = float(v)

    @classmethod
    def create(cls, session, name, unit='kg', cost_per_unit=0.0, stock_quantity=0.0):
        if not name or not name.strip():
            raise ValueError('Feed name required')
        feed = cls(name=name.strip(), unit=unit, cost_per_unit=float(cost_per_unit), stock_quantity=float(stock_quantity))
        session.add(feed)
        session.flush()
        return feed

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, id_):
        return session.query(cls).filter_by(id=id_).first()

    @classmethod
    def find_by_name(cls, session, name):
        return session.query(cls).filter_by(name=name).first()

    @classmethod
    def delete_by_id(cls, session, id_):
        obj = cls.find_by_id(session, id_)
        if not obj:
            return False
        session.delete(obj)
        session.flush()
        return True


class AnimalFeed(Base):
    __tablename__ = 'animal_feeds'

    id = Column(Integer, primary_key=True)
    animal_id = Column(Integer, ForeignKey('animals.id'))
    feed_id = Column(Integer, ForeignKey('feeds.id'))
    date_given = Column(DateTime, default=datetime.utcnow)
    quantity = Column(Float, default=0.0)

    animal = relationship('Animal', back_populates='feed_events')
    feed = relationship('Feed', back_populates='feed_events')

    @classmethod
    def create(cls, session, animal, feed, quantity, date_given=None):
        if quantity <= 0:
            raise ValueError('Quantity must be > 0')
        if date_given is None:
            date_given = datetime.utcnow()
        event = cls(animal=animal, feed=feed, quantity=float(quantity), date_given=date_given)
        # reduce feed stock
        if feed.stock_quantity - float(quantity) < 0:
            raise ValueError('Not enough feed in stock')
        feed.stock_quantity = feed.stock_quantity - float(quantity)
        session.add(event)
        session.flush()
        return event

    @classmethod
    def get_for_animal(cls, session, animal_id):
        return session.query(cls).filter_by(animal_id=animal_id).all()

    @classmethod
    def get_for_feed(cls, session, feed_id):
        return session.query(cls).filter_by(feed_id=feed_id).all()

class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    quantity = Column(Float, default=0.0)
    unit = Column(String, default="pcs")

    @classmethod
    def create(cls, session, name, category, quantity=0.0, unit="pcs"):
        item = cls(
            name=name.strip(),
            category=category.strip(),
            quantity=float(quantity),
            unit=unit.strip()
        )
        session.add(item)
        session.flush()
        return item

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, id_):
        return session.query(cls).filter_by(id=id_).first()

    @classmethod
    def delete_by_id(cls, session, id_):
        obj = cls.find_by_id(session, id_)
        if not obj:
            return False
        session.delete(obj)
        session.flush()
        return True



class Personnel(Base):
    __tablename__ = 'personnel'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    salary = Column(Float, default=0.0)

    @classmethod
    def create(cls, session, name, role, salary=0.0):
        if not name or not name.strip():
            raise ValueError("Name required")
        if not role or not role.strip():
            raise ValueError("Role required")
        if salary < 0:
            raise ValueError("Salary cannot be negative")

        person = cls(name=name.strip(), role=role.strip(), salary=float(salary))
        session.add(person)
        session.flush()
        return person

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, id_):
        return session.query(cls).filter_by(id=id_).first()

    @classmethod
    def delete_by_id(cls, session, id_):
        obj = cls.find_by_id(session, id_)
        if not obj:
            return False
        session.delete(obj)
        session.flush()
        return True


class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    animal_id = Column(Integer, ForeignKey('animals.id'), nullable=False)
    price = Column(Float, nullable=False)
    date = Column(Date, default=date.today)

    animal = relationship('Animal', back_populates='sales')

    @classmethod
    def create(cls, session, animal, price, date_=None):
        if not animal:
            raise ValueError("Animal required")
        if price <= 0:
            raise ValueError("Price must be positive")

        sale = cls(animal=animal, price=float(price), date=date_ or date.today())
        session.add(sale)
        session.flush()
        return sale

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, id_):
        return session.query(cls).filter_by(id=id_).first()

    @classmethod
    def delete_by_id(cls, session, id_):
        obj = cls.find_by_id(session, id_)
        if not obj:
            return False
        session.delete(obj)
        session.flush()
        return True
