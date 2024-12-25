from .chat import Chat
import logging

class Utility:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

        # Set up logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Create console handler if no handlers exist
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO if not self.kwargs.get("verbose", False) else logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # Set verbose logging if requested
        if self.kwargs.get("verbose", False):
            self.logger.setLevel(logging.DEBUG)
        
    @property
    def chat(self):
        return Chat(**self.kwargs)
    
    def selector(self, message: str, options: list, attempts: int = 3):
        """
        Prompts the LLM to select one option from a list of choices.
        
        :param message: The prompt or question to ask the LLM
        :type message: str
        :param options: List of valid options the LLM can choose from
        :type options: list
        :param attempts: Number of attempts before raising error, defaults to 3
        :type attempts: int, optional
        
        :returns: The selected option that matches one from the options list
        :rtype: str
        
        :raises ValueError: If no valid selection is made within the allowed attempts
        """
        chat = self.chat
        attempt = 0

        # Calculate max tokens needed for largest option, to help 
        # increase the chance of a match
        max_tokens = max(
            chat.token_counter([{"role": "assi stant", "content": option}])
            for option in options
        )

        self.chat.kwargs["max_tokens"] = max_tokens
        self.logger.debug(f"Max tokens needed: {max_tokens}")

        while attempt < attempts:
            # Add system message explaining the constraints
            chat.system(message)

            options_msg = f"You must respond with exactly one of these options, with no additional text: \n\n{'\n\n'.join(options)}"
            chat.system(options_msg)
            
            self.logger.debug(f"System message: {options_msg}\n\n{message}")
            
            # Get response from LLM
            responses = chat.ready()
            response = responses[0] if isinstance(responses, list) else responses
            
            # Check if response matches any option
            for option in options:
                if option.lower() == response.lower().strip():
                    self.logger.debug(f"Found exact match: {option}")
                    return option
            
            # If no match, try searching for the option in the response
            for option in options:
                if option.lower() in response.lower():
                    self.logger.debug(f"Found option in response: {option}")
                    return option
            
            attempt += 1

            self.logger.debug(f"Attempt {attempt + 1} failed: {response}")
            
            # Add error message for invalid response
            chat.system(f"Invalid selection. Please choose exactly one option from: {', '.join(options)}")
        
        raise ValueError(f"Failed to get valid selection after {attempts} attempts")
