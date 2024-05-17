from typing import Dict

class FlowItem:
    def run(self, inp: Dict):
        NotImplementedError("Subclasses must implement run method")

    def get_next_item(self):
        NotImplementedError("Subclasses must implement get_next_item method")
    
    def initialize(self, **kwargs):
        NotImplementedError("Subclass must implement initialize method!")