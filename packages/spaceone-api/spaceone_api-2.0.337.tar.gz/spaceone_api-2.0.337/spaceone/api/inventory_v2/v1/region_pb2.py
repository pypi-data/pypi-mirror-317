# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/inventory_v2/v1/region.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)spaceone/api/inventory_v2/v1/region.proto\x12\x1cspaceone.api.inventory_v2.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v2/query.proto\"\xa5\x02\n\x13\x43reateRegionRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0bregion_code\x18\x02 \x01(\t\x12\x10\n\x08provider\x18\x03 \x01(\t\x12%\n\x04tags\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\x12W\n\x0eresource_group\x18\x14 \x01(\x0e\x32?.spaceone.api.inventory_v2.v1.CreateRegionRequest.ResourceGroup\x12\x14\n\x0cworkspace_id\x18\x15 \x01(\t\"C\n\rResourceGroup\x12\x17\n\x13RESOURCE_GROUP_NONE\x10\x00\x12\n\n\x06\x44OMAIN\x10\x01\x12\r\n\tWORKSPACE\x10\x02\"]\n\x13UpdateRegionRequest\x12\x11\n\tregion_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12%\n\x04tags\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\"\"\n\rRegionRequest\x12\x11\n\tregion_id\x18\x01 \x01(\t\"\xac\x01\n\x0bRegionQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v2.Query\x12\x11\n\tregion_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x13\n\x0bregion_code\x18\x04 \x01(\t\x12\x10\n\x08provider\x18\x05 \x01(\t\x12\x13\n\x0b\x65xists_only\x18\x06 \x01(\x08\x12\x14\n\x0cworkspace_id\x18\x15 \x01(\t\"\xe1\x02\n\nRegionInfo\x12\x11\n\tregion_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0bregion_code\x18\x03 \x01(\t\x12\x10\n\x08provider\x18\x04 \x01(\t\x12%\n\x04tags\x18\x05 \x01(\x0b\x32\x17.google.protobuf.Struct\x12N\n\x0eresource_group\x18\x14 \x01(\x0e\x32\x36.spaceone.api.inventory_v2.v1.RegionInfo.ResourceGroup\x12\x11\n\tdomain_id\x18\x15 \x01(\t\x12\x14\n\x0cworkspace_id\x18\x16 \x01(\t\x12\x12\n\ncreated_at\x18\x1f \x01(\t\x12\x12\n\nupdated_at\x18  \x01(\t\"C\n\rResourceGroup\x12\x17\n\x13RESOURCE_GROUP_NONE\x10\x00\x12\n\n\x06\x44OMAIN\x10\x01\x12\r\n\tWORKSPACE\x10\x02\"]\n\x0bRegionsInfo\x12\x39\n\x07results\x18\x01 \x03(\x0b\x32(.spaceone.api.inventory_v2.v1.RegionInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"G\n\x0fRegionStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v2.StatisticsQuery2\xb0\x06\n\x06Region\x12\x90\x01\n\x06\x63reate\x12\x31.spaceone.api.inventory_v2.v1.CreateRegionRequest\x1a(.spaceone.api.inventory_v2.v1.RegionInfo\")\x82\xd3\xe4\x93\x02#\"\x1e/inventory-v2/v1/region/create:\x01*\x12\x90\x01\n\x06update\x12\x31.spaceone.api.inventory_v2.v1.UpdateRegionRequest\x1a(.spaceone.api.inventory_v2.v1.RegionInfo\")\x82\xd3\xe4\x93\x02#\"\x1e/inventory-v2/v1/region/update:\x01*\x12x\n\x06\x64\x65lete\x12+.spaceone.api.inventory_v2.v1.RegionRequest\x1a\x16.google.protobuf.Empty\")\x82\xd3\xe4\x93\x02#\"\x1e/inventory-v2/v1/region/delete:\x01*\x12\x84\x01\n\x03get\x12+.spaceone.api.inventory_v2.v1.RegionRequest\x1a(.spaceone.api.inventory_v2.v1.RegionInfo\"&\x82\xd3\xe4\x93\x02 \"\x1b/inventory-v2/v1/region/get:\x01*\x12\x85\x01\n\x04list\x12).spaceone.api.inventory_v2.v1.RegionQuery\x1a).spaceone.api.inventory_v2.v1.RegionsInfo\"\'\x82\xd3\xe4\x93\x02!\"\x1c/inventory-v2/v1/region/list:\x01*\x12w\n\x04stat\x12-.spaceone.api.inventory_v2.v1.RegionStatQuery\x1a\x17.google.protobuf.Struct\"\'\x82\xd3\xe4\x93\x02!\"\x1c/inventory-v2/v1/region/stat:\x01*BCZAgithub.com/cloudforet-io/api/dist/go/spaceone/api/inventory-v2/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.inventory_v2.v1.region_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'ZAgithub.com/cloudforet-io/api/dist/go/spaceone/api/inventory-v2/v1'
  _globals['_REGION'].methods_by_name['create']._loaded_options = None
  _globals['_REGION'].methods_by_name['create']._serialized_options = b'\202\323\344\223\002#\"\036/inventory-v2/v1/region/create:\001*'
  _globals['_REGION'].methods_by_name['update']._loaded_options = None
  _globals['_REGION'].methods_by_name['update']._serialized_options = b'\202\323\344\223\002#\"\036/inventory-v2/v1/region/update:\001*'
  _globals['_REGION'].methods_by_name['delete']._loaded_options = None
  _globals['_REGION'].methods_by_name['delete']._serialized_options = b'\202\323\344\223\002#\"\036/inventory-v2/v1/region/delete:\001*'
  _globals['_REGION'].methods_by_name['get']._loaded_options = None
  _globals['_REGION'].methods_by_name['get']._serialized_options = b'\202\323\344\223\002 \"\033/inventory-v2/v1/region/get:\001*'
  _globals['_REGION'].methods_by_name['list']._loaded_options = None
  _globals['_REGION'].methods_by_name['list']._serialized_options = b'\202\323\344\223\002!\"\034/inventory-v2/v1/region/list:\001*'
  _globals['_REGION'].methods_by_name['stat']._loaded_options = None
  _globals['_REGION'].methods_by_name['stat']._serialized_options = b'\202\323\344\223\002!\"\034/inventory-v2/v1/region/stat:\001*'
  _globals['_CREATEREGIONREQUEST']._serialized_start=199
  _globals['_CREATEREGIONREQUEST']._serialized_end=492
  _globals['_CREATEREGIONREQUEST_RESOURCEGROUP']._serialized_start=425
  _globals['_CREATEREGIONREQUEST_RESOURCEGROUP']._serialized_end=492
  _globals['_UPDATEREGIONREQUEST']._serialized_start=494
  _globals['_UPDATEREGIONREQUEST']._serialized_end=587
  _globals['_REGIONREQUEST']._serialized_start=589
  _globals['_REGIONREQUEST']._serialized_end=623
  _globals['_REGIONQUERY']._serialized_start=626
  _globals['_REGIONQUERY']._serialized_end=798
  _globals['_REGIONINFO']._serialized_start=801
  _globals['_REGIONINFO']._serialized_end=1154
  _globals['_REGIONINFO_RESOURCEGROUP']._serialized_start=425
  _globals['_REGIONINFO_RESOURCEGROUP']._serialized_end=492
  _globals['_REGIONSINFO']._serialized_start=1156
  _globals['_REGIONSINFO']._serialized_end=1249
  _globals['_REGIONSTATQUERY']._serialized_start=1251
  _globals['_REGIONSTATQUERY']._serialized_end=1322
  _globals['_REGION']._serialized_start=1325
  _globals['_REGION']._serialized_end=2141
# @@protoc_insertion_point(module_scope)
