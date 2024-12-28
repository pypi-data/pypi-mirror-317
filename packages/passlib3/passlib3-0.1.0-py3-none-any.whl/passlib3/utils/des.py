"""
passlib3.utils.des - DEPRECATED LOCATION, WILL BE REMOVED IN 2.0

This has been moved to :mod:`passlib3.crypto.des`.
"""
#=============================================================================
# import from new location
#=============================================================================
from warnings import warn
warn("the 'passlib3.utils.des' module has been relocated to 'passlib3.crypto.des' "
     "as of passlib3 1.7, and the old location will be removed in passlib3 2.0",
     DeprecationWarning)

#=============================================================================
# relocated functions
#=============================================================================
from passlib3.utils.decor import deprecated_function
from passlib3.crypto.des import expand_des_key, des_encrypt_block, des_encrypt_int_block

expand_des_key = deprecated_function(deprecated="1.7", removed="1.8",
    replacement="passlib3.crypto.des.expand_des_key")(expand_des_key)

des_encrypt_block = deprecated_function(deprecated="1.7", removed="1.8",
    replacement="passlib3.crypto.des.des_encrypt_block")(des_encrypt_block)

des_encrypt_int_block = deprecated_function(deprecated="1.7", removed="1.8",
    replacement="passlib3.crypto.des.des_encrypt_int_block")(des_encrypt_int_block)

#=============================================================================
# deprecated functions -- not carried over to passlib3.crypto.des
#=============================================================================
import struct
_unpack_uint64 = struct.Struct(">Q").unpack

@deprecated_function(deprecated="1.6", removed="1.8",
                     replacement="passlib3.crypto.des.des_encrypt_int_block()")
def mdes_encrypt_int_block(key, input, salt=0, rounds=1): # pragma: no cover -- deprecated & unused
    if isinstance(key, bytes):
        if len(key) == 7:
            key = expand_des_key(key)
        key = _unpack_uint64(key)[0]
    return des_encrypt_int_block(key, input, salt, rounds)

#=============================================================================
# eof
#=============================================================================
