# automatically generated by the FlatBuffers compiler, do not modify

# namespace: tabular

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class ListProjectionsResponse(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = ListProjectionsResponse()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsListProjectionsResponse(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # ListProjectionsResponse
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # ListProjectionsResponse
    def BucketName(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # ListProjectionsResponse
    def SchemaName(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # ListProjectionsResponse
    def TableName(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # ListProjectionsResponse
    def Projections(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from vast_flatbuf.tabular.ObjectDetails import ObjectDetails
            obj = ObjectDetails()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # ListProjectionsResponse
    def ProjectionsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # ListProjectionsResponse
    def ProjectionsIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        return o == 0

def Start(builder): builder.StartObject(4)
def ListProjectionsResponseStart(builder):
    """This method is deprecated. Please switch to Start."""
    return Start(builder)
def AddBucketName(builder, bucketName): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(bucketName), 0)
def ListProjectionsResponseAddBucketName(builder, bucketName):
    """This method is deprecated. Please switch to AddBucketName."""
    return AddBucketName(builder, bucketName)
def AddSchemaName(builder, schemaName): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(schemaName), 0)
def ListProjectionsResponseAddSchemaName(builder, schemaName):
    """This method is deprecated. Please switch to AddSchemaName."""
    return AddSchemaName(builder, schemaName)
def AddTableName(builder, tableName): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(tableName), 0)
def ListProjectionsResponseAddTableName(builder, tableName):
    """This method is deprecated. Please switch to AddTableName."""
    return AddTableName(builder, tableName)
def AddProjections(builder, projections): builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(projections), 0)
def ListProjectionsResponseAddProjections(builder, projections):
    """This method is deprecated. Please switch to AddProjections."""
    return AddProjections(builder, projections)
def StartProjectionsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def ListProjectionsResponseStartProjectionsVector(builder, numElems):
    """This method is deprecated. Please switch to Start."""
    return StartProjectionsVector(builder, numElems)
def End(builder): return builder.EndObject()
def ListProjectionsResponseEnd(builder):
    """This method is deprecated. Please switch to End."""
    return End(builder)