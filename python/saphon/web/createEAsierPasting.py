import json
with open("ipa-extended.json", "r", encoding="utf-8") as f:
    ipaDict = json.load(f)


with open("ipa-table.txt", "r", encoding="utf-8") as f:
    for line in f.readlines():
        line = line.strip()
        if len(line) == 0: continue

        elems = line.split(":")
        print(elems)
        keyMap = elems[0]
        phonemes = elems[1].strip().split()
        # out.write(str(phonemes) + "\n")
        if ipaDict.get(keyMap) != None:
            ipaDict[keyMap].extend(phonemes)
        else:
            ipaDict[keyMap] = phonemes

newDict = dict()
for key, val in ipaDict.items():
    newDict[key] = sorted(list(set(val)))

with open("output.txt", "w", encoding="utf-8") as out:
    out.write(str(newDict))