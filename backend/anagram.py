
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


# print(sorted("ana"))
# print(anagrams(["ana", "mircea", "gel", "leg", "elg", "aan"]))

