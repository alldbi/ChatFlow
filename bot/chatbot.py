from .config.config import Config


class ChatBot:
    def __init__(self, cfg: Config) -> None:
        self.cfg: Config = cfg
        pass

    def setup(self):
        """
        initializes a flow for the bot 
        """
        self.cfg.flow_file_path
        

    def reply(self):
        pass