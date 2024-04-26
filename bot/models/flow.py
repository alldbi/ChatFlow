from typing import Dict, List, Union, Type
import copy

from .node import *
from .flow_item import FlowItem
from .state import State
from .memory import Memory

class Flow:
    def __init__(self, model_name='gpt-3.5-turbo-0125', 
                 start_node:Union[FlowItem, Dict[FlowItem, Condition], None] =None,
                 states: Union[List[State], None]=None, 
                 start_state: Union[State, None]=None, 
                 is_output: bool = False) -> None:
        
        # TODO revise implementation of the history
        self.history: Memory = Memory()
        self.is_output = is_output
        self.model_name = model_name
        if states is None:
            if start_node is None:
                raise ValueError("start_node or states must be initiated!")
            self.start_node: Union[FlowItem, Dict[FlowItem, Condition]] = start_node
            self.state_updater = None
        else:
            if start_state is None:
                # set the first item of the list as start state
                start_state = states[0]
            self.state_updater = StateUpdater(self.model_name, initial_state=start_state, states=states)
            self.start_node = None

    def set_model(self):
        # set model_name of the flow for all of the flowItems that has None model_name
        pass
    
    def select_start_node(self):
        if self.start_node is None:
            return self.state_updater.current_state.associated_node
        else:
            return self.start_node

    def update_state(self):
        if self.state_updater is not None:
            history_str = self.history.get_history_str()
            self.state_updater.update_state(history_str)

    
    def run(self, inp: dict):
        self.history.add(inp)
        current_node = self.select_start_node()
        current_input = copy.deepcopy(inp)
        while True:
            current_input = current_node.run(current_input, self.history)
            if current_node.is_output:
                self.history.add(current_input)
                self.update_state()
                return current_input
        
            next_item = current_node.get_next_item()
            if next_item is None:
                ValueError('no next node to execute!')

            if isinstance(next_item, list):
                # TODO run all members of the list and then put the outputs in a single dictionary to pass to the next step OR????
                NotImplementedError("list input type is not implemented yet!")
                for item in next_item:
                    pass
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

    



    
