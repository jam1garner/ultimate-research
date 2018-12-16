import struct

def uint32(f):
    return struct.unpack('<L', f.read(4))[0]

def readString(myfile):
    chars = []
    while True:
        c = myfile.read(1)
        if c == b'\x00':
            return b''.join(chars).decode('latin')
        chars.append(c)

with open('nus3_found.csv', 'r') as f:
    offsets = [int(i.split(',')[0].rstrip('h'), 16) for i in f.readlines()]

with open('data.arc', 'rb') as f:
    for offset in offsets:
        try:
            f.seek(offset + 4)
            fileSize = uint32(f) + 8
            isNusaudio = (f.read(4) == b'AUDI')
            f.seek(offset + (0x48 if isNusaudio else 0xAD))
            fileName = readString(f)
            fullFileName = "{}_{}.{}".format(fileName, hex(offset), "nus3audio" if isNusaudio else "nus3bank")
            try:
                print(fullFileName)
            except:
                pass
            f.seek(offset)
            with open('nus3audio_uncompressed/'+fullFileName, 'wb') as out:
                out.write(f.read(fileSize))
        except:
            pass
