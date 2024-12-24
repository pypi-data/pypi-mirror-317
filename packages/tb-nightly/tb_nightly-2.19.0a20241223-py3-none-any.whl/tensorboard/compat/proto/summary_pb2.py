# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorboard/compat/proto/summary.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tensorboard.compat.proto import histogram_pb2 as tensorboard_dot_compat_dot_proto_dot_histogram__pb2
from tensorboard.compat.proto import tensor_pb2 as tensorboard_dot_compat_dot_proto_dot_tensor__pb2

from tensorboard.compat.proto.histogram_pb2 import *

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&tensorboard/compat/proto/summary.proto\x12\x0btensorboard\x1a(tensorboard/compat/proto/histogram.proto\x1a%tensorboard/compat/proto/tensor.proto\"\'\n\x12SummaryDescription\x12\x11\n\ttype_hint\x18\x01 \x01(\t\"\xe2\x01\n\x0fSummaryMetadata\x12<\n\x0bplugin_data\x18\x01 \x01(\x0b\x32\'.tensorboard.SummaryMetadata.PluginData\x12\x14\n\x0c\x64isplay_name\x18\x02 \x01(\t\x12\x1b\n\x13summary_description\x18\x03 \x01(\t\x12*\n\ndata_class\x18\x04 \x01(\x0e\x32\x16.tensorboard.DataClass\x1a\x32\n\nPluginData\x12\x13\n\x0bplugin_name\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\"\xe4\x04\n\x07Summary\x12)\n\x05value\x18\x01 \x03(\x0b\x32\x1a.tensorboard.Summary.Value\x1aX\n\x05Image\x12\x0e\n\x06height\x18\x01 \x01(\x05\x12\r\n\x05width\x18\x02 \x01(\x05\x12\x12\n\ncolorspace\x18\x03 \x01(\x05\x12\x1c\n\x14\x65ncoded_image_string\x18\x04 \x01(\x0c\x1a}\n\x05\x41udio\x12\x13\n\x0bsample_rate\x18\x01 \x01(\x02\x12\x14\n\x0cnum_channels\x18\x02 \x01(\x03\x12\x15\n\rlength_frames\x18\x03 \x01(\x03\x12\x1c\n\x14\x65ncoded_audio_string\x18\x04 \x01(\x0c\x12\x14\n\x0c\x63ontent_type\x18\x05 \x01(\t\x1a\xd4\x02\n\x05Value\x12\x11\n\tnode_name\x18\x07 \x01(\t\x12\x0b\n\x03tag\x18\x01 \x01(\t\x12.\n\x08metadata\x18\t \x01(\x0b\x32\x1c.tensorboard.SummaryMetadata\x12\x16\n\x0csimple_value\x18\x02 \x01(\x02H\x00\x12&\n\x1cobsolete_old_style_histogram\x18\x03 \x01(\x0cH\x00\x12+\n\x05image\x18\x04 \x01(\x0b\x32\x1a.tensorboard.Summary.ImageH\x00\x12,\n\x05histo\x18\x05 \x01(\x0b\x32\x1b.tensorboard.HistogramProtoH\x00\x12+\n\x05\x61udio\x18\x06 \x01(\x0b\x32\x1a.tensorboard.Summary.AudioH\x00\x12*\n\x06tensor\x18\x08 \x01(\x0b\x32\x18.tensorboard.TensorProtoH\x00\x42\x07\n\x05value*o\n\tDataClass\x12\x16\n\x12\x44\x41TA_CLASS_UNKNOWN\x10\x00\x12\x15\n\x11\x44\x41TA_CLASS_SCALAR\x10\x01\x12\x15\n\x11\x44\x41TA_CLASS_TENSOR\x10\x02\x12\x1c\n\x18\x44\x41TA_CLASS_BLOB_SEQUENCE\x10\x03\x42~\n\x18org.tensorflow.frameworkB\rSummaryProtosP\x01ZNgithub.com/tensorflow/tensorflow/tensorflow/go/core/framework/summary_go_proto\xf8\x01\x01P\x00\x62\x06proto3')

_DATACLASS = DESCRIPTOR.enum_types_by_name['DataClass']
DataClass = enum_type_wrapper.EnumTypeWrapper(_DATACLASS)
DATA_CLASS_UNKNOWN = 0
DATA_CLASS_SCALAR = 1
DATA_CLASS_TENSOR = 2
DATA_CLASS_BLOB_SEQUENCE = 3


_SUMMARYDESCRIPTION = DESCRIPTOR.message_types_by_name['SummaryDescription']
_SUMMARYMETADATA = DESCRIPTOR.message_types_by_name['SummaryMetadata']
_SUMMARYMETADATA_PLUGINDATA = _SUMMARYMETADATA.nested_types_by_name['PluginData']
_SUMMARY = DESCRIPTOR.message_types_by_name['Summary']
_SUMMARY_IMAGE = _SUMMARY.nested_types_by_name['Image']
_SUMMARY_AUDIO = _SUMMARY.nested_types_by_name['Audio']
_SUMMARY_VALUE = _SUMMARY.nested_types_by_name['Value']
SummaryDescription = _reflection.GeneratedProtocolMessageType('SummaryDescription', (_message.Message,), {
  'DESCRIPTOR' : _SUMMARYDESCRIPTION,
  '__module__' : 'tensorboard.compat.proto.summary_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.SummaryDescription)
  })
_sym_db.RegisterMessage(SummaryDescription)

SummaryMetadata = _reflection.GeneratedProtocolMessageType('SummaryMetadata', (_message.Message,), {

  'PluginData' : _reflection.GeneratedProtocolMessageType('PluginData', (_message.Message,), {
    'DESCRIPTOR' : _SUMMARYMETADATA_PLUGINDATA,
    '__module__' : 'tensorboard.compat.proto.summary_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.SummaryMetadata.PluginData)
    })
  ,
  'DESCRIPTOR' : _SUMMARYMETADATA,
  '__module__' : 'tensorboard.compat.proto.summary_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.SummaryMetadata)
  })
_sym_db.RegisterMessage(SummaryMetadata)
_sym_db.RegisterMessage(SummaryMetadata.PluginData)

Summary = _reflection.GeneratedProtocolMessageType('Summary', (_message.Message,), {

  'Image' : _reflection.GeneratedProtocolMessageType('Image', (_message.Message,), {
    'DESCRIPTOR' : _SUMMARY_IMAGE,
    '__module__' : 'tensorboard.compat.proto.summary_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.Summary.Image)
    })
  ,

  'Audio' : _reflection.GeneratedProtocolMessageType('Audio', (_message.Message,), {
    'DESCRIPTOR' : _SUMMARY_AUDIO,
    '__module__' : 'tensorboard.compat.proto.summary_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.Summary.Audio)
    })
  ,

  'Value' : _reflection.GeneratedProtocolMessageType('Value', (_message.Message,), {
    'DESCRIPTOR' : _SUMMARY_VALUE,
    '__module__' : 'tensorboard.compat.proto.summary_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.Summary.Value)
    })
  ,
  'DESCRIPTOR' : _SUMMARY,
  '__module__' : 'tensorboard.compat.proto.summary_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.Summary)
  })
_sym_db.RegisterMessage(Summary)
_sym_db.RegisterMessage(Summary.Image)
_sym_db.RegisterMessage(Summary.Audio)
_sym_db.RegisterMessage(Summary.Value)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030org.tensorflow.frameworkB\rSummaryProtosP\001ZNgithub.com/tensorflow/tensorflow/tensorflow/go/core/framework/summary_go_proto\370\001\001'
  _DATACLASS._serialized_start=1021
  _DATACLASS._serialized_end=1132
  _SUMMARYDESCRIPTION._serialized_start=136
  _SUMMARYDESCRIPTION._serialized_end=175
  _SUMMARYMETADATA._serialized_start=178
  _SUMMARYMETADATA._serialized_end=404
  _SUMMARYMETADATA_PLUGINDATA._serialized_start=354
  _SUMMARYMETADATA_PLUGINDATA._serialized_end=404
  _SUMMARY._serialized_start=407
  _SUMMARY._serialized_end=1019
  _SUMMARY_IMAGE._serialized_start=461
  _SUMMARY_IMAGE._serialized_end=549
  _SUMMARY_AUDIO._serialized_start=551
  _SUMMARY_AUDIO._serialized_end=676
  _SUMMARY_VALUE._serialized_start=679
  _SUMMARY_VALUE._serialized_end=1019
# @@protoc_insertion_point(module_scope)
