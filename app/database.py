# -*- coding: utf-8 -*-
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, String

basedir = os.path.abspath(os.path.dirname(__file__))

engine = create_engine("sqlite:///" + os.path.join(basedir, "../domain_rules.db") + "?check_same_thread=False", echo=True)

session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))

Base = declarative_base()


class DomainRule(Base):

    __tablename__ = "domain_rules"

    domain = Column(String, primary_key=True)
    element = Column(String)
    css_class = Column(String)

    def __repr__(self):
        return "<DomainRule(domain=%s, element=%s, css_class=%s)>" % \
               (self.domain, self.element, self.css_class)


def init_db():
    Base.metadata.create_all(engine)
