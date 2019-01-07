import sys
import struct

def u32(f):
    return struct.unpack('<L', f.read(4))[0]

with open(sys.argv[1], 'rb') as f:
    f.seek(8)
    size = u32(f)
    f.seek(0x10)
    count = int(size / 8)
    print('Hash,       Length')
    for i in range(count):
        hash,length = u32(f), u32(f)
        print(f'0x{hash:08X}, 0x{length:02X}')
