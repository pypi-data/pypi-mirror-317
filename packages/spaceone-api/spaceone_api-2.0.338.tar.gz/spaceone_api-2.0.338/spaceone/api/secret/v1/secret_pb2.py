# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/secret/v1/secret.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#spaceone/api/secret/v1/secret.proto\x12\x16spaceone.api.secret.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v2/query.proto\"\x8a\x03\n\x13\x43reateSecretRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12%\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tschema_id\x18\x03 \x01(\t\x12%\n\x04tags\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\x12Q\n\x0eresource_group\x18\x14 \x01(\x0e\x32\x39.spaceone.api.secret.v1.CreateSecretRequest.ResourceGroup\x12\x14\n\x0cworkspace_id\x18\x15 \x01(\t\x12\x12\n\nproject_id\x18\x16 \x01(\t\x12\x1a\n\x12service_account_id\x18\x17 \x01(\t\x12\x19\n\x11trusted_secret_id\x18\x18 \x01(\t\"P\n\rResourceGroup\x12\x17\n\x13RESOURCE_GROUP_NONE\x10\x00\x12\n\n\x06\x44OMAIN\x10\x01\x12\r\n\tWORKSPACE\x10\x02\x12\x0b\n\x07PROJECT\x10\x03\"q\n\x13UpdateSecretRequest\x12\x11\n\tsecret_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12%\n\x04tags\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x12\n\nproject_id\x18\x15 \x01(\t\"\"\n\rSecretRequest\x12\x11\n\tsecret_id\x18\x01 \x01(\t\"<\n\x14GetSecretDataRequest\x12\x11\n\tsecret_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x15 \x01(\t\"f\n\x17UpdateSecretDataRequest\x12\x11\n\tsecret_id\x18\x01 \x01(\t\x12\x11\n\tschema_id\x18\x02 \x01(\t\x12%\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\"\xce\x02\n\x0bSecretQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v2.Query\x12\x11\n\tsecret_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x38\n\x05state\x18\x04 \x01(\x0e\x32).spaceone.api.secret.v1.SecretQuery.State\x12\x11\n\tschema_id\x18\x05 \x01(\t\x12\x10\n\x08provider\x18\x06 \x01(\t\x12\x14\n\x0cworkspace_id\x18\x16 \x01(\t\x12\x12\n\nproject_id\x18\x15 \x01(\t\x12\x1a\n\x12service_account_id\x18\x17 \x01(\t\x12\x19\n\x11trusted_secret_id\x18\x18 \x01(\t\"2\n\x05State\x12\x0e\n\nSTATE_NONE\x10\x00\x12\x0b\n\x07\x45NABLED\x10\x01\x12\x0c\n\x08\x44ISABLED\x10\x02\"|\n\x0eSecretDataInfo\x12\x11\n\tencrypted\x18\x01 \x01(\x08\x12\x30\n\x0f\x65ncrypt_options\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12%\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\"\x8a\x04\n\nSecretInfo\x12\x11\n\tsecret_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x37\n\x05state\x18\x03 \x01(\x0e\x32(.spaceone.api.secret.v1.SecretInfo.State\x12\x11\n\tschema_id\x18\x04 \x01(\t\x12\x10\n\x08provider\x18\x05 \x01(\t\x12%\n\x04tags\x18\x06 \x01(\x0b\x32\x17.google.protobuf.Struct\x12H\n\x0eresource_group\x18\x14 \x01(\x0e\x32\x30.spaceone.api.secret.v1.SecretInfo.ResourceGroup\x12\x11\n\tdomain_id\x18\x15 \x01(\t\x12\x14\n\x0cworkspace_id\x18\x16 \x01(\t\x12\x12\n\nproject_id\x18\x17 \x01(\t\x12\x1a\n\x12service_account_id\x18\x18 \x01(\t\x12\x19\n\x11trusted_secret_id\x18\x19 \x01(\t\x12\x12\n\ncreated_at\x18\x1f \x01(\t\"2\n\x05State\x12\x0e\n\nSTATE_NONE\x10\x00\x12\x0b\n\x07\x45NABLED\x10\x01\x12\x0c\n\x08\x44ISABLED\x10\x02\"P\n\rResourceGroup\x12\x17\n\x13RESOURCE_GROUP_NONE\x10\x00\x12\n\n\x06\x44OMAIN\x10\x01\x12\r\n\tWORKSPACE\x10\x02\x12\x0b\n\x07PROJECT\x10\x03\"W\n\x0bSecretsInfo\x12\x33\n\x07results\x18\x01 \x03(\x0b\x32\".spaceone.api.secret.v1.SecretInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"Z\n\x0fSecretStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v2.StatisticsQuery\x12\x11\n\tdomain_id\x18\x02 \x01(\t2\xa9\t\n\x06Secret\x12~\n\x06\x63reate\x12+.spaceone.api.secret.v1.CreateSecretRequest\x1a\".spaceone.api.secret.v1.SecretInfo\"#\x82\xd3\xe4\x93\x02\x1d\"\x18/secret/v1/secret/create:\x01*\x12~\n\x06update\x12+.spaceone.api.secret.v1.UpdateSecretRequest\x1a\".spaceone.api.secret.v1.SecretInfo\"#\x82\xd3\xe4\x93\x02\x1d\"\x18/secret/v1/secret/update:\x01*\x12l\n\x06\x64\x65lete\x12%.spaceone.api.secret.v1.SecretRequest\x1a\x16.google.protobuf.Empty\"#\x82\xd3\xe4\x93\x02\x1d\"\x18/secret/v1/secret/delete:\x01*\x12x\n\x06\x65nable\x12%.spaceone.api.secret.v1.SecretRequest\x1a\".spaceone.api.secret.v1.SecretInfo\"#\x82\xd3\xe4\x93\x02\x1d\"\x18/secret/v1/secret/enable:\x01*\x12z\n\x07\x64isable\x12%.spaceone.api.secret.v1.SecretRequest\x1a\".spaceone.api.secret.v1.SecretInfo\"$\x82\xd3\xe4\x93\x02\x1e\"\x19/secret/v1/secret/disable:\x01*\x12\x80\x01\n\x0bupdate_data\x12/.spaceone.api.secret.v1.UpdateSecretDataRequest\x1a\x16.google.protobuf.Empty\"(\x82\xd3\xe4\x93\x02\"\"\x1d/secret/v1/secret/update-data:\x01*\x12\x62\n\x08get_data\x12,.spaceone.api.secret.v1.GetSecretDataRequest\x1a&.spaceone.api.secret.v1.SecretDataInfo\"\x00\x12r\n\x03get\x12%.spaceone.api.secret.v1.SecretRequest\x1a\".spaceone.api.secret.v1.SecretInfo\" \x82\xd3\xe4\x93\x02\x1a\"\x15/secret/v1/secret/get:\x01*\x12s\n\x04list\x12#.spaceone.api.secret.v1.SecretQuery\x1a#.spaceone.api.secret.v1.SecretsInfo\"!\x82\xd3\xe4\x93\x02\x1b\"\x16/secret/v1/secret/list:\x01*\x12k\n\x04stat\x12\'.spaceone.api.secret.v1.SecretStatQuery\x1a\x17.google.protobuf.Struct\"!\x82\xd3\xe4\x93\x02\x1b\"\x16/secret/v1/secret/stat:\x01*B=Z;github.com/cloudforet-io/api/dist/go/spaceone/api/secret/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.secret.v1.secret_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z;github.com/cloudforet-io/api/dist/go/spaceone/api/secret/v1'
  _globals['_SECRET'].methods_by_name['create']._loaded_options = None
  _globals['_SECRET'].methods_by_name['create']._serialized_options = b'\202\323\344\223\002\035\"\030/secret/v1/secret/create:\001*'
  _globals['_SECRET'].methods_by_name['update']._loaded_options = None
  _globals['_SECRET'].methods_by_name['update']._serialized_options = b'\202\323\344\223\002\035\"\030/secret/v1/secret/update:\001*'
  _globals['_SECRET'].methods_by_name['delete']._loaded_options = None
  _globals['_SECRET'].methods_by_name['delete']._serialized_options = b'\202\323\344\223\002\035\"\030/secret/v1/secret/delete:\001*'
  _globals['_SECRET'].methods_by_name['enable']._loaded_options = None
  _globals['_SECRET'].methods_by_name['enable']._serialized_options = b'\202\323\344\223\002\035\"\030/secret/v1/secret/enable:\001*'
  _globals['_SECRET'].methods_by_name['disable']._loaded_options = None
  _globals['_SECRET'].methods_by_name['disable']._serialized_options = b'\202\323\344\223\002\036\"\031/secret/v1/secret/disable:\001*'
  _globals['_SECRET'].methods_by_name['update_data']._loaded_options = None
  _globals['_SECRET'].methods_by_name['update_data']._serialized_options = b'\202\323\344\223\002\"\"\035/secret/v1/secret/update-data:\001*'
  _globals['_SECRET'].methods_by_name['get']._loaded_options = None
  _globals['_SECRET'].methods_by_name['get']._serialized_options = b'\202\323\344\223\002\032\"\025/secret/v1/secret/get:\001*'
  _globals['_SECRET'].methods_by_name['list']._loaded_options = None
  _globals['_SECRET'].methods_by_name['list']._serialized_options = b'\202\323\344\223\002\033\"\026/secret/v1/secret/list:\001*'
  _globals['_SECRET'].methods_by_name['stat']._loaded_options = None
  _globals['_SECRET'].methods_by_name['stat']._serialized_options = b'\202\323\344\223\002\033\"\026/secret/v1/secret/stat:\001*'
  _globals['_CREATESECRETREQUEST']._serialized_start=187
  _globals['_CREATESECRETREQUEST']._serialized_end=581
  _globals['_CREATESECRETREQUEST_RESOURCEGROUP']._serialized_start=501
  _globals['_CREATESECRETREQUEST_RESOURCEGROUP']._serialized_end=581
  _globals['_UPDATESECRETREQUEST']._serialized_start=583
  _globals['_UPDATESECRETREQUEST']._serialized_end=696
  _globals['_SECRETREQUEST']._serialized_start=698
  _globals['_SECRETREQUEST']._serialized_end=732
  _globals['_GETSECRETDATAREQUEST']._serialized_start=734
  _globals['_GETSECRETDATAREQUEST']._serialized_end=794
  _globals['_UPDATESECRETDATAREQUEST']._serialized_start=796
  _globals['_UPDATESECRETDATAREQUEST']._serialized_end=898
  _globals['_SECRETQUERY']._serialized_start=901
  _globals['_SECRETQUERY']._serialized_end=1235
  _globals['_SECRETQUERY_STATE']._serialized_start=1185
  _globals['_SECRETQUERY_STATE']._serialized_end=1235
  _globals['_SECRETDATAINFO']._serialized_start=1237
  _globals['_SECRETDATAINFO']._serialized_end=1361
  _globals['_SECRETINFO']._serialized_start=1364
  _globals['_SECRETINFO']._serialized_end=1886
  _globals['_SECRETINFO_STATE']._serialized_start=1185
  _globals['_SECRETINFO_STATE']._serialized_end=1235
  _globals['_SECRETINFO_RESOURCEGROUP']._serialized_start=501
  _globals['_SECRETINFO_RESOURCEGROUP']._serialized_end=581
  _globals['_SECRETSINFO']._serialized_start=1888
  _globals['_SECRETSINFO']._serialized_end=1975
  _globals['_SECRETSTATQUERY']._serialized_start=1977
  _globals['_SECRETSTATQUERY']._serialized_end=2067
  _globals['_SECRET']._serialized_start=2070
  _globals['_SECRET']._serialized_end=3263
# @@protoc_insertion_point(module_scope)
