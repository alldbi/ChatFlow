from typing import Dict, List

# class MemoryItem:
#     def __init__(self, index, value) -> None:
#         self.index = index
#         self.value = value

class Memory:
    def __init__(self) -> None:
        # self.current_index = 0
        self.history: List[Dict] = []

    def add(self, inp: Dict):
        self.history.append(inp)
        # for k, v in inp.items:
        #     if k in self.history:
        #         self.history[k].append(MemoryItem(self.current_index, v))
        #     else:
        #         self.history[k] = [MemoryItem(self.current_index, v)]
        # self.current_index += 1

    def get_history_str(self, variables: List[str] = None, count=None):
        if count is None:
            count = len(self.history)
        history_str = ""
        for i, item in enumerate(self.history[-count:]):
            history_str += f"# line {i} \n"
            if variables is None:
                for k, v in item.items():
                    history_str += f"{k} : {v}\n" 
            else:   
                for var in variables:
                    if var in item:
                        history_str += f"{var} : {item[var]}\n"
        return history_str