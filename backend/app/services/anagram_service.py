from app.repositories import anagram_repository
from app.anagram import calculate_key, anagrams

def process_words(words):
    words = [w.lower() for w in words]
    key = calculate_key(words)
    
    # seen = db_session.query(AnagramResult).filter_by(key=key).first() 
    seen = anagram_repository.find_by_key(key)#we check if there is a saved result in the table
    if seen:    
        return seen.to_dict()  #we convert the AnagramResult object to a dictionary
    
    list_of_anagrams = anagrams(words)
    saved = anagram_repository.save(key, words, list_of_anagrams)
    return{
        "id": saved.id,
        "words": words,
        "result": list_of_anagrams,
        "created_at": saved.created_at.isoformat(),
        "seen": False
    }

def get_history():
    results = anagram_repository.get_all()
    return [result.to_dict() for result in results]