import sys
import xml.etree.cElementTree as ET
import struct
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import SubElement

def u32(f):
    return struct.unpack('<L', f.read(4))[0]

def s32(f):
    return struct.unpack('<l', f.read(4))[0]

def f32(f):
    return struct.unpack('<f', f.read(4))[0]

def s16(f):
    return struct.unpack('<h', f.read(2))[0]

def EOF(f):
    temp = f.tell()
    f.seek(0, 2)
    retVal = f.tell()
    f.seek(temp)
    return retVal

class int32(int):
    pass

class uint32(int):
    pass

class unkInt(int):
    def __init__(self):
        self.type = 0

class short(int):
    pass

class ParamGroup(list):
    def __init__(self, itemCount=0, unk=0):
        self.itemCount = itemCount
        self.unk = unk

class Uint32Array(list):
    def __bytes__(self, f):
        return b''.join([b'\x0B', struct.pack('<L', len(self))] + [struct.pack('<L', i) for i in self])

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

def buildParamXml(parent, param):
    # Recursively build an XML tree from a param
    if type(param) == bool:
        ET.SubElement(parent, "bool").text = str(param)
    elif type(param) == short:
        ET.SubElement(parent, "short").text = str(param)
    elif type(param) == int32:
        ET.SubElement(parent, "int32").text = hex(param)
    elif type(param) == uint32:
        ET.SubElement(parent, "uint32").text = hex(param)
    elif type(param) == float:
        ET.SubElement(parent, "float").text = str(param)
    elif type(param) == unkInt:
        ET.SubElement(parent, "unkInt", type=param.type).text = str(param)
    elif type(param) == Uint32Array:
        ET.SubElement(parent, "Uint32Array").text = " ".join([str(i) for i in param])
    elif type(param) == ParamGroup:
        paramGroupNode = ET.SubElement(parent, "ParamGroup", unk=str(param.unk))
        for p in param:
            buildParamXml(paramGroupNode, p)

class UltimateParam:
    class Header:
        def __init__(self, file):
            self.read(file)
        
        def read(self, f):
            f.seek(0)
            self.magic = f.read(8).decode('ascii')
            crcTableSize = u32(f)
            otherTableSize = u32(f)
            self.crcTable = [(f.read(4), f.read(4)) for i in range(int(crcTableSize / 8))]
            self.otherTable = [(f.read(4), f.read(4)) for i in range(int(otherTableSize / 8))]
    
    def __init__(self, file):
        self.header = None
        self.params = []
        self.read(file)
    
    def groupParams(self):
        tempParams = []
        while len(self.params) > 0:
            current = self.params.pop()
            if type(current) == ParamGroup:
                for i in range(current.itemCount):
                    current.append(tempParams.pop(0))
            tempParams.insert(0, current)
        self.params = tempParams

    def read(self, f):
        eof = EOF(f)
        self.header = UltimateParam.Header(f)
        while f.tell() != eof:
            paramType = f.read(1)
            if paramType == b'\x01':
                self.params.append(bool(f.read(1)))
            elif paramType == b'\x04':
                self.params.append(short(s16(f)))
            elif paramType == b'\x06':
                self.params.append(int32(s32(f)))
            elif paramType == b'\x08':
                self.params.append(f32(f))
            elif paramType == b'\x09':
                self.params.append(uint32(u32(f)))
            elif paramType == b'\x0B':
                l = u32(f)
                self.params.append(Uint32Array([u32(f) for i in range(l)]))
            elif paramType in [b'\x07']:
                p = unkInt(u32(f))
                p.type = int(paramType)
                self.params.append(p)
            elif paramType == b'\x0C':    
                self.params.append(ParamGroup(u32(f), u32(f)))
            else:
                raise Exception('Type {} at position {}'.format(paramType, f.tell() - 1))
        self.groupParams()

    def writeXml(self, filename):
        root = ET.Element("params")
        for param in self.params:
            buildParamXml(root, param)
        with open(filename, 'w') as f:
            f.write(prettify(root))


with open(sys.argv[1], 'rb') as f:
    param = UltimateParam(f)
    outputName = sys.argv[1] + ".xml"
    param.writeXml(outputName)