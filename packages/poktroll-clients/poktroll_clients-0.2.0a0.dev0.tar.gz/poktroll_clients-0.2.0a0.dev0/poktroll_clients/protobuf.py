import importlib
from dataclasses import dataclass
from pprint import pprint
from typing import List

from google.protobuf import symbol_database, message

from poktroll_clients import go_ref, libpoktroll_clients, check_err
from poktroll_clients.cases import camel_to_snake_case
from poktroll_clients.ffi import ffi


@dataclass
class SerializedProto:
    """
    Represents a serialized protobuf message with its type URL and binary data.
    Handles conversion to C structures while ensuring proper memory management.
    """
    type_url: str
    data: bytes

    @staticmethod
    def from_c_struct(c_serialized_proto: ffi.CData):
        return SerializedProto(
            type_url=(ffi.string(c_serialized_proto.type_url, c_serialized_proto.type_url_length).decode('utf-8')),
            data=(bytes(ffi.buffer(c_serialized_proto.data, c_serialized_proto.data_length))),
        )

    def __init__(self, c_serialized_proto: ffi.CData = None, type_url: str = "", data: bytes = b""):
        self.type_url = type_url
        self.data = data

        if c_serialized_proto is not None:
            self.type_url = ffi.string(c_serialized_proto.type_url, c_serialized_proto.type_url_length).decode('utf-8')
            self.data = bytes(ffi.buffer(c_serialized_proto.data, c_serialized_proto.data_length))

    def to_c_struct(self) -> ffi.CData:
        """
        Converts the Python protobuf data to a C struct while preserving the underlying memory.
        Returns a C serialized_proto struct pointer.
        """
        serialized_proto = ffi.new("serialized_proto *")

        # Create buffers and store them as instance attributes to prevent GC
        self._type_url_bytes = self.type_url.encode('utf-8')
        self._type_url_buffer = ffi.new("uint8_t[]", self._type_url_bytes)
        self._data_buffer = ffi.new("uint8_t[]", self.data)

        # Assign the buffers to the C struct
        serialized_proto.type_url = self._type_url_buffer
        serialized_proto.type_url_length = len(self._type_url_bytes)
        serialized_proto.data = self._data_buffer
        serialized_proto.data_length = len(self.data)

        return serialized_proto


@dataclass
class ProtoMessageArray:
    """
    Represents an array of serialized protobuf messages.
    Handles conversion to C structures while ensuring proper memory management.
    """
    messages: List[SerializedProto]

    @staticmethod
    def from_c_struct(c_proto_message_array: ffi.CData):
        proto_message_array = ProtoMessageArray(messages=[])
        for i in range(c_proto_message_array.num_messages):
            serialized_proto = SerializedProto.from_c_struct(c_proto_message_array.messages[i])
            proto_message_array.messages.append(serialized_proto)

        return proto_message_array

    def to_c_struct(self) -> ffi.CData:
        """
        Converts the Python protobuf message array to a C struct while preserving the underlying memory.
        Returns a C proto_message_array struct pointer.
        """
        # Create the array structure
        proto_message_array = ffi.new("proto_message_array *")
        proto_message_array.num_messages = len(self.messages)

        # Allocate the array of message structures
        proto_message_array.messages = ffi.new("serialized_proto[]", len(self.messages))

        # Convert each message and store C structs as instance attributes
        self._message_structs = []
        for i, msg in enumerate(self.messages):
            # Create and store the C struct for this message
            c_msg = msg.to_c_struct()
            self._message_structs.append(c_msg)

            # Copy the data to the array
            proto_message_array.messages[i].type_url = c_msg.type_url
            proto_message_array.messages[i].type_url_length = c_msg.type_url_length
            proto_message_array.messages[i].data = c_msg.data
            proto_message_array.messages[i].data_length = c_msg.data_length

        return proto_message_array


def get_serialized_proto(go_proto_ref: go_ref) -> SerializedProto:
    """
    Converts a Go reference, which is assumed to be a concrete protobuf type, into
    the corresponding SerializedProto object. If the reference is not found or to
    a non-protobuf type, an error is raised.

    Args:
        go_proto_ref: Go reference to a protobuf message
    Returns:
        SerializedProto: SerializedProto object containing the type URL and data
        of the protobuf message
    Raises:
        FFIError: If the Go reference is not found or to a non-protobuf type
    """
    err_ptr = ffi.new("char **")

    c_serialized_proto = libpoktroll_clients.GetGoProtoAsSerializedProto(go_proto_ref, err_ptr)

    check_err(err_ptr)

    # TODO_IN_THIS_COMMIT: Free the C struct
    # NB: Caller is responsible for freeing the returned C struct.
    serialized_proto = SerializedProto.from_c_struct(c_serialized_proto)
    # ffi.free(c_serialized_proto)

    return serialized_proto


def deserialize_protobuf(serialized_proto: SerializedProto) -> message.Message:
    """
    Deserialize protocol buffer data given a type URL.

    Args:
        serialized_proto: SerializedProto object containing the serialized protobuf message.
    Returns:
        Deserialized protobuf message as its concrete type.
    Raises:
        ValueError: If type URL is invalid or message type cannot be found
        ImportError: If the protobuf module cannot be imported
    """

    # First, import the module containing the protobuf classes
    # This ensures the types are registered in the symbol database
    type_url = serialized_proto.type_url.lstrip("/")
    poktroll_namespace = type_url.rsplit(".", 1)[0]
    filename_prefix = camel_to_snake_case(type_url.rsplit('.', 1)[1])
    package_filename = f"{filename_prefix}_pb2"
    package_module = f"poktroll_clients.proto.{poktroll_namespace}.{package_filename}"

    try:
        importlib.import_module(package_module)
    except ImportError as e:
        try:
            # NB: Fallback to importing the types_pb2 module if the main module fails
            package_module = f"poktroll_clients.proto.{poktroll_namespace}.types_pb2"
            importlib.import_module(package_module)
        except ImportError as e:
            raise ImportError(f"Could not import protobuf module {package_module}: {str(e)}")

    # Extract the full message type from the type URL
    if '/' in type_url:
        _, full_type = type_url.split('/', 1)
    else:
        full_type = type_url

    # Split into package and message type to validate format
    parts = full_type.split('.')
    if len(parts) < 2:
        raise ValueError("Invalid type URL format")

    try:
        # Get the message class from the symbol database
        db = symbol_database.Default()
        message_class = db.GetSymbol(full_type)

        # Create a new message instance and parse the data
        message = message_class()
        message.ParseFromString(serialized_proto.data)

        return message
        # # Convert to dictionary for easier handling
        # return MessageToDict(message)

    except KeyError as e:
        raise ValueError(
            f"Could not find message type: {full_type}. Make sure it's registered in the symbol database.") from e
    except Exception as e:
        raise ValueError(f"Error deserializing protobuf: {str(e)}") from e


def get_proto_from_go_ref(go_proto_ref: go_ref) -> message.Message:
    """
    Converts a Go reference, which is assumed to be a concrete protobuf type, into
    the corresponding Python protobuf message. If the reference is not found or to
    a non-protobuf type, an error is raised.

    Args:
        go_proto_ref: Go reference to a protobuf message
    Returns:
        message.Message: Deserialized protobuf message
    Raises:
        FFIError: If the Go reference is not found or to a non-protobuf type
        ValueError: If the type URL is invalid or the message type cannot be found
        ImportError: If the protobuf module cannot be imported
    """
    serialized_proto = get_serialized_proto(go_proto_ref)
    return deserialize_protobuf(serialized_proto)
