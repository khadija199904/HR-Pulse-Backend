class JobSkill(Base):
    __tablename__ = 'job_skills'
    id = Column(Integer, primary_key=True)
    job_title = Column(String(500))
    skills_extracted = Column(Text)