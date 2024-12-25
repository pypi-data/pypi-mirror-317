from poktroll_clients import (
    go_ref,
    ffi,
    libpoktroll_clients,
    GoManagedMem, BlockQueryClient, Supply, check_err, check_ref,
)
from poktroll_clients.proto.poktroll.application.types_pb2 import Application
from poktroll_clients.proto.poktroll.gateway.types_pb2 import Gateway
from poktroll_clients.proto.poktroll.session.params_pb2 import Params as SessionParams
from poktroll_clients.proto.poktroll.session.types_pb2 import Session
from poktroll_clients.proto.poktroll.shared.params_pb2 import Params as SharedParams
from poktroll_clients.proto.poktroll.proof.params_pb2 import Params as ProofParams
from poktroll_clients.proto.poktroll.application.params_pb2 import Params as ApplicationParams
from poktroll_clients.proto.poktroll.shared.service_pb2 import Service
from poktroll_clients.proto.poktroll.shared.supplier_pb2 import Supplier
from poktroll_clients.protobuf import get_proto_from_go_ref, SerializedProto, deserialize_protobuf, ProtoMessageArray


class QueryClient(GoManagedMem):
    """
    A client which can query for any poktroll module state.
    """

    go_ref: go_ref
    err_ptr: ffi.CData

    def __init__(self, query_node_rpc_url: str, deps_ref: go_ref = -1):
        if deps_ref == -1:
            deps_ref = _new_query_client_depinject_config(query_node_rpc_url)

        self_ref = libpoktroll_clients.NewQueryClient(deps_ref,
                                                      query_node_rpc_url.encode('utf-8'),
                                                      self.err_ptr)
        super().__init__(self_ref)

    def get_shared_params(self) -> SharedParams:
        c_serialized_params: SerializedProto = libpoktroll_clients.QueryClient_GetSharedParams(self.go_ref,
                                                                                               self.err_ptr)
        # TODO_IN_THIS_COMMIT: free the C struct and its members
        check_err(self.err_ptr)

        serialized_params = SerializedProto.from_c_struct(c_serialized_params)
        return deserialize_protobuf(serialized_params)

    def get_session_grace_period_end_height(self, query_height: int) -> int:
        session_grace_period_end_height = libpoktroll_clients.QueryClient_GetSessionGracePeriodEndHeight(self.go_ref,
                                                                                                         query_height,
                                                                                                         self.err_ptr)
        check_err(self.err_ptr)

        return session_grace_period_end_height

    def get_claim_window_open_height(self, query_height: int) -> int:
        claim_window_open_height = libpoktroll_clients.QueryClient_GetClaimWindowOpenHeight(self.go_ref, query_height,
                                                                                            self.err_ptr)
        check_err(self.err_ptr)

        return claim_window_open_height

    def get_earliest_supplier_claim_commit_height(self, query_height: int, supplier_operator_address: str) -> int:
        earliest_supplier_claim_commit_height = libpoktroll_clients.QueryClient_GetEarliestSupplierClaimCommitHeight(
            self.go_ref, query_height, supplier_operator_address.encode('utf-8'), self.err_ptr)
        check_err(self.err_ptr)

        return earliest_supplier_claim_commit_height

    def get_proof_window_open_height(self, query_height: int) -> int:
        proof_window_open_height = libpoktroll_clients.QueryClient_GetProofWindowOpenHeight(self.go_ref, query_height,
                                                                                            self.err_ptr)
        check_err(self.err_ptr)

        return proof_window_open_height

    def get_earliest_supplier_proof_commit_height(self, query_height: int, supplier_operator_address: str) -> int:
        earliest_supplier_proof_commit_height = libpoktroll_clients.QueryClient_GetEarliestSupplierProofCommitHeight(
            self.go_ref, query_height, supplier_operator_address.encode('utf-8'), self.err_ptr)
        check_err(self.err_ptr)

        return earliest_supplier_proof_commit_height

    def get_compute_units_to_tokens_multiplier(self) -> int:
        compute_units_to_tokens_multiplier = libpoktroll_clients.QueryClient_GetComputeUnitsToTokensMultiplier(
            self.go_ref, self.err_ptr)
        check_err(self.err_ptr)

        return compute_units_to_tokens_multiplier

    def get_application_params(self) -> ApplicationParams:
        c_serialized_params = libpoktroll_clients.QueryClient_GetApplicationParams(self.go_ref, self.err_ptr)
        # TODO_IN_THIS_COMMIT: free the C struct and its members
        check_err(self.err_ptr)

        serialized_params = SerializedProto.from_c_struct(c_serialized_params)
        return deserialize_protobuf(serialized_params)

    # TODO_BLOCKED(@bryanchriswhite, poktroll#534): add commented methods once
    # Go method dependencies are available.

    # def get_supplier_params(self) -> SupplierParams:
    #     response_ref = libpoktroll_clients.QueryClient_GetSupplierParams(self.go_ref, self.err_ptr)

    # def get_gateway_params(self) -> GatewayParams:
    #     response_ref = libpoktroll_clients.QueryClient_GetGatewayParams(self.go_ref, self.err_ptr)

    def get_session_params(self) -> SessionParams:
        c_serialized_params = libpoktroll_clients.QueryClient_GetSessionParams(self.go_ref, self.err_ptr)
        # TODO_IN_THIS_COMMIT: free the C struct and its members
        check_err(self.err_ptr)

        serialized_params = SerializedProto.from_c_struct(c_serialized_params)
        return deserialize_protobuf(serialized_params)

    # def get_service_params(self) -> ServiceParams:
    #     response_ref = libpoktroll_clients.QueryClient_GetServiceParams(self.go_ref, self.err_ptr)

    def get_proof_params(self) -> ProofParams:
        c_serialized_params = libpoktroll_clients.QueryClient_GetProofParams(self.go_ref, self.err_ptr)
        # TODO_IN_THIS_COMMIT: free the C struct and its members

        check_err(self.err_ptr)

        serialized_params = SerializedProto.from_c_struct(c_serialized_params)
        return deserialize_protobuf(serialized_params)

    # def get_tokenomics_params(self) -> TokenomicsParams:
    #     response_ref = libpoktroll_clients.QueryClient_GetTokenomicsParams(self.go_ref, self.err_ptr)

    def get_application(self, app_address: str) -> Application:
        c_serialized_app = libpoktroll_clients.QueryClient_GetApplication(
            self.go_ref, app_address.encode('utf-8'), self.err_ptr)
        # TODO_IN_THIS_COMMIT: free the C struct and its members
        check_err(self.err_ptr)

        serialized_app = SerializedProto.from_c_struct(c_serialized_app)
        return deserialize_protobuf(serialized_app)

    def get_all_applications(self) -> list[Application]:
        c_proto_message_array = libpoktroll_clients.QueryClient_GetAllApplications(self.go_ref, self.err_ptr)
        # TODO_IN_THIS_COMMIT: free the C struct and its members
        check_err(self.err_ptr)

        proto_message_array = ProtoMessageArray.from_c_struct(c_proto_message_array)
        return [deserialize_protobuf(serialized_proto) for serialized_proto in proto_message_array.messages]

    # def get_gateway(self, gateway_address: str) -> Gateway:
    #     c_serialized_gateway = libpoktroll_clients.QueryClient_GetGateway(
    #         self.go_ref, gateway_address.encode('utf-8'), self.err_ptr)
    #     # TODO_IN_THIS_COMMIT: free the C struct and its members
    #     check_err(self.err_ptr)
    #
    #     serialized_gateway = SerializedProto.from_c_struct(c_serialized_gateway)
    #     return deserialize_protobuf(serialized_gateway)
    #
    # def get_all_gateways(self) -> list[Gateway]:
    #     c_proto_message_array = libpoktroll_clients.QueryClient_GetAllGateways(self.go_ref, self.err_ptr)
    #     # TODO_IN_THIS_COMMIT: free the C struct and its members
    #     check_err(self.err_ptr)
    #
    #     proto_message_array = ProtoMessageArray.from_c_struct(c_proto_message_array)
    #     return [deserialize_protobuf(serialized_proto) for serialized_proto in proto_message_array.messages]

    def get_supplier(self, supplier_operator_address: str) -> Supplier:
        c_serialized_supplier = libpoktroll_clients.QueryClient_GetSupplier(
            self.go_ref, supplier_operator_address.encode('utf-8'), self.err_ptr)
        # TODO_IN_THIS_COMMIT: free the C struct and its members
        check_err(self.err_ptr)

        serialized_supplier = SerializedProto.from_c_struct(c_serialized_supplier)
        return deserialize_protobuf(serialized_supplier)

    # def get_all_suppliers(self) -> list[Supplier]:
    #     c_proto_message_array = libpoktroll_clients.QueryClient_GetAllSuppliers(self.go_ref, self.err_ptr)
    #     # TODO_IN_THIS_COMMIT: free the C struct and its members
    #     check_err(self.err_ptr)
    #
    #     proto_message_array = ProtoMessageArray.from_c_struct(c_proto_message_array)
    #     return [deserialize_protobuf(serialized_proto) for serialized_proto in proto_message_array.messages]

    def get_session(self, app_address: str, service_id: str, block_height: int) -> Session:
        c_serialized_session = libpoktroll_clients.QueryClient_GetSession(
            self.go_ref, app_address.encode('utf-8'), service_id.encode('utf-8'), block_height, self.err_ptr)
        # TODO_IN_THIS_COMMIT: free the C struct and its members
        check_err(self.err_ptr)

        serialized_session = SerializedProto.from_c_struct(c_serialized_session)
        return deserialize_protobuf(serialized_session)

    def get_service(self, service_id: str) -> Service:
        c_serialized_service = libpoktroll_clients.QueryClient_GetService(
            self.go_ref, service_id.encode('utf-8'), self.err_ptr)
        # TODO_IN_THIS_COMMIT: free the C struct and its members
        check_err(self.err_ptr)

        serialized_service = SerializedProto.from_c_struct(c_serialized_service)
        return deserialize_protobuf(serialized_service)

    def get_service_relay_difficulty(self, service_id: str) -> int:
        c_service_relay_difficulty = libpoktroll_clients.QueryClient_GetServiceRelayDifficulty(
            self.go_ref, service_id.encode('utf-8'), self.err_ptr)
        # TODO_IN_THIS_COMMIT: free the C struct and its members
        check_err(self.err_ptr)


        serialized_service_relay_difficulty = SerializedProto.from_c_struct(c_service_relay_difficulty)
        return deserialize_protobuf(serialized_service_relay_difficulty)


def _new_query_client_depinject_config(
        query_node_rpc_url: str,
) -> go_ref:
    """
    Construct the required dependencies for the query client:
    - BlockQueryClient

    Args:
        query_node_rpc_url: The URL of the query node RPC server.
    Returns:
        A go_ref reference to the depinject config which contains the Go dependencies.
    Raises:
        ValueError: If the query_node_rpc_url is not specified.
    """

    # TODO_IN_THIS_COMMIT: add more detail to the error messages,
    # explaining the expected format, with an example.
    if not query_node_rpc_url:
        raise ValueError("query_node_rpc_url must be specified")

    block_query_client = BlockQueryClient(query_node_rpc_url)
    return Supply(block_query_client.go_ref)
