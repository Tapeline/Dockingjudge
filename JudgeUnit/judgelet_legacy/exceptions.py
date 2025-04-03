"""Provides exception classes"""


class SerializationException(Exception):
    """Thrown when any entity cannot be serialized or deserialized"""


class CompilerNotFoundException(Exception):
    """Thrown if requested compiler is not found on the judgelet"""
