# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/dashboard/v1/private_data_table.proto
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
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from spaceone.api.core.v2 import query_pb2 as spaceone_dot_api_dot_core_dot_v2_dot_query__pb2
from spaceone.api.dashboard.v1 import public_data_table_pb2 as spaceone_dot_api_dot_dashboard_dot_v1_dot_public__data__table__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n2spaceone/api/dashboard/v1/private_data_table.proto\x12\x19spaceone.api.dashboard.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v2/query.proto\x1a\x31spaceone/api/dashboard/v1/public_data_table.proto\"\xff\x01\n\x1a\x41\x64\x64PrivateDataTableRequest\x12\x11\n\twidget_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12:\n\x0bsource_type\x18\x03 \x01(\x0e\x32%.spaceone.api.dashboard.v1.SourceType\x12\x36\n\x07options\x18\x04 \x01(\x0b\x32%.spaceone.api.dashboard.v1.AddOptions\x12%\n\x04vars\x18\x05 \x01(\x0b\x32\x17.google.protobuf.Struct\x12%\n\x04tags\x18\x06 \x01(\x0b\x32\x17.google.protobuf.Struct\"\x86\x02\n TransformPrivateDataTableRequest\x12\x11\n\twidget_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x35\n\x08operator\x18\x03 \x01(\x0e\x32#.spaceone.api.dashboard.v1.Operator\x12<\n\x07options\x18\x04 \x01(\x0b\x32+.spaceone.api.dashboard.v1.TransformOptions\x12%\n\x04vars\x18\x05 \x01(\x0b\x32\x17.google.protobuf.Struct\x12%\n\x04tags\x18\x06 \x01(\x0b\x32\x17.google.protobuf.Struct\"\xbc\x01\n\x1dUpdatePrivateDataTableRequest\x12\x15\n\rdata_table_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12(\n\x07options\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12%\n\x04vars\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\x12%\n\x04tags\x18\x05 \x01(\x0b\x32\x17.google.protobuf.Struct\"0\n\x17PrivateDataTableRequest\x12\x15\n\rdata_table_id\x18\x01 \x01(\t\"\xed\x02\n\x1bLoadPrivateDataTableRequest\x12\x15\n\rdata_table_id\x18\x01 \x01(\t\x12W\n\x0bgranularity\x18\x02 \x01(\x0e\x32\x42.spaceone.api.dashboard.v1.LoadPrivateDataTableRequest.Granularity\x12\r\n\x05start\x18\x03 \x01(\t\x12\x0b\n\x03\x65nd\x18\x04 \x01(\t\x12(\n\x04sort\x18\x05 \x03(\x0b\x32\x1a.spaceone.api.core.v2.Sort\x12(\n\x04page\x18\x06 \x01(\x0b\x32\x1a.spaceone.api.core.v2.Page\x12%\n\x04vars\x18\x07 \x01(\x0b\x32\x17.google.protobuf.Struct\"G\n\x0bGranularity\x12\x14\n\x10GRANULARITY_NONE\x10\x00\x12\t\n\x05\x44\x41ILY\x10\x01\x12\x0b\n\x07MONTHLY\x10\x02\x12\n\n\x06YEARLY\x10\x03\"\xa6\x02\n\x15PrivateDataTableQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v2.Query\x12\x11\n\twidget_id\x18\x02 \x01(\t\x12\x15\n\rdata_table_id\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x36\n\tdata_type\x18\x05 \x01(\x0e\x32#.spaceone.api.dashboard.v1.DataType\x12:\n\x0bsource_type\x18\x06 \x01(\x0e\x32%.spaceone.api.dashboard.v1.SourceType\x12\x35\n\x08operator\x18\x07 \x01(\x0e\x32#.spaceone.api.dashboard.v1.Operator\"\x94\x06\n\x14PrivateDataTableInfo\x12\x15\n\rdata_table_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x44\n\x05state\x18\x03 \x01(\x0e\x32\x35.spaceone.api.dashboard.v1.PrivateDataTableInfo.State\x12\x36\n\tdata_type\x18\x04 \x01(\x0e\x32#.spaceone.api.dashboard.v1.DataType\x12:\n\x0bsource_type\x18\x05 \x01(\x0e\x32%.spaceone.api.dashboard.v1.SourceType\x12\x35\n\x08operator\x18\x06 \x01(\x0e\x32#.spaceone.api.dashboard.v1.Operator\x12(\n\x07options\x18\x07 \x01(\x0b\x32\x17.google.protobuf.Struct\x12%\n\x04tags\x18\x08 \x01(\x0b\x32\x17.google.protobuf.Struct\x12,\n\x0blabels_info\x18\t \x01(\x0b\x32\x17.google.protobuf.Struct\x12*\n\tdata_info\x18\n \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tsort_keys\x18\x0b \x03(\t\x12\x11\n\tcache_key\x18\x0c \x01(\t\x12\x15\n\rerror_message\x18\r \x01(\t\x12\x11\n\tdomain_id\x18\x15 \x01(\t\x12\x0f\n\x07user_id\x18\x16 \x01(\t\x12\x14\n\x0c\x64\x61shboard_id\x18\x17 \x01(\t\x12\x11\n\twidget_id\x18\x18 \x01(\t\x12\x12\n\ncreated_at\x18\x1f \x01(\t\x12\x12\n\nupdated_at\x18  \x01(\t\"P\n\rResourceGroup\x12\x17\n\x13RESOURCE_GROUP_NONE\x10\x00\x12\n\n\x06\x44OMAIN\x10\x01\x12\r\n\tWORKSPACE\x10\x02\x12\x0b\n\x07PROJECT\x10\x03\"7\n\x05State\x12\x0e\n\nSTATE_NONE\x10\x00\x12\r\n\tAVAILABLE\x10\x01\x12\x0f\n\x0bUNAVAILABLE\x10\x02\"n\n\x15PrivateDataTablesInfo\x12@\n\x07results\x18\x01 \x03(\x0b\x32/.spaceone.api.dashboard.v1.PrivateDataTableInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\x32\xe4\x08\n\x10PrivateDataTable\x12\x9e\x01\n\x03\x61\x64\x64\x12\x35.spaceone.api.dashboard.v1.AddPrivateDataTableRequest\x1a/.spaceone.api.dashboard.v1.PrivateDataTableInfo\"/\x82\xd3\xe4\x93\x02)\"$/dashboard/v1/private-data-table/add:\x01*\x12\xb0\x01\n\ttransform\x12;.spaceone.api.dashboard.v1.TransformPrivateDataTableRequest\x1a/.spaceone.api.dashboard.v1.PrivateDataTableInfo\"5\x82\xd3\xe4\x93\x02/\"*/dashboard/v1/private-data-table/transform:\x01*\x12\xa7\x01\n\x06update\x12\x38.spaceone.api.dashboard.v1.UpdatePrivateDataTableRequest\x1a/.spaceone.api.dashboard.v1.PrivateDataTableInfo\"2\x82\xd3\xe4\x93\x02,\"\'/dashboard/v1/private-data-table/update:\x01*\x12\x88\x01\n\x06\x64\x65lete\x12\x32.spaceone.api.dashboard.v1.PrivateDataTableRequest\x1a\x16.google.protobuf.Empty\"2\x82\xd3\xe4\x93\x02,\"\'/dashboard/v1/private-data-table/delete:\x01*\x12\x89\x01\n\x04load\x12\x36.spaceone.api.dashboard.v1.LoadPrivateDataTableRequest\x1a\x17.google.protobuf.Struct\"0\x82\xd3\xe4\x93\x02*\"%/dashboard/v1/private-data-table/load:\x01*\x12\x9b\x01\n\x03get\x12\x32.spaceone.api.dashboard.v1.PrivateDataTableRequest\x1a/.spaceone.api.dashboard.v1.PrivateDataTableInfo\"/\x82\xd3\xe4\x93\x02)\"$/dashboard/v1/private-data-table/get:\x01*\x12\x9c\x01\n\x04list\x12\x30.spaceone.api.dashboard.v1.PrivateDataTableQuery\x1a\x30.spaceone.api.dashboard.v1.PrivateDataTablesInfo\"0\x82\xd3\xe4\x93\x02*\"%/dashboard/v1/private-data-table/list:\x01*B@Z>github.com/cloudforet-io/api/dist/go/spaceone/api/dashboard/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.dashboard.v1.private_data_table_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z>github.com/cloudforet-io/api/dist/go/spaceone/api/dashboard/v1'
  _globals['_PRIVATEDATATABLE'].methods_by_name['add']._loaded_options = None
  _globals['_PRIVATEDATATABLE'].methods_by_name['add']._serialized_options = b'\202\323\344\223\002)\"$/dashboard/v1/private-data-table/add:\001*'
  _globals['_PRIVATEDATATABLE'].methods_by_name['transform']._loaded_options = None
  _globals['_PRIVATEDATATABLE'].methods_by_name['transform']._serialized_options = b'\202\323\344\223\002/\"*/dashboard/v1/private-data-table/transform:\001*'
  _globals['_PRIVATEDATATABLE'].methods_by_name['update']._loaded_options = None
  _globals['_PRIVATEDATATABLE'].methods_by_name['update']._serialized_options = b'\202\323\344\223\002,\"\'/dashboard/v1/private-data-table/update:\001*'
  _globals['_PRIVATEDATATABLE'].methods_by_name['delete']._loaded_options = None
  _globals['_PRIVATEDATATABLE'].methods_by_name['delete']._serialized_options = b'\202\323\344\223\002,\"\'/dashboard/v1/private-data-table/delete:\001*'
  _globals['_PRIVATEDATATABLE'].methods_by_name['load']._loaded_options = None
  _globals['_PRIVATEDATATABLE'].methods_by_name['load']._serialized_options = b'\202\323\344\223\002*\"%/dashboard/v1/private-data-table/load:\001*'
  _globals['_PRIVATEDATATABLE'].methods_by_name['get']._loaded_options = None
  _globals['_PRIVATEDATATABLE'].methods_by_name['get']._serialized_options = b'\202\323\344\223\002)\"$/dashboard/v1/private-data-table/get:\001*'
  _globals['_PRIVATEDATATABLE'].methods_by_name['list']._loaded_options = None
  _globals['_PRIVATEDATATABLE'].methods_by_name['list']._serialized_options = b'\202\323\344\223\002*\"%/dashboard/v1/private-data-table/list:\001*'
  _globals['_ADDPRIVATEDATATABLEREQUEST']._serialized_start=256
  _globals['_ADDPRIVATEDATATABLEREQUEST']._serialized_end=511
  _globals['_TRANSFORMPRIVATEDATATABLEREQUEST']._serialized_start=514
  _globals['_TRANSFORMPRIVATEDATATABLEREQUEST']._serialized_end=776
  _globals['_UPDATEPRIVATEDATATABLEREQUEST']._serialized_start=779
  _globals['_UPDATEPRIVATEDATATABLEREQUEST']._serialized_end=967
  _globals['_PRIVATEDATATABLEREQUEST']._serialized_start=969
  _globals['_PRIVATEDATATABLEREQUEST']._serialized_end=1017
  _globals['_LOADPRIVATEDATATABLEREQUEST']._serialized_start=1020
  _globals['_LOADPRIVATEDATATABLEREQUEST']._serialized_end=1385
  _globals['_LOADPRIVATEDATATABLEREQUEST_GRANULARITY']._serialized_start=1314
  _globals['_LOADPRIVATEDATATABLEREQUEST_GRANULARITY']._serialized_end=1385
  _globals['_PRIVATEDATATABLEQUERY']._serialized_start=1388
  _globals['_PRIVATEDATATABLEQUERY']._serialized_end=1682
  _globals['_PRIVATEDATATABLEINFO']._serialized_start=1685
  _globals['_PRIVATEDATATABLEINFO']._serialized_end=2473
  _globals['_PRIVATEDATATABLEINFO_RESOURCEGROUP']._serialized_start=2336
  _globals['_PRIVATEDATATABLEINFO_RESOURCEGROUP']._serialized_end=2416
  _globals['_PRIVATEDATATABLEINFO_STATE']._serialized_start=2418
  _globals['_PRIVATEDATATABLEINFO_STATE']._serialized_end=2473
  _globals['_PRIVATEDATATABLESINFO']._serialized_start=2475
  _globals['_PRIVATEDATATABLESINFO']._serialized_end=2585
  _globals['_PRIVATEDATATABLE']._serialized_start=2588
  _globals['_PRIVATEDATATABLE']._serialized_end=3712
# @@protoc_insertion_point(module_scope)
