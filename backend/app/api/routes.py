from flask import Blueprint, request, jsonify
from app.services import anagram_service

bp = Blueprint("main", __name__)

@bp.route("/api/anagrams", methods=["POST"])
def process_anagrams():
    data = request.get_json()
# TODO validate the input
    words = data["words"]
    result = anagram_service.process_words(words)
    # TODO if the string is in db it should return 200
    return jsonify(result), 201


@bp.route("/api/history", methods=["GET"])
def get_history():
    return jsonify(anagram_service.get_history()), 200
