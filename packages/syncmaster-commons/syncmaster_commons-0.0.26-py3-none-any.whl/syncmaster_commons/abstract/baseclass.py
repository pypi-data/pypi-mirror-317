import keyword
from abc import abstractmethod
from typing import Any, Union, override

from pydantic import BaseModel

from syncmaster_commons.abstract.enforcers import EnforceDocStringBaseClass


class SMBaseClass(BaseModel, metaclass=EnforceDocStringBaseClass):
    """SMBaseClass is an abstract base class for implementing a syncmaster library."""

    def to_dict(self):
        """
        Converts the object to a dictionary representation. Checks if the object has a `to_dict()` method and calls it.
        If the object does not have a `to_dict()` method, it raises a `NotImplementedError`. Also includes the object's
        attributes in the dictionary. If object is another class, it calls `to_dict()` on the related instance.

        Returns:
            dict: A dictionary containing the key-value pairs representing the object's attributes.
        """
        dict_obj = {}
        for field in self.model_fields:
            field_value = getattr(self, field)
            if hasattr(field_value, "to_dict"):
                dict_obj[field] = field_value.to_dict()
            else:
                dict_obj[field] = field_value
        return dict_obj

    @classmethod
    def from_dict(cls, payload: dict):
        """
        Create an instance of the class from a dictionary.

        Args:
            payload (dict): A dictionary containing the attributes to initialize the class.

        Returns:
            An instance of the class.
        """
        return cls(**payload)

class IncomingPayload(SMBaseClass):
    """
    IncomingPayload is responsible for representing a payload within the system,
    providing the mechanism to identify whether it is a dummy payload and whether
    it has already been processed. It also requires subclasses to specify the
    application name.
    Attributes:
        is_dummy (bool): Indicates whether the payload is a dummy payload.
        _is_processed (bool): Internal tracking flag indicating if the payload
            has been processed.
        payload (Union[dict,Any]): The payload data.
    Properties:
        app_name (str): Name of the application associated with this payload.
            Must be implemented by subclasses.
        is_processed (bool): Indicates if the payload has been processed.
    """
    is_dummy: bool = False
    _is_processed: bool = False
    payload: Union[dict,Any]

    @property
    def app_name(self) -> str:
        """
        Returns the name of the application.

        This method should be implemented by subclasses to provide the
        specific name of the application.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError("Method app_name is not implemented.")
    
    @property
    def is_processed(self) -> bool:
        """
        Returns the processed status of the payload.
        """
        return self._is_processed
    
    @abstractmethod
    def __call__(self, *args, **kwds):
        """
        Calls the instance as if it were a function.

        :param args: Positional arguments to be passed into the callable.
        :param kwds: Keyword arguments to be passed into the callable.
        :raises NotImplementedError: Indicates this method must be overridden in a subclass.
        """
        raise NotImplementedError("Method __call__ is not implemented.")



class ThirdPartyPayloadConsumedByAgent(SMBaseClass):
    """
    ThirdPartyPayload is an abstract base class that represents a payload from a third-party application.
    Attributes:
        task_id (int): The ID of the task.
        user_id (str): The ID of the user.
        org_id (int): The ID of the organization.
        org_name (str): The name of the organization.
    Property:
        app_name (str): Abstract property that should return the name of the application.
        _payload_type (str): Abstract property that should return the type of the payload.
        payload: Abstract property that should return the payload data.
        to_dict (dict): Converts the object to a dictionary representation, including the `app_name` attribute.
    """
    task_id: str
    user_id: str
    org_id: int
    org_name: str

    
    @property
    def app_name(self) -> str:
        """
        Returns the name of the application.

        This method should be implemented by subclasses to provide the
        specific name of the application.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError("Method app_name is not implemented.")
    
    @property
    def payload_type(self) -> str:
        """
        Returns the type of the payload.

        This method should be implemented by subclasses to provide the
        specific payload type.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError("Method _payload_type is not implemented.")
    
    @property
    def payload(self):
        """
        Returns the payload data.

        This method should be implemented by subclasses to provide the
        specific payload data.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError("Method payload is not implemented.")
    
    @override
    def to_dict(self) -> dict:
        """
        Converts the object to a dictionary representation.

        Returns:
            dict: A dictionary containing the key-value pairs representing the object's attributes.
        """
        dict_json = super().to_dict()
        dict_json["app_name"] = self.app_name
        dict_json["payload_type"] = self.payload_type        
        return dict_json
    