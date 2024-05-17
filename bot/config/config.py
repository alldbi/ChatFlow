# config file
import json
import os


class Config:
    """Config class for Chatbot"""

    def __init__(self, config_file: str = None):
        """Initialize the config class."""
        self.config_file = os.getenv('CONFIG_FILE')

        if self.config_file is None:
            raise ValueError(
                'Config file is not provided! Its address should be added to the env variables (CONFIG_FILE)!')

        self.llm_model = os.getenv("LLM_MODEL", 'gpt4')  # 'gpt-3.5-turbo-0125')
        self.temperature = float(os.getenv("TEMP", 0.1))
        self.max_tokens = int(os.getenv("MAX_TOKENS", 200))
        self.flow_file_path = os.getenv("FLOW_FILE_PATH", 'sample_flow.json')

        self.load_config_file()

    def load_config_file(self) -> None:
        """Load the config file."""
        if self.config_file is None:
            return None
        
        with open(self.config_file, "r") as f:
            config = json.load(f)
        for key, value in config.items():
            self.__dict__[key] = value