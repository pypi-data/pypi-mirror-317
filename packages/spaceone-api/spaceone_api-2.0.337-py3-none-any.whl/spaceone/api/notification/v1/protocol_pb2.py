# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/notification/v1/protocol.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+spaceone/api/notification/v1/protocol.proto\x12\x1cspaceone.api.notification.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v2/query.proto\"\x99\x02\n\rPluginRequest\x12\x11\n\tplugin_id\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12(\n\x07options\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12,\n\x0bsecret_data\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x0e\n\x06schema\x18\x05 \x01(\t\x12M\n\x0cupgrade_mode\x18\x06 \x01(\x0e\x32\x37.spaceone.api.notification.v1.PluginRequest.UpgradeMode\"-\n\x0bUpgradeMode\x12\x08\n\x04NONE\x10\x00\x12\x08\n\x04\x41UTO\x10\x01\x12\n\n\x06MANUAL\x10\x02\"\x93\x02\n\nPluginInfo\x12\x11\n\tplugin_id\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12(\n\x07options\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tsecret_id\x18\x04 \x01(\t\x12)\n\x08metadata\x18\x06 \x01(\x0b\x32\x17.google.protobuf.Struct\x12J\n\x0cupgrade_mode\x18\x07 \x01(\x0e\x32\x34.spaceone.api.notification.v1.PluginInfo.UpgradeMode\"-\n\x0bUpgradeMode\x12\x08\n\x04NONE\x10\x00\x12\x08\n\x04\x41UTO\x10\x01\x12\n\n\x06MANUAL\x10\x02\"\x8e\x01\n\x15\x43reateProtocolRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12@\n\x0bplugin_info\x18\x02 \x01(\x0b\x32+.spaceone.api.notification.v1.PluginRequest\x12%\n\x04tags\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\"a\n\x15UpdateProtocolRequest\x12\x13\n\x0bprotocol_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12%\n\x04tags\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\"\x80\x01\n\x1bUpdateProtocolPluginRequest\x12\x13\n\x0bprotocol_id\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12(\n\x07options\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x0b \x01(\t\"&\n\x0fProtocolRequest\x12\x13\n\x0bprotocol_id\x18\x01 \x01(\t\"\xf3\x02\n\rProtocolQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v2.Query\x12\x13\n\x0bprotocol_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12H\n\x05state\x18\x04 \x01(\x0e\x32\x39.spaceone.api.notification.v1.ProtocolQuery.ProtocolState\x12O\n\rprotocol_type\x18\x05 \x01(\x0e\x32\x38.spaceone.api.notification.v1.ProtocolQuery.ProtocolType\"4\n\rProtocolState\x12\x08\n\x04NONE\x10\x00\x12\x0b\n\x07\x45NABLED\x10\x01\x12\x0c\n\x08\x44ISABLED\x10\x02\"B\n\x0cProtocolType\x12\x16\n\x12PROTOCOL_TYPE_NONE\x10\x00\x12\x0c\n\x08INTERNAL\x10\x01\x12\x0c\n\x08\x45XTERNAL\x10\x02\"\x95\x04\n\x0cProtocolInfo\x12\x13\n\x0bprotocol_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12G\n\x05state\x18\x03 \x01(\x0e\x32\x38.spaceone.api.notification.v1.ProtocolInfo.ProtocolState\x12N\n\rprotocol_type\x18\x04 \x01(\x0e\x32\x37.spaceone.api.notification.v1.ProtocolInfo.ProtocolType\x12\x15\n\rresource_type\x18\x05 \x01(\t\x12+\n\ncapability\x18\x06 \x01(\x0b\x32\x17.google.protobuf.Struct\x12=\n\x0bplugin_info\x18\x07 \x01(\x0b\x32(.spaceone.api.notification.v1.PluginInfo\x12%\n\x04tags\x18\x08 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x15 \x01(\t\x12\x12\n\ncreated_at\x18\x1f \x01(\t\"4\n\rProtocolState\x12\x08\n\x04NONE\x10\x00\x12\x0b\n\x07\x45NABLED\x10\x01\x12\x0c\n\x08\x44ISABLED\x10\x02\"B\n\x0cProtocolType\x12\x16\n\x12PROTOCOL_TYPE_NONE\x10\x00\x12\x0c\n\x08INTERNAL\x10\x01\x12\x0c\n\x08\x45XTERNAL\x10\x02\"a\n\rProtocolsInfo\x12;\n\x07results\x18\x01 \x03(\x0b\x32*.spaceone.api.notification.v1.ProtocolInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"I\n\x11ProtocolStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v2.StatisticsQuery2\xa7\n\n\x08Protocol\x12\x96\x01\n\x06\x63reate\x12\x33.spaceone.api.notification.v1.CreateProtocolRequest\x1a*.spaceone.api.notification.v1.ProtocolInfo\"+\x82\xd3\xe4\x93\x02%\" /notification/v1/protocol/create:\x01*\x12\x96\x01\n\x06update\x12\x33.spaceone.api.notification.v1.UpdateProtocolRequest\x1a*.spaceone.api.notification.v1.ProtocolInfo\"+\x82\xd3\xe4\x93\x02%\" /notification/v1/protocol/update:\x01*\x12\xaa\x01\n\rupdate_plugin\x12\x39.spaceone.api.notification.v1.UpdateProtocolPluginRequest\x1a*.spaceone.api.notification.v1.ProtocolInfo\"2\x82\xd3\xe4\x93\x02,\"\'/notification/v1/protocol/update-plugin:\x01*\x12\x90\x01\n\x06\x65nable\x12-.spaceone.api.notification.v1.ProtocolRequest\x1a*.spaceone.api.notification.v1.ProtocolInfo\"+\x82\xd3\xe4\x93\x02%\" /notification/v1/protocol/enable:\x01*\x12\x92\x01\n\x07\x64isable\x12-.spaceone.api.notification.v1.ProtocolRequest\x1a*.spaceone.api.notification.v1.ProtocolInfo\",\x82\xd3\xe4\x93\x02&\"!/notification/v1/protocol/disable:\x01*\x12|\n\x06\x64\x65lete\x12-.spaceone.api.notification.v1.ProtocolRequest\x1a\x16.google.protobuf.Empty\"+\x82\xd3\xe4\x93\x02%\" /notification/v1/protocol/delete:\x01*\x12\x8a\x01\n\x03get\x12-.spaceone.api.notification.v1.ProtocolRequest\x1a*.spaceone.api.notification.v1.ProtocolInfo\"(\x82\xd3\xe4\x93\x02\"\"\x1d/notification/v1/protocol/get:\x01*\x12\x8b\x01\n\x04list\x12+.spaceone.api.notification.v1.ProtocolQuery\x1a+.spaceone.api.notification.v1.ProtocolsInfo\")\x82\xd3\xe4\x93\x02#\"\x1e/notification/v1/protocol/list:\x01*\x12{\n\x04stat\x12/.spaceone.api.notification.v1.ProtocolStatQuery\x1a\x17.google.protobuf.Struct\")\x82\xd3\xe4\x93\x02#\"\x1e/notification/v1/protocol/stat:\x01*BCZAgithub.com/cloudforet-io/api/dist/go/spaceone/api/notification/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.notification.v1.protocol_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'ZAgithub.com/cloudforet-io/api/dist/go/spaceone/api/notification/v1'
  _globals['_PROTOCOL'].methods_by_name['create']._loaded_options = None
  _globals['_PROTOCOL'].methods_by_name['create']._serialized_options = b'\202\323\344\223\002%\" /notification/v1/protocol/create:\001*'
  _globals['_PROTOCOL'].methods_by_name['update']._loaded_options = None
  _globals['_PROTOCOL'].methods_by_name['update']._serialized_options = b'\202\323\344\223\002%\" /notification/v1/protocol/update:\001*'
  _globals['_PROTOCOL'].methods_by_name['update_plugin']._loaded_options = None
  _globals['_PROTOCOL'].methods_by_name['update_plugin']._serialized_options = b'\202\323\344\223\002,\"\'/notification/v1/protocol/update-plugin:\001*'
  _globals['_PROTOCOL'].methods_by_name['enable']._loaded_options = None
  _globals['_PROTOCOL'].methods_by_name['enable']._serialized_options = b'\202\323\344\223\002%\" /notification/v1/protocol/enable:\001*'
  _globals['_PROTOCOL'].methods_by_name['disable']._loaded_options = None
  _globals['_PROTOCOL'].methods_by_name['disable']._serialized_options = b'\202\323\344\223\002&\"!/notification/v1/protocol/disable:\001*'
  _globals['_PROTOCOL'].methods_by_name['delete']._loaded_options = None
  _globals['_PROTOCOL'].methods_by_name['delete']._serialized_options = b'\202\323\344\223\002%\" /notification/v1/protocol/delete:\001*'
  _globals['_PROTOCOL'].methods_by_name['get']._loaded_options = None
  _globals['_PROTOCOL'].methods_by_name['get']._serialized_options = b'\202\323\344\223\002\"\"\035/notification/v1/protocol/get:\001*'
  _globals['_PROTOCOL'].methods_by_name['list']._loaded_options = None
  _globals['_PROTOCOL'].methods_by_name['list']._serialized_options = b'\202\323\344\223\002#\"\036/notification/v1/protocol/list:\001*'
  _globals['_PROTOCOL'].methods_by_name['stat']._loaded_options = None
  _globals['_PROTOCOL'].methods_by_name['stat']._serialized_options = b'\202\323\344\223\002#\"\036/notification/v1/protocol/stat:\001*'
  _globals['_PLUGINREQUEST']._serialized_start=201
  _globals['_PLUGINREQUEST']._serialized_end=482
  _globals['_PLUGINREQUEST_UPGRADEMODE']._serialized_start=437
  _globals['_PLUGINREQUEST_UPGRADEMODE']._serialized_end=482
  _globals['_PLUGININFO']._serialized_start=485
  _globals['_PLUGININFO']._serialized_end=760
  _globals['_PLUGININFO_UPGRADEMODE']._serialized_start=437
  _globals['_PLUGININFO_UPGRADEMODE']._serialized_end=482
  _globals['_CREATEPROTOCOLREQUEST']._serialized_start=763
  _globals['_CREATEPROTOCOLREQUEST']._serialized_end=905
  _globals['_UPDATEPROTOCOLREQUEST']._serialized_start=907
  _globals['_UPDATEPROTOCOLREQUEST']._serialized_end=1004
  _globals['_UPDATEPROTOCOLPLUGINREQUEST']._serialized_start=1007
  _globals['_UPDATEPROTOCOLPLUGINREQUEST']._serialized_end=1135
  _globals['_PROTOCOLREQUEST']._serialized_start=1137
  _globals['_PROTOCOLREQUEST']._serialized_end=1175
  _globals['_PROTOCOLQUERY']._serialized_start=1178
  _globals['_PROTOCOLQUERY']._serialized_end=1549
  _globals['_PROTOCOLQUERY_PROTOCOLSTATE']._serialized_start=1429
  _globals['_PROTOCOLQUERY_PROTOCOLSTATE']._serialized_end=1481
  _globals['_PROTOCOLQUERY_PROTOCOLTYPE']._serialized_start=1483
  _globals['_PROTOCOLQUERY_PROTOCOLTYPE']._serialized_end=1549
  _globals['_PROTOCOLINFO']._serialized_start=1552
  _globals['_PROTOCOLINFO']._serialized_end=2085
  _globals['_PROTOCOLINFO_PROTOCOLSTATE']._serialized_start=1429
  _globals['_PROTOCOLINFO_PROTOCOLSTATE']._serialized_end=1481
  _globals['_PROTOCOLINFO_PROTOCOLTYPE']._serialized_start=1483
  _globals['_PROTOCOLINFO_PROTOCOLTYPE']._serialized_end=1549
  _globals['_PROTOCOLSINFO']._serialized_start=2087
  _globals['_PROTOCOLSINFO']._serialized_end=2184
  _globals['_PROTOCOLSTATQUERY']._serialized_start=2186
  _globals['_PROTOCOLSTATQUERY']._serialized_end=2259
  _globals['_PROTOCOL']._serialized_start=2262
  _globals['_PROTOCOL']._serialized_end=3581
# @@protoc_insertion_point(module_scope)
