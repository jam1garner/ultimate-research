offsets = [(0x524FBEC8, 0x4D057C3),
           (0x57201698, 0x67C5E14),
           (0x5D9C74B8, 0x358E8A5),
           (0x60F55D68, 0x4ACBA58),
           (0x65A217C8, 0x9258407),
           (0x6EC79BD8, 0x2FA0811),
           (0x71C1A3F8, 0x16A9A95),
           (0x732C3E98, 0x34B1591),
           (0x76775438, 0xF554FCB)]

with open('data.arc', 'rb') as arc:
    for offset, size in offsets:
        arc.seek(offset)
        with open('webms/{}.webm'.format(hex(offset)), 'wb') as f:
            f.write(arc.read(size))