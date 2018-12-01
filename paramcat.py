import os, sys, struct, operator

def u32(f):
    return struct.unpack('<L', f.read(4))[0]

basename = os.path.splitext(sys.argv[1])[0]
#print(basename)
if not os.path.exists(basename):
    os.mkdir(basename)
with open(sys.argv[1], 'rb') as f:
    f.seek(8)
    hashTableSize = u32(f)
    f.seek(0x10)
    hashTable =  [(u32(f), u32(f)) for i in range(int(hashTableSize / 8))]
    #print(hashTable)

hashTable.sort(key=operator.itemgetter(1))
print(hashTable)

for hash,length in hashTable:
    if length > 8:
        continue
    os.system('hashcat64 --keep-guessing -a 3 -m 11500 -1 ?l?d_ -o {} {} {}'.format(
        # outpath
        os.path.join(basename+"/", "{}.txt".format(hex(hash)[2:])), 
        # hash
        "{:08X}:00000000".format(hash),
        # format
        "?1" * length
    ))