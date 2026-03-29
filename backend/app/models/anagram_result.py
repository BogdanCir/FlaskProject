from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime, timezone
from app.db import Base
import json

class AnagramResult(Base):# class AnagramResult(db.Model): ->with flask_sqlalchemy library:
    __tablename__ = "anagram_results"

#   id = db.Column(Integer, primary_key=True) 
    id = Column(Integer, primary_key=True)
    key = Column(String(1000), unique=True, nullable=False)
    words = Column(Text, nullable=False)
    result = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc)) #TODO should change the time to Romania/Bucharest



    def get_words(self):
        return json.loads(self.words)
    def get_result(self):
        return json.loads(self.result)
    
    #converting to dictionary to be able then to convert to json
    def to_dict(self):
        return {
            "id": self.id,
            "words": self.get_words(),
            "result": self.get_result(),
            "created_at": self.created_at.isoformat(), #changed date type to string to be json safe
            "seen": True,
        }