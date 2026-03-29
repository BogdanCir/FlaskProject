from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from flask_sqlalchemy import SQLAlchemy
from anagram import anagrams, calculate_key
from datetime import datetime, timezone
import json

app = Flask(__name__)


engine = create_engine("sqlite:///anagrams.db")# we connect to our engine SQLite

# how we talk with the db, scoped session means that for every http request it will create one separate session
db_session = scoped_session(sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine 
))
Base = declarative_base() #clasa de baza pt obiectele ORM
Base.query = db_session.query_property() #ca sa putem face query mai usor



# ======= if we want to use flask_sqlalchemy library ========
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///anagrams_.db"
# db = SQLAlchemy(app)

# ===============


class AnagramResult(Base):# class AnagramResult(db.Model): ->with flask_sqlalchemy library:
    __tablename__ = "anagram_results"

#   id = db.Column(Integer, primary_key=True) 
    id = Column(Integer, primary_key=True)
    key = Column(String(1000), unique=True, nullable=False)
    words = Column(Text, nullable=False)
    result = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))



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


# using flask_sqlalchemy library:
# with app.app_context():
    # db.create_all()

def init_db():
    Base.metadata.create_all(bind=engine)#here we create the db if they don't exist



# POST request for anagrams. The json body is structured with the key "words", ex: {"words": ["ana", "dan", "nad"]}
@app.route("/api/anagrams", methods=["POST"])
def process_anagrams(): 
    data = request.get_json()# we read the data sent

# TODO need to validate the input

    words = data["words"]# get the list of "words" 
    
    key = calculate_key(words)
    
    # seen = db_session.query(AnagramResult).filter_by(key=key).first() 
    seen = AnagramResult.query.filter_by(key=key).first()#we check if there is a saved result in the table

    if seen:    
        return jsonify(seen.to_dict()),200  #we convert the AnagramResult object to a dictionary
    
    list_of_anagrams = anagrams(words)
    
    new_anagram = AnagramResult( 
            key= key,
            words = json.dumps(words),
            result = json.dumps(list_of_anagrams)
        )

    try:
        db_session.add(new_anagram) 
        db_session.commit()
    except:
        db_session.rollback()
        raise 

    return jsonify({
        "id": new_anagram.id,
        "words": words,
        "result": list_of_anagrams,
        "created_at": new_anagram.created_at.isoformat(),
        "seen": False
    }), 201

@app.route("/api/history", methods=["GET"])
def get_history():
    results = AnagramResult.query.order_by(AnagramResult.created_at.desc()).all()
    return jsonify([result.to_dict() for result in results]), 200

# here we close the session 
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    init_db()
    app.run(debug=True)