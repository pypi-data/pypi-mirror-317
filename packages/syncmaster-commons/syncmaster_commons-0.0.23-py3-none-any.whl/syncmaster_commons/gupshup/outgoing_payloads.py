from typing import override  # type: ignore

from syncmaster_commons.abstract.baseclass import SMBaseClass

# https://docs.gupshup.io/docs/whatsapp-message-type-outbound-free-form


class OutGoingPayload(SMBaseClass):
    """
    OutGoingPayload class inherits from SMBaseClass and represents the payload for outgoing messages.

    Attributes:
        type_text (str): A property that should be implemented in subclasses to return the type of the payload as text.

    Methods:
        from_dict(cls, payload_dict: dict) -> "OutGoingPayload":
            Creates an OutGoingPayload object from a dictionary.

        to_dict(self) -> dict:
            Converts the object to a dictionary representation, including the object's attributes and type.
    """

    @property
    def type_text(self):
        raise NotImplementedError("`type_text` property not implemented.")

    @classmethod
    def from_dict(cls, payload_dict: dict) -> "OutGoingPayload":
        """
        Creates a OutGoingPayload object from a dictionary.
        Args:
            payload_dict (dict): The dictionary containing the payload data.
        Returns:
            OutGoingPayload: The OutGoingPayload object created from the dictionary.
        """
        for key, value in payload_dict.items():
            setattr(cls, key, value)
        return cls

    @override
    def to_dict(self) -> dict:
        """
        Converts the object to a dictionary representation. Checks if the object has a `to_dict()` method and calls it.
        If the object does not have a `to_dict()` method, it raises a `NotImplementedError`. Also includes the object's
        attributes in the dictionary. If object is another class, it calls `to_dict()` on the related instance.

        Returns:
            dict: A dictionary containing the key-value pairs representing the object's attributes.
        """
        dict_json = super().to_dict()
        dict_json["type"] = self.type_text
        return dict_json


class TextPayload(OutGoingPayload):
    """TextPayload is a class responsible for handling text outgoing payloads for the Gupshup API."""

    text: str

    @property
    def type_text(self):
        return "text"


class FilePayload(OutGoingPayload):
    """FilePayload is a class responsible for handling file outgoing payloads for the Gupshup API."""

    url: str
    caption: str
    filename: str
    id: str

    @property
    def type_text(self):
        return "file"
