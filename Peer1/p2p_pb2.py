# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: p2p.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tp2p.proto\"/\n\rUploadRequest\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\"!\n\x0eUploadResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"#\n\x0f\x44ownloadRequest\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\" \n\x10\x44ownloadResponse\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\"\x12\n\x10ListFilesRequest\"\"\n\x11ListFilesResponse\x12\r\n\x05\x66iles\x18\x01 \x03(\t2\x9c\x01\n\nP2PService\x12)\n\x06Upload\x12\x0e.UploadRequest\x1a\x0f.UploadResponse\x12/\n\x08\x44ownload\x12\x10.DownloadRequest\x1a\x11.DownloadResponse\x12\x32\n\tListFiles\x12\x11.ListFilesRequest\x1a\x12.ListFilesResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'p2p_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_UPLOADREQUEST']._serialized_start=13
  _globals['_UPLOADREQUEST']._serialized_end=60
  _globals['_UPLOADRESPONSE']._serialized_start=62
  _globals['_UPLOADRESPONSE']._serialized_end=95
  _globals['_DOWNLOADREQUEST']._serialized_start=97
  _globals['_DOWNLOADREQUEST']._serialized_end=132
  _globals['_DOWNLOADRESPONSE']._serialized_start=134
  _globals['_DOWNLOADRESPONSE']._serialized_end=166
  _globals['_LISTFILESREQUEST']._serialized_start=168
  _globals['_LISTFILESREQUEST']._serialized_end=186
  _globals['_LISTFILESRESPONSE']._serialized_start=188
  _globals['_LISTFILESRESPONSE']._serialized_end=222
  _globals['_P2PSERVICE']._serialized_start=225
  _globals['_P2PSERVICE']._serialized_end=381
# @@protoc_insertion_point(module_scope)