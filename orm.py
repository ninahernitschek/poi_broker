class Ztf(Base):
    __tablename__ = 'indextable2'
    id = Column(Integer, primary_key=True)
    date = Column(Integer)
    candid = Column(Integer)
    objectId = Column(String)
    jd = Column(Float)
    filter = Column(Integer)
    ra = Column(Float)
    dec = Column(Float)
    mgpsf = Column(Float)
    magap = Column(Float)

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