import os
import sys
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Ztf(Base):
    #OLD
    #__tablename__ = 'indextable'
    #id = Column(Integer, primary_key=True)
    #date = Column(Integer)
    #candid = Column(Integer)
    #objectId = Column(String)
    #jd = Column(Float)
    #filter = Column(Integer)
    #ra = Column(Float)
    #dec = Column(Float)
    #magpsf = Column(Float)
    #magap = Column(Float)
    
    __tablename__ = 'featuretable'
    #id = Column(Integer, primary_key=True)
    date_alert_mjd = db.Column(db.Float, primary_key=True)
    alert_id = db.Column(db.String, primary_key=True)
    ztf_object_id = db.Column(db.String)
    locus_id = db.Column(db.String, primary_key=True)
    locus_ra = db.Column(db.Float)
    locus_dec = db.Column(db.Float)
    ant_mag_corrected = db.Column(db.Float)    

    # @property
    # def ra(self):
    #     ra = shape.to_shape(self.location).x
    #     if ra < 0:
    #         ra = ra + 360
    #     return ra
    # @property
    # def dec(self):
    #     return shape.to_shape(self.location).y

    def __str__(self):
        return self.objectId


# Create an engine that stores data in the local sqlite file.
engine = create_engine('sqlite:///ztf_alerts_manual.db')
 
# Create all tables in the engine. This is equivalent to "Create Table" # statements in raw SQL.
#Base.metadata.create_all(engine)
# ? TODO: Add Create Table statements? Or do we always pre-create the table?

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
