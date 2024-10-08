from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.orm import Session

from ..models import Member
from .base import CRUDBase
from ..models import Event


class CRUDEvent(CRUDBase[Event]):
    def get_next_upcoming_event(self, db: Session, limit=1) -> list[Event]:
        return (((db.query(self.model)
                  .filter(self.model.start_time > datetime.now()))
                 .order_by(desc(self.model.start_time)))
                 .limit(limit).all())

    def participate(self, db: Session, event_id: int, member_id: int) -> Event:
        event = db.query(Event).get(event_id)
        member = db.query(Member).get(member_id)
        if event is None or member is None:
            raise ValueError("Event or Member not found")
        if member not in event.participants:
            event.participants.append(member)
            db.commit()
        else:
            raise ValueError("Member already participating in the event")
        return event

    @staticmethod
    def remove_participant(db: Session, event_id: int, member_id: int) -> Event:
        event = db.query(Event).get(event_id)
        member = db.query(Member).get(member_id)
        if event is None or member is None:
            raise ValueError("Event or Member not found")
        if member in event.participants:
            event.participants.remove(member)
            db.commit()
        else:
            raise ValueError("Member not participating in the event")
        return event

    def get_multi(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(self.model).order_by(desc(self.model.start_time)).offset(skip).limit(limit).all()

    def get_upcoming_events(self, db: Session, limit=10):
        return ((db.query(self.model)
                  .filter(self.model.start_time > datetime.now()))
                 .order_by(self.model.start_time)
                .limit(limit).all())


event_repository = CRUDEvent(Event)
