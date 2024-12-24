# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorboard/compat/proto/meta_graph.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from tensorboard.compat.proto import graph_pb2 as tensorboard_dot_compat_dot_proto_dot_graph__pb2
from tensorboard.compat.proto import op_def_pb2 as tensorboard_dot_compat_dot_proto_dot_op__def__pb2
from tensorboard.compat.proto import tensor_pb2 as tensorboard_dot_compat_dot_proto_dot_tensor__pb2
from tensorboard.compat.proto import tensor_shape_pb2 as tensorboard_dot_compat_dot_proto_dot_tensor__shape__pb2
from tensorboard.compat.proto import types_pb2 as tensorboard_dot_compat_dot_proto_dot_types__pb2
from tensorboard.compat.proto import saved_object_graph_pb2 as tensorboard_dot_compat_dot_proto_dot_saved__object__graph__pb2
from tensorboard.compat.proto import saver_pb2 as tensorboard_dot_compat_dot_proto_dot_saver__pb2
from tensorboard.compat.proto import struct_pb2 as tensorboard_dot_compat_dot_proto_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)tensorboard/compat/proto/meta_graph.proto\x12\x0btensorboard\x1a\x19google/protobuf/any.proto\x1a$tensorboard/compat/proto/graph.proto\x1a%tensorboard/compat/proto/op_def.proto\x1a%tensorboard/compat/proto/tensor.proto\x1a+tensorboard/compat/proto/tensor_shape.proto\x1a$tensorboard/compat/proto/types.proto\x1a\x31tensorboard/compat/proto/saved_object_graph.proto\x1a$tensorboard/compat/proto/saver.proto\x1a%tensorboard/compat/proto/struct.proto\"\xb3\x07\n\x0cMetaGraphDef\x12<\n\rmeta_info_def\x18\x01 \x01(\x0b\x32%.tensorboard.MetaGraphDef.MetaInfoDef\x12(\n\tgraph_def\x18\x02 \x01(\x0b\x32\x15.tensorboard.GraphDef\x12(\n\tsaver_def\x18\x03 \x01(\x0b\x32\x15.tensorboard.SaverDef\x12\x44\n\x0e\x63ollection_def\x18\x04 \x03(\x0b\x32,.tensorboard.MetaGraphDef.CollectionDefEntry\x12\x42\n\rsignature_def\x18\x05 \x03(\x0b\x32+.tensorboard.MetaGraphDef.SignatureDefEntry\x12\x31\n\x0e\x61sset_file_def\x18\x06 \x03(\x0b\x32\x19.tensorboard.AssetFileDef\x12\x37\n\x10object_graph_def\x18\x07 \x01(\x0b\x32\x1d.tensorboard.SavedObjectGraph\x1a\xf8\x02\n\x0bMetaInfoDef\x12\x1a\n\x12meta_graph_version\x18\x01 \x01(\t\x12-\n\x10stripped_op_list\x18\x02 \x01(\x0b\x32\x13.tensorboard.OpList\x12&\n\x08\x61ny_info\x18\x03 \x01(\x0b\x32\x14.google.protobuf.Any\x12\x0c\n\x04tags\x18\x04 \x03(\t\x12\x1a\n\x12tensorflow_version\x18\x05 \x01(\t\x12\x1e\n\x16tensorflow_git_version\x18\x06 \x01(\t\x12\x1e\n\x16stripped_default_attrs\x18\x07 \x01(\x08\x12T\n\x10\x66unction_aliases\x18\x08 \x03(\x0b\x32:.tensorboard.MetaGraphDef.MetaInfoDef.FunctionAliasesEntry\x1a\x36\n\x14\x46unctionAliasesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1aP\n\x12\x43ollectionDefEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12)\n\x05value\x18\x02 \x01(\x0b\x32\x1a.tensorboard.CollectionDef:\x02\x38\x01\x1aN\n\x11SignatureDefEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12(\n\x05value\x18\x02 \x01(\x0b\x32\x19.tensorboard.SignatureDef:\x02\x38\x01\"\xe4\x03\n\rCollectionDef\x12\x38\n\tnode_list\x18\x01 \x01(\x0b\x32#.tensorboard.CollectionDef.NodeListH\x00\x12:\n\nbytes_list\x18\x02 \x01(\x0b\x32$.tensorboard.CollectionDef.BytesListH\x00\x12:\n\nint64_list\x18\x03 \x01(\x0b\x32$.tensorboard.CollectionDef.Int64ListH\x00\x12:\n\nfloat_list\x18\x04 \x01(\x0b\x32$.tensorboard.CollectionDef.FloatListH\x00\x12\x36\n\x08\x61ny_list\x18\x05 \x01(\x0b\x32\".tensorboard.CollectionDef.AnyListH\x00\x1a\x19\n\x08NodeList\x12\r\n\x05value\x18\x01 \x03(\t\x1a\x1a\n\tBytesList\x12\r\n\x05value\x18\x01 \x03(\x0c\x1a\x1e\n\tInt64List\x12\x11\n\x05value\x18\x01 \x03(\x03\x42\x02\x10\x01\x1a\x1e\n\tFloatList\x12\x11\n\x05value\x18\x01 \x03(\x02\x42\x02\x10\x01\x1a.\n\x07\x41nyList\x12#\n\x05value\x18\x01 \x03(\x0b\x32\x14.google.protobuf.AnyB\x06\n\x04kind\"\xd7\x03\n\nTensorInfo\x12\x0e\n\x04name\x18\x01 \x01(\tH\x00\x12\x37\n\ncoo_sparse\x18\x04 \x01(\x0b\x32!.tensorboard.TensorInfo.CooSparseH\x00\x12\x43\n\x10\x63omposite_tensor\x18\x05 \x01(\x0b\x32\'.tensorboard.TensorInfo.CompositeTensorH\x00\x12$\n\x05\x64type\x18\x02 \x01(\x0e\x32\x15.tensorboard.DataType\x12\x33\n\x0ctensor_shape\x18\x03 \x01(\x0b\x32\x1d.tensorboard.TensorShapeProto\x1a\x65\n\tCooSparse\x12\x1a\n\x12values_tensor_name\x18\x01 \x01(\t\x12\x1b\n\x13indices_tensor_name\x18\x02 \x01(\t\x12\x1f\n\x17\x64\x65nse_shape_tensor_name\x18\x03 \x01(\t\x1am\n\x0f\x43ompositeTensor\x12-\n\ttype_spec\x18\x01 \x01(\x0b\x32\x1a.tensorboard.TypeSpecProto\x12+\n\ncomponents\x18\x02 \x03(\x0b\x32\x17.tensorboard.TensorInfoB\n\n\x08\x65ncoding\"\xaa\x03\n\x0cSignatureDef\x12\x35\n\x06inputs\x18\x01 \x03(\x0b\x32%.tensorboard.SignatureDef.InputsEntry\x12\x37\n\x07outputs\x18\x02 \x03(\x0b\x32&.tensorboard.SignatureDef.OutputsEntry\x12\x13\n\x0bmethod_name\x18\x03 \x01(\t\x12\x39\n\x08\x64\x65\x66\x61ults\x18\x04 \x03(\x0b\x32\'.tensorboard.SignatureDef.DefaultsEntry\x1a\x46\n\x0bInputsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12&\n\x05value\x18\x02 \x01(\x0b\x32\x17.tensorboard.TensorInfo:\x02\x38\x01\x1aG\n\x0cOutputsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12&\n\x05value\x18\x02 \x01(\x0b\x32\x17.tensorboard.TensorInfo:\x02\x38\x01\x1aI\n\rDefaultsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\'\n\x05value\x18\x02 \x01(\x0b\x32\x18.tensorboard.TensorProto:\x02\x38\x01\"N\n\x0c\x41ssetFileDef\x12,\n\x0btensor_info\x18\x01 \x01(\x0b\x32\x17.tensorboard.TensorInfo\x12\x10\n\x08\x66ilename\x18\x02 \x01(\tB\x87\x01\n\x18org.tensorflow.frameworkB\x0fMetaGraphProtosP\x01ZUgithub.com/tensorflow/tensorflow/tensorflow/go/core/protobuf/for_core_protos_go_proto\xf8\x01\x01\x62\x06proto3')



_METAGRAPHDEF = DESCRIPTOR.message_types_by_name['MetaGraphDef']
_METAGRAPHDEF_METAINFODEF = _METAGRAPHDEF.nested_types_by_name['MetaInfoDef']
_METAGRAPHDEF_METAINFODEF_FUNCTIONALIASESENTRY = _METAGRAPHDEF_METAINFODEF.nested_types_by_name['FunctionAliasesEntry']
_METAGRAPHDEF_COLLECTIONDEFENTRY = _METAGRAPHDEF.nested_types_by_name['CollectionDefEntry']
_METAGRAPHDEF_SIGNATUREDEFENTRY = _METAGRAPHDEF.nested_types_by_name['SignatureDefEntry']
_COLLECTIONDEF = DESCRIPTOR.message_types_by_name['CollectionDef']
_COLLECTIONDEF_NODELIST = _COLLECTIONDEF.nested_types_by_name['NodeList']
_COLLECTIONDEF_BYTESLIST = _COLLECTIONDEF.nested_types_by_name['BytesList']
_COLLECTIONDEF_INT64LIST = _COLLECTIONDEF.nested_types_by_name['Int64List']
_COLLECTIONDEF_FLOATLIST = _COLLECTIONDEF.nested_types_by_name['FloatList']
_COLLECTIONDEF_ANYLIST = _COLLECTIONDEF.nested_types_by_name['AnyList']
_TENSORINFO = DESCRIPTOR.message_types_by_name['TensorInfo']
_TENSORINFO_COOSPARSE = _TENSORINFO.nested_types_by_name['CooSparse']
_TENSORINFO_COMPOSITETENSOR = _TENSORINFO.nested_types_by_name['CompositeTensor']
_SIGNATUREDEF = DESCRIPTOR.message_types_by_name['SignatureDef']
_SIGNATUREDEF_INPUTSENTRY = _SIGNATUREDEF.nested_types_by_name['InputsEntry']
_SIGNATUREDEF_OUTPUTSENTRY = _SIGNATUREDEF.nested_types_by_name['OutputsEntry']
_SIGNATUREDEF_DEFAULTSENTRY = _SIGNATUREDEF.nested_types_by_name['DefaultsEntry']
_ASSETFILEDEF = DESCRIPTOR.message_types_by_name['AssetFileDef']
MetaGraphDef = _reflection.GeneratedProtocolMessageType('MetaGraphDef', (_message.Message,), {

  'MetaInfoDef' : _reflection.GeneratedProtocolMessageType('MetaInfoDef', (_message.Message,), {

    'FunctionAliasesEntry' : _reflection.GeneratedProtocolMessageType('FunctionAliasesEntry', (_message.Message,), {
      'DESCRIPTOR' : _METAGRAPHDEF_METAINFODEF_FUNCTIONALIASESENTRY,
      '__module__' : 'tensorboard.compat.proto.meta_graph_pb2'
      # @@protoc_insertion_point(class_scope:tensorboard.MetaGraphDef.MetaInfoDef.FunctionAliasesEntry)
      })
    ,
    'DESCRIPTOR' : _METAGRAPHDEF_METAINFODEF,
    '__module__' : 'tensorboard.compat.proto.meta_graph_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.MetaGraphDef.MetaInfoDef)
    })
  ,

  'CollectionDefEntry' : _reflection.GeneratedProtocolMessageType('CollectionDefEntry', (_message.Message,), {
    'DESCRIPTOR' : _METAGRAPHDEF_COLLECTIONDEFENTRY,
    '__module__' : 'tensorboard.compat.proto.meta_graph_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.MetaGraphDef.CollectionDefEntry)
    })
  ,

  'SignatureDefEntry' : _reflection.GeneratedProtocolMessageType('SignatureDefEntry', (_message.Message,), {
    'DESCRIPTOR' : _METAGRAPHDEF_SIGNATUREDEFENTRY,
    '__module__' : 'tensorboard.compat.proto.meta_graph_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.MetaGraphDef.SignatureDefEntry)
    })
  ,
  'DESCRIPTOR' : _METAGRAPHDEF,
  '__module__' : 'tensorboard.compat.proto.meta_graph_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.MetaGraphDef)
  })
_sym_db.RegisterMessage(MetaGraphDef)
_sym_db.RegisterMessage(MetaGraphDef.MetaInfoDef)
_sym_db.RegisterMessage(MetaGraphDef.MetaInfoDef.FunctionAliasesEntry)
_sym_db.RegisterMessage(MetaGraphDef.CollectionDefEntry)
_sym_db.RegisterMessage(MetaGraphDef.SignatureDefEntry)

CollectionDef = _reflection.GeneratedProtocolMessageType('CollectionDef', (_message.Message,), {

  'NodeList' : _reflection.GeneratedProtocolMessageType('NodeList', (_message.Message,), {
    'DESCRIPTOR' : _COLLECTIONDEF_NODELIST,
    '__module__' : 'tensorboard.compat.proto.meta_graph_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.CollectionDef.NodeList)
    })
  ,

  'BytesList' : _reflection.GeneratedProtocolMessageType('BytesList', (_message.Message,), {
    'DESCRIPTOR' : _COLLECTIONDEF_BYTESLIST,
    '__module__' : 'tensorboard.compat.proto.meta_graph_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.CollectionDef.BytesList)
    })
  ,

  'Int64List' : _reflection.GeneratedProtocolMessageType('Int64List', (_message.Message,), {
    'DESCRIPTOR' : _COLLECTIONDEF_INT64LIST,
    '__module__' : 'tensorboard.compat.proto.meta_graph_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.CollectionDef.Int64List)
    })
  ,

  'FloatList' : _reflection.GeneratedProtocolMessageType('FloatList', (_message.Message,), {
    'DESCRIPTOR' : _COLLECTIONDEF_FLOATLIST,
    '__module__' : 'tensorboard.compat.proto.meta_graph_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.CollectionDef.FloatList)
    })
  ,

  'AnyList' : _reflection.GeneratedProtocolMessageType('AnyList', (_message.Message,), {
    'DESCRIPTOR' : _COLLECTIONDEF_ANYLIST,
    '__module__' : 'tensorboard.compat.proto.meta_graph_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.CollectionDef.AnyList)
    })
  ,
  'DESCRIPTOR' : _COLLECTIONDEF,
  '__module__' : 'tensorboard.compat.proto.meta_graph_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.CollectionDef)
  })
_sym_db.RegisterMessage(CollectionDef)
_sym_db.RegisterMessage(CollectionDef.NodeList)
_sym_db.RegisterMessage(CollectionDef.BytesList)
_sym_db.RegisterMessage(CollectionDef.Int64List)
_sym_db.RegisterMessage(CollectionDef.FloatList)
_sym_db.RegisterMessage(CollectionDef.AnyList)

TensorInfo = _reflection.GeneratedProtocolMessageType('TensorInfo', (_message.Message,), {

  'CooSparse' : _reflection.GeneratedProtocolMessageType('CooSparse', (_message.Message,), {
    'DESCRIPTOR' : _TENSORINFO_COOSPARSE,
    '__module__' : 'tensorboard.compat.proto.meta_graph_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.TensorInfo.CooSparse)
    })
  ,

  'CompositeTensor' : _reflection.GeneratedProtocolMessageType('CompositeTensor', (_message.Message,), {
    'DESCRIPTOR' : _TENSORINFO_COMPOSITETENSOR,
    '__module__' : 'tensorboard.compat.proto.meta_graph_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.TensorInfo.CompositeTensor)
    })
  ,
  'DESCRIPTOR' : _TENSORINFO,
  '__module__' : 'tensorboard.compat.proto.meta_graph_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.TensorInfo)
  })
_sym_db.RegisterMessage(TensorInfo)
_sym_db.RegisterMessage(TensorInfo.CooSparse)
_sym_db.RegisterMessage(TensorInfo.CompositeTensor)

SignatureDef = _reflection.GeneratedProtocolMessageType('SignatureDef', (_message.Message,), {

  'InputsEntry' : _reflection.GeneratedProtocolMessageType('InputsEntry', (_message.Message,), {
    'DESCRIPTOR' : _SIGNATUREDEF_INPUTSENTRY,
    '__module__' : 'tensorboard.compat.proto.meta_graph_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.SignatureDef.InputsEntry)
    })
  ,

  'OutputsEntry' : _reflection.GeneratedProtocolMessageType('OutputsEntry', (_message.Message,), {
    'DESCRIPTOR' : _SIGNATUREDEF_OUTPUTSENTRY,
    '__module__' : 'tensorboard.compat.proto.meta_graph_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.SignatureDef.OutputsEntry)
    })
  ,

  'DefaultsEntry' : _reflection.GeneratedProtocolMessageType('DefaultsEntry', (_message.Message,), {
    'DESCRIPTOR' : _SIGNATUREDEF_DEFAULTSENTRY,
    '__module__' : 'tensorboard.compat.proto.meta_graph_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.SignatureDef.DefaultsEntry)
    })
  ,
  'DESCRIPTOR' : _SIGNATUREDEF,
  '__module__' : 'tensorboard.compat.proto.meta_graph_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.SignatureDef)
  })
_sym_db.RegisterMessage(SignatureDef)
_sym_db.RegisterMessage(SignatureDef.InputsEntry)
_sym_db.RegisterMessage(SignatureDef.OutputsEntry)
_sym_db.RegisterMessage(SignatureDef.DefaultsEntry)

AssetFileDef = _reflection.GeneratedProtocolMessageType('AssetFileDef', (_message.Message,), {
  'DESCRIPTOR' : _ASSETFILEDEF,
  '__module__' : 'tensorboard.compat.proto.meta_graph_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.AssetFileDef)
  })
_sym_db.RegisterMessage(AssetFileDef)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030org.tensorflow.frameworkB\017MetaGraphProtosP\001ZUgithub.com/tensorflow/tensorflow/tensorflow/go/core/protobuf/for_core_protos_go_proto\370\001\001'
  _METAGRAPHDEF_METAINFODEF_FUNCTIONALIASESENTRY._options = None
  _METAGRAPHDEF_METAINFODEF_FUNCTIONALIASESENTRY._serialized_options = b'8\001'
  _METAGRAPHDEF_COLLECTIONDEFENTRY._options = None
  _METAGRAPHDEF_COLLECTIONDEFENTRY._serialized_options = b'8\001'
  _METAGRAPHDEF_SIGNATUREDEFENTRY._options = None
  _METAGRAPHDEF_SIGNATUREDEFENTRY._serialized_options = b'8\001'
  _COLLECTIONDEF_INT64LIST.fields_by_name['value']._options = None
  _COLLECTIONDEF_INT64LIST.fields_by_name['value']._serialized_options = b'\020\001'
  _COLLECTIONDEF_FLOATLIST.fields_by_name['value']._options = None
  _COLLECTIONDEF_FLOATLIST.fields_by_name['value']._serialized_options = b'\020\001'
  _SIGNATUREDEF_INPUTSENTRY._options = None
  _SIGNATUREDEF_INPUTSENTRY._serialized_options = b'8\001'
  _SIGNATUREDEF_OUTPUTSENTRY._options = None
  _SIGNATUREDEF_OUTPUTSENTRY._serialized_options = b'8\001'
  _SIGNATUREDEF_DEFAULTSENTRY._options = None
  _SIGNATUREDEF_DEFAULTSENTRY._serialized_options = b'8\001'
  _METAGRAPHDEF._serialized_start=413
  _METAGRAPHDEF._serialized_end=1360
  _METAGRAPHDEF_METAINFODEF._serialized_start=822
  _METAGRAPHDEF_METAINFODEF._serialized_end=1198
  _METAGRAPHDEF_METAINFODEF_FUNCTIONALIASESENTRY._serialized_start=1144
  _METAGRAPHDEF_METAINFODEF_FUNCTIONALIASESENTRY._serialized_end=1198
  _METAGRAPHDEF_COLLECTIONDEFENTRY._serialized_start=1200
  _METAGRAPHDEF_COLLECTIONDEFENTRY._serialized_end=1280
  _METAGRAPHDEF_SIGNATUREDEFENTRY._serialized_start=1282
  _METAGRAPHDEF_SIGNATUREDEFENTRY._serialized_end=1360
  _COLLECTIONDEF._serialized_start=1363
  _COLLECTIONDEF._serialized_end=1847
  _COLLECTIONDEF_NODELIST._serialized_start=1674
  _COLLECTIONDEF_NODELIST._serialized_end=1699
  _COLLECTIONDEF_BYTESLIST._serialized_start=1701
  _COLLECTIONDEF_BYTESLIST._serialized_end=1727
  _COLLECTIONDEF_INT64LIST._serialized_start=1729
  _COLLECTIONDEF_INT64LIST._serialized_end=1759
  _COLLECTIONDEF_FLOATLIST._serialized_start=1761
  _COLLECTIONDEF_FLOATLIST._serialized_end=1791
  _COLLECTIONDEF_ANYLIST._serialized_start=1793
  _COLLECTIONDEF_ANYLIST._serialized_end=1839
  _TENSORINFO._serialized_start=1850
  _TENSORINFO._serialized_end=2321
  _TENSORINFO_COOSPARSE._serialized_start=2097
  _TENSORINFO_COOSPARSE._serialized_end=2198
  _TENSORINFO_COMPOSITETENSOR._serialized_start=2200
  _TENSORINFO_COMPOSITETENSOR._serialized_end=2309
  _SIGNATUREDEF._serialized_start=2324
  _SIGNATUREDEF._serialized_end=2750
  _SIGNATUREDEF_INPUTSENTRY._serialized_start=2532
  _SIGNATUREDEF_INPUTSENTRY._serialized_end=2602
  _SIGNATUREDEF_OUTPUTSENTRY._serialized_start=2604
  _SIGNATUREDEF_OUTPUTSENTRY._serialized_end=2675
  _SIGNATUREDEF_DEFAULTSENTRY._serialized_start=2677
  _SIGNATUREDEF_DEFAULTSENTRY._serialized_end=2750
  _ASSETFILEDEF._serialized_start=2752
  _ASSETFILEDEF._serialized_end=2830
# @@protoc_insertion_point(module_scope)
