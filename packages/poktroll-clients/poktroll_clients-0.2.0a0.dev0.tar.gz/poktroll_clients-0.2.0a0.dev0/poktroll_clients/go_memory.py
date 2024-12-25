from typing import Callable

from cffi import FFIError

from poktroll_clients.ffi import ffi, libpoktroll_clients

go_ref = int
callback_type = Callable[[ffi.CData, ffi.CData], None]


# TODO_IN_THIS_COMMIT: switch to an err_msg[] array

def check_err(err_ptr: ffi.CData) -> None:
    """
    TODO_IN_THIS_COMMIT: comment...
    """
    if err_ptr[0] != ffi.NULL:
        raise FFIError(ffi.string(err_ptr[0]))


def check_ref(go_ref: go_ref) -> None:
    # TODO_NEXT_LIBPOKTROLL_CLIENT_VERSION: this should be 0.
    if go_ref < 0:
        raise FFIError("unexpected empty go_ref")


class GoManagedMem:
    """
    A base class for all objects which embed Go-managed memory.

    Attributes:
        go_ref: The Go-managed memory reference (int).
    """

    go_ref: go_ref
    err_ptr: ffi.CData = ffi.new("char **")

    def __init__(self, go_ref: go_ref):
        """
        Constructor for GoManagedMem. Stores the Go-managed memory reference.
        """

        self.go_ref = go_ref
        self.err_ptr = ffi.new("char **")

        check_err(self.err_ptr)
        check_ref(go_ref)

    def __del__(self):
        """
        Destructor for GoManagedMem. Frees the Go-managed memory associated with the reference.
        """

        libpoktroll_clients.FreeGoMem(self.go_ref)
