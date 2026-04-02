from flask import Blueprint, request, jsonify
from app.services import anagram_service

bp = Blueprint("main", __name__)

@bp.route("/api/anagrams", methods=["POST"])
def process_anagrams():
    data = request.get_json() or {}

    words = data["words"]

#  validate the input
    if not isinstance(words, list) or not words:
        return jsonify({"error": "words must be a non-empty list"}), 400
    
    cleaned_words = [w.strip() for w in words if w.strip()]

    if not all(w.isalpha() for w in cleaned_words):
        return jsonify({"error": "only letters are allowed"}), 400
    
    result = anagram_service.process_words(words)

    #  if the string is in db it should return 200
    status = 201
    if result["seen"]:  status = 200
    return jsonify(result), status



@bp.route("/api/history", methods=["GET"])
def get_history():
    return jsonify(anagram_service.get_history()), 200
  