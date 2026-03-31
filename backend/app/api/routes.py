from flask import Blueprint, request, jsonify
from app.services import anagram_service

bp = Blueprint("main", __name__)

@bp.route("/api/anagrams", methods=["POST"])
def process_anagrams():
    data = request.get_json()

#  validate the input
    if not data:
        return jsonify({"You need to put some input"})
    
    words = data["words"]
    result = anagram_service.process_words(words)

    #  if the string is in db it should return 200
    status = 201
    if result["seen"]:  status = 200
    return jsonify(result), status



@bp.route("/api/history", methods=["GET"])
def get_history():
    return jsonify(anagram_service.get_history()), 200
  