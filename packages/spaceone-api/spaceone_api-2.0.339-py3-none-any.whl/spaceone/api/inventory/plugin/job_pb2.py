# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/inventory/plugin/job.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'spaceone/api/inventory/plugin/job.proto\x12\x1dspaceone.api.inventory.plugin\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\"\x83\x01\n\nTaskFilter\x12\x11\n\tproviders\x18\x01 \x03(\t\x12\x1c\n\x14\x63loud_service_groups\x18\x02 \x03(\t\x12\x1b\n\x13\x63loud_service_types\x18\x03 \x03(\t\x12\x14\n\x0cregion_codes\x18\x04 \x03(\t\x12\x11\n\tresources\x18\x05 \x03(\t\"\xa8\x01\n\x0eGetTaskRequest\x12,\n\x0bsecret_data\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\x12(\n\x07options\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12>\n\x0btask_filter\x18\x03 \x01(\x0b\x32).spaceone.api.inventory.plugin.TaskFilter\"9\n\x08TaskInfo\x12-\n\x0ctask_options\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\"C\n\tTasksInfo\x12\x36\n\x05tasks\x18\x01 \x03(\x0b\x32\'.spaceone.api.inventory.plugin.TaskInfo2m\n\x03Job\x12\x66\n\tget_tasks\x12-.spaceone.api.inventory.plugin.GetTaskRequest\x1a(.spaceone.api.inventory.plugin.TasksInfo\"\x00\x42\x44ZBgithub.com/cloudforet-io/api/dist/go/spaceone/api/inventory/pluginb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.inventory.plugin.job_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'ZBgithub.com/cloudforet-io/api/dist/go/spaceone/api/inventory/plugin'
  _globals['_TASKFILTER']._serialized_start=134
  _globals['_TASKFILTER']._serialized_end=265
  _globals['_GETTASKREQUEST']._serialized_start=268
  _globals['_GETTASKREQUEST']._serialized_end=436
  _globals['_TASKINFO']._serialized_start=438
  _globals['_TASKINFO']._serialized_end=495
  _globals['_TASKSINFO']._serialized_start=497
  _globals['_TASKSINFO']._serialized_end=564
  _globals['_JOB']._serialized_start=566
  _globals['_JOB']._serialized_end=675
# @@protoc_insertion_point(module_scope)
