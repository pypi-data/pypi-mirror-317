# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorboard/compat/proto/cluster.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&tensorboard/compat/proto/cluster.proto\x12\x0btensorboard\"s\n\x06JobDef\x12\x0c\n\x04name\x18\x01 \x01(\t\x12-\n\x05tasks\x18\x02 \x03(\x0b\x32\x1e.tensorboard.JobDef.TasksEntry\x1a,\n\nTasksEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\".\n\nClusterDef\x12 \n\x03job\x18\x01 \x03(\x0b\x32\x13.tensorboard.JobDefB\x87\x01\n\x1aorg.tensorflow.distruntimeB\rClusterProtosP\x01ZUgithub.com/tensorflow/tensorflow/tensorflow/go/core/protobuf/for_core_protos_go_proto\xf8\x01\x01\x62\x06proto3')



_JOBDEF = DESCRIPTOR.message_types_by_name['JobDef']
_JOBDEF_TASKSENTRY = _JOBDEF.nested_types_by_name['TasksEntry']
_CLUSTERDEF = DESCRIPTOR.message_types_by_name['ClusterDef']
JobDef = _reflection.GeneratedProtocolMessageType('JobDef', (_message.Message,), {

  'TasksEntry' : _reflection.GeneratedProtocolMessageType('TasksEntry', (_message.Message,), {
    'DESCRIPTOR' : _JOBDEF_TASKSENTRY,
    '__module__' : 'tensorboard.compat.proto.cluster_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.JobDef.TasksEntry)
    })
  ,
  'DESCRIPTOR' : _JOBDEF,
  '__module__' : 'tensorboard.compat.proto.cluster_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.JobDef)
  })
_sym_db.RegisterMessage(JobDef)
_sym_db.RegisterMessage(JobDef.TasksEntry)

ClusterDef = _reflection.GeneratedProtocolMessageType('ClusterDef', (_message.Message,), {
  'DESCRIPTOR' : _CLUSTERDEF,
  '__module__' : 'tensorboard.compat.proto.cluster_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.ClusterDef)
  })
_sym_db.RegisterMessage(ClusterDef)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\032org.tensorflow.distruntimeB\rClusterProtosP\001ZUgithub.com/tensorflow/tensorflow/tensorflow/go/core/protobuf/for_core_protos_go_proto\370\001\001'
  _JOBDEF_TASKSENTRY._options = None
  _JOBDEF_TASKSENTRY._serialized_options = b'8\001'
  _JOBDEF._serialized_start=55
  _JOBDEF._serialized_end=170
  _JOBDEF_TASKSENTRY._serialized_start=126
  _JOBDEF_TASKSENTRY._serialized_end=170
  _CLUSTERDEF._serialized_start=172
  _CLUSTERDEF._serialized_end=218
# @@protoc_insertion_point(module_scope)
