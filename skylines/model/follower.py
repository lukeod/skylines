# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Integer, DateTime
from sqlalchemy.orm import relation

from .base import DeclarativeBase
from .session import DBSession


class Follower(DeclarativeBase):
    __tablename__ = 'followers'

    id = Column(Integer, autoincrement=True, primary_key=True)

    source_id = Column(Integer, ForeignKey('tg_user.id'), index=True)
    source = relation('User', foreign_keys=[source_id],
                      backref='following')

    destination_id = Column(Integer, ForeignKey('tg_user.id'), index=True)
    destination = relation('User', foreign_keys=[destination_id],
                           backref='followers')

    time = Column(DateTime, nullable=False, default=datetime.utcnow)

    @classmethod
    def follows(cls, source, destination):
        return cls.query(source=source, destination=destination).count() > 0

    @classmethod
    def follow(cls, source, destination):
        f = cls.query(source=source, destination=destination).first()
        if not f:
            f = Follower(source=source, destination=destination)
            DBSession.add(f)

    @classmethod
    def unfollow(cls, source, destination):
        cls.query(source=source, destination=destination).delete()
