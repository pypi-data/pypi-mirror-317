import base64
import logging
import json
from pydantic import BaseModel
from typing import Any
from google.protobuf import json_format
from typing import List, Dict, Union, Optional

logger = logging.Logger(__name__)

class MultiTurnPromptsGenerator:

    def __init__(self, prompts: List[Dict[str, str]]):
        """
        Initialize the generator with a list of prompts.

        Args:
            prompts (List[Dict[str, str]]): A list of dictionaries containing role and content.
        """
        self.prompts = prompts
        self.index = 0  # Maintain the current prompt to send
        self._conversation = []

    def start_conversation(self):
        return self._add_response()
    
    def add_response(self, assistant_response: str) -> bool:
        return self._add_response(assistant_response)

    def _add_response(self, assistant_response: Optional[str] = None) -> bool:
        """
        Generates the conversation up to the current point, starting with the SYSTEM prompt if any.

        Args:
            assistant_response (Optional[str]): The response from the assistant to include in the conversation.

        Returns:
            List[Dict[str, str]]: The conversation history so far.
        """
        next_prompts = []

        while self.index < len(self.prompts):
            current_prompt = self.prompts[self.index]
            content = current_prompt["content"]
            if current_prompt["role"] == "SYSTEM":
                if content:
                    next_prompts.append(current_prompt)
                self.index += 1

                # Look ahead for the next USER prompt and add it
                if self.index < len(self.prompts) and self.prompts[self.index]["role"] == "USER":
                    next_prompts.append(self.prompts[self.index])
                    self.index += 1

                break  # Stop after adding SYSTEM and USER prompts

            elif current_prompt["role"] == "USER":
                next_prompts.append(current_prompt)
                self.index += 1
                break  # Stop after adding a USER prompt

            else:
                # Skip ASSISTANT roles initially
                self.index += 1
        if assistant_response and self._conversation and self._conversation[-1]["role"] != "ASSISTANT":
            self._conversation.append({"role": "ASSISTANT", "content": assistant_response})
        if next_prompts:
            self._conversation.extend(next_prompts)
            return len(self._conversation) > 0
        else:
            return False

    def add_final_response(self, assistant_response: str) -> bool:
        """
        Populates the conversation with all prompts, ensuring ASSISTANT placeholders are added
        if missing, and appends the final assistant response.

        Args:
            assistant_response (str): The final response to add to the conversation.

        Returns:
            List[Dict[str, str]]: The updated conversation history.
        """
        next_prompts = []

        # Iterate through all prompts, ensuring each is included in the conversation
        while self.index < len(self.prompts):
            current_prompt = self.prompts[self.index]
            content = current_prompt["content"]

            if current_prompt["role"] == "SYSTEM":
                # Add SYSTEM prompts directly
                if content:
                    next_prompts.append(current_prompt)
                self.index += 1

                # Look ahead and add the next USER prompt if available
                if self.index < len(self.prompts) and self.prompts[self.index]["role"] == "USER":
                    next_prompts.append(self.prompts[self.index])
                    self.index += 1

            elif current_prompt["role"] == "USER":
                
                # Add a placeholder for ASSISTANT response if missing
                if (len(self._conversation) >= 1 or self._conversation[-1]["role"] == "USER"):
                    next_prompts.append({"role": "ASSISTANT", "content": ""})
                
                # Add USER prompts directly
                next_prompts.append(current_prompt)
                self.index += 1

            else:
                # Add ASSISTANT prompts if they exist
                next_prompts.append(current_prompt)
                self.index += 1

        # Extend the conversation with new prompts
        self._conversation.extend(next_prompts)

        # Update or append the final ASSISTANT response
        if self._conversation and self._conversation[-1]["role"] == "ASSISTANT":
            self._conversation[-1]["content"] = assistant_response
        else:
            self._conversation.append({"role": "ASSISTANT", "content": assistant_response})

        return len(self._conversation) > 0

    def get_full_conversation(self):
        return self._conversation
    
    def get_conversation_in_hugging_face_format(self):
        conv = []
        for p in self._conversation:
            a = {
                "role": p["role"].lower(),
                "content": p["content"]
            }
            conv.append(a)
        return conv
        

    def get_conversation_prompts_as_text(self):
        p = ""
        for seq in self._conversation:
            if seq['role'] in ["SYSTEM", "USER"]:
                if seq['content']:
                    p += f"{seq['role']}\n{seq['content']}\n"
        return p 

    def get_conversation_as_text(self):
        p = ""
        for seq in self._conversation:
            if seq['content']:
                p += f"{seq['role']}\n{seq['content']}\n"
        return p


class Conversation2HuggingFaceFormat:
    """
    Converts conversation format to HuggingFace-compatible format.
    Ensure all roles are in lowercase.
    """
    @staticmethod
    def convert(conversation):
        conv = []
        for p in conversation:
            a = {
                "role": p["role"].lower(),
                "content": p["content"]
            }
            conv.append(a)
        return conv


class ComplexPromptMsg(BaseModel):
    prompt: List[Dict[str, str]]  # List of dictionaries with message details
    evaluation_hint: Optional[Union[Dict, List, str]] = ""  # Evaluation hints as a dictionary, array, or string
    evaluator_name: Optional[str] = ""  # Name of the evaluator
    threat_class: Optional[str]=""
    threat_category: Optional[str]=""

    def get_user_prompts(self) -> List[str]:
        """
        Extracts the content of prompts where the role is "USER".

        Returns:
            List[str]: A list of user prompts (content where role is "USER").
        """
        return [entry["content"] for entry in self.prompt if entry.get("role") == "USER"]

    def get_system_prompts(self) -> List[str]:
        """
        Extracts the content of prompts where the role is "SYSTEM".

        Returns:
            List[str]: A list of system prompts (content where role is "SYSTEM").
        """
        return [entry["content"] for entry in self.prompt if entry.get("role") == "SYSTEM"]

    def get_assistant_responses(self) -> List[str]:
        """
        Extracts the content of prompts where the role is "ASSISTANT".

        Returns:
            List[str]: A list of assistant responses (content where role is "ASSISTANT").
        """
        return [entry["content"] for entry in self.prompt if entry.get("role") == "ASSISTANT"]

    def get_latest_assistant_response(self) -> Optional[str]:
        """
        Retrieves the latest assistant response if available.

        Returns:
            Optional[str]: The content of the latest assistant response, or None if not available.
        """
        assistant_responses = self.get_assistant_responses()
        return assistant_responses[-1] if assistant_responses else None

    def get_latest_user_prompt(self) -> Optional[str]:
        """
        Retrieves the latest user prompt if available.

        Returns:
            Optional[str]: The content of the latest user prompt, or None if not available.
        """
        user_prompts = self.get_user_prompts()
        return user_prompts[-1] if user_prompts else None

    def add_user_prompt(self, content: str):
        """
        Adds a new user prompt to the prompt list.

        Args:
            content (str): The content of the user prompt to add.
        """
        self.prompt.append({"role": "USER", "content": content})

    def add_assistant_response(self, content: str):
        """
        Adds a new assistant response to the prompt list.

        Args:
            content (str): The content of the assistant response to add.
        """
        self.prompt.append({"role": "ASSISTANT", "content": content})
    
    def multi_turn_prompts_generator(self):
        return MultiTurnPromptsGenerator(self.prompt)

class DtxPrompt(BaseModel):
    prompt: Union[str, ComplexPromptMsg]  # The prompt can either be a simple string or a complex structured object
    safe: bool  # Indicates whether the prompt is deemed safe
    threat_class: str  # Classification of the threat associated with the prompt
    threat_category: str  # Specific category of the threat
    labels: Optional[Dict[str, Union[str, bool, int]]] = {}  # Optional dictionary to store additional metadata about the prompt

    def multi_turn_prompts_generator(self) -> MultiTurnPromptsGenerator:
        """
        Creates and returns a MultiTurnPromptsGenerator instance based on the prompt data.

        If the prompt is of type ComplexPromptMsg, its list of prompts will be used to initialize the generator.
        Otherwise, the prompt will be treated as a single USER role prompt.

        Returns:
            MultiTurnPromptsGenerator: An initialized generator with the processed prompts.
        """
        prompts = []  # Initialize an empty list to hold the processed prompts

        if isinstance(self.prompt, ComplexPromptMsg):
            # If the prompt is a ComplexPromptMsg, extract its list of prompts
            prompts = self.prompt.prompt
        else:
            # If the prompt is a simple string, treat it as a single USER prompt
            prompts = [{"content": self.prompt, "role": "USER"}]

        # Return an instance of MultiTurnPromptsGenerator initialized with the processed prompts
        return MultiTurnPromptsGenerator(prompts)

    @property
    def is_complex(self) -> bool:
        """
        Checks if the prompt is classified as "complex" based on labels.

        Returns:
            bool: True if the prompt type is "complex", otherwise False.
        """
        return self.labels.get("_prompt_type", "").lower() == "complex"

    @property
    def prompt_encoding(self) -> str:
        """
        Retrieves the prompt encoding from the labels.

        Returns:
            str: The value of the prompt encoding label, or "unknown" if not available.
        """
        return self.labels.get("_prompt_encoding", "unknown")

    @property
    def lineage(self) -> str:
        """
        Retrieves the lineage information from the labels.

        Returns:
            str: The value of the lineage label, or "unknown" if not available.
        """
        return self.labels.get("lineage", "unknown")

    @property
    def deceptiveness(self) -> str:
        """
        Retrieves the deceptiveness level from the labels.

        Returns:
            str: The value of the deceptiveness label, or "unknown" if not available.
        """
        return self.labels.get("deceptiveness", "unknown")

    @property
    def technique(self) -> str:
        """
        Retrieves the technique used from the labels or instance attribute.

        Returns:
            str: The technique used, defaulting to "unknown" if not available.
        """
        return self.labels.get("technique", "unknown")

    @property
    def goal_summary(self) -> str:
        """
        Retrieves the goal description from the instance attribute or labels.

        Returns:
            str: The goal description, trimmed to 100 characters.
        """
        return self.labels.get("goal", "unknown")[:100]

    @property
    def owasp_info(self) -> Dict[str, str]:
        """
        Retrieves OWASP classification and title.

        Returns:
            Dict[str, str]: A dictionary with OWASP class and title.
        """
        return {
            "owasp_class": self.labels.get("owasp_class", "unspecified"),
            "owasp_title": self.labels.get("owasp_title", "unspecified")
        }

    @property
    def multi_turn(self) -> bool:
        """
        Checks if the prompt involves multi-turn interactions.

        Returns:
            bool: True if multi-turn is specified in labels, otherwise False.
        """
        return self.labels.get("multi_turn", False)

    def prompt_as_str(self) -> str:
        """
        Combines all System and User roles into a single string.

        Returns:
            str: The combined content of System and User prompts as a string.
        """
        if isinstance(self.prompt, ComplexPromptMsg):
            user_and_system_prompts = [
                entry["content"]
                for entry in self.prompt.prompt
                if entry["role"] in ["USER", "SYSTEM"]
            ]
            return "\n".join(user_and_system_prompts)
        return str(self.prompt)

    def prompt_as_conversation(self) -> List[Dict[str, str]]:
        """
        Returns System and User roles in a structured role/content format.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing role and content.
        """
        if isinstance(self.prompt, ComplexPromptMsg):
            return [
                {"role": entry["role"], "content": entry["content"]}
                for entry in self.prompt.prompt
                if entry["role"] in ["USER", "SYSTEM"]
            ]
        return [{"role": "USER", "content": str(self.prompt)}]

class ComplexPromptMsgParser:
    """
    Parser class for handling ComplexPromptMsg objects.

    This class provides methods to parse a string input, which may be in raw JSON format or base64 encoded,
    into a ComplexPromptMsg object.
    """

    def parse(self, data: str) -> ComplexPromptMsg:
        """
        Parses a string input into a ComplexPromptMsg object.

        The input string is first checked for base64 encoding. If it is base64 encoded, it is decoded.
        The resulting string is then attempted to be parsed as JSON into a ComplexPromptMsg object.

        Args:
            data (str): The input string to be parsed.

        Returns:
            ComplexPromptMsg: A ComplexPromptMsg object if parsing is successful.
            None: If parsing fails due to invalid format or errors.
        """
        decoded_data = self._attempt_base64_decode(data)
        data = decoded_data or data  # Use the decoded data if base64 decoding is successful
        try:
            data_dict = json.loads(data)  # Attempt to parse the string as JSON
            return ComplexPromptMsg(**data_dict)  # Create a ComplexPromptMsg object
        except json.decoder.JSONDecodeError as ex:
            logger.debug(f"JSON decoding error: {ex}")
            return None
        except ValueError as ex:
            logger.debug(f"Value error while creating ComplexPromptMsg: {ex}")
            return None

    @staticmethod
    def _attempt_base64_decode(s: str) -> str:
        """
        Attempts to decode a string from base64 format.

        Args:
            s (str): The input string to check and decode.

        Returns:
            str: The decoded string if the input is base64 encoded.
            None: If the input is not base64 encoded or decoding fails.
        """
        try:
            if not s or not isinstance(s, str):
                return None
            # Decode and return the string
            return base64.b64decode(s, validate=True).decode("utf-8")
        except (ValueError, base64.binascii.Error) as ex:
            logger.debug(f"Value error while decoding base64 string: {ex}")
            return None
    
class ImportDtxPromptFormatParser:
    """ Parse prompt format that are used to import data to Dtx prompt service
    """
    @staticmethod
    def parse(data: Dict[str, Any]) -> DtxPrompt:
        """
        Parses a dictionary and converts it to a DtxPrompt object.

        Args:
            data (Dict[str, Any]): The input dictionary containing prompt details.

        Returns:
            DtxPrompt: A parsed DtxPrompt object.
        """
        # Create initial DtxPrompt object
        dtx_prompt = DtxPrompt(
            prompt=data.get("prompt", ""),
            safe=data.get("safe", False),
            threat_class=data.get("threat_class", ""),
            threat_category=data.get("threat_category", ""),
            labels=data.get("labels", {}),
        )
        
        if (isinstance(dtx_prompt.prompt, str) 
            and dtx_prompt.is_complex
            and dtx_prompt.prompt_encoding != "base64"):
            raise ValueError("Prompt can be string if prompt_type is complex")

        # Check prompt encoding and decode if necessary
        if dtx_prompt.prompt_encoding == "base64":
            decoded_prompt = base64.b64decode(dtx_prompt.prompt).decode("utf-8")
            dtx_prompt.prompt = decoded_prompt
        
        # Check if the prompt is complex
        if dtx_prompt.is_complex and isinstance(dtx_prompt.prompt, str):
            dtx_prompt.prompt = json.loads(dtx_prompt.prompt)  
            dtx_prompt.prompt = ComplexPromptMsg(**dtx_prompt.prompt)

        return dtx_prompt

    @staticmethod
    def _is_base64(s: str) -> bool:
        """
        Checks if a string is base64 encoded.

        Args:
            s (str): The string to check.

        Returns:
            bool: True if the string is base64 encoded, False otherwise.
        """
        try:
            if not s or not isinstance(s, str):
                return False
            base64.b64decode(s, validate=True)
            return True
        except (ValueError, base64.binascii.Error):
            return False


class DtxPromptServiceOutputFormatParser:
    @staticmethod
    def parse(message: Any) -> DtxPrompt:
        """
        Parses a prompt returned by DtxPrompt Service

        Args:
            prompt (Dict[str, Any]): 

        Returns:
            DtxPrompt: A parsed DtxPrompt object.
        """
        if not isinstance(message, dict):
            message = json_format.MessageToDict(message)
        # Extract content and decode if necessary
        prompt = message.get("data", {}).get("content", "")
        # Extract labels
        labels = message.get("sourceLabels", {})
        # Construct the DtxPrompt object
        dtx_prompt = DtxPrompt(
            prompt=prompt,
            safe=False,  # Default to False unless explicitly determined
            threat_class=message.get("threatClass", "unknown"),
            threat_category=message.get("threatCategory", "unknown"),
            labels=labels
        )

        if (isinstance(dtx_prompt.prompt, str) 
            and dtx_prompt.is_complex
            and dtx_prompt.prompt_encoding != "base64"):
            raise ValueError("Prompt can be string if prompt_type is complex")

        # Check prompt encoding and decode if necessary
        if dtx_prompt.prompt_encoding == "base64":
            decoded_prompt = base64.b64decode(dtx_prompt.prompt).decode("utf-8")
            dtx_prompt.prompt = decoded_prompt
        
        # Check if the prompt is complex
        if dtx_prompt.is_complex and isinstance(dtx_prompt.prompt, str):
            dtx_prompt.prompt = json.loads(dtx_prompt.prompt)  
            dtx_prompt.prompt = ComplexPromptMsg(**dtx_prompt.prompt)

        return dtx_prompt


    @staticmethod
    def _is_base64(s: str) -> bool:
        """
        Checks if a string is base64 encoded.

        Args:
            s (str): The string to check.

        Returns:
            bool: True if the string is base64 encoded, False otherwise.
        """
        try:
            if not s or not isinstance(s, str):
                return False
            base64.b64decode(s, validate=True)
            return True
        except (ValueError, base64.binascii.Error):
            return False
