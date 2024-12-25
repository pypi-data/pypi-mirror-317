from poktroll_clients.ffi import ffi, libpoktroll_clients
from poktroll_clients.go_memory import GoManagedMem, go_ref


class TxContext(GoManagedMem):
    """
    TODO_IN_THIS_COMMIT: comment
    """

    go_ref: go_ref
    err_ptr: ffi.CData

    def __init__(self, tx_node_rpc_url: str):
        """
        Constructor for TxContext.
        :param tx_node_rpc_url: The gRPC URL for the client to use (e.g. tcp://127.0.0.1:26657).
        """

        go_ref = libpoktroll_clients.NewTxContext(tx_node_rpc_url.encode('utf-8'), self.err_ptr)
        super().__init__(go_ref)
