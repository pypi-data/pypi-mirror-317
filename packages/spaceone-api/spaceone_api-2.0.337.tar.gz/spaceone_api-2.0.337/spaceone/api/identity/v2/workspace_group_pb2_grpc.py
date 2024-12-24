# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from spaceone.api.identity.v2 import workspace_group_pb2 as spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2

GRPC_GENERATED_VERSION = '1.64.1'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in spaceone/api/identity/v2/workspace_group_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class WorkspaceGroupStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.create = channel.unary_unary(
                '/spaceone.api.identity.v2.WorkspaceGroup/create',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.CreateWorkspaceGroupRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupInfo.FromString,
                _registered_method=True)
        self.update = channel.unary_unary(
                '/spaceone.api.identity.v2.WorkspaceGroup/update',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.UpdateWorkspaceGroupRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupInfo.FromString,
                _registered_method=True)
        self.delete = channel.unary_unary(
                '/spaceone.api.identity.v2.WorkspaceGroup/delete',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.add_users = channel.unary_unary(
                '/spaceone.api.identity.v2.WorkspaceGroup/add_users',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.UsersWorkspaceGroupRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupInfo.FromString,
                _registered_method=True)
        self.remove_users = channel.unary_unary(
                '/spaceone.api.identity.v2.WorkspaceGroup/remove_users',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.UsersWorkspaceGroupRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupInfo.FromString,
                _registered_method=True)
        self.update_role = channel.unary_unary(
                '/spaceone.api.identity.v2.WorkspaceGroup/update_role',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupUpdateRoleRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupInfo.FromString,
                _registered_method=True)
        self.get = channel.unary_unary(
                '/spaceone.api.identity.v2.WorkspaceGroup/get',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupInfo.FromString,
                _registered_method=True)
        self.list = channel.unary_unary(
                '/spaceone.api.identity.v2.WorkspaceGroup/list',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupSearchQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupsInfo.FromString,
                _registered_method=True)
        self.stat = channel.unary_unary(
                '/spaceone.api.identity.v2.WorkspaceGroup/stat',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupStatQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                _registered_method=True)


class WorkspaceGroupServicer(object):
    """Missing associated documentation comment in .proto file."""

    def create(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def add_users(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def remove_users(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update_role(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WorkspaceGroupServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'create': grpc.unary_unary_rpc_method_handler(
                    servicer.create,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.CreateWorkspaceGroupRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupInfo.SerializeToString,
            ),
            'update': grpc.unary_unary_rpc_method_handler(
                    servicer.update,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.UpdateWorkspaceGroupRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupInfo.SerializeToString,
            ),
            'delete': grpc.unary_unary_rpc_method_handler(
                    servicer.delete,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'add_users': grpc.unary_unary_rpc_method_handler(
                    servicer.add_users,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.UsersWorkspaceGroupRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupInfo.SerializeToString,
            ),
            'remove_users': grpc.unary_unary_rpc_method_handler(
                    servicer.remove_users,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.UsersWorkspaceGroupRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupInfo.SerializeToString,
            ),
            'update_role': grpc.unary_unary_rpc_method_handler(
                    servicer.update_role,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupUpdateRoleRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupInfo.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupInfo.SerializeToString,
            ),
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupSearchQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupsInfo.SerializeToString,
            ),
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupStatQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.identity.v2.WorkspaceGroup', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('spaceone.api.identity.v2.WorkspaceGroup', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class WorkspaceGroup(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.identity.v2.WorkspaceGroup/create',
            spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.CreateWorkspaceGroupRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def update(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.identity.v2.WorkspaceGroup/update',
            spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.UpdateWorkspaceGroupRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.identity.v2.WorkspaceGroup/delete',
            spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def add_users(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.identity.v2.WorkspaceGroup/add_users',
            spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.UsersWorkspaceGroupRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def remove_users(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.identity.v2.WorkspaceGroup/remove_users',
            spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.UsersWorkspaceGroupRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def update_role(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.identity.v2.WorkspaceGroup/update_role',
            spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupUpdateRoleRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.identity.v2.WorkspaceGroup/get',
            spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def list(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.identity.v2.WorkspaceGroup/list',
            spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupSearchQuery.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupsInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def stat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.identity.v2.WorkspaceGroup/stat',
            spaceone_dot_api_dot_identity_dot_v2_dot_workspace__group__pb2.WorkspaceGroupStatQuery.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
