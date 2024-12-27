from sqlalchemy import and_

from driink.models import Session, WaterLog


def get_water_log(start=None, end=None):
    with Session() as session:
        query = session.query(WaterLog)
        if start is not None and end is not None:
            query = query.filter(
                and_(
                    WaterLog.timestamp >= start,
                    WaterLog.timestamp <= end
                )
            )
        return query.all()


def log_drink(amount):
    with Session() as session:
        water_log = WaterLog(amount=amount)
        session.add(water_log)
        session.commit()
