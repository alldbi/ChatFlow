from typing import Union, Dict

from .node import StrOutputNode, JsonOutputNode
from .flow_item import FlowItem

class DecisionMaker(FlowItem):
    def __init__(self, input_node: JsonOutputNode,
                 output_nodes: Dict[Dict[str, object],Union[JsonOutputNode, StrOutputNode]]) -> None:
        """

        output_nodes : {{'a': true}: node_1, {'a':false}: node_2}
        """
        self.input_node: JsonOutputNode = input_node
        self.output_nodes: Dict[Dict[str, object],Union[JsonOutputNode, StrOutputNode]] = output_nodes
    
    def run(self, inp: Dict):
        # run 
        pass