from typing import Optional, override

from syncmaster_commons.abstract.baseclass import IncomingPayload, SMBaseClass


class _RootMessagePayloadGupshup(SMBaseClass):
    """
    A class representing the root message payload for Gupshup.

    This class inherits from `SMBaseClass` and provides a property to get the type of the payload.

    Attributes:
        payload_type (str): A property that should return the type of the payload. This method must be implemented by subclasses.

    Methods:
        payload_type: Raises NotImplementedError if not implemented in a subclass.
    """

    @property
    def payload_type(self) -> str:
        """Returns the type of the payload."""
        raise NotImplementedError("Method payload_type is not implemented.")
    
    @override
    def to_dict(self) -> dict:
        """
        Converts the object to a dictionary representation, including the object's attributes and type.

        Returns:
            dict: A dictionary containing the key-value pairs representing the object's attributes.
        """
        dict_json = super().to_dict()
        dict_json["type"] = self.payload_type
        return dict_json

class ImagePayLoad(_RootMessagePayloadGupshup):
    """_ImagePayLoad is a class responsible handling image payloads for the Gupshup API."""

    url: str
    caption: Optional[str] = None
    contentType: str
    urlExpiry: int
    is_expired: bool = False

    @property
    def payload_type(self) -> str:
        """Returns the type of the payload."""
        return "image"

    @classmethod
    def from_dict(cls, image_dict: dict) -> "ImagePayLoad":
        """
        Creates a _ImagePayLoad object from a dictionary.
        Args:
            image_dict (dict): The dictionary containing the image data.
        Returns:
            _ImagePayLoad: The _ImagePayLoad object created from the dictionary.
        """
        return cls(
            url=image_dict["url"],
            caption=image_dict.get("caption"),
            contentType=image_dict["contentType"],
            urlExpiry=image_dict["urlExpiry"],
            is_expired=image_dict.get("is_expired", False),
        )


class TextPayLoad(_RootMessagePayloadGupshup):
    """_TextPayLoad is a class responsible handling text payloads for the Gupshup API."""

    text: str

    @property
    def payload_type(self) -> str:
        """Returns the type of the payload."""
        return "text"

    @classmethod
    def from_dict(cls, text_dict: dict) -> "TextPayLoad":
        """
        Creates a _TextPayLoad object from a dictionary.
        Args:
            text_dict (dict): The dictionary containing the text data.
        Returns:
            _TextPayLoad: The _TextPayLoad object created from the dictionary.
        """
        return cls(text=text_dict["text"])