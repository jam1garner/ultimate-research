import binascii

def crc32(s):
    return binascii.crc32(s.lower().encode('utf8'))

with open('paramHashTable.csv', 'r') as f:
    hashTable = [ line.split(',') for line in f.readlines() if not line.isspace() ]

hashesByLength = {}

for hashPair in hashTable:
    length = int(hashPair[1])
    if not length in hashesByLength:
        hashesByLength[length] = []
    hashesByLength[length].append(int(hashPair[0], 16))


stringsByLength = {}
with open('string_dump.txt', 'r') as f:
    strings = [line.rstrip('\n') for line in f.readlines() if not line.isspace()]

for string in strings:
    length = len(string)
    if not length in stringsByLength:
        stringsByLength[length] = []
    stringsByLength[length].append(string)

foundHashes = []
for length, hashes in hashesByLength.items():
    if length in stringsByLength:
        for string in stringsByLength[length]:
            if crc32(string) in hashes:
                foundHashes.append((crc32(string), string))

print(foundHashes)
print(len(foundHashes))

with open('param_hashes_dump.csv', 'w') as f:
    for hashPair in foundHashes:
        print(f"{hex(hashPair[0] + (len(hashPair[1]) << 32))},{hashPair[1].lower()}", file=f)
