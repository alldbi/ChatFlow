from typing import Dict, Any
from enum import Enum

class Operator(Enum):
    EQUALS = 'equals'
    MORE = 'more than'
    LESS = 'less than'
    CONTAINS = 'contains' # for string values


class Condition:
    def __init__(self, variable: str, value: Any, operator: Operator) -> None:
        self.variable = variable
        self.operator: Operator = operator
        self.value = value

    def evaluate(self, inp: Dict):
        if self.variable in inp:
            inp_value = inp[self.variable]
            return self._compare(inp_value)
        else:
            return False
        
    def _compare(self, inp_value):
        try:
            if self.operator == Operator.EQUALS:
                return self.value == inp_value
            if self.operator == Operator.LESS:
                return inp_value < self.value
            if self.operator == Operator.MORE:
                return inp_value > self.value
            if self.operator == Operator.CONTAINS:
                return self.value in inp_value.lower()
            
        except Exception as e:
            print(f"operation is not possible: {e}")
            return False