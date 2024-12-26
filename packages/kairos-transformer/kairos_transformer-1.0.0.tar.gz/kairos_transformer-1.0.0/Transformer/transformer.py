"""
Transformer Module

This module provides functionality to transform Python objects for tracking and
monitoring. It implements a proxy-based system that allows for dynamic attribute
access, method interception, and reference tracking across the entire object graph.

Key Features:
    - Object transformation and proxying
    - Reference tracking and reshaping
    - Support for both mutable and immutable types
    - Class and instance wrapping capabilities
"""

import gc
from typing import Any, Type, TypeVar

from .exceptions import TransformationError
from .proxy import (
    ComplexProxy,
    DictProxy,
    DynamicProxy,
    FloatProxy,
    FrozensetProxy,
    IntProxy,
    ReferenceTransformer,
    StrProxy,
    TupleProxy,
)

T = TypeVar("T")
TransformedObject = Any


class Transformer(ReferenceTransformer):
    """
    A class that transforms Python objects to enable tracking and monitoring.

    The Transformer class serves as the main entry point for object transformation.
    It maintains a registry of transformed instances and provides methods to transform
    various Python types into their corresponding proxy objects.

    Attributes:
        _instances (dict): A registry mapping object IDs to their transformed proxies.
                         This ensures consistency in transformation across the
                         object graph.

    Example:
        >>> transformer = Transformer()
        >>> obj = {"key": "value"}
        >>> transformed = transformer.transform(obj)
        >>> transformed.new_key = "new_value"  # Dynamic attribute assignment
        >>> print(transformed)  # DictProxy({'key': 'value', 'new_key': 'new_value'})
    """

    def __init__(self) -> None:
        """
        Initialize a new Transformer instance.

        Creates an empty registry to track transformed objects and their proxies.
        This ensures that the same object is always transformed to the same proxy.
        """
        self._instances: dict[int, Any] = {}

    def transform(self, value: object) -> TransformedObject:
        """
        Transform a Python object into its corresponding proxy object.

        This method handles different Python types by creating appropriate
        proxy objects.
        For built-in types, it uses specialized proxy classes
        (IntProxy, DictProxy, etc.).
        For custom classes, it creates a dynamic proxy that preserves the
        original interface.

        Args:
            value (T): The object to transform. Can be of any Python type.

        Returns:
            TransformedObject[T]: A proxy object that wraps the original value while
                                maintaining its interface and adding
                                tracking capabilities.

        Examples:
            >>> transformer = Transformer()
            >>> dict_proxy = transformer.transform({"a": 1})
            >>> int_proxy = transformer.transform(42)
            >>> list_proxy = transformer.transform([1, 2, 3])
        """
        # Handle basic immutable types with specialized proxies
        if isinstance(value, int):
            return IntProxy(value, self)
        elif isinstance(value, float):
            return FloatProxy(value, self)
        elif isinstance(value, str):
            return StrProxy(value, self)
        elif isinstance(value, tuple):
            return TupleProxy(value, self)
        elif isinstance(value, frozenset):
            return FrozensetProxy(value, self)
        elif isinstance(value, complex):
            return ComplexProxy(value, self)
        # Handle mutable types
        elif isinstance(value, dict):
            return DictProxy(value, self)
        elif isinstance(value, (list, set)):
            return DynamicProxy(value, self)
        # Handle classes and other objects
        elif isinstance(value, type):
            return self.wrap_class(value)
        else:
            return DynamicProxy(value, self)

    def wrap_class(self, cls: type[Any]) -> type[Any]:
        """
        Create a proxy subclass that wraps the given class.

        This method creates a new class that inherits from the original class
        and adds proxy functionality. All instances of the wrapped class will
        automatically be proxied.

        Args:
            cls (Type[T]): The class to wrap with proxy functionality.

        Returns:
            Type[T]: A new class that inherits from the original and includes
                    proxy capabilities.

        Example:
            >>> @transformer.wrap_class
            >>> class MyClass:
            >>>     def __init__(self):
            >>>         self.value = 42
        """
        transformer = self

        class WrappedClass(cls):
            """
            A proxy subclass that wraps the original class.

            This class intercepts attribute access and method calls to provide
            tracking and monitoring capabilities while maintaining the original
            class's interface.
            """

            _transformer = transformer

            def __init__(self, *args, **kwargs):
                """
                Initialize the wrapped class instance.

                Creates a DynamicProxy for the instance after calling the original
                class's __init__ method.
                """
                super().__init__(*args, **kwargs)
                self._proxy = DynamicProxy(self, transformer=self._transformer)

            def __getattribute__(self, name: str) -> Any:
                """
                Intercept attribute access to provide proxy functionality.

                Special attributes (starting with '_') are accessed directly,
                while other attributes are accessed through the proxy.
                """
                if name in {"_proxy", "_transformer"} or name.startswith("_"):
                    return super().__getattribute__(name)
                try:
                    return self._proxy.__getattr__(name)
                except AttributeError:
                    return super().__getattribute__(name)

            def __setattr__(self, name: str, value: Any) -> None:
                """
                Intercept attribute assignment to maintain proxy consistency.

                Special attributes are set directly, while other attributes
                are set through the proxy to maintain transformation consistency.
                """
                if name in {"_proxy", "_transformer"} or name.startswith("_"):
                    super().__setattr__(name, value)
                else:
                    self._proxy.__setattr__(name, value)

            def get_original(self) -> Any:
                """
                Retrieve the original unwrapped instance.

                Returns:
                    T: The original instance without proxy wrapping.
                """
                return self._proxy.get_original()

        # Set appropriate class name and docstring
        WrappedClass.__name__ = f"Wrapped{cls.__name__}"
        WrappedClass.__doc__ = f"Proxy subclass of {cls.__name__}"
        return WrappedClass

    def reshape_references(self, original: object, transformed: Any) -> None:
        """
        Update all references to the original object with the transformed version.

        This method scans the entire object graph to find references to the original
        object and replaces them with references to the transformed proxy object.

        Args:
            original (T): The original object whose references need to be updated.
            transformed (Any): The transformed proxy object to replace references with.

        Raises:
            TransformationError: If an error occurs during reference reshaping.
        """
        try:
            # Get all objects that reference the original object
            referrers = gc.get_referrers(original)
            for ref in referrers:
                # Handle dictionary references (both keys and values)
                if isinstance(ref, dict):
                    # Replace dictionary keys
                    keys_to_replace = [k for k in ref if k is original]
                    for k in keys_to_replace:
                        ref.pop(k)
                        ref[transformed] = k
                    # Replace dictionary values
                    for key, value in list(ref.items()):
                        if value is original:
                            ref[key] = transformed
                # Handle list references
                elif isinstance(ref, list):
                    for idx, item in enumerate(ref):
                        if item is original:
                            ref[idx] = transformed
                # Handle object attributes
                elif hasattr(ref, "__dict__"):
                    for attr, value in ref.__dict__.items():
                        if value is original:
                            setattr(ref, attr, transformed)
        except Exception as e:
            raise TransformationError(
                f"Error reshaping references: {e}") from None

    def add_class(self, cls: Type[T]) -> None:
        """
        Register a class for transformation tracking.

        This method wraps the class and makes it available globally for transformation.

        Args:
            cls (Type[T]): The class to add to the transformation registry.
        """
        wrapped_cls = self.wrap_class(cls)
        globals()[wrapped_cls.__name__] = wrapped_cls

    def add_instance(self, instance: object) -> None:
        """
        Register an instance for transformation tracking.

        This method transforms the instance and adds it to the transformation registry.

        Args:
            instance (object): The instance to add to the transformation registry.
        """
        self.transform(instance)
