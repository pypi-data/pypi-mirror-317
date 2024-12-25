from poktroll_clients.ffi import ffi, libpoktroll_clients
from poktroll_clients.go_memory import GoManagedMem, go_ref


class EventsQueryClient(GoManagedMem):
    """
    TODO_IN_THIS_COMMIT: comment
    """

    go_ref: go_ref
    err_ptr: ffi.CData

    def __init__(self, query_node_rpc_websocket_url: str):
        self_ref = libpoktroll_clients.NewEventsQueryClient(query_node_rpc_websocket_url.encode('utf-8'))
        super().__init__(self_ref)

    def EventsBytes(self, query: str) -> go_ref:
        return libpoktroll_clients.EventsQueryClientEventsBytes(self.go_ref, query.encode('utf-8'))
