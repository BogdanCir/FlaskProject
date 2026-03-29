from app.db import db_session
from app.models.anagram_result import AnagramResult
import json


def find_by_key(key):
    return AnagramResult.query.filter_by(key=key).first()


def save(key, words, result):
    new_result = AnagramResult(
        key=key,
        words=json.dumps(words),
        result=json.dumps(result)
    )

    try:
        db_session.add(new_result)
        db_session.commit()
    except Exception:
        #in case of failure roll back
        db_session.rollback()
        raise

    return new_result


def get_all():
    return AnagramResult.query.order_by(AnagramResult.created_at.desc()).all()