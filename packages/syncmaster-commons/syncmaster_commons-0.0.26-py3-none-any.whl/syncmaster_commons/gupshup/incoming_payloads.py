from typing import Literal, Optional, Union, override

from pydantic import Field

from syncmaster_commons.abstract.baseclass import IncomingPayload, SMBaseClass
from syncmaster_commons.gupshup.atomic_payload import ImagePayLoad, TextPayLoad


class _Sender(SMBaseClass):
    """_Sender is a class responsible for handling the sender details for the Gupshup API."""

    phone: str
    name: str
    country_code: str
    dial_code: str

    @classmethod
    def from_dict(cls, sender_dict: dict) -> "_Sender":
        """
        Creates a _Sender object from a dictionary.
        Args:
            sender_dict (dict): The dictionary containing the sender data.
        Returns:
            _Sender: The _Sender object created from the dictionary.
        """
        return cls(
            phone=sender_dict["phone"],
            name=sender_dict["name"],
            country_code=sender_dict["country_code"],
            dial_code=sender_dict["dial_code"],
        )

class _EventPayloadGupshup(SMBaseClass):
    """
    A specialized event payload class for Gupshup that inherits from SMBaseClass.
    This class is designed to handle the representation of incoming Gupshup event
    payloads, providing the following functionalities:
    Attributes:
        _type (str): A property method that must be implemented to return the
                     specific type of the Gupshup event payload.
    Methods:
        to_dict() -> dict:
            Converts the object's attributes into a dictionary, including the
            required 'type' key, which is populated by the `_type` property.
    """
    payload_type: Optional[str] = None

    @property
    def event_type(self) -> str:
        """Returns the type of the payload."""
        raise NotImplementedError("Method event_type is not implemented.")
    
    @override
    def to_dict(self) -> dict:
        """
        Converts the object to a dictionary representation, including the `type` attribute.

        Returns:
            dict: A dictionary containing the key-value pairs representing the object's attributes.
        """
        dict_json = super().to_dict()
        dict_json["type"] = self.payload_type
        return dict_json





class _MessagePayLoad(_EventPayloadGupshup):
    """
    _PayLoad class represents a payload structure for the CRM assistant.
    Attributes:
        id (str): Unique identifier for the payload.
        source (str): Source of the payload.
        payload (Union[_ImagePayLoad, _TextPayLoad]): The actual payload which can be either an image or text.
        sender (_Sender): The sender information of the payload.
    """

    id: str
    source: str
    payload: Union[ImagePayLoad, TextPayLoad]
    sender: _Sender

    @property
    def event_type(self) -> str:
        """Returns the type of the payload."""
        return "message"


    @classmethod
    def from_dict(cls, payload_dict: dict) -> "_MessagePayLoad":
        """
        Creates a _PayLoad object from a dictionary.
        Args:
            payload_dict (dict): The dictionary containing the payload data.
        Returns:
            _PayLoad: The _PayLoad object created from the dictionary.
        """
        sender = _Sender.from_dict(payload_dict["sender"])
        if payload_dict["type"] == "image":
            payload = ImagePayLoad.from_dict(payload_dict["payload"])
        elif payload_dict["type"] == "text":
            payload = TextPayLoad.from_dict(payload_dict["payload"])
        else:
            raise NotImplementedError(
                f"Payload type {payload_dict['payload']['type']} not supported."
            )
        return cls(
            id=payload_dict["id"],
            source=payload_dict["source"],
            payload=payload,
            sender=sender,
            payload_type=payload_dict["type"],
        )

class _MessageEventPayLoad(_EventPayloadGupshup):
    """ """

    id: str
    destination: str
    payload: dict

    @property
    def event_type(self) -> str:
        """Returns the type of the payload."""
        return "message-event"

    @classmethod
    def from_dict(cls, payload_dict: dict) -> "_MessageEventPayLoad":
        """
        Creates a _PayLoad object from a dictionary.
        Args:
            payload_dict (dict): The dictionary containing the payload data.
        Returns:
            _PayLoad: The _PayLoad object created from the dictionary.
        """
        return cls(
            id=payload_dict["id"],
            destination=payload_dict["destination"],
            payload=payload_dict["payload"],
        )


class _BillingEventPayload(_EventPayloadGupshup):
    """

    Class for handling billing event payloads.

    Example:
    {'app': 'SyncMaster', 'timestamp': 1733229369353, 'version': 2, 'type': 'billing-event',
    'payload': {'deductions': {'type': 'service', 'model': 'CBP', 'source': 'whatsapp', 'billable': False},
    'references': {'id': '38034703-f873-40ba-b562-61849b1d6431', 'gsId': '1637d49e-f9c4-4361-8121-e4bdc108ebaf', 'conversationId': '42a9b4d675a89a483c676a6fd0a725e0', 'destination': '919582344421'}}}"""

    deductions: dict
    references: dict

    @property
    def event_type(self) -> str:
        """Returns the type of the payload."""
        return "billing-event"

    @classmethod
    def from_dict(cls, payload_dict: dict) -> "_BillingEventPayload":
        """
        Creates a _PayLoad object from a dictionary.
        Args:
            payload_dict (dict): The dictionary containing the payload data.
        Returns:
            _PayLoad: The _PayLoad object created from the dictionary.
        """
        return cls(
            deductions=payload_dict["deductions"],
            references=payload_dict["references"],
        )


class _UserEventPayload(_EventPayloadGupshup):
    """ """

    phone: str

    @property
    def event_type(self) -> str:
        """Returns the type of the payload."""
        return "user-event"

    @classmethod
    def from_dict(cls, payload_dict: dict) -> "_UserEventPayload":
        """
        Creates a _PayLoad object from a dictionary.
        Args:
            payload_dict (dict): The dictionary containing the payload data.
        Returns:
            _PayLoad: The _PayLoad object created from the dictionary.
        """
        return cls(
            phone=payload_dict["phone"],
        )


class _PayLoad(SMBaseClass):
    """
    _PayLoad class represents a payload structure for the gupshup app.
    """

    payload: Union[
        _MessagePayLoad, _MessageEventPayLoad, _BillingEventPayload, _UserEventPayload
    ]
    event_type: Literal["message", "message-event", "billing-event", "user-event"]

    @override
    def to_dict(self) -> dict:
        """
        Converts the object to a dictionary representation, including the object's attributes and type.

        Returns:
            dict: A dictionary containing the key-value pairs representing the object's attributes.
        """
        dict_json = super().to_dict()
        dict_json["type"] = self.event_type        
        dict_json.pop("event_type")        
        return dict_json
    
    @classmethod
    def from_dict(cls, payload_dict: dict) -> "_PayLoad":
        """
        Creates a _PayLoad object from a dictionary.
        Args:
            payload_dict (dict): The dictionary containing the payload data.
        Returns:
            _PayLoad: The _PayLoad object created from the dictionary.
        """
        if payload_dict["type"] == "message":
            payload = _MessagePayLoad.from_dict(payload_dict["payload"])            
        elif payload_dict["type"] == "message-event":
            payload = _MessageEventPayLoad.from_dict(payload_dict["payload"])
        elif payload_dict["type"] == "user-event":
            payload = _UserEventPayload.from_dict(payload_dict["payload"])
        else:
            raise NotImplementedError(
                f"Payload type {payload_dict['type']} not supported."
            )
        return cls(payload=payload, event_type=payload_dict["type"])


class GupshupIncomingPayLoad(IncomingPayload):
    """
    GupshupIncomingPayLoad class represents the incoming payload from the Gupshup application.
    Attributes:
        app (str): The name of the application.
        timestamp (int): The timestamp of the payload.
        payload (_PayLoad): The payload data.
    Methods:
        app_name() -> str:
        from_dict(payload_dict: dict) -> "GupshupIncomingPayLoad":
        __call__(*args, **kwargs) -> dict:
   """

    app: str
    timestamp: int    
    payload: _PayLoad = Field(..., description="The payload data.")

    @property
    def app_name(self) -> str:
        """
        Returns the name of the Gupshup application.

        :return: The application name as a string.
        :rtype: str
        """
        return 'WhatsApp'

    @classmethod
    def from_dict(cls, payload_dict: dict) -> "GupshupIncomingPayLoad":
        """
        Creates a PayLoad object from a dictionary.
        Args:
            payload_dict (dict): The dictionary containing the payload data.
        Returns:
            PayLoad: The PayLoad object created from the dictionary.
        """
        payload:_PayLoad = _PayLoad.from_dict(payload_dict["payload"] if "payload" in payload_dict["payload"] else payload_dict)
        app = payload_dict["app"]
        timestamp = payload_dict["timestamp"]
        is_dummy = payload_dict.get("is_dummy", False)
        return cls(app=app, timestamp=timestamp, payload=payload, is_dummy=is_dummy)

    def __call__(self, *args, **kwargs) -> dict:
        """
        Processes the incoming payload and updates the kwargs dictionary.

        If the instance is marked as a dummy, it sets the `_is_processed` attribute to True.
        If the payload is of type `_MessagePayLoad`, it converts the payload to a dictionary
        and updates the kwargs with the incoming payload and sender's phone number.
        Otherwise, it sets the `_is_processed` attribute to True and logs the payload type.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments to be updated with incoming payload data.

        Returns:
            dict: The updated kwargs dictionary.
        """
        if self.is_dummy:
            self._is_processed = True
        elif isinstance(self.payload.payload, _MessagePayLoad):
            kwargs["incoming_payload"] = self.to_dict()
        else:
            self._is_processed = True
            print(
                "Not a message payload, payload of type ",
                self.payload.payload.__class__.__name__,
            )
        return kwargs


