from typing import Dict, List, Set, Union
from enum import Enum

from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from pydantic import BaseModel
from pydantic import create_model

from .flow_item import FlowItem
from .condition import Condition

class Node(FlowItem):
    def __init__(self, model_name,
                 prompt_template: str, 
                 input_variables:List[str], 
                 output_variables: Union[Dict[str, type], str],
                 next_item: Union[FlowItem, List[FlowItem], Dict[FlowItem, Condition], None]=None,
                 temperature: float = 0.1,
                 max_tokens: int = 400,
                 verbose: bool = False,
                 return_inputs: bool = False,
                 is_output: bool = False) -> None:
        self.template = prompt_template
        self.input_variables: List[str] = input_variables
        self.output_variables: str = output_variables
        self.next: Union[FlowItem, List[FlowItem], Dict[FlowItem, Condition]] = next_item
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.return_inputs = return_inputs
        self.is_output = is_output
        self.verbose = verbose

    def set_next_item(self, next: Union[FlowItem, List[FlowItem], Dict[FlowItem, Condition]])-> None:
        self.next = next
    
    def get_next_item(self):
        return self.next


class JsonOutputNode(Node):
    def __init__(self, model_name,
                 prompt_template: str, 
                 input_variables:List[str], 
                 output_variables: Dict[str, type],
                 next_item: Union[FlowItem, List[FlowItem], Dict[FlowItem, Condition], None]=None,
                 temperature: float = 0.1,
                 max_tokens: int = 400,
                 verbose: bool = False,
                 return_inputs: bool = False,
                 is_output: bool = False
                 ) -> None:
        """

        input_variables: a list of input variable names
        output_variables: a dictionary with variable names keys and variable types values
                {'a':int, 'b':str}
        """
        super().__init__(model_name, prompt_template, input_variables, output_variables, next_item, temperature, max_tokens, verbose, return_inputs, is_output)

        self.parser = self._get_output_parser()

        llm = ChatOpenAI(model_name=model_name, temperature=temperature, max_tokens=max_tokens, verbose=verbose)
        self.model = llm.with_structured_output(
                    self._get_output_model(),
                    method="json_mode",
                    include_raw=True
                )
        
        self.prompt = PromptTemplate(template=self.template
                                     ,input_variables=self.input_variables
                                    #  ,partial_variables={"format_instructions": self.parser.get_format_instructions()}
                                     )
        # self.chain = self.prompt | self.model | self.parser
        self.chain = self.prompt | self.model
    
    
    def run(self, inp: Dict):
        try:
            output = self.chain.invoke(input=inp)['parsed']
        except Exception as e:
            print(e)
            output = {k: None for k in self.output_variables}
        
        if self.return_inputs:
            output.update(inp)
            return output
        
        return output

    def _get_output_model(self):
        output_model = create_model('OutputModel', **{k: (v, ...) for k, v in self.output_variables.items()})
        return output_model
    
    def _get_output_parser(self) -> JsonOutputParser:
        parser = JsonOutputParser()
        output_model = self._get_output_model()
        parser.pydantic_object = output_model
        return parser


class StrOutputNode(Node):
    def __init__(self, model_name,
                 prompt_template: str, 
                 input_variables:List[str], 
                 output_variables: str,
                 next_item: Union[FlowItem, List[FlowItem], Dict[FlowItem, Condition], None]=None,
                 temperature: float = 0.1,
                 max_tokens: int = 400,
                 verbose: bool = False,
                 return_inputs: bool = False,
                 is_output: bool = False
                 ) -> None:
        """

        input_variables: a list of input variable names
        output_variable: a string that is the name of the output string
        """
        super().__init__(model_name, prompt_template, input_variables, output_variables, next_item, temperature, max_tokens, verbose, return_inputs, is_output)

        self.parser = self._get_output_parser()

        self.model = ChatOpenAI(model_name=model_name, temperature=temperature, max_tokens=max_tokens, verbose=verbose)
        
        self.prompt = PromptTemplate(template=self.template
                                     ,input_variables=self.input_variables
                                     )
        # self.chain = self.prompt | self.model | self.parser
        self.chain = self.prompt | self.model
        
    
    def run(self, inp: Dict):
        # TODO run the prompt and generate output
        try:
            output = {self.output_variables: self.chain.invoke(input=inp).content}
        except Exception as e:
            print(e)
            output = {self.output_variables: None}
        if self.return_inputs:
            return output.update(self.input_variables)
        return output
    
    def _get_output_parser(self) -> StrOutputParser:
        return StrOutputParser


class RetrievalJsonOutputNode(JsonOutputNode):
    def __init__(self, model_name, 
                 prompt_template: str, 
                 input_variables: List[str], 
                 output_variables: Dict[str, type],
                 next_item: Union[FlowItem, List[FlowItem], Dict[FlowItem, Condition]], 
                 temperature: float = 0.1, 
                 max_tokens: int = 400, 
                 verbose: bool = False, 
                 return_inputs: bool = False,
                 is_output: bool = False) -> None:
        super().__init__(model_name, prompt_template, input_variables, output_variables, next_item, temperature, max_tokens, verbose, return_inputs, is_output)
        # TODO


class RetrievalStrOutputNode(StrOutputNode):
    def __init__(self, model_name, 
                 prompt_template: str, 
                 input_variables: List[str], 
                 output_variables: str,
                 next_item: Union[FlowItem, List[FlowItem], Dict[FlowItem, Condition], None]=None, 
                 temperature: float = 0.1, 
                 max_tokens: int = 400, 
                 verbose: bool = False, 
                 return_inputs: bool = False,
                 is_output: bool = False) -> None:
        super().__init__(model_name, prompt_template, input_variables, output_variables, next_item, temperature, max_tokens, verbose, return_inputs, is_output)
        # TODO


class NodeFactory:
    @staticmethod
    def create_node(model_name, 
                    prompt_template: str, 
                    input_variables: List[str], 
                    output_variables: Union[Dict[str, type], str],
                    next_item: Union[FlowItem, List[FlowItem], Dict[FlowItem, Condition], None]=None, 
                    temperature: float = 0.1, 
                    max_tokens: int = 400, 
                    verbose: bool = False, 
                    return_inputs: bool = False,
                    is_output: bool = False) -> Node:
        if isinstance(output_variables, str):
            return StrOutputNode(model_name, prompt_template, 
                                 input_variables, output_variables, next_item,
                                 temperature, max_tokens, verbose, 
                                 return_inputs, is_output)
        elif isinstance(output_variables, Dict):
            return JsonOutputNode(model_name, prompt_template, 
                                 input_variables, output_variables, next_item,
                                 temperature, max_tokens, verbose, 
                                 return_inputs, is_output)
        else:
            raise ValueError("invalid output variables type!")
        

