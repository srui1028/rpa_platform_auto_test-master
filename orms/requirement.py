#!/usr/bin/python
# -*- coding: UTF-8 -*-
from decimal import Decimal

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float

Base = declarative_base()


class Requirement(Base):
    __tablename__ = 'requirement'

    id = Column(String, primary_key=True)
    status = Column(Integer)
    name = Column(String)
    organization_id = Column(String)
    use_system = Column(String)
    business_label = Column(String)
    cost_time = Column(Decimal)
    user_num = Column(Integer)
    description = Column(String)
    operate_step = Column(String)
    deleted = Column(Integer)
    org_id = Column(Integer)
    scene = Column(String)
    manual_days = Column(Float)
    create_at = Column(Date)
    update_at = Column(Date)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


if __name__ == '__main__':
    pass
