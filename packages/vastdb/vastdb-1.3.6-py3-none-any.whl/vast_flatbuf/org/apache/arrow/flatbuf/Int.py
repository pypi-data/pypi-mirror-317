# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flatbuf

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Int(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Int()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsInt(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Int
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Int
    def BitWidth(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # Int
    def IsSigned(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

def Start(builder): builder.StartObject(2)
def IntStart(builder):
    """This method is deprecated. Please switch to Start."""
    return Start(builder)
def AddBitWidth(builder, bitWidth): builder.PrependInt32Slot(0, bitWidth, 0)
def IntAddBitWidth(builder, bitWidth):
    """This method is deprecated. Please switch to AddBitWidth."""
    return AddBitWidth(builder, bitWidth)
def AddIsSigned(builder, isSigned): builder.PrependBoolSlot(1, isSigned, 0)
def IntAddIsSigned(builder, isSigned):
    """This method is deprecated. Please switch to AddIsSigned."""
    return AddIsSigned(builder, isSigned)
def End(builder): return builder.EndObject()
def IntEnd(builder):
    """This method is deprecated. Please switch to End."""
    return End(builder)