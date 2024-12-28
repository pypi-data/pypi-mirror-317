import inspect
from pydantic.main import _model_construction


class EnforceDocStringBaseClass(_model_construction.ModelMetaclass):
    """
    Metaclass that enforces the presence of docstrings in classes and their methods.

    This metaclass ensures that any class using it as a metaclass must have a docstring.
    Additionally, all methods defined within the class (not inherited) must also have docstrings.
    If a class or method is missing a docstring, a TypeError will be raised during class creation.

    Usage:
        class MyClass(metaclass=EnforceDocStringBaseClass):
            \"\"\"This is a class docstring.\"\"\"

            def my_method(self):
                \"\"\"This is a method docstring.\"\"\"
                pass

    Raises:
        TypeError: If the class or any of its methods do not have a docstring.
    """

    def __new__(cls, name, bases, attrs):
        # Create the new class first
        new_class = super().__new__(cls, name, bases, attrs)

        # class must have a docstring
        if not new_class.__doc__:
            raise TypeError(
                f"Class '{name}' must have a docstring. All classes must have a docstring."
            )

        # Iterate over all attributes in the fully constructed class
        for attr_name, attr_value in new_class.__dict__.items():
            # Check if the attribute is a method defined in this class (not inherited)
            if callable(attr_value) and inspect.isfunction(attr_value):
                # Ensure the method has a docstring
                if not attr_value.__doc__:
                    raise TypeError(
                        f"Method '{attr_name}' in class '{name}' must have a docstring."
                    )

        return new_class