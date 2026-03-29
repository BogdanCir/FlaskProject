
# calculate the anagrams from a list of strings
def anagrams(strs):
    resolve = {}
    for word in strs:
        if ''.join(sorted(word)) in resolve.keys():
            dict_val = resolve[''.join(sorted(word))]
            dict_val.append(word)
        else:
            resolve[''.join(sorted(word))] = [word]
    return list(resolve.values())

# here we calculate the key of the string. If we have the same key, we return the response directly from the db
def calculate_key(words):
    return "".join(sorted(w.lower() for w in words))
# print(sorted("ana"))
# print(calculate_key(["ana", "mircea", "gel", "leg", "elg", "aan"]))
# print(anagrams(["ana", "mircea", "gel", "leg", "elg", "aan"]))

