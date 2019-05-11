from sqlalchemy import Column, Integer, String

from .base import session_factory, Base


class Job(Base):
    __tablename__ = 'job'
    id = Column('id', Integer, primary_key=True)
    company_name = Column('company_name', String)
    job_title = Column('job_title', String)
    location = Column('location', String)


def add_record(company_name, job_title, location):
    if record_exists(company_name, job_title, location):
        return
    session = session_factory()
    job = Job(
        company_name=company_name,
        job_title=job_title,
        location=location
    )
    session.add(job)
    session.commit()
    session.close()


def record_exists(company_name, job_title, location):
    session = session_factory()
    result = session.query(Job).filter(Job.company_name == company_name).filter(
        Job.job_title == job_title).filter(Job.location == location)
    session.close()
    if result.count() == 0:
        return False
    return True
