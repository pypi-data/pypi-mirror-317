# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flatbuf

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

# A function call expression
class Call(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Call()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsCall(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Call
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # The function to call
    # Call
    def Name(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # The arguments passed to `name`.
    # Call
    def Arguments(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from vast_flatbuf.org.apache.arrow.computeir.flatbuf.Expression import Expression
            obj = Expression()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Call
    def ArgumentsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Call
    def ArgumentsIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

    # Possible ordering of input. These are useful
    # in aggregates where ordering in meaningful such as
    # string concatenation
    # Call
    def Orderings(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from vast_flatbuf.org.apache.arrow.computeir.flatbuf.SortKey import SortKey
            obj = SortKey()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Call
    def OrderingsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Call
    def OrderingsIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        return o == 0

def Start(builder): builder.StartObject(3)
def CallStart(builder):
    """This method is deprecated. Please switch to Start."""
    return Start(builder)
def AddName(builder, name): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(name), 0)
def CallAddName(builder, name):
    """This method is deprecated. Please switch to AddName."""
    return AddName(builder, name)
def AddArguments(builder, arguments): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(arguments), 0)
def CallAddArguments(builder, arguments):
    """This method is deprecated. Please switch to AddArguments."""
    return AddArguments(builder, arguments)
def StartArgumentsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def CallStartArgumentsVector(builder, numElems):
    """This method is deprecated. Please switch to Start."""
    return StartArgumentsVector(builder, numElems)
def AddOrderings(builder, orderings): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(orderings), 0)
def CallAddOrderings(builder, orderings):
    """This method is deprecated. Please switch to AddOrderings."""
    return AddOrderings(builder, orderings)
def StartOrderingsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def CallStartOrderingsVector(builder, numElems):
    """This method is deprecated. Please switch to Start."""
    return StartOrderingsVector(builder, numElems)
def End(builder): return builder.EndObject()
def CallEnd(builder):
    """This method is deprecated. Please switch to End."""
    return End(builder)