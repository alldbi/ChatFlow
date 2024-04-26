class State:
    def __init__(self, name, definition, associated_node) -> None:
        self.name = name
        self.definition = definition
        self.associated_node = associated_node
    
    def __str__(self) -> str:
        return f"""
state name: {self.name}
state definition: {self.definition}
"""