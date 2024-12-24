# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ommx/v1/parametric_instance.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ommx.v1 import constraint_pb2 as ommx_dot_v1_dot_constraint__pb2
from ommx.v1 import constraint_hints_pb2 as ommx_dot_v1_dot_constraint__hints__pb2
from ommx.v1 import decision_variables_pb2 as ommx_dot_v1_dot_decision__variables__pb2
from ommx.v1 import function_pb2 as ommx_dot_v1_dot_function__pb2
from ommx.v1 import instance_pb2 as ommx_dot_v1_dot_instance__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n!ommx/v1/parametric_instance.proto\x12\x07ommx.v1\x1a\x18ommx/v1/constraint.proto\x1a\x1eommx/v1/constraint_hints.proto\x1a ommx/v1/decision_variables.proto\x1a\x16ommx/v1/function.proto\x1a\x16ommx/v1/instance.proto"\x97\x02\n\tParameter\x12\x0e\n\x02id\x18\x01 \x01(\x04R\x02id\x12\x17\n\x04name\x18\x02 \x01(\tH\x00R\x04name\x88\x01\x01\x12\x1e\n\nsubscripts\x18\x03 \x03(\x03R\nsubscripts\x12\x42\n\nparameters\x18\x04 \x03(\x0b\x32".ommx.v1.Parameter.ParametersEntryR\nparameters\x12%\n\x0b\x64\x65scription\x18\x05 \x01(\tH\x01R\x0b\x64\x65scription\x88\x01\x01\x1a=\n\x0fParametersEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x42\x07\n\x05_nameB\x0e\n\x0c_description"\xfc\x03\n\x12ParametricInstance\x12?\n\x0b\x64\x65scription\x18\x01 \x01(\x0b\x32\x1d.ommx.v1.Instance.DescriptionR\x0b\x64\x65scription\x12H\n\x12\x64\x65\x63ision_variables\x18\x02 \x03(\x0b\x32\x19.ommx.v1.DecisionVariableR\x11\x64\x65\x63isionVariables\x12\x32\n\nparameters\x18\x03 \x03(\x0b\x32\x12.ommx.v1.ParameterR\nparameters\x12/\n\tobjective\x18\x04 \x01(\x0b\x32\x11.ommx.v1.FunctionR\tobjective\x12\x35\n\x0b\x63onstraints\x18\x05 \x03(\x0b\x32\x13.ommx.v1.ConstraintR\x0b\x63onstraints\x12-\n\x05sense\x18\x06 \x01(\x0e\x32\x17.ommx.v1.Instance.SenseR\x05sense\x12\x43\n\x10\x63onstraint_hints\x18\x07 \x01(\x0b\x32\x18.ommx.v1.ConstraintHintsR\x0f\x63onstraintHints\x12K\n\x13removed_constraints\x18\x08 \x03(\x0b\x32\x1a.ommx.v1.RemovedConstraintR\x12removedConstraintsBc\n\x0b\x63om.ommx.v1B\x17ParametricInstanceProtoP\x01\xa2\x02\x03OXX\xaa\x02\x07Ommx.V1\xca\x02\x07Ommx\\V1\xe2\x02\x13Ommx\\V1\\GPBMetadata\xea\x02\x08Ommx::V1b\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, "ommx.v1.parametric_instance_pb2", _globals
)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals["DESCRIPTOR"]._loaded_options = None
    _globals[
        "DESCRIPTOR"
    ]._serialized_options = b"\n\013com.ommx.v1B\027ParametricInstanceProtoP\001\242\002\003OXX\252\002\007Ommx.V1\312\002\007Ommx\\V1\342\002\023Ommx\\V1\\GPBMetadata\352\002\010Ommx::V1"
    _globals["_PARAMETER_PARAMETERSENTRY"]._loaded_options = None
    _globals["_PARAMETER_PARAMETERSENTRY"]._serialized_options = b"8\001"
    _globals["_PARAMETER"]._serialized_start = 187
    _globals["_PARAMETER"]._serialized_end = 466
    _globals["_PARAMETER_PARAMETERSENTRY"]._serialized_start = 380
    _globals["_PARAMETER_PARAMETERSENTRY"]._serialized_end = 441
    _globals["_PARAMETRICINSTANCE"]._serialized_start = 469
    _globals["_PARAMETRICINSTANCE"]._serialized_end = 977
# @@protoc_insertion_point(module_scope)
