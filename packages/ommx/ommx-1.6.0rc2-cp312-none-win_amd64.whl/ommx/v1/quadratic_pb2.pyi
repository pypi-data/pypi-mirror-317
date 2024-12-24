"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import ommx.v1.linear_pb2
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class Quadratic(google.protobuf.message.Message):
    """Quadratic function as a COO-style sparse matrix and linear sparse vector.

    COOrdinate format, also known as triplet format, is a way to represent sparse matrices as a list of non-zero elements.
    It consists of three lists: the row indices, the column indices, and the values of the non-zero elements with following constraints:

    - Entries and coordinates sorted by row, then column.
    - There are no duplicate entries (i.e. duplicate (i,j) locations)
    - Data arrays MAY have explicit zeros.

    Note that this matrix is not assured to be symmetric nor upper triangular.
    For example, a quadratic function `x1^2 + x2^2 + 2x1*x2` can be represented as:

    - `{ rows: [0, 0, 1], columns: [0, 1, 1], values: [1, 2, 1] }`, i.e. an upper triangular matrix `[[1, 2], [0, 1]`
    - `{ rows: [0, 0, 1, 1], columns: [0, 1, 0, 1], values: [1, 1, 1, 1] }`, i.e. a symmetric matrix `[[1, 1], [1, 1]]`

    or even a non-symmetric, non-trianglar matrix as `x1^2 + 3x1*x2 - x2*x1 + x2^2`:

    - `{ rows: [0, 0, 1, 1], columns: [0, 1, 0, 1], values: [1, 3, -1, 1] }`, i.e. a non-symmetric matrix `[[1, 3], [-1, 1]]`
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ROWS_FIELD_NUMBER: builtins.int
    COLUMNS_FIELD_NUMBER: builtins.int
    VALUES_FIELD_NUMBER: builtins.int
    LINEAR_FIELD_NUMBER: builtins.int
    @property
    def rows(
        self,
    ) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[
        builtins.int
    ]: ...
    @property
    def columns(
        self,
    ) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[
        builtins.int
    ]: ...
    @property
    def values(
        self,
    ) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[
        builtins.float
    ]: ...
    @property
    def linear(self) -> ommx.v1.linear_pb2.Linear: ...
    def __init__(
        self,
        *,
        rows: collections.abc.Iterable[builtins.int] | None = ...,
        columns: collections.abc.Iterable[builtins.int] | None = ...,
        values: collections.abc.Iterable[builtins.float] | None = ...,
        linear: ommx.v1.linear_pb2.Linear | None = ...,
    ) -> None: ...
    def HasField(
        self, field_name: typing.Literal["_linear", b"_linear", "linear", b"linear"]
    ) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing.Literal[
            "_linear",
            b"_linear",
            "columns",
            b"columns",
            "linear",
            b"linear",
            "rows",
            b"rows",
            "values",
            b"values",
        ],
    ) -> None: ...
    def WhichOneof(
        self, oneof_group: typing.Literal["_linear", b"_linear"]
    ) -> typing.Literal["linear"] | None: ...

global___Quadratic = Quadratic
