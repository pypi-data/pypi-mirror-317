# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/inventory/v1/cloud_service_type.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n2spaceone/api/inventory/v1/cloud_service_type.proto\x12\x19spaceone.api.inventory.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v2/query.proto\"\x9f\x02\n\x1d\x43reateCloudServiceTypeRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08provider\x18\x02 \x01(\t\x12\r\n\x05group\x18\x03 \x01(\t\x12\x14\n\x0cservice_code\x18\x04 \x01(\t\x12\x12\n\nis_primary\x18\x05 \x01(\x08\x12\x10\n\x08is_major\x18\x06 \x01(\x08\x12\x15\n\rresource_type\x18\x07 \x01(\t\x12)\n\x08metadata\x18\x0b \x01(\x0b\x32\x17.google.protobuf.Struct\x12*\n\x06labels\x18\x0c \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12%\n\x04tags\x18\r \x01(\x0b\x32\x17.google.protobuf.Struct\"\x8f\x02\n\x1dUpdateCloudServiceTypeRequest\x12\x1d\n\x15\x63loud_service_type_id\x18\x01 \x01(\t\x12\x14\n\x0cservice_code\x18\x02 \x01(\t\x12\x12\n\nis_primary\x18\x03 \x01(\x08\x12\x10\n\x08is_major\x18\x04 \x01(\x08\x12\x15\n\rresource_type\x18\x05 \x01(\t\x12)\n\x08metadata\x18\x0b \x01(\x0b\x32\x17.google.protobuf.Struct\x12*\n\x06labels\x18\x0c \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12%\n\x04tags\x18\r \x01(\x0b\x32\x17.google.protobuf.Struct\"8\n\x17\x43loudServiceTypeRequest\x12\x1d\n\x15\x63loud_service_type_id\x18\x01 \x01(\t\"\x9a\x02\n\x15\x43loudServiceTypeQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v2.Query\x12\x1d\n\x15\x63loud_service_type_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x10\n\x08provider\x18\x04 \x01(\t\x12\r\n\x05group\x18\x05 \x01(\t\x12\x1e\n\x16\x63loud_service_type_key\x18\x06 \x01(\t\x12\x14\n\x0cservice_code\x18\x07 \x01(\t\x12\x12\n\nis_primary\x18\x08 \x01(\x08\x12\x10\n\x08is_major\x18\t \x01(\x08\x12\x15\n\rresource_type\x18\n \x01(\t\x12\x14\n\x0cworkspace_id\x18\x15 \x01(\t\"\xa6\x03\n\x14\x43loudServiceTypeInfo\x12\x1d\n\x15\x63loud_service_type_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08provider\x18\x03 \x01(\t\x12\r\n\x05group\x18\x04 \x01(\t\x12\x1e\n\x16\x63loud_service_type_key\x18\x05 \x01(\t\x12\x14\n\x0cservice_code\x18\x06 \x01(\t\x12\x12\n\nis_primary\x18\x07 \x01(\x08\x12\x10\n\x08is_major\x18\x08 \x01(\x08\x12\x15\n\rresource_type\x18\t \x01(\t\x12)\n\x08metadata\x18\x0b \x01(\x0b\x32\x17.google.protobuf.Struct\x12%\n\x04tags\x18\x0c \x01(\x0b\x32\x17.google.protobuf.Struct\x12*\n\x06labels\x18\r \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12\x11\n\tdomain_id\x18\x15 \x01(\t\x12\x14\n\x0cworkspace_id\x18\x16 \x01(\t\x12\x12\n\ncreated_at\x18\x1f \x01(\t\x12\x12\n\nupdated_at\x18  \x01(\t\"n\n\x15\x43loudServiceTypesInfo\x12@\n\x07results\x18\x01 \x03(\x0b\x32/.spaceone.api.inventory.v1.CloudServiceTypeInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"d\n\x19\x43loudServiceTypeStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v2.StatisticsQuery\x12\x11\n\tdomain_id\x18\x02 \x01(\t2\xb8\x07\n\x10\x43loudServiceType\x12\xa7\x01\n\x06\x63reate\x12\x38.spaceone.api.inventory.v1.CreateCloudServiceTypeRequest\x1a/.spaceone.api.inventory.v1.CloudServiceTypeInfo\"2\x82\xd3\xe4\x93\x02,\"\'/inventory/v1/cloud-service-type/create:\x01*\x12\xa7\x01\n\x06update\x12\x38.spaceone.api.inventory.v1.UpdateCloudServiceTypeRequest\x1a/.spaceone.api.inventory.v1.CloudServiceTypeInfo\"2\x82\xd3\xe4\x93\x02,\"\'/inventory/v1/cloud-service-type/update:\x01*\x12\x88\x01\n\x06\x64\x65lete\x12\x32.spaceone.api.inventory.v1.CloudServiceTypeRequest\x1a\x16.google.protobuf.Empty\"2\x82\xd3\xe4\x93\x02,\"\'/inventory/v1/cloud-service-type/delete:\x01*\x12\x9b\x01\n\x03get\x12\x32.spaceone.api.inventory.v1.CloudServiceTypeRequest\x1a/.spaceone.api.inventory.v1.CloudServiceTypeInfo\"/\x82\xd3\xe4\x93\x02)\"$/inventory/v1/cloud-service-type/get:\x01*\x12\x9c\x01\n\x04list\x12\x30.spaceone.api.inventory.v1.CloudServiceTypeQuery\x1a\x30.spaceone.api.inventory.v1.CloudServiceTypesInfo\"0\x82\xd3\xe4\x93\x02*\"%/inventory/v1/cloud-service-type/list:\x01*\x12\x87\x01\n\x04stat\x12\x34.spaceone.api.inventory.v1.CloudServiceTypeStatQuery\x1a\x17.google.protobuf.Struct\"0\x82\xd3\xe4\x93\x02*\"%/inventory/v1/cloud-service-type/stat:\x01*B@Z>github.com/cloudforet-io/api/dist/go/spaceone/api/inventory/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.inventory.v1.cloud_service_type_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z>github.com/cloudforet-io/api/dist/go/spaceone/api/inventory/v1'
  _globals['_CLOUDSERVICETYPE'].methods_by_name['create']._loaded_options = None
  _globals['_CLOUDSERVICETYPE'].methods_by_name['create']._serialized_options = b'\202\323\344\223\002,\"\'/inventory/v1/cloud-service-type/create:\001*'
  _globals['_CLOUDSERVICETYPE'].methods_by_name['update']._loaded_options = None
  _globals['_CLOUDSERVICETYPE'].methods_by_name['update']._serialized_options = b'\202\323\344\223\002,\"\'/inventory/v1/cloud-service-type/update:\001*'
  _globals['_CLOUDSERVICETYPE'].methods_by_name['delete']._loaded_options = None
  _globals['_CLOUDSERVICETYPE'].methods_by_name['delete']._serialized_options = b'\202\323\344\223\002,\"\'/inventory/v1/cloud-service-type/delete:\001*'
  _globals['_CLOUDSERVICETYPE'].methods_by_name['get']._loaded_options = None
  _globals['_CLOUDSERVICETYPE'].methods_by_name['get']._serialized_options = b'\202\323\344\223\002)\"$/inventory/v1/cloud-service-type/get:\001*'
  _globals['_CLOUDSERVICETYPE'].methods_by_name['list']._loaded_options = None
  _globals['_CLOUDSERVICETYPE'].methods_by_name['list']._serialized_options = b'\202\323\344\223\002*\"%/inventory/v1/cloud-service-type/list:\001*'
  _globals['_CLOUDSERVICETYPE'].methods_by_name['stat']._loaded_options = None
  _globals['_CLOUDSERVICETYPE'].methods_by_name['stat']._serialized_options = b'\202\323\344\223\002*\"%/inventory/v1/cloud-service-type/stat:\001*'
  _globals['_CREATECLOUDSERVICETYPEREQUEST']._serialized_start=205
  _globals['_CREATECLOUDSERVICETYPEREQUEST']._serialized_end=492
  _globals['_UPDATECLOUDSERVICETYPEREQUEST']._serialized_start=495
  _globals['_UPDATECLOUDSERVICETYPEREQUEST']._serialized_end=766
  _globals['_CLOUDSERVICETYPEREQUEST']._serialized_start=768
  _globals['_CLOUDSERVICETYPEREQUEST']._serialized_end=824
  _globals['_CLOUDSERVICETYPEQUERY']._serialized_start=827
  _globals['_CLOUDSERVICETYPEQUERY']._serialized_end=1109
  _globals['_CLOUDSERVICETYPEINFO']._serialized_start=1112
  _globals['_CLOUDSERVICETYPEINFO']._serialized_end=1534
  _globals['_CLOUDSERVICETYPESINFO']._serialized_start=1536
  _globals['_CLOUDSERVICETYPESINFO']._serialized_end=1646
  _globals['_CLOUDSERVICETYPESTATQUERY']._serialized_start=1648
  _globals['_CLOUDSERVICETYPESTATQUERY']._serialized_end=1748
  _globals['_CLOUDSERVICETYPE']._serialized_start=1751
  _globals['_CLOUDSERVICETYPE']._serialized_end=2703
# @@protoc_insertion_point(module_scope)
