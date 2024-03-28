from typing import Dict, List, Union, Type

from .node import *
from .decision_maker import DecisionMaker
from .flow_item import FlowItem

class Flow:
    def __init__(self, flow_items: List[Union[JsonOutputNode, StrOutputNode, DecisionMaker, Type['Flow']]], is_output: bool = False) -> None:
        self.flow_items: List[Union[JsonOutputNode, StrOutputNode, Type['Flow'], DecisionMaker]] = flow_items
        self.is_output = is_output

    def run(self, inp: Dict):
        for fi in self.flow_items:
            output = fi.run()
        pass

    



    
