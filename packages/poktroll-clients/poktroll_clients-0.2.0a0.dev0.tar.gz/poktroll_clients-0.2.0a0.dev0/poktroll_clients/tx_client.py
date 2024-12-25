import asyncio
from typing import Dict, Tuple
from urllib.parse import urlparse

from atomics import INTEGRAL, atomic, INT
from google.protobuf.message import Message

from cffi import FFIError

from poktroll_clients import (
    EventsQueryClient,
    BlockClient,
    BlockQueryClient,
    SupplyMany,
    TxContext,
    libpoktroll_clients,
    ffi,
    go_ref,
    GoManagedMem,
    check_err,
    check_ref,
)
from poktroll_clients.protobuf import SerializedProto, ProtoMessageArray


class TxClient(GoManagedMem):
    """
    TODO_IN_THIS_COMMIT: comment
    """

    go_ref: go_ref
    err_ptr: ffi.CData
    _callback_idx: INTEGRAL = atomic(width=8, atype=INT)
    _callback_fns: Dict[int, Tuple[ffi.CData, ffi.CData, ffi.CData]] = {}

    def __init__(self,
                 signing_key_name: str,
                 deps_ref: go_ref = -1,
                 query_node_rpc_url: str = "",
                 tx_node_rpc_url: str = ""):
        """
        Constructor for TxClient.

        If deps_ref is not provided, a depinject config will be created using the provided query_node_rpc_url
        and tx_node_rpc_url. If, then, either of these are not provided, a ValueError will be raised.
        """
        if deps_ref == -1:
            deps_ref = _new_tx_client_depinject_config(query_node_rpc_url, tx_node_rpc_url)

        go_ref = libpoktroll_clients.NewTxClient(deps_ref, signing_key_name.encode('utf-8'), self.err_ptr)
        super().__init__(go_ref)

        check_err(self.err_ptr)
        check_ref(go_ref)

    async def sign_and_broadcast(self, *msgs: Message) -> asyncio.Future:
        """
        Signs and broadcasts a transaction.
        :param msgs: The protobuf Message(s) to sign and broadcast.
        :return: Future that completes when the transaction is processed.
        """

        op, future = self._new_async_operation()

        serialized_msgs = ProtoMessageArray(messages=[
            SerializedProto(
                type_url=msg.DESCRIPTOR.full_name,
                data=msg.SerializeToString()
            ) for msg in msgs
        ])

        err_ch_ref = libpoktroll_clients.TxClient_SignAndBroadcastMany(  # <-- line 71
            op,
            self.go_ref,
            serialized_msgs.to_c_struct(),
        )

        if err_ch_ref == -1:
            error_msg = ffi.string(op.ctx.error_msg).decode('utf-8')
            future.set_exception(FFIError(error_msg))

        return await future

    def _new_async_operation(self) -> Tuple[ffi.CData, asyncio.Future]:
        """
        Creates a new AsyncOperation with callbacks and associated Future.
        The callbacks are protected from garbage collection by storing in self._callback_fns.
        """

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        future = loop.create_future()

        # Create AsyncContext
        ctx = ffi.new("AsyncContext *")
        next_callback_idx = self._callback_idx.fetch_inc()

        # Define callbacks
        @ffi.callback("void(AsyncContext*, const void*)")
        def success_cb(ctx, result):
            try:
                loop.call_soon_threadsafe(future.set_result, None)
            finally:
                self._free_callback(next_callback_idx)

        @ffi.callback("void(AsyncContext*, const char*)")
        def error_cb(ctx, error):
            try:
                error_str = ffi.string(error).decode('utf-8')
                loop.call_soon_threadsafe(future.set_exception, Exception(error_str))
            except Exception as e:
                future.set_exception(e)
            finally:
                self._free_callback(next_callback_idx)

        @ffi.callback("void(AsyncContext*)")
        def cleanup_cb(ctx):
            self._free_callback(next_callback_idx)

        # Create AsyncOperation
        op = ffi.new("AsyncOperation *")
        op.ctx = ctx
        op.on_success = success_cb
        op.on_error = error_cb
        op.cleanup = cleanup_cb

        # Store callbacks to protect from garbage collection
        self._callback_fns[next_callback_idx] = (success_cb, error_cb, cleanup_cb)

        return op, future

    def _free_callback(self, callback_idx: int):
        """
        Clean up stored callbacks.
        """
        self._callback_fns.pop(callback_idx)


def _new_tx_client_depinject_config(
        query_node_rpc_url: str,
        tx_node_rpc_url: str
) -> go_ref:
    """
    TODO_IN_THIS_COMMIT: comment
    """

    # TODO_IN_THIS_COMMIT: add more detail to the error messages,
    # explaining the expected format, with an example.
    if not query_node_rpc_url:
        raise ValueError("query_node_rpc_url must be specified")

    if not tx_node_rpc_url:
        raise ValueError("tx_node_rpc_url must be specified")

    query_node_ws_url = urlparse(query_node_rpc_url)._replace(scheme="ws", path="websocket")
    events_query_client = EventsQueryClient(query_node_ws_url.geturl())
    block_query_client = BlockQueryClient(query_node_rpc_url)

    deps_ref = SupplyMany(events_query_client, block_query_client)
    block_client = BlockClient(deps_ref)

    tx_ctx = TxContext(tx_node_rpc_url)

    return SupplyMany(events_query_client, block_client, tx_ctx)
