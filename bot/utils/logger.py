from typing import List, Dict

class LogItem:
    def __init__(self, id: int, node_name: str='', state_name: str = '', inp: Dict = {}, out: Dict= {}) -> None:
        self.node_name = node_name
        self.state_name = state_name
        self.id = id
        self.inp = inp
        self.out = out

    def __str__(self) -> str:
        return f"""id: {self.id}
node name: {self.node_name}
state name: {self.state_name}
node input: [{','.join([k+':'+v for k,v in self.inp.items()])}]
node output: [{','.join([k+':'+v for k,v in self.out.items()])}]
"""

class Logger:
    def __init__(self, debug: bool=False) -> None:
        self.current_id = 0
        self.logs: List[LogItem] = []
        self.debug = debug
        
    def log(self, node_name: str='', state_name: str = '', inp: Dict = {}, out: Dict= {}):
        log_item =LogItem(id=self.current_id, node_name=node_name, state_name=state_name, inp=inp, out=out)
        self.logs.append(log_item)
        self.current_id += 1
        print(log_item)

    def print_logs(self, k=0):
        print(10*'='+'Chatbot Logs'+10*'=')
        for li in self.logs[-k:]:
            print(li)
            print(32*'=')


