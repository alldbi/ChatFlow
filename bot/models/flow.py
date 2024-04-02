from typing import Dict, List, Union, Type

from .node import *
from .decision_maker import DecisionMaker
from .flow_item import FlowItem

class Flow:
    def __init__(self, start_node: FlowItem, is_output: bool = False) -> None:
        self.start_node: FlowItem = start_node
        self.is_output = is_output

    def run(self, inp: dict):
        current_node = self.start_node
        current_input = inp
        while True:
            current_input = current_node.run(current_input)
            if current_node.is_output:
                return current_input
        
            next_item = current_node.get_next_item()
            if next_item is None:
                ValueError('no next node to execute!')

            if isinstance(next_item, list):
                # TODO run all members of the list and then put the outputs in a single dictionary to pass to the next step OR????
                NotImplementedError("list input type is not implemented yet!")
                pass

            elif isinstance(next_item, dict):
                # choose the node that will continue the way
                for k, v in next_item.items():
                    # print(current_input)
                    if v.evaluate(current_input):
                        current_node = k
                        break

            else:
                current_node = next_item

    



    
