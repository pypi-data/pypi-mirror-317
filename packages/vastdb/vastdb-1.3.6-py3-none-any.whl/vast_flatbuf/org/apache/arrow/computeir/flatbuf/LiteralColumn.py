# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flatbuf

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

# A single column of literal values.
class LiteralColumn(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = LiteralColumn()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsLiteralColumn(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # LiteralColumn
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # The literal values of the column
    # LiteralColumn
    def Elements(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from vast_flatbuf.org.apache.arrow.computeir.flatbuf.Literal import Literal
            obj = Literal()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # LiteralColumn
    def ElementsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # LiteralColumn
    def ElementsIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        return o == 0

def Start(builder): builder.StartObject(1)
def LiteralColumnStart(builder):
    """This method is deprecated. Please switch to Start."""
    return Start(builder)
def AddElements(builder, elements): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(elements), 0)
def LiteralColumnAddElements(builder, elements):
    """This method is deprecated. Please switch to AddElements."""
    return AddElements(builder, elements)
def StartElementsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def LiteralColumnStartElementsVector(builder, numElems):
    """This method is deprecated. Please switch to Start."""
    return StartElementsVector(builder, numElems)
def End(builder): return builder.EndObject()
def LiteralColumnEnd(builder):
    """This method is deprecated. Please switch to End."""
    return End(builder)