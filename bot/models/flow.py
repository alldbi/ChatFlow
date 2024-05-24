from typing import Dict, List, Union, Type
import copy

from .node import *
from .flow_item import FlowItem
from .state import State
from .memory import Memory


class Flow:
    def __init__(self, model_name='gpt-3.5-turbo-0125',
                 start_node: Union[FlowItem, Dict[FlowItem, Condition], None] = None,
                 states: Union[List[State], None] = None,
                 start_state: Union[State, None] = None,
                 is_output: bool = False) -> None:

        # TODO revise implementation of the history
        self.history: Memory = Memory()
        self.is_output = is_output
        self.model_name = model_name
        self.states: List[State] = states
        if states is None:
            if start_node is None:
                raise ValueError("start_node or states must be initiated!")
            self.start_node: Union[FlowItem, Dict[FlowItem, Condition]] = start_node
            self.state_updater = None
        else:
            if start_state is None:
                # set the first item of the list as start state
                start_state = states[0]
            self.state_updater = StateUpdater(initial_state=start_state, states=states, model_name=self.model_name)
            self.start_node = None

    def initialize(self):
        all_nodes = self.get_all_nodes()
        for node in all_nodes:
            node.initialize(model_name=self.model_name)

    def get_all_nodes(self, ):
        # returns a list of all nodes in the flow
        all_nodes = []
        current_node: Node = self.start_node
        if current_node:
            all_nodes = self.get_all_node_successors(current_node)
        else:
            for state in self.states:
                current_node = state.associated_node
                if current_node is not None:
                    all_nodes.extend(self.get_all_node_successors(current_node))

        return all_nodes

    def get_all_node_successors(self, node: Node):
        successors = [node]
        next_item = node.get_next_item()
        if next_item is None:
            # nothing to add
            return successors
        if isinstance(next_item, FlowItem):
            successors.extend(self.get_all_node_successors(next_item))
            return successors
        else:
            for item in next_item:
                successors.extend(self.get_all_node_successors(item))
            return successors

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

    def run(self, inp: dict, verbose: bool = False):
        self.history.add(inp)
        current_node = self.select_start_node()
        current_input = copy.deepcopy(inp)
        while True:
            if verbose:
                print(10 * "<", " For Debugging ", 10 * ">")
                print("Current State: ", self.state_updater.current_state)
                print("Current Node: ", current_node)
                print("Current Variables: ", current_input)
                print(10 * "<", " For Debugging ", 10 * ">")
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
