from typing import override

from syncmaster_commons.abstract.baseclass import \
    ThirdPartyPayloadConsumedByAgent
from syncmaster_commons.gupshup.incoming_payloads import GupshupIncomingPayLoad


class _AgentRequestPayloadGupshup(ThirdPartyPayloadConsumedByAgent):
    """
    _AgentRequestPayloadGupshup is a class that represents the payload consumed by an agent from Gupshup.
    Attributes:
        _incoming_payload (GupshupIncomingPayLoad): The incoming payload from Gupshup.
    Properties:
        app_name (str): Returns the name of the application, which is 'gupshup'.
        _payload_type (str): Returns the type of the payload.
        payload (dict): Constructs and returns the payload dictionary with an added payload type.
    Methods:
        from_dict(cls, payload_dict: dict) -> "_AgentRequestPayloadGupshup":
  """
    incoming_payload: GupshupIncomingPayLoad
    
    @property
    def app_name(self) -> str:
        """
        Returns the name of the application.

        :return: The string 'gupshup'.
        :rtype: str
        """
        return self.incoming_payload.app_name
    
    @property
    def payload_type(self) -> str:
        """
        Returns the incoming payload’s payload type.

        This property retrieves the type of the payload contained within the incoming payload,
        providing insight into how the payload should be processed or interpreted.

        Returns:
            str: The type of the payload.
        """
        return self.incoming_payload.payload.payload.payload_type
    
    @property
    def payload(self) -> dict:
        """
        Constructs and returns the payload dictionary.
        This method retrieves the payload from the incoming payload object,
        converts it to a dictionary, and adds the payload type to the dictionary.
        Returns:
            dict: The payload dictionary with an added payload type.
        """
       
        payload = self.incoming_payload.payload.payload.payload
        output_dict = payload.to_dict() 
        output_dict["payload_type"] = self.payload_type
        if self.payload_type == "text":
            output_dict["messages"] = ("user", output_dict["text"])
        else:
            raise NotImplementedError(f"Payload type '{self.payload_type}' is not supported.")    
        return output_dict

    @classmethod
    def from_dict(cls, payload_dict: dict) -> "_AgentRequestPayloadGupshup":
        """
        Creates an instance of _AgentRequestPayloadGupshup from a dictionary.
        Args:
            cls: The class itself.
            payload_dict (dict): A dictionary containing the payload data.
        Returns:
            _AgentRequestPayloadGupshup: An instance of the class populated with data from the dictionary.
        Raises:
            KeyError: If 'task_id', 'user_id', or 'org_id' keys are missing in the payload_dict.
        """
        
        incoming_payload = GupshupIncomingPayLoad.from_dict(payload_dict["incoming_payload"])
        print(incoming_payload)
        if payload_dict.get("user_id", None) is None:
            payload_dict["user_id"] = incoming_payload.payload.payload.sender.phone
        return cls(
            incoming_payload=incoming_payload,
            task_id=payload_dict["task_id"],
            org_name=payload_dict["org_name"],
            user_id=payload_dict["user_id"],
            org_id=payload_dict["org_id"],
        )
    
