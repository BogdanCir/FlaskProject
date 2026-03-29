from flask import Flask, request, jsonify
from flask_cors import CORS
from anagram import anagrams

app = Flask(__name__)

# POST request for anagrams. The json body is structured with the key "words", ex: {"words": ["ana", "dan", "nad"]}
@app.route("/api/anagrams", methods=["POST"])
def process_anagrams(): 

# we read the data sent
    data = request.get_json()

# TODO need to validate the input

# get the list of "words"
    words = data["words"]

# process the anagrams
    list_of_anagrams = anagrams(words)

    return jsonify({
        "words": words,
        "list_of_anagrams": list_of_anagrams,
    }), 201

if __name__ == "__main__":
    app.run(debug=True)