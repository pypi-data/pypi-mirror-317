# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/cost_analysis/v1/job_task.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from spaceone.api.core.v2 import query_pb2 as spaceone_dot_api_dot_core_dot_v2_dot_query__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,spaceone/api/cost_analysis/v1/job_task.proto\x12\x1dspaceone.api.cost_analysis.v1\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v2/query.proto\"%\n\x0eJobTaskRequest\x12\x13\n\x0bjob_task_id\x18\x01 \x01(\t\"\xbe\x02\n\x0cJobTaskQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v2.Query\x12\x13\n\x0bjob_task_id\x18\x02 \x01(\t\x12\x42\n\x06status\x18\x03 \x01(\x0e\x32\x32.spaceone.api.cost_analysis.v1.JobTaskQuery.Status\x12\x14\n\x0cworkspace_id\x18\x15 \x01(\t\x12\x0e\n\x06job_id\x18\x16 \x01(\t\x12\x16\n\x0e\x64\x61ta_source_id\x18\x17 \x01(\t\"k\n\x06Status\x12\x0e\n\nSCOPE_NONE\x10\x00\x12\x0b\n\x07PENDING\x10\x01\x12\x0f\n\x0bIN_PROGRESS\x10\x02\x12\x0b\n\x07SUCCESS\x10\x03\x12\x0b\n\x07\x46\x41ILURE\x10\x04\x12\x0b\n\x07TIMEOUT\x10\x05\x12\x0c\n\x08\x43\x41NCELED\x10\x06\"\xf7\x04\n\x0bJobTaskInfo\x12\x13\n\x0bjob_task_id\x18\x01 \x01(\t\x12\x41\n\x06status\x18\x02 \x01(\x0e\x32\x31.spaceone.api.cost_analysis.v1.JobTaskInfo.Status\x12(\n\x07options\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x15\n\rcreated_count\x18\x04 \x01(\x05\x12\x12\n\nerror_code\x18\x05 \x01(\t\x12\x15\n\rerror_message\x18\x06 \x01(\t\x12P\n\x0eresource_group\x18\x14 \x01(\x0e\x32\x38.spaceone.api.cost_analysis.v1.JobTaskInfo.ResourceGroup\x12\x11\n\tdomain_id\x18\x15 \x01(\t\x12\x14\n\x0cworkspace_id\x18\x16 \x01(\t\x12\x0e\n\x06job_id\x18\x17 \x01(\t\x12\x16\n\x0e\x64\x61ta_source_id\x18\x18 \x01(\t\x12\x12\n\ncreated_at\x18\x1f \x01(\t\x12\x12\n\nstarted_at\x18  \x01(\t\x12\x12\n\nupdated_at\x18! \x01(\t\x12\x13\n\x0b\x66inished_at\x18\" \x01(\t\"k\n\x06Status\x12\x0e\n\nSCOPE_NONE\x10\x00\x12\x0b\n\x07PENDING\x10\x01\x12\x0f\n\x0bIN_PROGRESS\x10\x02\x12\x0b\n\x07SUCCESS\x10\x03\x12\x0b\n\x07\x46\x41ILURE\x10\x04\x12\x0b\n\x07TIMEOUT\x10\x05\x12\x0c\n\x08\x43\x41NCELED\x10\x06\"C\n\rResourceGroup\x12\x17\n\x13RESOURCE_GROUP_NONE\x10\x00\x12\n\n\x06\x44OMAIN\x10\x01\x12\r\n\tWORKSPACE\x10\x02\"`\n\x0cJobTasksInfo\x12;\n\x07results\x18\x01 \x03(\x0b\x32*.spaceone.api.cost_analysis.v1.JobTaskInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"H\n\x10JobTaskStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v2.StatisticsQuery2\xa4\x03\n\x07JobTask\x12\x8b\x01\n\x03get\x12-.spaceone.api.cost_analysis.v1.JobTaskRequest\x1a*.spaceone.api.cost_analysis.v1.JobTaskInfo\")\x82\xd3\xe4\x93\x02#\"\x1e/cost-analysis/v1/job-task/get:\x01*\x12\x8c\x01\n\x04list\x12+.spaceone.api.cost_analysis.v1.JobTaskQuery\x1a+.spaceone.api.cost_analysis.v1.JobTasksInfo\"*\x82\xd3\xe4\x93\x02$\"\x1f/cost-analysis/v1/job-task/list:\x01*\x12|\n\x04stat\x12/.spaceone.api.cost_analysis.v1.JobTaskStatQuery\x1a\x17.google.protobuf.Struct\"*\x82\xd3\xe4\x93\x02$\"\x1f/cost-analysis/v1/job-task/stat:\x01*BDZBgithub.com/cloudforet-io/api/dist/go/spaceone/api/cost_analysis/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.cost_analysis.v1.job_task_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'ZBgithub.com/cloudforet-io/api/dist/go/spaceone/api/cost_analysis/v1'
  _globals['_JOBTASK'].methods_by_name['get']._loaded_options = None
  _globals['_JOBTASK'].methods_by_name['get']._serialized_options = b'\202\323\344\223\002#\"\036/cost-analysis/v1/job-task/get:\001*'
  _globals['_JOBTASK'].methods_by_name['list']._loaded_options = None
  _globals['_JOBTASK'].methods_by_name['list']._serialized_options = b'\202\323\344\223\002$\"\037/cost-analysis/v1/job-task/list:\001*'
  _globals['_JOBTASK'].methods_by_name['stat']._loaded_options = None
  _globals['_JOBTASK'].methods_by_name['stat']._serialized_options = b'\202\323\344\223\002$\"\037/cost-analysis/v1/job-task/stat:\001*'
  _globals['_JOBTASKREQUEST']._serialized_start=173
  _globals['_JOBTASKREQUEST']._serialized_end=210
  _globals['_JOBTASKQUERY']._serialized_start=213
  _globals['_JOBTASKQUERY']._serialized_end=531
  _globals['_JOBTASKQUERY_STATUS']._serialized_start=424
  _globals['_JOBTASKQUERY_STATUS']._serialized_end=531
  _globals['_JOBTASKINFO']._serialized_start=534
  _globals['_JOBTASKINFO']._serialized_end=1165
  _globals['_JOBTASKINFO_STATUS']._serialized_start=424
  _globals['_JOBTASKINFO_STATUS']._serialized_end=531
  _globals['_JOBTASKINFO_RESOURCEGROUP']._serialized_start=1098
  _globals['_JOBTASKINFO_RESOURCEGROUP']._serialized_end=1165
  _globals['_JOBTASKSINFO']._serialized_start=1167
  _globals['_JOBTASKSINFO']._serialized_end=1263
  _globals['_JOBTASKSTATQUERY']._serialized_start=1265
  _globals['_JOBTASKSTATQUERY']._serialized_end=1337
  _globals['_JOBTASK']._serialized_start=1340
  _globals['_JOBTASK']._serialized_end=1760
# @@protoc_insertion_point(module_scope)
