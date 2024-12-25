from poktroll_clients.ffi import ffi, libpoktroll_clients
from poktroll_clients.go_memory import GoManagedMem, go_ref, check_err
from poktroll_clients.proto.tendermint.types.block_pb2 import Block
from poktroll_clients.protobuf import get_proto_from_go_ref


class BlockClient(GoManagedMem):
    """
    TODO_IN_THIS_COMMIT: comment
    """

    go_ref: go_ref
    err_ptr: ffi.CData

    def __init__(self, deps_ref: go_ref):
        """
        Constructor for BlockClient.
        :param deps_ref: A Go-managed memory reference to a depinject config.
        """

        go_ref = libpoktroll_clients.NewBlockClient(deps_ref, self.err_ptr)
        super().__init__(go_ref)


class BlockQueryClient(GoManagedMem):
    """
    TODO_IN_THIS_COMMIT: comment
    """

    go_ref: go_ref
    err_ptr: ffi.CData

    def __init__(self, query_node_rpc_url: str):
        go_ref = libpoktroll_clients.NewBlockQueryClient(query_node_rpc_url.encode('utf-8'),
                                                         self.err_ptr)

        super().__init__(go_ref)

    def block(self, query_height: int = 0) -> Block:
        """
        TODO_IN_THIS_COMMIT: comment
        """
        if query_height < 1:
            c_query_height = ffi.NULL
        else:
            c_query_height = ffi.new("int64_t *", query_height)


        block_ref = libpoktroll_clients.BlockQueryClient_Block(self.go_ref, c_query_height, self.err_ptr)
        check_err(self.err_ptr)

        return get_proto_from_go_ref(block_ref)
