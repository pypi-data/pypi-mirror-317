"""passlib3.ext.django.models -- monkeypatch django hashing framework"""
#=============================================================================
# imports
#=============================================================================
# core
# site
# pkg
from passlib3.context import CryptContext
from passlib3.ext.django.utils import DjangoContextAdapter
# local
__all__ = ["password_context"]

#=============================================================================
# global attrs
#=============================================================================

#: adapter instance used to drive most of this
adapter = DjangoContextAdapter()

# the context object which this patches contrib.auth to use for password hashing.
# configuration controlled by ``settings.PASSLIB_CONFIG``.
password_context = adapter.context

#: hook callers should use if context is changed
context_changed = adapter.reset_hashers

#=============================================================================
# main code
#=============================================================================

# load config & install monkeypatch
adapter.load_model()

#=============================================================================
# eof
#=============================================================================
